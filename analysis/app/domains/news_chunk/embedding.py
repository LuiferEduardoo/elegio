"""Embed news chunks and upsert them into the Qdrant ``news_chunks`` collection.

Mirrors ``proposal_chunk.embedding``: Qdrant point id == MySQL ``news_chunks.id``
so upserts are idempotent. ``content_chunk`` is already vitaminized, so it is
both the embedded text and the payload ``content``. The rest of the payload is
hydrated by joining ``news`` and ``candidates``.
"""

from collections.abc import Iterable

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sqlalchemy import Connection, select

from app.core.database import candidates_table, news_chunks_table, news_table
from app.core.embedder import Embedder
from app.core.qdrant_client import NEWS_COLLECTION_NAME


def get_all_chunk_ids(conn: Connection) -> list[int]:
    """All non-deleted news-chunk IDs from MySQL."""
    rows = conn.execute(
        select(news_chunks_table.c.id)
        .where(news_chunks_table.c.deleted_at.is_(None))
        .order_by(news_chunks_table.c.id)
    ).all()
    return [row.id for row in rows]


def get_existing_qdrant_ids(
    client: QdrantClient, ids: list[int], collection: str = NEWS_COLLECTION_NAME
) -> set[int]:
    """Among ``ids``, which ones are already stored in Qdrant."""
    if not ids:
        return set()
    points = client.retrieve(
        collection_name=collection,
        ids=ids,
        with_payload=False,
        with_vectors=False,
    )
    return {p.id for p in points}


def fetch_chunks(conn: Connection, ids: Iterable[int]) -> list[dict]:
    ids_list = list(ids)
    if not ids_list:
        return []
    rows = conn.execute(
        select(
            news_chunks_table.c.id,
            news_chunks_table.c.content_chunk,
            news_table.c.id.label("news_id"),
            news_table.c.uuid.label("news_uuid"),
            news_table.c.candidate_id,
            news_table.c.publishing_house,
            news_table.c.source_type,
            candidates_table.c.presidential_candidate.label("candidate_name"),
        )
        .select_from(
            news_chunks_table.join(
                news_table, news_chunks_table.c.news_id == news_table.c.id
            ).join(
                candidates_table,
                news_table.c.candidate_id == candidates_table.c.id,
            )
        )
        .where(news_chunks_table.c.id.in_(ids_list))
    ).all()
    return [
        {
            "id": r.id,
            "content": r.content_chunk,
            "news_id": r.news_id,
            "news_uuid": r.news_uuid,
            "candidate_id": r.candidate_id,
            "candidate_name": r.candidate_name,
            "publishing_house": r.publishing_house,
            "source_type": r.source_type,
        }
        for r in rows
    ]


def embed_and_upsert(
    client: QdrantClient,
    embedder: Embedder,
    chunks: list[dict],
    collection: str = NEWS_COLLECTION_NAME,
) -> int:
    """Embed the vitaminized chunks and upsert them into Qdrant."""
    if not chunks:
        return 0

    vectors = embedder.embed_passages([c["content"] for c in chunks])

    points = [
        PointStruct(
            id=c["id"],
            vector=vector,
            payload={
                "news_id": c["news_id"],
                "news_uuid": c["news_uuid"],
                "candidate_id": c["candidate_id"],
                "candidate_name": c["candidate_name"],
                "publishing_house": c["publishing_house"],
                "source_type": c["source_type"],
                "content": c["content"],
            },
        )
        for c, vector in zip(chunks, vectors, strict=True)
    ]
    client.upsert(collection_name=collection, points=points)
    return len(points)
