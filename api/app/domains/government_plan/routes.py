from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import PUBLIC_RATE_LIMIT, limiter
from app.domains.government_plan import service
from app.domains.government_plan.schemas import GovernmentPlanList, GovernmentPlanRead

router = APIRouter(prefix="/government-plans", tags=["government-plans"])


@router.get("", response_model=GovernmentPlanList)
@limiter.limit(PUBLIC_RATE_LIMIT)
async def list_government_plans(
    request: Request,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> GovernmentPlanList:
    plans, total = await service.list_government_plans(db, limit, offset)
    return GovernmentPlanList(
        items=[GovernmentPlanRead.model_validate(p) for p in plans],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{candidate_id}", response_model=GovernmentPlanList)
@limiter.limit(PUBLIC_RATE_LIMIT)
async def list_government_plans_by_candidate(
    request: Request,
    candidate_id: int = Path(gt=0),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> GovernmentPlanList:
    try:
        plans, total = await service.list_government_plans_by_candidate(
            db, candidate_id, limit, offset
        )
    except service.CandidateNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return GovernmentPlanList(
        items=[GovernmentPlanRead.model_validate(p) for p in plans],
        total=total,
        limit=limit,
        offset=offset,
    )
