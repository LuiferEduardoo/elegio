"""CLI: chunk loaded news into the ``news_chunks`` table.

Run after ``scripts.load_news``. Each news article with no chunks yet is split
and stored as vitaminized chunks (candidate + outlet + headline prefix).

    python -m scripts.chunk_news
"""

from app.core.database import engine
from app.domains.news_chunk.service import chunk_and_insert, get_pending_news


def main() -> None:
    with engine.connect() as conn:
        pending = get_pending_news(conn)
        print(f"Pending news: {len(pending)}")

        errors: list[tuple[int, str]] = []
        total_chunks = 0

        for i, news in enumerate(pending, 1):
            try:
                n = chunk_and_insert(conn, news)
                total_chunks += n
                marker = "·" if n else "∅"
                print(f"[{i}/{len(pending)}] {marker} News {news.id}: {n} chunk(s)")
            except Exception as e:
                print(f"[{i}/{len(pending)}] x News {news.id}: {e}")
                errors.append((news.id, str(e)))
                conn.rollback()

        print(f"\nTotal chunks created: {total_chunks}")
        if errors:
            print(f"{len(errors)} errors:")
            for nid, msg in errors:
                print(f"  - News {nid}: {msg}")


if __name__ == "__main__":
    main()
