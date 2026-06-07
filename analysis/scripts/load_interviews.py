"""CLI: load interview transcripts into the ``interviews`` / ``interview_segments`` tables.

Reads ``scripts/videos.yaml`` (for the candidate name → id mapping) and the
matching ``transcripts/<slug>.json`` files. Each video becomes one interview;
its segments are merged per speaker into interview_segments. Idempotent on
``interviews.uuid`` (== video_id).

    python -m scripts.load_interviews                       # default paths
    python -m scripts.load_interviews path/to/videos.yaml   # custom input
"""

import json
import sys
from pathlib import Path

import yaml

from app.core.database import engine
from app.domains.interview.loader import (
    candidate_id_by_name,
    existing_uuids,
    insert_interview,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_YAML = REPO_ROOT / "scripts" / "videos.yaml"
TRANSCRIPTS_DIR = REPO_ROOT / "transcripts"


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _videos_for(slug: str) -> list[dict]:
    """Load ``transcripts/<slug>.json`` (empty if missing)."""
    path = TRANSCRIPTS_DIR / f"{slug}.json"
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

        inserted = skipped = missing_candidate = 0
        total_segments = 0

        for candidate in candidates:
            slug = candidate["slug"]
            name = candidate.get("name", slug)
            candidate_id = name_to_id.get(name)
            if candidate_id is None:
                print(f"! candidate not found in DB: {name!r} (slug={slug}) — skipping")
                missing_candidate += len(_videos_for(slug))
                continue

            for video in _videos_for(slug):
                if video["video_id"] in already:
                    skipped += 1
                    continue
                try:
                    n = insert_interview(conn, video, candidate_id=candidate_id)
                except Exception as e:
                    print(f"  x {video['video_id']}: {e}")
                    conn.rollback()
                    continue
                inserted += 1
                total_segments += n
                print(f"  · {video['video_id']}: {n} merged segment(s)")

    print(
        f"\nInserted interviews: {inserted} | merged segments: {total_segments} | "
        f"skipped: {skipped} | missing candidate: {missing_candidate}"
    )


if __name__ == "__main__":
    arg = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_YAML
    main(arg)
