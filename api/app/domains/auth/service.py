import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.domains.auth.schemas import AuthTokenRequest
from app.domains.session.models import Session as VisitorSession
from app.domains.visitor.models import Visitor


async def create_visitor_token(
    db: AsyncSession, payload: AuthTokenRequest
) -> tuple[Visitor, str]:
    visitor = Visitor(
        visitor_uid=uuid.uuid4().hex,
        total_sessions=1,
        **payload.visitor.model_dump(),
    )
    db.add(visitor)
    await db.flush()

    session = VisitorSession(visitor_id=visitor.id, **payload.session.model_dump())
    db.add(session)

    await db.commit()
    await db.refresh(visitor)
    await db.refresh(session)

    token = create_access_token(
        {
            "visitor_id": visitor.id,
            "session_id": session.id,
        }
    )

    return visitor, token
