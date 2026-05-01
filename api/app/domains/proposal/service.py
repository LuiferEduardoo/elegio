from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.posture import models as _posture_models  # noqa: F401  registers Posture mapper for Proposal.postures
from app.domains.proposal.models import Proposal
from app.domains.source import models as _source_models  # noqa: F401  registers Source mapper for Proposal.sources
from app.domains.tagging import models as _tagging_models  # noqa: F401  registers Tagging mapper for Proposal.taggings


class ProposalNotFoundError(Exception):
    pass


def _eager_options() -> tuple:
    return (
        selectinload(Proposal.category),
        selectinload(Proposal.candidate),
        selectinload(Proposal.postures),
        selectinload(Proposal.taggings),
        selectinload(Proposal.sources),
    )


async def list_proposals(
    db: AsyncSession,
    limit: int,
    offset: int,
    candidate_id: int | None = None,
    category_id: int | None = None,
) -> tuple[list[Proposal], int]:
    filters = [Proposal.deleted_at.is_(None)]
    if candidate_id is not None:
        filters.append(Proposal.candidate_id == candidate_id)
    if category_id is not None:
        filters.append(Proposal.category_id == category_id)

    total = (
        await db.execute(select(func.count(Proposal.id)).where(*filters))
    ).scalar_one()

    result = await db.execute(
        select(Proposal)
        .options(*_eager_options())
        .where(*filters)
        .order_by(Proposal.id)
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total


async def get_proposal(db: AsyncSession, proposal_id: int) -> Proposal:
    result = await db.execute(
        select(Proposal)
        .options(*_eager_options())
        .where(Proposal.id == proposal_id, Proposal.deleted_at.is_(None))
    )
    proposal = result.scalar_one_or_none()
    if proposal is None:
        raise ProposalNotFoundError(f"Proposal {proposal_id} not found")
    return proposal
