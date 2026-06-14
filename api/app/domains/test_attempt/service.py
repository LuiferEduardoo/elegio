import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.test.models import Test
from app.domains.test_attempt.models import TestAttempt
from app.domains.visitor.models import Visitor


class TestNotFoundError(Exception):
    pass


class VisitorNotFoundError(Exception):
    pass


class TestAttemptNotFoundError(Exception):
    pass


async def initialize_test_attempt(
    db: AsyncSession, test_id: int, visitor_id: int
) -> TestAttempt:
    test = await db.get(Test, test_id)
    if test is None or test.deleted_at is not None:
        raise TestNotFoundError(f"Test {test_id} not found")

    visitor = await db.get(Visitor, visitor_id)
    if visitor is None or visitor.deleted_at is not None:
        raise VisitorNotFoundError(f"Visitor {visitor_id} not found")

    attempt = TestAttempt(
        uuid=str(uuid.uuid4()),
        visitor_id=visitor_id,
        test_id=test_id,
    )
    db.add(attempt)

    await db.commit()
    await db.refresh(attempt)

    return attempt


async def get_current_test_attempt_by_visitor(
    db: AsyncSession, visitor_id: int, test_id: int | None = None
) -> TestAttempt:
    filters = [
        TestAttempt.visitor_id == visitor_id,
        TestAttempt.deleted_at.is_(None),
    ]
    if test_id is not None:
        filters.append(TestAttempt.test_id == test_id)

    result = await db.execute(
        select(TestAttempt)
        .where(*filters)
        .order_by(TestAttempt.created_at.desc(), TestAttempt.id.desc())
        .limit(1)
    )
    attempt = result.scalar_one_or_none()
    if attempt is None:
        detail = f"No test attempt found for visitor {visitor_id}"
        if test_id is not None:
            detail += f" and test {test_id}"
        raise TestAttemptNotFoundError(detail)
    return attempt
