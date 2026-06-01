from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import PUBLIC_RATE_LIMIT, limiter
from app.domains.search import service
from app.domains.search.schemas import SearchResponse

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/proposals", response_model=SearchResponse)
@limiter.limit(PUBLIC_RATE_LIMIT)
async def search_proposals(
    request: Request,
    q: str = Query(..., min_length=1, description="Search query"),
    category_id: int | None = Query(None, gt=0),
    candidate_id: int | None = Query(None, gt=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> SearchResponse:
    try:
        return await service.search_proposals(db, q, category_id, candidate_id, limit)
    except service.InvalidCandidateForSearchError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
