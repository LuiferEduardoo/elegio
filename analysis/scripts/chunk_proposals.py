from app.core.database import engine
from app.domains.proposal_chunk.service import (
    chunk_and_insert,
    get_pending_proposals,
)


def main() -> None:
    with engine.connect() as conn:
        pending = get_pending_proposals(conn)
        print(f"Pending proposals: {len(pending)}")

        errors: list[tuple[int, str]] = []
        total_chunks = 0

        for i, proposal in enumerate(pending, 1):
            try:
                n = chunk_and_insert(conn, proposal)
                total_chunks += n
                marker = "·" if n else "∅"
                print(f"[{i}/{len(pending)}] {marker} Proposal {proposal.id}: {n} chunk(s)")
            except Exception as e:
                print(f"[{i}/{len(pending)}] x Proposal {proposal.id}: {e}")
                errors.append((proposal.id, str(e)))
                conn.rollback()

        print(f"\nTotal chunks created: {total_chunks}")
        if errors:
            print(f"{len(errors)} errors:")
            for pid, msg in errors:
                print(f"  - Proposal {pid}: {msg}")


if __name__ == "__main__":
    main()
