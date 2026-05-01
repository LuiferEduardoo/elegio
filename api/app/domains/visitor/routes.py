from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.visitor import service
from app.domains.visitor.schemas import (
    SessionRead,
    VisitorRead,
    VisitorTrackRequest,
    VisitorTrackResponse,
)

router = APIRouter(prefix="/visitors", tags=["visitors"])


@router.post(
    "",
    response_model=VisitorTrackResponse,
    status_code=status.HTTP_201_CREATED,
)
async def track_visitor(
    payload: VisitorTrackRequest,
    db: AsyncSession = Depends(get_db),
) -> VisitorTrackResponse:
    visitor, session = await service.track_visit(db, payload.visitor, payload.session)
    return VisitorTrackResponse(
        visitor=VisitorRead.model_validate(visitor),
        session=SessionRead.model_validate(session),
    )
