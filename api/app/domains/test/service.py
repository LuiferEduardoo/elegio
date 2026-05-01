from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.test.models import Test


async def list_tests(
    db: AsyncSession, limit: int, offset: int
) -> tuple[list[Test], int]:
    base_filter = Test.deleted_at.is_(None)

    total = (
        await db.execute(select(func.count(Test.id)).where(base_filter))
    ).scalar_one()

    result = await db.execute(
        select(Test).where(base_filter).order_by(Test.id).limit(limit).offset(offset)
    )
    return list(result.scalars().all()), total
