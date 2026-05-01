from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.proposal import service
from app.domains.proposal.schemas import ProposalList, ProposalRead

router = APIRouter(prefix="/proposals", tags=["proposals"])


@router.get("", response_model=ProposalList)
async def list_proposals(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> ProposalList:
    proposals, total = await service.list_proposals(db, limit, offset)
    return ProposalList(
        items=[ProposalRead.model_validate(p) for p in proposals],
        total=total,
        limit=limit,
        offset=offset,
    )
