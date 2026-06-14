from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import PRIVATE_RATE_LIMIT, limiter
from app.core.security import get_token_payload
from app.domains.answer import service
from app.domains.answer.schemas import (
    AffinityResponse,
    AnswerCreate,
    AnswerCreateResponse,
    AnswerList,
    AnswerRead,
    AnswerUpdate,
)

router = APIRouter(prefix="/answers", tags=["answers"])


@router.post(
    "/{test_attempt_id}",
    response_model=AnswerCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(PRIVATE_RATE_LIMIT)
async def create_answer(
    request: Request,
    payload: AnswerCreate,
    test_attempt_id: int = Path(gt=0),
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> AnswerCreateResponse:
    try:
        answer, test_completed, test_status = await service.create_answer(
            db, payload, token_payload.get("visitor_id"), test_attempt_id
        )
    except (
        service.TestAttemptNotFoundError,
        service.QuestionNotFoundError,
        service.ResponseOptionNotFoundError,
    ) as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    except (
        service.TestAttemptNotInProgressError,
        service.QuestionDoesNotBelongToTestError,
        service.ResponseOptionDoesNotBelongToQuestionError,
    ) as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

    return AnswerCreateResponse(
        answer=AnswerRead.model_validate(answer),
        test_completed=test_completed,
        test_attempt_status=test_status,
    )


@router.patch("/{test_attempt_id}/{answer_id}", response_model=AnswerRead)
@limiter.limit(PRIVATE_RATE_LIMIT)
async def update_answer(
    request: Request,
    payload: AnswerUpdate,
    test_attempt_id: int = Path(gt=0),
    answer_id: int = Path(gt=0),
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> AnswerRead:
    try:
        answer = await service.update_answer(
            db, answer_id, payload, token_payload.get("visitor_id"), test_attempt_id
        )
    except (
        service.AnswerNotFoundError,
        service.TestAttemptNotFoundError,
        service.ResponseOptionNotFoundError,
    ) as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    except (
        service.TestAttemptNotInProgressError,
        service.ResponseOptionDoesNotBelongToQuestionError,
    ) as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

    return AnswerRead.model_validate(answer)


@router.get("/affinity", response_model=AffinityResponse)
@limiter.limit(PRIVATE_RATE_LIMIT)
async def get_affinity(
    request: Request,
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> AffinityResponse:
    try:
        return await service.get_affinity(
            db, token_payload.get("visitor_id")
        )
    except service.TestAttemptNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.get("/{test_id}", response_model=AnswerList)
@limiter.limit(PRIVATE_RATE_LIMIT)
async def list_answers(
    request: Request,
    test_id: int = Path(gt=0),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> AnswerList:
    answers, total = await service.list_answers(
        db,
        token_payload.get("visitor_id"),
        test_id,
        limit,
        offset,
    )
    return AnswerList(
        items=[AnswerRead.model_validate(a) for a in answers],
        total=total,
        limit=limit,
        offset=offset,
    )
