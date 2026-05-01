import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.domains.session.models import Session as VisitorSession
from app.domains.test.models import Test
from app.domains.test_attempt.models import TestAttempt
from app.domains.test_attempt.schemas import TestAttemptInitialize
from app.domains.visitor.models import Visitor


class TestNotFoundError(Exception):
    pass


class TestAttemptNotFoundError(Exception):
    pass


async def initialize_test_attempt(
    db: AsyncSession, payload: TestAttemptInitialize
) -> tuple[TestAttempt, Visitor, str]:
    test = await db.get(Test, payload.test_id)
    if test is None or test.deleted_at is not None:
        raise TestNotFoundError(f"Test {payload.test_id} not found")

    visitor = Visitor(
        visitor_uid=uuid.uuid4().hex,
        total_sessions=1,
        **payload.visitor.model_dump(),
    )
    db.add(visitor)
    await db.flush()

    session = VisitorSession(visitor_id=visitor.id, **payload.session.model_dump())
    db.add(session)
    await db.flush()

    attempt = TestAttempt(
        uuid=str(uuid.uuid4()),
        visitor_id=visitor.id,
        test_id=payload.test_id,
    )
    db.add(attempt)

    await db.commit()
    await db.refresh(attempt)
    await db.refresh(visitor)

    token = create_access_token(
        {
            "test_attempt_uuid": attempt.uuid,
            "visitor_id": visitor.id,
            "test_id": payload.test_id,
        }
    )

    return attempt, visitor, token


async def get_test_attempt_by_uuid(
    db: AsyncSession, attempt_uuid: str
) -> TestAttempt:
    result = await db.execute(
        select(TestAttempt).where(
            TestAttempt.uuid == attempt_uuid,
            TestAttempt.deleted_at.is_(None),
        )
    )
    attempt = result.scalar_one_or_none()
    if attempt is None:
        raise TestAttemptNotFoundError(f"TestAttempt {attempt_uuid} not found")
    return attempt
