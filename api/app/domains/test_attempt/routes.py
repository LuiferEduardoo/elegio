from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.test_attempt import service
from app.domains.test_attempt.schemas import (
    TestAttemptInitialize,
    TestAttemptInitializeResponse,
    TestAttemptList,
    TestAttemptRead,
)

router = APIRouter(prefix="/test-attempts", tags=["test-attempts"])


@router.post(
    "/initialize",
    response_model=TestAttemptInitializeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def initialize_test_attempt(
    payload: TestAttemptInitialize,
    db: AsyncSession = Depends(get_db),
) -> TestAttemptInitializeResponse:
    try:
        attempt, visitor, token = await service.initialize_test_attempt(db, payload)
    except service.TestNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return TestAttemptInitializeResponse(
        test_attempt=TestAttemptRead.model_validate(attempt),
        visitor_id=visitor.id,
        token=token,
    )


@router.get("/by-ip", response_model=TestAttemptList)
async def list_by_ip(
    ip_address: str = Query(..., max_length=45),
    test_id: int | None = Query(None, gt=0),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> TestAttemptList:
    attempts, total = await service.list_test_attempts_by_ip(
        db, ip_address, limit, offset, test_id=test_id
    )
    return TestAttemptList(
        items=[TestAttemptRead.model_validate(a) for a in attempts],
        total=total,
        limit=limit,
        offset=offset,
    )
