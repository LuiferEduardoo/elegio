"""Affinity scoring strategies.

Each test ``type`` gets its own method on :class:`Affinity`. For now only
``POLITICAL_SPECTRUM`` is implemented: it averages the visitor's answers per
category and ranks candidates by the Weighted Manhattan Distance between those
averages and each candidate's (rhetorically weighted) postures:

    distance(user, candidate) = Σ |user_avg[c] − candidate_avg[c]| × weight[c]
    affinity = 1 − distance / Σ (2 × weight[c])   # axis range [-1, 1] → max diff = 2
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.answer.models import Answer
from app.domains.answer.schemas import (
    AffinityResponse,
    CandidateAffinity,
    CategoryAverage,
)
from app.domains.candidate.models import Candidate
from app.domains.category.models import Category
from app.domains.posture.models import Posture
from app.domains.proposal.models import Proposal
from app.domains.question.models import Question
from app.domains.response_option.models import ResponseOption
from app.domains.rhetorical_weight.models import RhetoricalWeight
from app.domains.rhetorical_weight.service import apply_rhetorical_weight
from app.domains.test_attempt.models import TestAttempt


class Affinity:
    """Computes a visitor's affinity with candidates for a test attempt."""

    @staticmethod
    async def compute_political_spectrum_affinity(
        db: AsyncSession, attempt: TestAttempt
    ) -> AffinityResponse:
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
                test_attempt_uuid=attempt.uuid,
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
                    RhetoricalWeight.value.label("rhetorical_weight"),
                )
                .select_from(Proposal)
                .join(Posture, Posture.proposal_id == Proposal.id)
                .outerjoin(
                    RhetoricalWeight,
                    (RhetoricalWeight.candidate_id == Proposal.candidate_id)
                    & (RhetoricalWeight.category_id == Proposal.category_id)
                    & (RhetoricalWeight.deleted_at.is_(None)),
                )
                .where(
                    Proposal.deleted_at.is_(None),
                    Posture.deleted_at.is_(None),
                    Proposal.category_id.in_(user_by_category.keys()),
                )
                .group_by(
                    Proposal.candidate_id,
                    Proposal.category_id,
                    RhetoricalWeight.value,
                )
            )
        ).all()

        candidate_vectors: dict[int, dict[int, float]] = {}
        for row in candidate_rows:
            weight = (
                float(row.rhetorical_weight)
                if row.rhetorical_weight is not None
                else None
            )
            candidate_vectors.setdefault(row.candidate_id, {})[row.category_id] = (
                apply_rhetorical_weight(float(row.avg_value), weight)
            )

        if not candidate_vectors:
            return AffinityResponse(
                test_attempt_uuid=attempt.uuid,
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
                distance += (
                    abs(user_cat.average - candidate_vec[cat_id]) * user_cat.weight
                )
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
            test_attempt_uuid=attempt.uuid,
            user_averages=user_averages,
            candidates=rankings,
        )
