"""CLI: embed interview chunks and upsert them into the Qdrant ``interview_chunks`` collection.

Run after ``scripts.chunk_interviews``. Only chunks missing from Qdrant are
embedded, so re-runs are cheap.

    python -m scripts.embed_interviews
"""

from itertools import batched

from app.core.database import engine
from app.core.embedder import Embedder
from app.core.qdrant_client import (
    INTERVIEW_COLLECTION_NAME,
    ensure_collection,
    get_qdrant_client,
)
from app.domains.interview_chunk.embedding import (
    embed_and_upsert,
    fetch_chunks,
    get_all_chunk_ids,
    get_existing_qdrant_ids,
)

BATCH_SIZE = 64


def main() -> None:
    qdrant = get_qdrant_client()
    ensure_collection(qdrant, INTERVIEW_COLLECTION_NAME)
    embedder = Embedder()

    with engine.connect() as conn:
        all_ids = get_all_chunk_ids(conn)
        print(f"Total interview chunks in MySQL: {len(all_ids)}")

        existing = get_existing_qdrant_ids(qdrant, all_ids)
        pending = [i for i in all_ids if i not in existing]
        print(f"Already in Qdrant:             {len(existing)}")
        print(f"Pending:                       {len(pending)}\n")

        if not pending:
            print("Nothing to do.")
            return

        errors: list[tuple[int, str]] = []
        total_upserted = 0
        total_batches = (len(pending) + BATCH_SIZE - 1) // BATCH_SIZE

        for batch_idx, batch_ids in enumerate(batched(pending, BATCH_SIZE), 1):
            batch_ids = list(batch_ids)
            try:
                chunks = fetch_chunks(conn, batch_ids)
                n = embed_and_upsert(qdrant, embedder, chunks)
                total_upserted += n
                print(f"[{batch_idx}/{total_batches}] · upserted {n} chunks")
            except Exception as e:
                print(f"[{batch_idx}/{total_batches}] x batch starting at id={batch_ids[0]}: {e}")
                errors.append((batch_ids[0], str(e)))

        print(f"\nTotal upserted: {total_upserted}")
        if errors:
            print(f"{len(errors)} batch(es) failed:")
            for first_id, msg in errors:
                print(f"  - batch starting at id={first_id}: {msg}")


if __name__ == "__main__":
    main()
