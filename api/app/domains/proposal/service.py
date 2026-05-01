from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.posture import models as _posture_models  # noqa: F401  registers Posture mapper for Proposal.postures
from app.domains.proposal.models import Proposal


async def list_proposals(
    db: AsyncSession, limit: int, offset: int
) -> tuple[list[Proposal], int]:
    base_filter = Proposal.deleted_at.is_(None)

    total = (
        await db.execute(select(func.count(Proposal.id)).where(base_filter))
    ).scalar_one()

    result = await db.execute(
        select(Proposal)
        .options(
            selectinload(Proposal.category),
            selectinload(Proposal.candidate),
            selectinload(Proposal.postures),
        )
        .where(base_filter)
        .order_by(Proposal.id)
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total
