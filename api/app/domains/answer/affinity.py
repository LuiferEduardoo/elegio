"""Affinity scoring strategies.

Each test ``type`` gets its own method on :class:`Affinity`. For now only
``POLITICAL_SPECTRUM`` is implemented: it averages the visitor's answers per
category and ranks candidates by the Weighted Manhattan Distance between those
averages and each candidate's (rhetorically weighted) postures:

    distance(user, candidate) = Σ |user_avg[c] − candidate_avg[c]| × weight[c]
    affinity = 1 − distance / Σ (2 × weight[c])   # axis range [-1, 1] → max diff = 2
"""

from collections import defaultdict

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
from app.domains.question.models import Question, QuestionType
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

    @staticmethod
    async def compute_programmatic_alignment_affinity(
        db: AsyncSession, attempt: TestAttempt
    ) -> AffinityResponse:
        """Score each candidate from the visitor's direct answers to that
        candidate's proposals (90%) plus their emotional reaction to the
        candidate's videos (10%).

        Per proposal question i (tied to a candidate and a category):
            R_i = response_option.value                     # agree/neutral/disagree
            X_i = response_option.programmatic_alignment_value  # posture R×O
            A_i = (R_i + 1) / 2                              # agreement → [0, 1]

        A contradiction penalty shrinks each category's weight by the variance
        of the visitor's postures within it:
            W̃_cat = W_cat × (1 − σ²(X within category))

        Candidate proposal match (over that candidate's questions):
            match_k = Σ (W̃_cat,i × A_i) / Σ W̃_cat,i

        Emotion (video_emotion_slider answers in [-1, 1]) maps to [0, 1] as
        (e + 1) / 2, averaged per candidate (0.5 when the candidate has none):
            final_k = 0.9 × match_k + 0.1 × emotion_k
        """
        proposal_rows = (
            await db.execute(
                select(
                    Question.candidate_id.label("candidate_id"),
                    Category.id.label("category_id"),
                    Category.name.label("category_name"),
                    Category.weight.label("weight"),
                    ResponseOption.value.label("response_value"),
                    ResponseOption.programmatic_alignment_value.label("posture"),
                )
                .select_from(Answer)
                .join(Question, Answer.question_id == Question.id)
                .join(ResponseOption, Answer.response_option_id == ResponseOption.id)
                .join(Category, Question.category_id == Category.id)
                .where(
                    Answer.test_attempt_id == attempt.id,
                    Answer.deleted_at.is_(None),
                    Answer.response_option_id.is_not(None),
                    Question.deleted_at.is_(None),
                    Question.candidate_id.is_not(None),
                    Question.type_question != QuestionType.VIDEO_EMOTION_SLIDER,
                    ResponseOption.programmatic_alignment_value.is_not(None),
                )
            )
        ).all()

        if not proposal_rows:
            return AffinityResponse(
                test_attempt_uuid=attempt.uuid,
                user_averages=[],
                candidates=[],
            )

        # Contradiction penalty: effective weight per category from the variance
        # of the visitor's postures (X) within that category.
        postures_by_category: dict[int, list[float]] = defaultdict(list)
        category_meta: dict[int, tuple[str, float]] = {}
        for row in proposal_rows:
            postures_by_category[row.category_id].append(float(row.posture))
            category_meta[row.category_id] = (row.category_name, float(row.weight))

        effective_weight: dict[int, float] = {}
        mean_posture: dict[int, float] = {}
        for category_id, postures in postures_by_category.items():
            mean = sum(postures) / len(postures)
            variance = sum((p - mean) ** 2 for p in postures) / len(postures)
            _, weight = category_meta[category_id]
            effective_weight[category_id] = weight * (1.0 - min(variance, 1.0))
            mean_posture[category_id] = mean

        # Candidate proposal match: weighted average of agreement A.
        weighted_sum: dict[int, float] = defaultdict(float)
        weight_sum: dict[int, float] = defaultdict(float)
        agreement_values: dict[int, list[float]] = defaultdict(list)
        categories_by_candidate: dict[int, set[int]] = defaultdict(set)
        for row in proposal_rows:
            agreement = (float(row.response_value) + 1.0) / 2.0
            weight = effective_weight[row.category_id]
            weighted_sum[row.candidate_id] += weight * agreement
            weight_sum[row.candidate_id] += weight
            agreement_values[row.candidate_id].append(agreement)
            categories_by_candidate[row.candidate_id].add(row.category_id)

        # Emotion (10%): average of the candidate's video reactions, mapped to [0, 1].
        emotion_rows = (
            await db.execute(
                select(
                    Question.candidate_id.label("candidate_id"),
                    Answer.emotion_answer.label("emotion"),
                )
                .select_from(Answer)
                .join(Question, Answer.question_id == Question.id)
                .where(
                    Answer.test_attempt_id == attempt.id,
                    Answer.deleted_at.is_(None),
                    Answer.emotion_answer.is_not(None),
                    Question.deleted_at.is_(None),
                    Question.candidate_id.is_not(None),
                    Question.type_question == QuestionType.VIDEO_EMOTION_SLIDER,
                )
            )
        ).all()
        emotion_by_candidate: dict[int, list[float]] = defaultdict(list)
        for row in emotion_rows:
            emotion_by_candidate[row.candidate_id].append(
                (float(row.emotion) + 1.0) / 2.0
            )

        candidate_ids = set(weighted_sum.keys())
        candidates_by_id = {
            c.id: c
            for c in (
                await db.execute(
                    select(Candidate).where(
                        Candidate.id.in_(candidate_ids),
                        Candidate.deleted_at.is_(None),
                    )
                )
            )
            .scalars()
            .all()
        }

        rankings: list[CandidateAffinity] = []
        for candidate_id in candidate_ids:
            candidate = candidates_by_id.get(candidate_id)
            if candidate is None:
                continue

            if weight_sum[candidate_id] > 0:
                proposal_match = weighted_sum[candidate_id] / weight_sum[candidate_id]
            else:
                # Every category fully contradicted: fall back to the plain mean
                # of agreement so the candidate still gets a meaningful score.
                values = agreement_values[candidate_id]
                proposal_match = sum(values) / len(values) if values else 0.0

            emotions = emotion_by_candidate.get(candidate_id)
            emotion_score = sum(emotions) / len(emotions) if emotions else 0.5

            final = 0.9 * proposal_match + 0.1 * emotion_score
            final = max(0.0, min(1.0, final))

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
                    affinity=final,
                    distance=0.0,
                    categories_compared=len(categories_by_candidate[candidate_id]),
                )
            )

        rankings.sort(key=lambda c: c.affinity, reverse=True)

        user_averages = [
            CategoryAverage(
                category_id=category_id,
                category_name=category_meta[category_id][0],
                weight=category_meta[category_id][1],
                average=mean_posture[category_id],
            )
            for category_id in postures_by_category
        ]

        return AffinityResponse(
            test_attempt_uuid=attempt.uuid,
            user_averages=user_averages,
            candidates=rankings,
        )
