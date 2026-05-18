import time

from sqlalchemy import Connection, select

from app.core.database import (
    categories_table,
    engine,
    postures_table,
    proposals_table,
)
from app.core.gemini_client import GeminiClassifier
from app.domains.posture_proposal.schemas import CategoryRead, ProposalRead
from app.domains.posture_proposal.service import PostureService


def get_pending_proposals(conn: Connection) -> list[ProposalRead]:
    """Proposals that don't have a posture yet, with category eagerly loaded."""
    stmt = (
        select(
            proposals_table.c.id,
            proposals_table.c.title,
            proposals_table.c.summary,
            proposals_table.c.full_text,
            categories_table.c.id.label("category_id"),
            categories_table.c.name.label("category_name"),
            categories_table.c.weight.label("category_weight"),
        )
        .select_from(
            proposals_table.join(
                categories_table,
                proposals_table.c.category_id == categories_table.c.id,
            ).outerjoin(
                postures_table,
                postures_table.c.proposal_id == proposals_table.c.id,
            )
        )
        .where(postures_table.c.id.is_(None))
    )

    return [
        ProposalRead(
            id=row.id,
            title=row.title,
            summary=row.summary,
            full_text=row.full_text,
            category=CategoryRead(
                id=row.category_id,
                name=row.category_name,
                weight=row.category_weight,
            ),
        )
        for row in conn.execute(stmt)
    ]


def main() -> None:
    classifier = GeminiClassifier(model="gemini-2.5-pro")

    with engine.connect() as conn:
        service = PostureService(conn, classifier)
        pending = get_pending_proposals(conn)
        print(f"Pending proposals: {len(pending)}")

        errors: list[tuple[int, str]] = []

        for i, prop in enumerate(pending, 1):
            try:
                posture = service.rate_proposal(prop)
                print(
                    f"[{i}/{len(pending)}] "
                    f"Proposal {prop.id} ({prop.category.name}): "
                    f"{posture.axis_value:+.2f} ({posture.confidence.value})"
                )
                time.sleep(1)
            except Exception as e:
                print(f"[{i}/{len(pending)}] x Proposal {prop.id}: {e}")
                errors.append((prop.id, str(e)))
                conn.rollback()
                time.sleep(5)

        if errors:
            print(f"\n{len(errors)} errors:")
            for pid, msg in errors:
                print(f"  - Proposal {pid}: {msg}")


if __name__ == "__main__":
    main()
