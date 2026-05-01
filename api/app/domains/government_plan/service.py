from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.candidate.models import Candidate
from app.domains.government_plan.models import GovernmentPlan


class CandidateNotFoundError(Exception):
    pass


async def list_government_plans(
    db: AsyncSession, limit: int, offset: int
) -> tuple[list[GovernmentPlan], int]:
    base_filter = GovernmentPlan.deleted_at.is_(None)

    total = (
        await db.execute(select(func.count(GovernmentPlan.id)).where(base_filter))
    ).scalar_one()

    result = await db.execute(
        select(GovernmentPlan)
        .options(selectinload(GovernmentPlan.candidate))
        .where(base_filter)
        .order_by(GovernmentPlan.id)
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total


async def list_government_plans_by_candidate(
    db: AsyncSession, candidate_id: int, limit: int, offset: int
) -> tuple[list[GovernmentPlan], int]:
    candidate = await db.get(Candidate, candidate_id)
    if candidate is None or candidate.deleted_at is not None:
        raise CandidateNotFoundError(f"Candidate {candidate_id} not found")

    filters = (
        GovernmentPlan.deleted_at.is_(None),
        GovernmentPlan.candidate_id == candidate_id,
    )

    total = (
        await db.execute(select(func.count(GovernmentPlan.id)).where(*filters))
    ).scalar_one()

    result = await db.execute(
        select(GovernmentPlan)
        .options(selectinload(GovernmentPlan.candidate))
        .where(*filters)
        .order_by(GovernmentPlan.id)
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total
