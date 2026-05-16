from collections.abc import Iterable

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sqlalchemy import Connection, select

from app.core.database import proposal_chunks_table
from app.core.embedder import Embedder
from app.core.qdrant_client import COLLECTION_NAME


def get_all_chunk_ids(conn: Connection) -> list[int]:
    """All non-deleted chunk IDs from MySQL."""
    rows = conn.execute(
        select(proposal_chunks_table.c.id)
        .where(proposal_chunks_table.c.deleted_at.is_(None))
        .order_by(proposal_chunks_table.c.id)
    ).all()
    return [row.id for row in rows]


def get_existing_qdrant_ids(
    client: QdrantClient, ids: list[int], collection: str = COLLECTION_NAME
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


def fetch_chunks(
    conn: Connection, ids: Iterable[int]
) -> list[dict]:
    ids_list = list(ids)
    if not ids_list:
        return []
    rows = conn.execute(
        select(
            proposal_chunks_table.c.id,
            proposal_chunks_table.c.proposal_id,
            proposal_chunks_table.c.chunk_index,
            proposal_chunks_table.c.total_chunks,
            proposal_chunks_table.c.content,
        ).where(proposal_chunks_table.c.id.in_(ids_list))
    ).all()
    return [
        {
            "id": r.id,
            "proposal_id": r.proposal_id,
            "chunk_index": r.chunk_index,
            "total_chunks": r.total_chunks,
            "content": r.content,
        }
        for r in rows
    ]


def embed_and_upsert(
    client: QdrantClient,
    embedder: Embedder,
    chunks: list[dict],
    collection: str = COLLECTION_NAME,
) -> int:
    """Embed the given chunks and upsert them into Qdrant.

    Point ID = MySQL chunk id, so the operation is naturally idempotent.
    The payload mirrors the row so the Qdrant dashboard is self-explanatory
    and downstream consumers can hydrate results without round-tripping MySQL.
    """
    if not chunks:
        return 0

    vectors = embedder.embed_passages([c["content"] for c in chunks])

    points = [
        PointStruct(
            id=c["id"],
            vector=vector,
            payload={
                "proposal_id": c["proposal_id"],
                "chunk_index": c["chunk_index"],
                "total_chunks": c["total_chunks"],
                "content": c["content"],
            },
        )
        for c, vector in zip(chunks, vectors, strict=True)
    ]
    client.upsert(collection_name=collection, points=points)
    return len(points)
