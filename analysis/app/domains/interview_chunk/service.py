"""Chunk loaded interviews into the ``interview_chunks`` table.

Finds interviews with no chunks yet, reads their merged ``interview_segments``
in order and groups them into conversational chunks with :func:`chunk_turns`.
"""

from sqlalchemy import Connection, exists, select

from app.core.database import interview_chunks_table, interview_segments_table
from app.domains.interview_chunk.chunker import Turn, chunk_turns


def get_pending_interview_ids(conn: Connection) -> list[int]:
    """Interview ids that have segments but no chunks yet."""
    already_chunked = exists().where(
        interview_chunks_table.c.interview_id == interview_segments_table.c.interview_id,
        interview_chunks_table.c.deleted_at.is_(None),
    )
    rows = conn.execute(
        select(interview_segments_table.c.interview_id)
        .where(interview_segments_table.c.deleted_at.is_(None), ~already_chunked)
        .distinct()
        .order_by(interview_segments_table.c.interview_id)
    ).all()
    return [r.interview_id for r in rows]


def _turns(conn: Connection, interview_id: int) -> list[Turn]:
    rows = conn.execute(
        select(
            interview_segments_table.c.start_time,
            interview_segments_table.c.end_time,
            interview_segments_table.c.speaker,
            interview_segments_table.c.text_segment,
        )
        .where(
            interview_segments_table.c.interview_id == interview_id,
            interview_segments_table.c.deleted_at.is_(None),
        )
        .order_by(interview_segments_table.c.id)
    ).all()
    return [Turn(r.start_time, r.end_time, r.speaker, r.text_segment) for r in rows]


def chunk_and_insert(conn: Connection, interview_id: int) -> int:
    """Chunk one interview's turns and persist all chunks atomically."""
    chunks = chunk_turns(_turns(conn, interview_id))
    if not chunks:
        return 0

    total = len(chunks)
    conn.execute(
        interview_chunks_table.insert(),
        [
            {
                "interview_id": interview_id,
                "chunk_index": i,
                "total_chunks": total,
                "start_time": c.start_time,
                "end_time": c.end_time,
                "content_chunk": c.content,
            }
            for i, c in enumerate(chunks)
        ],
    )
    conn.commit()
    return total
