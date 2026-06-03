"""Orchestrates the end-to-end transcription pipeline for one video, with
per-step caching so a failure in any expensive step does not waste the others.

Pipeline:
    yt-dlp  →  ffmpeg (wav 16 kHz mono + Whisper-sized mp3 chunks)
            →  OpenAI Whisper (transcript segments)
            →  pyannote.audio (diarization turns)
            →  align transcript ↔ diarization
            →  Gemini maps SPEAKER_XX → real names from the participant list
            →  output dict matching the user-facing JSON schema

Cache layout under ``cache_root/<youtube_id>/``:
    audio.mp3          downloaded once
    audio.wav          re-encoded once
    chunks/            recomputed (cheap)
    transcript.json    Whisper output (expensive — cached)
    diarization.json   pyannote output (expensive — cached)
    speakers.json      { "participants": [...], "mapping": {...} }
                       (invalidated automatically if participants change)
"""

import json
import re
import urllib.parse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.domains.transcription import (
    aligner,
    audio,
    diarizer,
    downloader,
    speaker_mapper,
    whisper_client,
)
from app.domains.transcription.diarizer import DiarSegment
from app.domains.transcription.hallucinations import filter_hallucinations
from app.domains.transcription.whisper_client import TranscriptSegment


_YT_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def youtube_id(url: str) -> str:
    """Extract the canonical 11-char YouTube id from common URL shapes."""
    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or "").lower()
    candidate = ""
    if host.endswith("youtu.be"):
        candidate = parsed.path.lstrip("/").split("/", 1)[0]
    elif "youtube.com" in host:
        if parsed.path == "/watch":
            candidate = urllib.parse.parse_qs(parsed.query).get("v", [""])[0]
        elif parsed.path.startswith(("/shorts/", "/embed/", "/v/")):
            parts = parsed.path.split("/")
            candidate = parts[2] if len(parts) > 2 else ""
    if not _YT_ID_RE.match(candidate):
        raise ValueError(f"Could not extract a YouTube id from URL: {url!r}")
    return candidate


@dataclass(slots=True)
class VideoSpec:
    video_id: str
    url: str
    title: str
    published_date: str
    format_type: str  # "debate" | "interview" | "pronouncing"
    organized_by: str
    host_or_interviewer: str
    participants: list[str]
    language: str = "es"


def _hms(seconds: float) -> str:
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_transcript(path: Path) -> list[TranscriptSegment]:
    return [TranscriptSegment(**s) for s in json.loads(path.read_text(encoding="utf-8"))]


def _load_diarization(path: Path) -> list[DiarSegment]:
    return [DiarSegment(**s) for s in json.loads(path.read_text(encoding="utf-8"))]


def process_video(spec: VideoSpec, cache_root: Path) -> dict[str, Any]:
    yt_id = youtube_id(spec.url)
    work_dir = cache_root / yt_id
    work_dir.mkdir(parents=True, exist_ok=True)

    transcript_cache = work_dir / "transcript.json"
    diarization_cache = work_dir / "diarization.json"
    speakers_cache = work_dir / "speakers.json"

    # --- Audio (idempotent) ---
    mp3 = downloader.download_audio(spec.url, work_dir)
    wav = audio.to_diarization_wav(mp3, work_dir)

    # --- Whisper transcript (cached) ---
    if transcript_cache.exists():
        transcript = _load_transcript(transcript_cache)
    else:
        chunks = audio.chunk_for_whisper(mp3, work_dir / "chunks")
        transcript = whisper_client.transcribe_chunks(chunks, language=spec.language)
        _write_json(transcript_cache, [asdict(s) for s in transcript])

    # Strip known Whisper hallucinations (Amara.org tagline, consecutive
    # duplicates) before alignment, regardless of cache origin.
    transcript = filter_hallucinations(transcript)

    # --- pyannote diarization (cached) ---
    if diarization_cache.exists():
        diarization = _load_diarization(diarization_cache)
    else:
        diarization = diarizer.diarize(wav)
        _write_json(diarization_cache, [asdict(d) for d in diarization])

    aligned = aligner.align(transcript, diarization)

    # --- Speaker mapping (cached; invalidated if participants change) ---
    name_map: dict[str, str] = {}
    if speakers_cache.exists():
        cached = json.loads(speakers_cache.read_text(encoding="utf-8"))
        if cached.get("participants") == spec.participants:
            name_map = cached.get("mapping", {})
    if not name_map:
        name_map = speaker_mapper.resolve_speaker_names(aligned, spec.participants)
        _write_json(speakers_cache, {"participants": spec.participants, "mapping": name_map})

    segments_out = [
        {
            "start_time": _hms(seg.start),
            "end_time": _hms(seg.end),
            "speaker": name_map.get(seg.speaker, seg.speaker),
            "text": seg.text,
        }
        for seg in aligned
    ]

    return {
        "video_id": spec.video_id,
        "source_type": "video_broadcast",
        "platform": "YouTube",
        "title": spec.title,
        "url": spec.url,
        "published_date": spec.published_date,
        "processed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "metadata": {
            "format_type": spec.format_type,
            "organized_by": spec.organized_by,
            "host_or_interviewer": spec.host_or_interviewer,
            "participants": spec.participants,
        },
        "transcript_segments": segments_out,
    }
