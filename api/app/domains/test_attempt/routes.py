from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import PRIVATE_RATE_LIMIT, limiter
from app.core.security import get_token_payload
from app.domains.test_attempt import service
from app.domains.test_attempt.schemas import TestAttemptInitialize, TestAttemptRead

router = APIRouter(prefix="/test-attempts", tags=["test-attempts"])


def _get_visitor_id(token_payload: dict[str, Any]) -> int:
    visitor_id = token_payload.get("visitor_id")
    if not visitor_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token missing visitor_id")
    return visitor_id


@router.post(
    "/initialize",
    response_model=TestAttemptRead,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(PRIVATE_RATE_LIMIT)
async def initialize_test_attempt(
    request: Request,
    payload: TestAttemptInitialize,
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> TestAttemptRead:
    visitor_id = _get_visitor_id(token_payload)

    try:
        attempt = await service.initialize_test_attempt(db, payload.test_id, visitor_id)
    except (service.TestNotFoundError, service.VisitorNotFoundError) as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return TestAttemptRead.model_validate(attempt)


@router.get("", response_model=TestAttemptRead)
@limiter.limit(PRIVATE_RATE_LIMIT)
async def get_test_attempt_from_token(
    request: Request,
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> TestAttemptRead:
    visitor_id = _get_visitor_id(token_payload)

    try:
        attempt = await service.get_current_test_attempt_by_visitor(db, visitor_id)
    except service.TestAttemptNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return TestAttemptRead.model_validate(attempt)
