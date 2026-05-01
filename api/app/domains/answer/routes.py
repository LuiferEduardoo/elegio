from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.answer import service
from app.domains.answer.schemas import (
    AnswerCreate,
    AnswerCreateResponse,
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
    db: AsyncSession = Depends(get_db),
) -> AnswerCreateResponse:
    try:
        answer, test_completed, test_status = await service.create_answer(db, payload)
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
    db: AsyncSession = Depends(get_db),
) -> AnswerRead:
    try:
        answer = await service.update_answer(db, answer_id, payload)
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
