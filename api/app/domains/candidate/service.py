from collections.abc import Iterable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.candidate.models import Candidate
from app.domains.candidate.schemas import CategoryAverage
from app.domains.category.models import Category
from app.domains.posture.models import Posture
from app.domains.proposal.models import Proposal
from app.domains.rhetorical_weight.models import RhetoricalWeight
from app.domains.rhetorical_weight.service import apply_rhetorical_weight


class CandidateNotFoundError(Exception):
    pass


async def get_candidate(db: AsyncSession, candidate_id: int) -> Candidate:
    candidate = await db.get(Candidate, candidate_id)
    if candidate is None or candidate.deleted_at is not None:
        raise CandidateNotFoundError(f"Candidate {candidate_id} not found")
    return candidate


async def list_candidates(
    db: AsyncSession, limit: int, offset: int
) -> tuple[list[Candidate], int]:
    base_filter = Candidate.deleted_at.is_(None)

    total = (
        await db.execute(select(func.count(Candidate.id)).where(base_filter))
    ).scalar_one()

    result = await db.execute(
        select(Candidate)
        .where(base_filter)
        .order_by(Candidate.id)
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total


async def get_category_averages_by_candidate(
    db: AsyncSession, candidate_ids: Iterable[int]
) -> dict[int, list[CategoryAverage]]:
    """Return per-category averages of posture.axis_value for each given candidate.

    Aggregates in a single query to avoid N+1 over a page of candidates.
    Candidates with no rated proposals are simply absent from the result.
    """
    ids = list(candidate_ids)
    if not ids:
        return {}

    rows = (
        await db.execute(
            select(
                Proposal.candidate_id.label("candidate_id"),
                Category.id.label("category_id"),
                Category.name.label("category_name"),
                Category.weight.label("weight"),
                Category.negative_pole_name.label("negative_pole_name"),
                Category.negative_pole_description.label("negative_pole_description"),
                Category.positive_pole_name.label("positive_pole_name"),
                Category.positive_pole_description.label("positive_pole_description"),
                func.avg(Posture.axis_value).label("avg_value"),
                func.count(func.distinct(Proposal.id)).label("proposals_count"),
                RhetoricalWeight.value.label("rhetorical_weight"),
                RhetoricalWeight.editorial_justification.label("editorial_justification"),
            )
            .select_from(Proposal)
            .join(Posture, Posture.proposal_id == Proposal.id)
            .join(Category, Proposal.category_id == Category.id)
            .outerjoin(
                RhetoricalWeight,
                (RhetoricalWeight.candidate_id == Proposal.candidate_id)
                & (RhetoricalWeight.category_id == Category.id)
                & (RhetoricalWeight.deleted_at.is_(None)),
            )
            .where(
                Proposal.candidate_id.in_(ids),
                Proposal.deleted_at.is_(None),
                Posture.deleted_at.is_(None),
                Category.deleted_at.is_(None),
            )
            .group_by(
                Proposal.candidate_id,
                Category.id,
                Category.name,
                Category.weight,
                Category.negative_pole_name,
                Category.negative_pole_description,
                Category.positive_pole_name,
                Category.positive_pole_description,
                RhetoricalWeight.value,
                RhetoricalWeight.editorial_justification,
            )
            .order_by(Proposal.candidate_id, Category.id)
        )
    ).all()

    averages: dict[int, list[CategoryAverage]] = {}
    for row in rows:
        avg_value = float(row.avg_value)
        weight = float(row.rhetorical_weight) if row.rhetorical_weight is not None else None
        averages.setdefault(row.candidate_id, []).append(
            CategoryAverage(
                category_id=row.category_id,
                category_name=row.category_name,
                weight=float(row.weight),
                negative_pole_name=row.negative_pole_name,
                negative_pole_description=row.negative_pole_description,
                positive_pole_name=row.positive_pole_name,
                positive_pole_description=row.positive_pole_description,
                average=avg_value,
                adjusted_average=apply_rhetorical_weight(avg_value, weight),
                rhetorical_weight=weight,
                editorial_justification=row.editorial_justification,
                proposals_count=int(row.proposals_count),
            )
        )
    return averages
