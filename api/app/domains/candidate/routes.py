from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.candidate import service
from app.domains.candidate.schemas import CandidateList, CandidateRead

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("", response_model=CandidateList)
async def list_candidates(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> CandidateList:
    candidates, total = await service.list_candidates(db, limit, offset)
    return CandidateList(
        items=[CandidateRead.model_validate(c) for c in candidates],
        total=total,
        limit=limit,
        offset=offset,
    )
