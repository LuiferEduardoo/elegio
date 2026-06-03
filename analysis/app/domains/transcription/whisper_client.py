"""Thin wrapper around the OpenAI audio transcription API.

Uses ``gpt-4o-transcribe`` with ``verbose_json`` segment timestamps —
gpt-4o-transcribe is less prone than ``whisper-1`` to the "Subtítulos
realizados por la comunidad de Amara.org" hallucination loop on music or
silence, because it was not trained on the same subtitle-credits corpus.

Returns segments with absolute timestamps in the original audio's timeline.
The caller is expected to feed the chunks produced by
:func:`app.domains.transcription.audio.chunk_for_whisper` so each chunk's
local timestamps are shifted by the chunk's start offset.
"""

from dataclasses import dataclass
from pathlib import Path

from openai import OpenAI

from app.config import settings

MODEL = "gpt-4o-transcribe"


@dataclass(slots=True)
class TranscriptSegment:
    start: float  # seconds, absolute from the start of the original audio
    end: float
    text: str


_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


def transcribe_chunks(
    chunks: list[tuple[Path, float]], language: str | None = "es"
) -> list[TranscriptSegment]:
    """Transcribe each ``(chunk_path, offset)`` pair and concatenate segments
    with timestamps shifted into the original audio's timeline."""
    client = _get_client()
    all_segments: list[TranscriptSegment] = []
    for chunk_path, offset in chunks:
        with chunk_path.open("rb") as f:
            response = client.audio.transcriptions.create(
                file=f,
                model=MODEL,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
                language=language,
            )
        for seg in getattr(response, "segments", []) or []:
            start = float(seg.get("start", 0.0) if isinstance(seg, dict) else seg.start)
            end = float(seg.get("end", 0.0) if isinstance(seg, dict) else seg.end)
            text = (seg.get("text", "") if isinstance(seg, dict) else seg.text).strip()
            if not text:
                continue
            all_segments.append(
                TranscriptSegment(start=start + offset, end=end + offset, text=text)
            )
    all_segments.sort(key=lambda s: s.start)
    return all_segments
