"""CLI: read scripts/videos.yaml and produce transcripts/<slug>.json per candidate.

Usage:
    python -m scripts.transcribe_videos                       # default paths
    python -m scripts.transcribe_videos path/to/videos.yaml   # custom input

Per-video JSON is cached under transcripts/_videos/<youtube_id>.json (keyed by
the canonical YouTube video id parsed from the URL, so re-runs skip work even
if you renamed `video_id`, moved the entry between candidates, or edited
metadata). Delete the cache file to force re-processing that single video.
"""

import json
import sys
from pathlib import Path

import yaml

from app.domains.transcription.service import VideoSpec, process_video, youtube_id

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_YAML = REPO_ROOT / "scripts" / "videos.yaml"
TRANSCRIPTS_DIR = REPO_ROOT / "transcripts"
AUDIO_CACHE_DIR = REPO_ROOT / "audio_cache"
PER_VIDEO_DIR = TRANSCRIPTS_DIR / "_videos"


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _video_spec(raw: dict) -> VideoSpec:
    return VideoSpec(
        video_id=raw["video_id"],
        url=raw["url"],
        title=raw["title"],
        published_date=raw["published_date"],
        format_type=raw["format_type"],
        organized_by=raw["organized_by"],
        host_or_interviewer=raw["host_or_interviewer"],
        participants=list(raw["participants"]),
        language=raw.get("language", "es"),
    )


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main(yaml_path: Path = DEFAULT_YAML) -> None:
    config = _load_yaml(yaml_path)
    candidates = config.get("candidates", [])
    if not candidates:
        print(f"No candidates in {yaml_path}")
        return

    PER_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    # Upfront summary: classify every entry as cached / pending before doing work.
    total = sum(len(c.get("videos", [])) for c in candidates)
    cached_count = 0
    for c in candidates:
        for raw in c.get("videos", []):
            try:
                yt_id = youtube_id(raw["url"])
            except ValueError:
                continue
            if (PER_VIDEO_DIR / f"{yt_id}.json").exists():
                cached_count += 1
    pending = total - cached_count
    print(
        f"Total videos: {total} — cached (will skip): {cached_count}, "
        f"pending (will process): {pending}"
    )

    for candidate in candidates:
        slug = candidate["slug"]
        name = candidate.get("name", slug)
        videos = candidate.get("videos", [])
        print(f"\n=== {name} ({len(videos)} video(s)) ===")

        outputs: list[dict] = []
        for raw in videos:
            spec = _video_spec(raw)
            try:
                yt_id = youtube_id(spec.url)
            except ValueError as e:
                print(f"  ! {spec.video_id}: {e}")
                continue
            cache_path = PER_VIDEO_DIR / f"{yt_id}.json"
            if cache_path.exists():
                print(f"  · {spec.video_id} [{yt_id}]: cached, skipping")
                outputs.append(json.loads(cache_path.read_text(encoding="utf-8")))
                continue

            print(f"  · {spec.video_id} [{yt_id}]: processing...")
            try:
                result = process_video(spec, AUDIO_CACHE_DIR)
            except Exception as e:
                print(f"    ! failed: {e!r}")
                continue
            _write_json(cache_path, result)
            outputs.append(result)
            print(f"    ✓ {len(result['transcript_segments'])} segments")

        if not outputs:
            print(f"  (no videos transcribed for {slug})")
            continue

        out_path = TRANSCRIPTS_DIR / f"{slug}.json"
        _write_json(out_path, outputs)
        print(f"  → wrote {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    arg = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_YAML
    main(arg)
