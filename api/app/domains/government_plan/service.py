from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.government_plan.models import GovernmentPlan


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
