"""Re-embed every proposal chunk and rebuild the Qdrant collection.

Run this after switching the embedding model or its output dimensionality
(e.g. e5-large/1024 -> gemini-embedding-001/1536). It drops the existing
collection, recreates it at the current EMBEDDING_DIM, and re-upserts all
non-deleted chunks.

    GEMINI_API_KEY=... QDRANT_URL=... DATABASE_URL=... python reindex.py
"""

from app.core.database import engine
from app.core.embedder import EMBEDDING_DIM, MODEL_NAME, Embedder
from app.core.qdrant_client import COLLECTION_NAME, ensure_collection, get_qdrant_client
from app.domains.proposal_chunk.embedding import (
    embed_and_upsert,
    fetch_chunks,
    get_all_chunk_ids,
)

BATCH = 100


def main() -> None:
    client = get_qdrant_client()
    embedder = Embedder()

    if client.collection_exists(COLLECTION_NAME):
        print(f"Dropping existing collection '{COLLECTION_NAME}'...")
        client.delete_collection(COLLECTION_NAME)
    ensure_collection(client)
    print(f"Collection '{COLLECTION_NAME}' ready ({MODEL_NAME}, dim {EMBEDDING_DIM}).")

    with engine.connect() as conn:
        ids = get_all_chunk_ids(conn)
        print(f"Re-indexing {len(ids)} chunks...")
        done = 0
        for start in range(0, len(ids), BATCH):
            chunks = fetch_chunks(conn, ids[start : start + BATCH])
            done += embed_and_upsert(client, embedder, chunks)
            print(f"  {done}/{len(ids)}")

    print("Done.")


if __name__ == "__main__":
    main()
