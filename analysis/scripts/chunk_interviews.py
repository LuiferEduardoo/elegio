"""CLI: chunk loaded interviews into the ``interview_chunks`` table.

Run after ``scripts.load_interviews``. Each interview with no chunks yet has its
merged turns grouped into conversational chunks.

    python -m scripts.chunk_interviews
"""

from app.core.database import engine
from app.domains.interview_chunk.service import (
    chunk_and_insert,
    get_pending_interview_ids,
)


def main() -> None:
    with engine.connect() as conn:
        pending = get_pending_interview_ids(conn)
        print(f"Pending interviews: {len(pending)}")

        errors: list[tuple[int, str]] = []
        total_chunks = 0

        for i, interview_id in enumerate(pending, 1):
            try:
                n = chunk_and_insert(conn, interview_id)
                total_chunks += n
                marker = "·" if n else "∅"
                print(f"[{i}/{len(pending)}] {marker} Interview {interview_id}: {n} chunk(s)")
            except Exception as e:
                print(f"[{i}/{len(pending)}] x Interview {interview_id}: {e}")
                errors.append((interview_id, str(e)))
                conn.rollback()

        print(f"\nTotal chunks created: {total_chunks}")
        if errors:
            print(f"{len(errors)} errors:")
            for iid, msg in errors:
                print(f"  - Interview {iid}: {msg}")


if __name__ == "__main__":
    main()
