from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import PUBLIC_RATE_LIMIT, limiter
from app.domains.proposal import service
from app.domains.proposal.schemas import ProposalList, ProposalRead

router = APIRouter(prefix="/proposals", tags=["proposals"])


@router.get("", response_model=ProposalList)
@limiter.limit(PUBLIC_RATE_LIMIT)
async def list_proposals(
    request: Request,
    candidate_id: int | None = Query(None, gt=0),
    category_id: int | None = Query(None, gt=0),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> ProposalList:
    proposals, total = await service.list_proposals(
        db,
        limit,
        offset,
        candidate_id=candidate_id,
        category_id=category_id,
    )
    return ProposalList(
        items=[ProposalRead.model_validate(p) for p in proposals],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{proposal_id}", response_model=ProposalRead)
@limiter.limit(PUBLIC_RATE_LIMIT)
async def get_proposal(
    request: Request,
    proposal_id: int = Path(gt=0),
    db: AsyncSession = Depends(get_db),
) -> ProposalRead:
    try:
        proposal = await service.get_proposal(db, proposal_id)
    except service.ProposalNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    return ProposalRead.model_validate(proposal)
