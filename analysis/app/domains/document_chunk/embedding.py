"""Embed document chunks and upsert them into the Qdrant ``document_chunks`` collection.

Mirrors ``news_chunk.embedding``: Qdrant point id == MySQL ``document_chunks.id``
so upserts are idempotent. ``content_chunk`` is the structure-aware text, used as
both the embedded text and the payload ``content``. The rest of the payload is
hydrated by joining ``documents`` and ``candidates``.
"""

from collections.abc import Iterable

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sqlalchemy import Connection, select

from app.core.database import candidates_table, document_chunks_table, documents_table
from app.core.embedder import Embedder
from app.core.qdrant_client import DOCUMENT_COLLECTION_NAME


def get_all_chunk_ids(conn: Connection) -> list[int]:
    """All non-deleted document-chunk IDs from MySQL."""
    rows = conn.execute(
        select(document_chunks_table.c.id)
        .where(document_chunks_table.c.deleted_at.is_(None))
        .order_by(document_chunks_table.c.id)
    ).all()
    return [row.id for row in rows]


def get_existing_qdrant_ids(
    client: QdrantClient, ids: list[int], collection: str = DOCUMENT_COLLECTION_NAME
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
            document_chunks_table.c.id,
            document_chunks_table.c.content_chunk,
            documents_table.c.id.label("document_id"),
            documents_table.c.uuid.label("document_uuid"),
            documents_table.c.candidate_id,
            documents_table.c.source_type,
            documents_table.c.type,
            documents_table.c.title,
            documents_table.c.publishing_house,
            documents_table.c.url,
            candidates_table.c.presidential_candidate.label("candidate_name"),
        )
        .select_from(
            document_chunks_table.join(
                documents_table,
                document_chunks_table.c.document_id == documents_table.c.id,
            ).join(
                candidates_table,
                documents_table.c.candidate_id == candidates_table.c.id,
            )
        )
        .where(document_chunks_table.c.id.in_(ids_list))
    ).all()
    return [
        {
            "id": r.id,
            "content": r.content_chunk,
            "document_id": r.document_id,
            "document_uuid": r.document_uuid,
            "candidate_id": r.candidate_id,
            "candidate_name": r.candidate_name,
            "source_type": r.source_type,
            "type": r.type,
            "title": r.title,
            "publishing_house": r.publishing_house,
            "url": r.url,
        }
        for r in rows
    ]


def embed_and_upsert(
    client: QdrantClient,
    embedder: Embedder,
    chunks: list[dict],
    collection: str = DOCUMENT_COLLECTION_NAME,
) -> int:
    """Embed the document chunks and upsert them into Qdrant."""
    if not chunks:
        return 0

    vectors = embedder.embed_passages([c["content"] for c in chunks])

    points = [
        PointStruct(
            id=c["id"],
            vector=vector,
            payload={
                "document_id": c["document_id"],
                "document_uuid": c["document_uuid"],
                "candidate_id": c["candidate_id"],
                "candidate_name": c["candidate_name"],
                "source_type": c["source_type"],
                "type": c["type"],
                "title": c["title"],
                "publishing_house": c["publishing_house"],
                "url": c["url"],
                "content": c["content"],
            },
        )
        for c, vector in zip(chunks, vectors, strict=True)
    ]
    client.upsert(collection_name=collection, points=points)
    return len(points)
