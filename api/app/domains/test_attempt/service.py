from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.session.models import Session as VisitorSession
from app.domains.test.models import Test
from app.domains.test_attempt.models import TestAttempt
from app.domains.visitor.models import Visitor


class VisitorNotFoundError(Exception):
    pass


class TestNotFoundError(Exception):
    pass


async def create_test_attempt(
    db: AsyncSession, test_id: int, ip_address: str
) -> TestAttempt:
    test = await db.get(Test, test_id)
    if test is None or test.deleted_at is not None:
        raise TestNotFoundError(f"Test {test_id} not found")

    visitor = (
        await db.execute(
            select(Visitor)
            .join(VisitorSession, VisitorSession.visitor_id == Visitor.id)
            .where(VisitorSession.ip_address == ip_address)
            .order_by(VisitorSession.started_at.desc())
            .limit(1)
        )
    ).scalars().first()

    if visitor is None:
        raise VisitorNotFoundError(
            f"No visitor found for ip_address={ip_address}"
        )

    attempt = TestAttempt(visitor_id=visitor.id, test_id=test_id)
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)
    return attempt
