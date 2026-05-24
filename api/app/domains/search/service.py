"""Hybrid (dense + BM25) proposal search with RRF fusion.

Pipeline per request:
  1. Embed the query with multilingual-e5-large (in-process).
  2. Run a dense search against Qdrant, filtered by category/candidate via
     payload conditions.
  3. Run BM25 against the in-memory index, applying the same filters.
  4. Collapse each list from chunk-level to proposal-level (keep the best
     chunk per proposal).
  5. Fuse the two proposal lists with Reciprocal Rank Fusion:
        score(p) = Σ 1 / (k + rank_i(p))    with k = 60
  6. Hydrate the top results from MySQL.
"""

from collections import defaultdict
from collections.abc import Iterable

from qdrant_client.models import FieldCondition, Filter, MatchValue
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.bm25_index import BM25Hit, get_bm25_index
from app.core.embedder import get_embedder
from app.core.qdrant_client import COLLECTION_NAME, get_qdrant_client
from app.domains.proposal.models import Proposal
from app.domains.proposal.schemas import (
    CandidateInProposal,
    CategoryInProposal,
    SourceInProposal,
    TaggingInProposal,
)
from app.domains.search.schemas import SearchHit, SearchResponse

RRF_K = 60


def _build_qdrant_filter(
    category_id: int | None, candidate_id: int | None
) -> Filter | None:
    conditions: list[FieldCondition] = []
    if category_id is not None:
        conditions.append(
            FieldCondition(key="category_id", match=MatchValue(value=category_id))
        )
    if candidate_id is not None:
        conditions.append(
            FieldCondition(key="candidate_id", match=MatchValue(value=candidate_id))
        )
    if not conditions:
        return None
    return Filter(must=conditions)


def _collapse_to_proposals(
    items: Iterable[tuple[int, float, str | None]],
) -> list[tuple[int, float, str | None]]:
    """Keep only the first (best-ranked) chunk per proposal, preserving order."""
    seen: set[int] = set()
    out: list[tuple[int, float, str | None]] = []
    for proposal_id, score, excerpt in items:
        if proposal_id in seen:
            continue
        seen.add(proposal_id)
        out.append((proposal_id, score, excerpt))
    return out


def _rrf(rank_lists: list[list[int]], k: int = RRF_K) -> list[tuple[int, float]]:
    scores: dict[int, float] = defaultdict(float)
    for ranked in rank_lists:
        for zero_idx, pid in enumerate(ranked):
            scores[pid] += 1.0 / (k + zero_idx + 1)
    return sorted(scores.items(), key=lambda kv: kv[1], reverse=True)


async def search_proposals(
    db: AsyncSession,
    query: str,
    category_id: int | None,
    candidate_id: int | None,
    limit: int,
) -> SearchResponse:
    overshoot = max(20, limit * 3)

    # --- Semantic (Qdrant) ---
    embedder = get_embedder()
    qdrant = get_qdrant_client()
    query_vec = embedder.embed_query(query)
    qdrant_filter = _build_qdrant_filter(category_id, candidate_id)

    sem_points = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vec,
        query_filter=qdrant_filter,
        limit=overshoot,
        with_payload=True,
    )
    sem_items = [
        (
            int(p.payload["proposal_id"]),
            float(p.score),
            p.payload.get("content"),
        )
        for p in sem_points
        if p.payload is not None and "proposal_id" in p.payload
    ]
    sem_proposals = _collapse_to_proposals(sem_items)

    # --- Lexical (BM25) ---
    bm25 = get_bm25_index()
    lex_hits: list[BM25Hit] = await bm25.search(
        db, query, category_id, candidate_id, overshoot
    )
    lex_items = [(h.proposal_id, h.score, h.content) for h in lex_hits]
    lex_proposals = _collapse_to_proposals(lex_items)

    # --- RRF fusion ---
    fused = _rrf(
        [
            [pid for pid, _, _ in sem_proposals],
            [pid for pid, _, _ in lex_proposals],
        ]
    )
    top = fused[:limit]
    if not top:
        return SearchResponse(query=query, total=0, items=[])

    # --- Hydrate from MySQL ---
    top_ids = [pid for pid, _ in top]
    result = await db.execute(
        select(Proposal)
        .where(
            Proposal.id.in_(top_ids),
            Proposal.deleted_at.is_(None),
        )
        .options(
            selectinload(Proposal.candidate),
            selectinload(Proposal.category),
            selectinload(Proposal.taggings),
            selectinload(Proposal.sources),
        )
    )
    proposals_by_id = {p.id: p for p in result.scalars().all()}

    sem_idx = {
        pid: (i, score, excerpt)
        for i, (pid, score, excerpt) in enumerate(sem_proposals)
    }
    lex_idx = {
        pid: (i, score, excerpt)
        for i, (pid, score, excerpt) in enumerate(lex_proposals)
    }

    items: list[SearchHit] = []
    for pid, rrf_score in top:
        proposal = proposals_by_id.get(pid)
        if proposal is None:
            continue
        sem_info = sem_idx.get(pid)
        lex_info = lex_idx.get(pid)
        excerpt = None
        if sem_info and sem_info[2]:
            excerpt = sem_info[2]
        elif lex_info and lex_info[2]:
            excerpt = lex_info[2]
        items.append(
            SearchHit(
                proposal_id=proposal.id,
                title=proposal.title,
                summary=proposal.summary,
                candidate=CandidateInProposal.model_validate(proposal.candidate),
                category=CategoryInProposal.model_validate(proposal.category),
                taggings=[
                    TaggingInProposal.model_validate(t) for t in proposal.taggings
                ],
                sources=[
                    SourceInProposal.model_validate(s) for s in proposal.sources
                ],
                score=rrf_score,
                semantic_rank=(sem_info[0] + 1) if sem_info else None,
                semantic_score=sem_info[1] if sem_info else None,
                lexical_rank=(lex_info[0] + 1) if lex_info else None,
                lexical_score=lex_info[1] if lex_info else None,
                excerpt=excerpt,
            )
        )

    return SearchResponse(query=query, total=len(items), items=items)
