"""ffmpeg-backed audio helpers: chunking for the Whisper 25 MB cap and
re-encoding to the format pyannote prefers (wav 16 kHz mono PCM).
"""

import subprocess
from pathlib import Path

WHISPER_MAX_BYTES = 24 * 1024 * 1024  # leave a small margin under OpenAI's 25 MB cap


def to_diarization_wav(src: Path, out_dir: Path) -> Path:
    """Re-encode ``src`` to 16 kHz mono PCM wav (what pyannote expects).

    Idempotent: returns the existing wav if it has already been produced.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{src.stem}.wav"
    if out_path.exists():
        return out_path
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(src),
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(out_path),
        ],
        check=True,
    )
    return out_path


def _probe_duration_seconds(path: Path) -> float:
    out = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(out.stdout.strip())


def chunk_for_whisper(src: Path, out_dir: Path) -> list[tuple[Path, float]]:
    """Return ``[(chunk_path, chunk_offset_seconds), ...]`` covering ``src``.

    If ``src`` already fits under the Whisper limit, returns it as a single chunk
    at offset 0. Otherwise splits it by time into roughly equal mp3 pieces and
    keeps the per-chunk wall-clock offset so segment timestamps can be re-aligned
    against the original timeline.
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    if src.stat().st_size <= WHISPER_MAX_BYTES:
        return [(src, 0.0)]

    duration = _probe_duration_seconds(src)
    n_chunks = max(2, int(src.stat().st_size // WHISPER_MAX_BYTES) + 1)
    chunk_seconds = duration / n_chunks

    chunks: list[tuple[Path, float]] = []
    for i in range(n_chunks):
        start = i * chunk_seconds
        chunk_path = out_dir / f"{src.stem}.chunk{i:02d}.mp3"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-ss",
                f"{start:.3f}",
                "-t",
                f"{chunk_seconds:.3f}",
                "-i",
                str(src),
                "-c:a",
                "libmp3lame",
                "-b:a",
                "64k",
                "-ac",
                "1",
                str(chunk_path),
            ],
            check=True,
        )
        chunks.append((chunk_path, start))
    return chunks
