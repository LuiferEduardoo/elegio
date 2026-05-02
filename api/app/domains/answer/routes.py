from api.app.core.security import get_token_payload
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.answer import service
from app.domains.answer.schemas import (
    AnswerCreate,
    AnswerCreateResponse,
    AnswerList,
    AnswerRead,
    AnswerUpdate,
)

router = APIRouter(prefix="/answers", tags=["answers"])


@router.post(
    "",
    response_model=AnswerCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_answer(
    payload: AnswerCreate,
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> AnswerCreateResponse:
    try:
        answer, test_completed, test_status = await service.create_answer(db, {**payload, "uuid_test_attempt": token_payload.get("test_attempt_uuid")})
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


@router.patch("/{answer_id}", response_model=AnswerRead)
async def update_answer(
    payload: AnswerUpdate,
    answer_id: int = Path(gt=0),
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> AnswerRead:
    try:
        answer = await service.update_answer(db, answer_id, payload, token_payload.get("test_attempt_uuid"))
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


@router.get("/by-ip", response_model=AnswerList)
async def list_answers_by_ip_and_test(
    ip_address: str = Query(..., max_length=45),
    test_id: int = Query(..., gt=0),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> AnswerList:
    answers, total = await service.list_answers_by_ip_and_test(
        db, ip_address, test_id, limit, offset
    )
    return AnswerList(
        items=[AnswerRead.model_validate(a) for a in answers],
        total=total,
        limit=limit,
        offset=offset,
    )
