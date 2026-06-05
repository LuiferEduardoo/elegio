"""CLI: chunk loaded documents into the ``document_chunks`` table.

Run after ``scripts.load_documents``. Each document with no chunks yet is split
with the structure-aware Markdown chunker (headings/sections, tables, bullets).

    python -m scripts.chunk_documents
"""

from app.core.database import engine
from app.domains.document_chunk.service import (
    chunk_and_insert,
    get_pending_documents,
)


def main() -> None:
    with engine.connect() as conn:
        pending = get_pending_documents(conn)
        print(f"Pending documents: {len(pending)}")

        errors: list[tuple[int, str]] = []
        total_chunks = 0

        for i, document in enumerate(pending, 1):
            try:
                n = chunk_and_insert(conn, document)
                total_chunks += n
                marker = "·" if n else "∅"
                print(f"[{i}/{len(pending)}] {marker} Document {document.id}: {n} chunk(s)")
            except Exception as e:
                print(f"[{i}/{len(pending)}] x Document {document.id}: {e}")
                errors.append((document.id, str(e)))
                conn.rollback()

        print(f"\nTotal chunks created: {total_chunks}")
        if errors:
            print(f"{len(errors)} errors:")
            for did, msg in errors:
                print(f"  - Document {did}: {msg}")


if __name__ == "__main__":
    main()
