from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.answer.models import Answer
from app.domains.answer.schemas import (
    AffinityResponse,
    AnswerCreateWithAttempt,
    AnswerUpdate,
    CandidateAffinity,
    CategoryAverage,
)
from app.domains.candidate.models import Candidate
from app.domains.category.models import Category
from app.domains.posture.models import Posture
from app.domains.proposal.models import Proposal
from app.domains.question.models import Question
from app.domains.response_option.models import ResponseOption
from app.domains.session.models import Session as VisitorSession
from app.domains.test_attempt.models import TestAttempt, TestStatus
from app.domains.visitor.models import Visitor


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
    db: AsyncSession, payload: AnswerCreateWithAttempt
) -> tuple[Answer, bool, TestStatus]:
    attempt = await db.get(TestAttempt, payload.test_attempt_uuid)
    if attempt is None or attempt.deleted_at is not None:
        raise TestAttemptNotFoundError(
            f"TestAttempt {payload.test_attempt_uuid} not found"
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
    db: AsyncSession, answer_id: int, payload: AnswerUpdate, uuid_test_attempt: str
) -> Answer:
    answer = await db.get(Answer, answer_id)
    if answer is None or answer.deleted_at is not None:
        raise AnswerNotFoundError(f"Answer {answer_id} not found")

    attempt = (
        await db.execute(
            select(TestAttempt).where(
                TestAttempt.uuid_test_attempt == uuid_test_attempt
            )
        )
    ).scalar_one_or_none()

    if attempt is None or attempt.deleted_at is not None:
        raise TestAttemptNotFoundError(
            f"TestAttempt {uuid_test_attempt} not found"
        )
    if attempt.status != TestStatus.IN_PROGRESS:
        raise TestAttemptNotInProgressError(
            f"TestAttempt {attempt.id} is {attempt.status.value}; cannot update answers"
        )
    
    if answer.test_attempt_id != attempt.id:
        raise AnswerNotFoundError(f"Answer {answer_id} not found in the current test attempt")

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


async def get_affinity(
    db: AsyncSession, test_attempt_uuid: str
) -> AffinityResponse:
    """Average the user's answers per category and rank candidates by Weighted
    Manhattan Distance against those averages.

    distance(user, candidate) = Σ |user_avg[c] − candidate_avg[c]| × weight[c]
    affinity = 1 − distance / Σ (2 × weight[c])    # axis range [-1, 1] → max diff = 2
    """
    attempt = (
        await db.execute(
            select(TestAttempt).where(
                TestAttempt.uuid == test_attempt_uuid,
                TestAttempt.deleted_at.is_(None),
            )
        )
    ).scalar_one_or_none()
    if attempt is None:
        raise TestAttemptNotFoundError(
            f"TestAttempt {test_attempt_uuid} not found"
        )

    user_rows = (
        await db.execute(
            select(
                Category.id.label("category_id"),
                Category.name.label("category_name"),
                Category.weight.label("weight"),
                func.avg(ResponseOption.value).label("avg_value"),
            )
            .select_from(Answer)
            .join(Question, Answer.question_id == Question.id)
            .join(ResponseOption, Answer.response_option_id == ResponseOption.id)
            .join(Category, Question.category_id == Category.id)
            .where(
                Answer.test_attempt_id == attempt.id,
                Answer.deleted_at.is_(None),
                Question.deleted_at.is_(None),
                Question.category_id.is_not(None),
                Answer.response_option_id.is_not(None),
            )
            .group_by(Category.id, Category.name, Category.weight)
        )
    ).all()

    user_averages = [
        CategoryAverage(
            category_id=row.category_id,
            category_name=row.category_name,
            weight=float(row.weight),
            average=float(row.avg_value),
        )
        for row in user_rows
    ]

    if not user_averages:
        return AffinityResponse(
            test_attempt_uuid=test_attempt_uuid,
            user_averages=[],
            candidates=[],
        )

    user_by_category = {ua.category_id: ua for ua in user_averages}

    candidate_rows = (
        await db.execute(
            select(
                Proposal.candidate_id.label("candidate_id"),
                Proposal.category_id.label("category_id"),
                func.avg(Posture.axis_value).label("avg_value"),
            )
            .select_from(Proposal)
            .join(Posture, Posture.proposal_id == Proposal.id)
            .where(
                Proposal.deleted_at.is_(None),
                Posture.deleted_at.is_(None),
                Proposal.category_id.in_(user_by_category.keys()),
            )
            .group_by(Proposal.candidate_id, Proposal.category_id)
        )
    ).all()

    candidate_vectors: dict[int, dict[int, float]] = {}
    for row in candidate_rows:
        candidate_vectors.setdefault(row.candidate_id, {})[row.category_id] = float(
            row.avg_value
        )

    if not candidate_vectors:
        return AffinityResponse(
            test_attempt_uuid=test_attempt_uuid,
            user_averages=user_averages,
            candidates=[],
        )

    candidates_by_id = {
        c.id: c
        for c in (
            await db.execute(
                select(Candidate).where(
                    Candidate.id.in_(candidate_vectors.keys()),
                    Candidate.deleted_at.is_(None),
                )
            )
        )
        .scalars()
        .all()
    }

    rankings: list[CandidateAffinity] = []
    for candidate_id, candidate_vec in candidate_vectors.items():
        candidate = candidates_by_id.get(candidate_id)
        if candidate is None:
            continue

        common = candidate_vec.keys() & user_by_category.keys()
        if not common:
            continue

        distance = 0.0
        max_distance = 0.0
        for cat_id in common:
            user_cat = user_by_category[cat_id]
            distance += abs(user_cat.average - candidate_vec[cat_id]) * user_cat.weight
            max_distance += 2.0 * user_cat.weight

        affinity = 1.0 - (distance / max_distance) if max_distance > 0 else 0.0

        rankings.append(
            CandidateAffinity(
                candidate_id=candidate.id,
                presidential_candidate=candidate.presidential_candidate,
                vice_presidential_candidate=candidate.vice_presidential_candidate,
                political_group=candidate.political_group,
                political_spectrum=candidate.political_spectrum,
                photo_president=candidate.photo_president,
                photo_vice_president=candidate.photo_vice_president,
                photo_of_political_group=candidate.photo_of_political_group,
                affinity=affinity,
                distance=distance,
                categories_compared=len(common),
            )
        )

    rankings.sort(key=lambda c: c.affinity, reverse=True)

    return AffinityResponse(
        test_attempt_uuid=test_attempt_uuid,
        user_averages=user_averages,
        candidates=rankings,
    )


async def list_answers(
    db: AsyncSession, test_attempt_uuid: str, test_id: int, limit: int, offset: int
) -> tuple[list[Answer], int]:
    attempt_ids_subq = (
        select(TestAttempt.id)
        .where(
            TestAttempt.uuid == test_attempt_uuid,
            TestAttempt.test_id == test_id,
            TestAttempt.deleted_at.is_(None),
        )
        .scalar_subquery()
    )

    filters = (
        Answer.deleted_at.is_(None),
        Answer.test_attempt_id.in_(attempt_ids_subq),
    )

    total = (
        await db.execute(select(func.count(Answer.id)).where(*filters))
    ).scalar_one()

    result = await db.execute(
        select(Answer)
        .where(*filters)
        .order_by(Answer.created_at.desc(), Answer.id.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total
