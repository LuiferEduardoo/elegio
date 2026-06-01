"""Lazy global BM25 index over all (non-deleted) proposal_chunks.

Loaded on first search, held in memory for the lifetime of the worker.
After new chunks land, call ``refresh(db)`` to rebuild — there is no
auto-invalidation. Each uvicorn worker has its own copy.
"""

import asyncio
import re
from dataclasses import dataclass

from rank_bm25 import BM25Okapi
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.proposal.models import Proposal
from app.domains.proposal_chunk.models import ProposalChunk

_TOKEN_RE = re.compile(r"\w+", flags=re.UNICODE)


def tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


@dataclass(slots=True)
class ChunkMeta:
    id: int
    proposal_id: int
    category_id: int
    candidate_id: int
    content: str


@dataclass(slots=True)
class BM25Hit:
    chunk_id: int
    proposal_id: int
    category_id: int
    candidate_id: int
    score: float
    content: str


class BM25Index:
    def __init__(self) -> None:
        self._bm25: BM25Okapi | None = None
        self._meta: list[ChunkMeta] = []
        self._lock = asyncio.Lock()

    async def _load(self, db: AsyncSession) -> None:
        stmt = (
            select(
                ProposalChunk.id,
                ProposalChunk.content,
                ProposalChunk.proposal_id,
                Proposal.category_id,
                Proposal.candidate_id,
            )
            .select_from(ProposalChunk)
            .join(Proposal, ProposalChunk.proposal_id == Proposal.id)
            .where(
                ProposalChunk.deleted_at.is_(None),
                Proposal.deleted_at.is_(None),
            )
        )
        rows = (await db.execute(stmt)).all()

        self._meta = [
            ChunkMeta(
                id=r.id,
                proposal_id=r.proposal_id,
                category_id=r.category_id,
                candidate_id=r.candidate_id,
                content=r.content,
            )
            for r in rows
        ]
        corpus = [tokenize(m.content) for m in self._meta]
        self._bm25 = BM25Okapi(corpus) if corpus else None

    async def ensure_loaded(self, db: AsyncSession) -> None:
        if self._bm25 is not None:
            return
        async with self._lock:
            if self._bm25 is None:
                await self._load(db)

    async def refresh(self, db: AsyncSession) -> None:
        async with self._lock:
            await self._load(db)

    async def search(
        self,
        db: AsyncSession,
        query: str,
        category_id: int | None,
        allowed_candidate_ids: set[int] | None,
        limit: int,
    ) -> list[BM25Hit]:
        await self.ensure_loaded(db)
        if self._bm25 is None or not self._meta:
            return []

        tokens = tokenize(query)
        if not tokens:
            return []

        scores = self._bm25.get_scores(tokens)
        hits: list[BM25Hit] = []
        for meta, score in zip(self._meta, scores, strict=True):
            if score <= 0:
                continue
            if category_id is not None and meta.category_id != category_id:
                continue
            if allowed_candidate_ids is not None and meta.candidate_id not in allowed_candidate_ids:
                continue
            hits.append(
                BM25Hit(
                    chunk_id=meta.id,
                    proposal_id=meta.proposal_id,
                    category_id=meta.category_id,
                    candidate_id=meta.candidate_id,
                    score=float(score),
                    content=meta.content,
                )
            )
        hits.sort(key=lambda h: h.score, reverse=True)
        return hits[:limit]


_instance: BM25Index | None = None


def get_bm25_index() -> BM25Index:
    """Return the process-wide BM25Index singleton."""
    global _instance
    if _instance is None:
        _instance = BM25Index()
    return _instance
