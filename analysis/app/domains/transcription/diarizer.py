"""Speaker diarization with pyannote.audio (`pyannote/speaker-diarization-3.1`).

Returns time intervals labelled with anonymous speaker IDs (``SPEAKER_00``,
``SPEAKER_01``, ...). Mapping those to real participant names is the
:mod:`app.domains.transcription.speaker_mapper` step.

Requirements:
- ``HF_TOKEN`` set to a HuggingFace access token whose account has accepted the
  license at https://huggingface.co/pyannote/speaker-diarization-3.1.
- First run downloads ~250 MB of weights.
- On CPU diarization runs at roughly 10x realtime; a CUDA GPU is much faster.
"""

from dataclasses import dataclass
from pathlib import Path

from pyannote.audio import Pipeline

from app.config import settings

MODEL_ID = "pyannote/speaker-diarization-3.1"


@dataclass(slots=True)
class DiarSegment:
    start: float
    end: float
    speaker: str  # e.g. "SPEAKER_00"


_pipeline: Pipeline | None = None


def _get_pipeline() -> Pipeline:
    global _pipeline
    if _pipeline is None:
        if not settings.hf_token:
            raise RuntimeError(
                "HF_TOKEN is required for pyannote. Set it in .env and accept the "
                f"model license at https://huggingface.co/{MODEL_ID}."
            )
        _pipeline = Pipeline.from_pretrained(MODEL_ID, use_auth_token=settings.hf_token)
    return _pipeline


def diarize(audio_path: Path) -> list[DiarSegment]:
    annotation = _get_pipeline()(str(audio_path))
    out: list[DiarSegment] = []
    for turn, _, speaker in annotation.itertracks(yield_label=True):
        out.append(DiarSegment(start=float(turn.start), end=float(turn.end), speaker=speaker))
    out.sort(key=lambda s: s.start)
    return out
