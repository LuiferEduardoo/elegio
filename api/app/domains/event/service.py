from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.event.models import Event
from app.domains.event.schemas import EventCreate
from app.domains.session.models import Session as VisitorSession


class SessionNotFoundError(Exception):
    pass


async def create_event(db: AsyncSession, payload: EventCreate) -> Event:
    session = (
        await db.execute(
            select(VisitorSession)
            .where(VisitorSession.ip_address == payload.ip_address)
            .order_by(VisitorSession.started_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()

    if session is None:
        raise SessionNotFoundError(
            f"No session found for ip_address={payload.ip_address}"
        )

    event = Event(
        session_id=session.id,
        visitor_id=session.visitor_id,
        **payload.model_dump(exclude={"ip_address"}),
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event
