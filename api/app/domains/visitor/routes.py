from fastapi import APIRouter, Depends, Query, status
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


@router.get("/by-ip", response_model=list[VisitorRead])
async def get_visitors_by_ip(
    ip_address: str = Query(..., max_length=45),
    db: AsyncSession = Depends(get_db),
) -> list[VisitorRead]:
    visitors = await service.get_visitors_by_ip(db, ip_address)
    return [VisitorRead.model_validate(v) for v in visitors]
