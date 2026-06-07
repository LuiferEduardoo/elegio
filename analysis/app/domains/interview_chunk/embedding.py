"""Embed interview chunks and upsert them into the Qdrant ``interview_chunks`` collection.

Mirrors the other chunk embedders: Qdrant point id == MySQL
``interview_chunks.id`` so upserts are idempotent. ``content_chunk`` (speaker-
labelled turns) is the embedded text and payload ``content``; the rest of the
payload is hydrated by joining ``interviews`` and ``candidates``.
"""

from collections.abc import Iterable

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sqlalchemy import Connection, select

from app.core.database import (
    candidates_table,
    interview_chunks_table,
    interviews_table,
)
from app.core.embedder import Embedder
from app.core.qdrant_client import INTERVIEW_COLLECTION_NAME


def get_all_chunk_ids(conn: Connection) -> list[int]:
    """All non-deleted interview-chunk IDs from MySQL."""
    rows = conn.execute(
        select(interview_chunks_table.c.id)
        .where(interview_chunks_table.c.deleted_at.is_(None))
        .order_by(interview_chunks_table.c.id)
    ).all()
    return [row.id for row in rows]


def get_existing_qdrant_ids(
    client: QdrantClient, ids: list[int], collection: str = INTERVIEW_COLLECTION_NAME
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
            interview_chunks_table.c.id,
            interview_chunks_table.c.content_chunk,
            interview_chunks_table.c.start_time,
            interview_chunks_table.c.end_time,
            interviews_table.c.id.label("interview_id"),
            interviews_table.c.uuid.label("interview_uuid"),
            interviews_table.c.candidate_id,
            interviews_table.c.source_type,
            interviews_table.c.format_type,
            interviews_table.c.title,
            interviews_table.c.media_outlet,
            interviews_table.c.url_video_audio,
            candidates_table.c.presidential_candidate.label("candidate_name"),
        )
        .select_from(
            interview_chunks_table.join(
                interviews_table,
                interview_chunks_table.c.interview_id == interviews_table.c.id,
            ).join(
                candidates_table,
                interviews_table.c.candidate_id == candidates_table.c.id,
            )
        )
        .where(interview_chunks_table.c.id.in_(ids_list))
    ).all()
    return [
        {
            "id": r.id,
            "content": r.content_chunk,
            "start_time": r.start_time.strftime("%H:%M:%S") if r.start_time else None,
            "end_time": r.end_time.strftime("%H:%M:%S") if r.end_time else None,
            "interview_id": r.interview_id,
            "interview_uuid": r.interview_uuid,
            "candidate_id": r.candidate_id,
            "candidate_name": r.candidate_name,
            "source_type": r.source_type,
            "format_type": r.format_type,
            "title": r.title,
            "media_outlet": r.media_outlet,
            "url_video_audio": r.url_video_audio,
        }
        for r in rows
    ]


def embed_and_upsert(
    client: QdrantClient,
    embedder: Embedder,
    chunks: list[dict],
    collection: str = INTERVIEW_COLLECTION_NAME,
) -> int:
    """Embed the interview chunks and upsert them into Qdrant."""
    if not chunks:
        return 0

    vectors = embedder.embed_passages([c["content"] for c in chunks])

    points = [
        PointStruct(
            id=c["id"],
            vector=vector,
            payload={
                "interview_id": c["interview_id"],
                "interview_uuid": c["interview_uuid"],
                "candidate_id": c["candidate_id"],
                "candidate_name": c["candidate_name"],
                "source_type": c["source_type"],
                "format_type": c["format_type"],
                "title": c["title"],
                "media_outlet": c["media_outlet"],
                "url_video_audio": c["url_video_audio"],
                "start_time": c["start_time"],
                "end_time": c["end_time"],
                "content": c["content"],
            },
        )
        for c, vector in zip(chunks, vectors, strict=True)
    ]
    client.upsert(collection_name=collection, points=points)
    return len(points)
