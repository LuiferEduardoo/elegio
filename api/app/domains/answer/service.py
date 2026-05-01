from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.answer.models import Answer
from app.domains.answer.schemas import AnswerCreate, AnswerUpdate
from app.domains.question.models import Question
from app.domains.response_option.models import ResponseOption
from app.domains.test_attempt.models import TestAttempt, TestStatus


class AnswerNotFoundError(Exception):
    pass


class TestAttemptNotFoundError(Exception):
    pass


class TestAttemptNotInProgressError(Exception):
    pass


class QuestionNotFoundError(Exception):
    pass


class QuestionDoesNotBelongToTestError(Exception):
    pass


class ResponseOptionNotFoundError(Exception):
    pass


class ResponseOptionDoesNotBelongToQuestionError(Exception):
    pass


async def create_answer(
    db: AsyncSession, payload: AnswerCreate
) -> tuple[Answer, bool, TestStatus]:
    attempt = await db.get(TestAttempt, payload.test_attempt_id)
    if attempt is None or attempt.deleted_at is not None:
        raise TestAttemptNotFoundError(
            f"TestAttempt {payload.test_attempt_id} not found"
        )
    if attempt.status != TestStatus.IN_PROGRESS:
        raise TestAttemptNotInProgressError(
            f"TestAttempt {attempt.id} is {attempt.status.value}; cannot accept new answers"
        )

    question = await db.get(Question, payload.question_id)
    if question is None or question.deleted_at is not None:
        raise QuestionNotFoundError(f"Question {payload.question_id} not found")
    if question.test_id != attempt.test_id:
        raise QuestionDoesNotBelongToTestError(
            f"Question {question.id} does not belong to test {attempt.test_id}"
        )

    if payload.response_option_id is not None:
        option = await db.get(ResponseOption, payload.response_option_id)
        if option is None or option.deleted_at is not None:
            raise ResponseOptionNotFoundError(
                f"ResponseOption {payload.response_option_id} not found"
            )
        if option.question_id != payload.question_id:
            raise ResponseOptionDoesNotBelongToQuestionError(
                f"ResponseOption {option.id} does not belong to question {payload.question_id}"
            )

    answer = Answer(**payload.model_dump())
    db.add(answer)
    await db.flush()

    questions_total = (
        await db.execute(
            select(func.count(Question.id)).where(
                Question.test_id == attempt.test_id,
                Question.is_active.is_(True),
                Question.deleted_at.is_(None),
            )
        )
    ).scalar_one()

    answered_count = (
        await db.execute(
            select(func.count(func.distinct(Answer.question_id))).where(
                Answer.test_attempt_id == attempt.id,
                Answer.deleted_at.is_(None),
            )
        )
    ).scalar_one()

    test_completed = (
        questions_total > 0 and answered_count >= questions_total
    )

    if test_completed:
        attempt.status = TestStatus.COMPLETED
        attempt.finished_at = datetime.utcnow()

    await db.commit()
    await db.refresh(answer)
    await db.refresh(attempt)

    return answer, test_completed, attempt.status


async def update_answer(
    db: AsyncSession, answer_id: int, payload: AnswerUpdate
) -> Answer:
    answer = await db.get(Answer, answer_id)
    if answer is None or answer.deleted_at is not None:
        raise AnswerNotFoundError(f"Answer {answer_id} not found")

    attempt = await db.get(TestAttempt, answer.test_attempt_id)
    if attempt is None or attempt.deleted_at is not None:
        raise TestAttemptNotFoundError(
            f"TestAttempt {answer.test_attempt_id} not found"
        )
    if attempt.status != TestStatus.IN_PROGRESS:
        raise TestAttemptNotInProgressError(
            f"TestAttempt {attempt.id} is {attempt.status.value}; cannot update answers"
        )

    updates = payload.model_dump(exclude_unset=True)

    if "response_option_id" in updates and updates["response_option_id"] is not None:
        option = await db.get(ResponseOption, updates["response_option_id"])
        if option is None or option.deleted_at is not None:
            raise ResponseOptionNotFoundError(
                f"ResponseOption {updates['response_option_id']} not found"
            )
        if option.question_id != answer.question_id:
            raise ResponseOptionDoesNotBelongToQuestionError(
                f"ResponseOption {option.id} does not belong to question {answer.question_id}"
            )

    for field, value in updates.items():
        setattr(answer, field, value)

    await db.commit()
    await db.refresh(answer)
    return answer
