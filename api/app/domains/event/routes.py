from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.event import service
from app.domains.event.schemas import EventCreate, EventRead

router = APIRouter(prefix="/events", tags=["events"])


@router.post(
    "",
    response_model=EventRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    payload: EventCreate,
    db: AsyncSession = Depends(get_db),
) -> EventRead:
    try:
        event = await service.create_event(db, payload)
    except service.SessionNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    return EventRead.model_validate(event)
