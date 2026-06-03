"""Re-transcribe only the first ``[0, T]`` slice of a cached video.

Useful when Whisper got stuck in a hallucination loop over an intro of
music/silence and the real content starts much later. This script reuses
``audio_cache/<youtube_id>/audio.mp3``, sends only the requested slice to
Whisper, and rewrites ``transcript.json`` by replacing every segment whose
``start < T`` with the freshly transcribed ones. Diarization and speaker
mapping are NOT re-run — they only depend on the (unchanged) audio.

The previous transcript is kept at ``transcript.json.bak`` in case you want
to inspect/revert. The per-video aggregate at
``transcripts/_videos/<youtube_id>.json`` is removed so the next
``python -m scripts.transcribe_videos`` rebuilds it (cheaply, since every
expensive step is already cached).

Usage:
    python -m scripts.repair_transcript <youtube_id> <until>

    # Examples
    python -m scripts.repair_transcript tHUJ4OTZ7RM 00:49:04
    python -m scripts.repair_transcript JxnfFnSgUKE 00:40:02
    python -m scripts.repair_transcript JxnfFnSgUKE 2402     # plain seconds OK
"""

import json
import re
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

from app.domains.transcription import whisper_client

REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIO_CACHE_DIR = REPO_ROOT / "audio_cache"
PER_VIDEO_DIR = REPO_ROOT / "transcripts" / "_videos"

_HMS_RE = re.compile(r"^(\d+):([0-5]?\d):([0-5]?\d)$")
_MS_RE = re.compile(r"^(\d+):([0-5]?\d)$")


def _parse_time(arg: str) -> float:
    """Accept HH:MM:SS, MM:SS, or plain seconds; return seconds as float."""
    if _HMS_RE.match(arg):
        h, m, s = arg.split(":")
        return int(h) * 3600 + int(m) * 60 + int(s)
    if _MS_RE.match(arg):
        m, s = arg.split(":")
        return int(m) * 60 + int(s)
    return float(arg)


def _slice_audio(src: Path, until_seconds: float, out: Path) -> None:
    """Encode ``src[0:until]`` to a 64 kbps mono mp3 (Whisper-friendly)."""
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(src),
            "-t",
            f"{until_seconds:.3f}",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "64k",
            "-ac",
            "1",
            str(out),
        ],
        check=True,
    )


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__.strip())
        sys.exit(1)

    yt_id, until_arg = sys.argv[1], sys.argv[2]
    until_seconds = _parse_time(until_arg)

    work_dir = AUDIO_CACHE_DIR / yt_id
    mp3_full = work_dir / "audio.mp3"
    transcript_cache = work_dir / "transcript.json"
    if not mp3_full.exists():
        raise SystemExit(f"Missing audio cache: {mp3_full}")
    if not transcript_cache.exists():
        raise SystemExit(f"Missing transcript cache: {transcript_cache}")

    slice_path = work_dir / f"repair-0-{int(until_seconds)}s.mp3"
    print(f"Slicing audio [0, {until_seconds:.2f}s] → {slice_path.name}")
    _slice_audio(mp3_full, until_seconds, slice_path)

    print(f"Re-transcribing slice with {whisper_client.MODEL}...")
    new_segments = whisper_client.transcribe_chunks(
        [(slice_path, 0.0)], language="es"
    )
    print(f"  ✓ got {len(new_segments)} fresh segments")

    raw = json.loads(transcript_cache.read_text(encoding="utf-8"))
    kept = [s for s in raw if float(s["start"]) >= until_seconds]
    fresh = [asdict(s) for s in new_segments]
    merged = sorted(fresh + kept, key=lambda s: s["start"])

    backup = transcript_cache.with_suffix(".json.bak")
    backup.write_text(
        json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    transcript_cache.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"  ✓ transcript: replaced {len(raw) - len(kept)} segments before "
        f"{until_seconds:.2f}s with {len(fresh)} fresh ones "
        f"({len(merged)} total). Backup at {backup.name}."
    )

    aggregated = PER_VIDEO_DIR / f"{yt_id}.json"
    if aggregated.exists():
        aggregated.unlink()
        print(
            f"  ✓ removed {aggregated.relative_to(REPO_ROOT)} — re-run "
            "`python -m scripts.transcribe_videos` to rebuild the per-video JSON."
        )


if __name__ == "__main__":
    main()
