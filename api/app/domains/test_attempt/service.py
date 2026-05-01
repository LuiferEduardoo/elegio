from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.session.models import Session as VisitorSession
from app.domains.test.models import Test
from app.domains.test_attempt.models import TestAttempt
from app.domains.visitor.models import Visitor


class VisitorNotFoundError(Exception):
    pass


class TestNotFoundError(Exception):
    pass


async def _resolve_visitor_id_by_ip(
    db: AsyncSession, ip_address: str
) -> int | None:
    return (
        await db.execute(
            select(Visitor.id)
            .join(VisitorSession, VisitorSession.visitor_id == Visitor.id)
            .where(VisitorSession.ip_address == ip_address)
            .order_by(VisitorSession.started_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()


async def create_test_attempt(
    db: AsyncSession, test_id: int, ip_address: str
) -> TestAttempt:
    test = await db.get(Test, test_id)
    if test is None or test.deleted_at is not None:
        raise TestNotFoundError(f"Test {test_id} not found")

    visitor_id = await _resolve_visitor_id_by_ip(db, ip_address)
    if visitor_id is None:
        raise VisitorNotFoundError(
            f"No visitor found for ip_address={ip_address}"
        )

    attempt = TestAttempt(visitor_id=visitor_id, test_id=test_id)
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)
    return attempt


async def list_test_attempts_by_ip(
    db: AsyncSession,
    ip_address: str,
    limit: int,
    offset: int,
    test_id: int | None = None,
) -> tuple[list[TestAttempt], int]:
    visitor_id = await _resolve_visitor_id_by_ip(db, ip_address)
    if visitor_id is None:
        return [], 0

    filters = [
        TestAttempt.visitor_id == visitor_id,
        TestAttempt.deleted_at.is_(None),
    ]
    if test_id is not None:
        filters.append(TestAttempt.test_id == test_id)

    total = (
        await db.execute(select(func.count(TestAttempt.id)).where(*filters))
    ).scalar_one()

    result = await db.execute(
        select(TestAttempt)
        .where(*filters)
        .order_by(TestAttempt.started_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total
