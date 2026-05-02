from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import PUBLIC_RATE_LIMIT, limiter
from app.core.security import get_token_payload
from app.domains.test_attempt import service
from app.domains.test_attempt.schemas import (
    TestAttemptInitialize,
    TestAttemptInitializeResponse,
    TestAttemptRead,
)

router = APIRouter(prefix="/test-attempts", tags=["test-attempts"])


@router.post(
    "/initialize",
    response_model=TestAttemptInitializeResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(PUBLIC_RATE_LIMIT)
async def initialize_test_attempt(
    request: Request,
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


@router.get("", response_model=TestAttemptRead)
async def get_test_attempt_from_token(
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> TestAttemptRead:
    attempt_uuid = token_payload.get("test_attempt_uuid")
    if not attempt_uuid:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Token missing test_attempt_uuid"
        )

    try:
        attempt = await service.get_test_attempt_by_uuid(db, attempt_uuid)
    except service.TestAttemptNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return TestAttemptRead.model_validate(attempt)
