"""Align Whisper transcript segments with pyannote diarization turns.

For each transcript segment we pick the speaker whose diarization turns overlap
it the most in time. Segments with no overlap fall back to the previous
speaker if any, else ``"unknown"``.
"""

from dataclasses import dataclass

from app.domains.transcription.diarizer import DiarSegment
from app.domains.transcription.whisper_client import TranscriptSegment


@dataclass(slots=True)
class AlignedSegment:
    start: float
    end: float
    speaker: str  # diarization label (e.g. "SPEAKER_00") or "unknown"
    text: str


def _best_speaker(
    seg: TranscriptSegment, diar: list[DiarSegment], fallback: str
) -> str:
    best_overlap = 0.0
    best_speaker = fallback
    for d in diar:
        overlap = max(0.0, min(seg.end, d.end) - max(seg.start, d.start))
        if overlap > best_overlap:
            best_overlap = overlap
            best_speaker = d.speaker
    return best_speaker


def align(
    transcript: list[TranscriptSegment], diarization: list[DiarSegment]
) -> list[AlignedSegment]:
    out: list[AlignedSegment] = []
    last_speaker = "unknown"
    for seg in transcript:
        speaker = _best_speaker(seg, diarization, last_speaker)
        last_speaker = speaker
        out.append(
            AlignedSegment(start=seg.start, end=seg.end, speaker=speaker, text=seg.text)
        )
    return out
