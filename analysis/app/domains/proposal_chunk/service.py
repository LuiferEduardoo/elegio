from sqlalchemy import Connection, exists, select

from app.core.database import proposal_chunks_table, proposals_table
from app.domains.proposal_chunk.chunker import chunk_text
from app.domains.proposal_chunk.schemas import ProposalText


def get_pending_proposals(conn: Connection) -> list[ProposalText]:
    """Proposals that don't have any chunks yet (and aren't soft-deleted)."""
    already_chunked = (
        exists()
        .where(
            proposal_chunks_table.c.proposal_id == proposals_table.c.id,
            proposal_chunks_table.c.deleted_at.is_(None),
        )
    )
    stmt = (
        select(
            proposals_table.c.id,
            proposals_table.c.title,
            proposals_table.c.summary,
            proposals_table.c.full_text,
        )
        .where(
            proposals_table.c.deleted_at.is_(None),
            ~already_chunked,
        )
        .order_by(proposals_table.c.id)
    )
    return [
        ProposalText(
            id=row.id,
            title=row.title,
            summary=row.summary,
            full_text=row.full_text,
        )
        for row in conn.execute(stmt)
    ]


def chunk_and_insert(conn: Connection, proposal: ProposalText) -> int:
    """Chunk a single proposal and persist all chunks in one transaction.

    Returns the number of chunks inserted (0 if the proposal has no text).
    """
    chunks = chunk_text(proposal.to_chunkable())
    if not chunks:
        return 0

    total = len(chunks)
    conn.execute(
        proposal_chunks_table.insert(),
        [
            {
                "proposal_id": proposal.id,
                "chunk_index": i,
                "total_chunks": total,
                "content": content,
            }
            for i, content in enumerate(chunks)
        ],
    )
    conn.commit()
    return total
