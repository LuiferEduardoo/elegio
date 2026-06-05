"""CLI: load extracted news into the ``news`` MySQL table.

Reads ``scripts/news.yaml`` (candidate + publishing_house metadata) and the
matching ``news/<slug>.json`` aggregates (extracted content), joins them by
``new_id`` and inserts one row per article. Idempotent on ``news.uuid``.

Run ``scripts.extract_news`` first to produce the JSON. Then:

    python -m scripts.load_news                     # default paths
    python -m scripts.load_news path/to/news.yaml   # custom input
"""

import json
import sys
from pathlib import Path

import yaml

from app.core.database import engine
from app.domains.news.loader import (
    build_news_row,
    candidate_id_by_name,
    existing_uuids,
    insert_news,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_YAML = REPO_ROOT / "scripts" / "news.yaml"
NEWS_DIR = REPO_ROOT / "news"


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _articles_by_id(slug: str) -> dict[str, dict]:
    """Load ``news/<slug>.json`` indexed by ``new_id`` (empty if missing)."""
    path = NEWS_DIR / f"{slug}.json"
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {a["new_id"]: a for a in payload}


def main(yaml_path: Path = DEFAULT_YAML) -> None:
    config = _load_yaml(yaml_path)
    candidates = config.get("candidates", [])
    if not candidates:
        print(f"No candidates in {yaml_path}")
        return

    with engine.connect() as conn:
        name_to_id = candidate_id_by_name(conn)
        already = existing_uuids(conn)

        to_insert: list[dict] = []
        skipped = missing_candidate = missing_article = 0

        for candidate in candidates:
            slug = candidate["slug"]
            name = candidate.get("name", slug)
            candidate_id = name_to_id.get(name)
            if candidate_id is None:
                print(f"! candidate not found in DB: {name!r} (slug={slug}) — skipping")
                missing_candidate += len(candidate.get("news", []))
                continue

            articles = _articles_by_id(slug)
            for raw in candidate.get("news", []):
                new_id = raw["new_id"]
                if new_id in already:
                    skipped += 1
                    continue
                article = articles.get(new_id)
                if article is None:
                    print(f"  ! no extracted JSON for {new_id} (slug={slug})")
                    missing_article += 1
                    continue
                to_insert.append(
                    build_news_row(
                        article,
                        candidate_id=candidate_id,
                        publishing_house=raw.get("publishing_house", ""),
                        url=raw.get("url", ""),
                    )
                )

        inserted = insert_news(conn, to_insert)

    print(
        f"\nInserted: {inserted} | already in DB (skipped): {skipped} | "
        f"missing candidate: {missing_candidate} | missing JSON: {missing_article}"
    )


if __name__ == "__main__":
    arg = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_YAML
    main(arg)
