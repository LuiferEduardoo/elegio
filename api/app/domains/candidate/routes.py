from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import PUBLIC_RATE_LIMIT, limiter
from app.domains.candidate import service
from app.domains.candidate.schemas import CandidateList, CandidateRead

router = APIRouter(prefix="/candidates", tags=["candidates"])


def _build_candidate_read(
    candidate, averages_by_id: dict[int, list]
) -> CandidateRead:
    read = CandidateRead.model_validate(candidate)
    read.category_averages = averages_by_id.get(candidate.id, [])
    return read


@router.get("", response_model=CandidateList)
@limiter.limit(PUBLIC_RATE_LIMIT)
async def list_candidates(
    request: Request,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> CandidateList:
    candidates, total = await service.list_candidates(db, limit, offset)
    averages_by_id = await service.get_category_averages_by_candidate(
        db, [c.id for c in candidates]
    )
    return CandidateList(
        items=[_build_candidate_read(c, averages_by_id) for c in candidates],
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
    averages_by_id = await service.get_category_averages_by_candidate(
        db, [candidate.id]
    )
    return _build_candidate_read(candidate, averages_by_id)
