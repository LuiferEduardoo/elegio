from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.test_attempt import service
from app.domains.test_attempt.schemas import TestAttemptCreate, TestAttemptRead

router = APIRouter(prefix="/test-attempts", tags=["test-attempts"])


@router.post(
    "",
    response_model=TestAttemptRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_test_attempt(
    payload: TestAttemptCreate,
    db: AsyncSession = Depends(get_db),
) -> TestAttemptRead:
    try:
        attempt = await service.create_test_attempt(
            db, test_id=payload.test_id, ip_address=payload.ip_address
        )
    except service.TestNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    except service.VisitorNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return TestAttemptRead.model_validate(attempt)
