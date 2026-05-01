import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.domains.session.models import Session as VisitorSession
from app.domains.test.models import Test
from app.domains.test_attempt.models import TestAttempt
from app.domains.test_attempt.schemas import TestAttemptInitialize
from app.domains.visitor.models import Visitor


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
