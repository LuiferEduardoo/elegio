from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import PUBLIC_RATE_LIMIT, limiter
from app.domains.candidate import service
from app.domains.candidate.schemas import CandidateList, CandidateRead

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("", response_model=CandidateList)
@limiter.limit(PUBLIC_RATE_LIMIT)
async def list_candidates(
    request: Request,
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


@router.get("/{candidate_id}", response_model=CandidateRead)
@limiter.limit(PUBLIC_RATE_LIMIT)
async def get_candidate(
    request: Request,
    candidate_id: int = Path(gt=0),
    db: AsyncSession = Depends(get_db),
) -> CandidateRead:
    try:
        candidate = await service.get_candidate(db, candidate_id)
    except service.CandidateNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    return CandidateRead.model_validate(candidate)
