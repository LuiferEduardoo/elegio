from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.candidate.models import Candidate


async def list_candidates(
    db: AsyncSession, limit: int, offset: int
) -> tuple[list[Candidate], int]:
    base_filter = Candidate.deleted_at.is_(None)

    total = (
        await db.execute(select(func.count(Candidate.id)).where(base_filter))
    ).scalar_one()

    result = await db.execute(
        select(Candidate)
        .where(base_filter)
        .order_by(Candidate.id)
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total
