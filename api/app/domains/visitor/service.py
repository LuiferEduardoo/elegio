import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.session.models import Session as VisitorSession
from app.domains.visitor.models import Visitor
from app.domains.visitor.schemas import SessionCreate, VisitorCreate


async def track_visit(
    db: AsyncSession,
    visitor_data: VisitorCreate,
    session_data: SessionCreate,
) -> tuple[Visitor, VisitorSession]:
    visitor = Visitor(
        visitor_uid=uuid.uuid4().hex,
        total_sessions=1,
        **visitor_data.model_dump(),
    )
    db.add(visitor)
    await db.flush()

    session = VisitorSession(visitor_id=visitor.id, **session_data.model_dump())
    db.add(session)

    await db.commit()
    await db.refresh(visitor)
    await db.refresh(session)

    return visitor, session


async def get_visitors_by_ip(db: AsyncSession, ip_address: str) -> list[Visitor]:
    result = await db.execute(
        select(Visitor)
        .join(VisitorSession, VisitorSession.visitor_id == Visitor.id)
        .where(VisitorSession.ip_address == ip_address)
        .distinct()
    )
    return list(result.scalars().all())
