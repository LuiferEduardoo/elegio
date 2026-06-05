"""Chunk loaded documents into the ``document_chunks`` table.

Finds documents with no chunks yet and splits their Markdown ``content`` with
the structure-aware :func:`chunk_markdown`, storing each chunk (heading context
included) in ``content_chunk``.
"""

from dataclasses import dataclass

from sqlalchemy import Connection, exists, select

from app.core.database import document_chunks_table, documents_table
from app.domains.document_chunk.chunker import chunk_markdown


@dataclass(slots=True)
class DocumentForChunking:
    id: int
    content: str


def get_pending_documents(conn: Connection) -> list[DocumentForChunking]:
    """Documents that have no chunks yet (and aren't soft-deleted)."""
    already_chunked = exists().where(
        document_chunks_table.c.document_id == documents_table.c.id,
        document_chunks_table.c.deleted_at.is_(None),
    )
    stmt = (
        select(documents_table.c.id, documents_table.c.content)
        .where(documents_table.c.deleted_at.is_(None), ~already_chunked)
        .order_by(documents_table.c.id)
    )
    return [DocumentForChunking(id=r.id, content=r.content) for r in conn.execute(stmt)]


def chunk_and_insert(conn: Connection, document: DocumentForChunking) -> int:
    """Chunk one document and persist all chunks atomically."""
    chunks = chunk_markdown(document.content)
    if not chunks:
        return 0

    total = len(chunks)
    conn.execute(
        document_chunks_table.insert(),
        [
            {
                "document_id": document.id,
                "chunk_index": i,
                "total_chunks": total,
                "content_chunk": chunk,
            }
            for i, chunk in enumerate(chunks)
        ],
    )
    conn.commit()
    return total
