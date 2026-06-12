from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import PRIVATE_RATE_LIMIT, limiter
from app.core.security import get_token_payload
from app.domains.event import service
from app.domains.event.schemas import EventCreate, EventRead

router = APIRouter(prefix="/events", tags=["events"])


@router.post(
    "",
    response_model=EventRead,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(PRIVATE_RATE_LIMIT)
async def create_event(
    request: Request,
    payload: EventCreate,
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> EventRead:
    visitor_id = token_payload.get("visitor_id")
    if not visitor_id:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Token missing visitor_id"
        )

    try:
        event = await service.create_event(db, payload, visitor_id)
    except service.SessionNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return EventRead.model_validate(event)
