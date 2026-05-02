from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import PUBLIC_RATE_LIMIT, limiter
from app.domains.test import service
from app.domains.test.schemas import TestList, TestRead

router = APIRouter(prefix="/tests", tags=["tests"])


@router.get("", response_model=TestList)
@limiter.limit(PUBLIC_RATE_LIMIT)
async def list_tests(
    request: Request,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> TestList:
    tests, total = await service.list_tests(db, limit, offset)
    return TestList(
        items=[TestRead.model_validate(t) for t in tests],
        total=total,
        limit=limit,
        offset=offset,
    )
