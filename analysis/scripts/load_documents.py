"""CLI: load extracted documents into the ``documents`` MySQL table.

Reads ``scripts/documents.yaml`` (for the candidate name → id mapping) and the
matching ``documents/<slug>.json`` aggregates (which already carry every other
field) and inserts one row per PDF. Idempotent on ``documents.uuid``.

Run ``scripts.extract_documents`` first to produce the JSON. Then:

    python -m scripts.load_documents                          # default paths
    python -m scripts.load_documents path/to/documents.yaml   # custom input
"""

import json
import sys
from pathlib import Path

import yaml

from app.core.database import engine
from app.domains.document.loader import (
    build_document_row,
    candidate_id_by_name,
    existing_uuids,
    insert_documents,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_YAML = REPO_ROOT / "scripts" / "documents.yaml"
DOCS_DIR = REPO_ROOT / "documents"


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _documents_for(slug: str) -> list[dict]:
    """Load ``documents/<slug>.json`` (empty if missing)."""
    path = DOCS_DIR / f"{slug}.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


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
        skipped = missing_candidate = 0

        for candidate in candidates:
            slug = candidate["slug"]
            name = candidate.get("name", slug)
            candidate_id = name_to_id.get(name)
            if candidate_id is None:
                print(f"! candidate not found in DB: {name!r} (slug={slug}) — skipping")
                missing_candidate += len(candidate.get("documents", []))
                continue

            for doc in _documents_for(slug):
                if doc["doc_id"] in already:
                    skipped += 1
                    continue
                to_insert.append(build_document_row(doc, candidate_id=candidate_id))

        inserted = insert_documents(conn, to_insert)

    print(
        f"\nInserted: {inserted} | already in DB (skipped): {skipped} | "
        f"missing candidate: {missing_candidate}"
    )


if __name__ == "__main__":
    arg = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_YAML
    main(arg)
