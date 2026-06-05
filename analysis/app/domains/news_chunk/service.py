"""Chunk loaded news into the ``news_chunks`` table.

Mirrors ``proposal_chunk.service``: find news with no chunks yet, split the raw
content with the shared paragraph-aware chunker, then store the *vitaminized*
text (candidate + outlet + headline prefix) in ``content_chunk`` so the value
embedded later is exactly what lives in MySQL.
"""

from dataclasses import dataclass

from sqlalchemy import Connection, exists, select

from app.core.database import candidates_table, news_chunks_table, news_table
from app.domains.news_chunk.vitaminize import vitaminize
from app.domains.proposal_chunk.chunker import chunk_text


@dataclass(slots=True)
class NewsForChunking:
    id: int
    title: str
    content_raw: str
    publishing_house: str
    candidate_name: str


def get_pending_news(conn: Connection) -> list[NewsForChunking]:
    """News rows that have no chunks yet (and aren't soft-deleted)."""
    already_chunked = exists().where(
        news_chunks_table.c.news_id == news_table.c.id,
        news_chunks_table.c.deleted_at.is_(None),
    )
    stmt = (
        select(
            news_table.c.id,
            news_table.c.title,
            news_table.c.content_raw,
            news_table.c.publishing_house,
            candidates_table.c.presidential_candidate.label("candidate_name"),
        )
        .select_from(
            news_table.join(
                candidates_table,
                news_table.c.candidate_id == candidates_table.c.id,
            )
        )
        .where(news_table.c.deleted_at.is_(None), ~already_chunked)
        .order_by(news_table.c.id)
    )
    return [
        NewsForChunking(
            id=r.id,
            title=r.title,
            content_raw=r.content_raw,
            publishing_house=r.publishing_house,
            candidate_name=r.candidate_name,
        )
        for r in conn.execute(stmt)
    ]


def chunk_and_insert(conn: Connection, news: NewsForChunking) -> int:
    """Chunk one news article and persist all (vitaminized) chunks atomically."""
    chunks = chunk_text(news.content_raw)
    if not chunks:
        return 0

    total = len(chunks)
    conn.execute(
        news_chunks_table.insert(),
        [
            {
                "news_id": news.id,
                "chunk_index": i,
                "total_chunks": total,
                "content_chunk": vitaminize(
                    candidate_name=news.candidate_name,
                    publishing_house=news.publishing_house,
                    title=news.title,
                    chunk=chunk,
                ),
            }
            for i, chunk in enumerate(chunks)
        ],
    )
    conn.commit()
    return total
