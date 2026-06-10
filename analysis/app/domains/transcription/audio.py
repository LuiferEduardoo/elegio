"""ffmpeg-backed audio helpers: chunking for the Whisper 25 MB cap and
re-encoding to the format pyannote prefers (wav 16 kHz mono PCM).

Long silences (pre-stream waits, dead air) are detected with ffmpeg's
``silencedetect`` and excluded from the chunks sent to Whisper, so they are
never billed. Each chunk carries the absolute start of its speech interval as
its offset, which keeps the transcript timestamps on the original video's
timeline (diarization still runs on the full wav, so alignment is unaffected).
"""

import math
import re
import subprocess
from pathlib import Path

WHISPER_MAX_BYTES = 24 * 1024 * 1024  # leave a small margin under OpenAI's 25 MB cap

# mp3 64 kbps mono → 8 KB/s; cap each chunk's duration so it stays under the limit
MAX_CHUNK_SECONDS = WHISPER_MAX_BYTES / (64_000 / 8)

SILENCE_NOISE = "-35dB"  # below this level audio counts as silence
SILENCE_MIN_SECONDS = 3.0  # only skip silences at least this long (speech pauses stay)
SPEECH_PADDING_SECONDS = 0.5  # keep a margin around speech so words aren't clipped

_SILENCE_START_RE = re.compile(r"silence_start:\s*(-?[0-9.]+)")
_SILENCE_END_RE = re.compile(r"silence_end:\s*(-?[0-9.]+)")


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


def detect_speech_intervals(src: Path) -> list[tuple[float, float]]:
    """Return ``[(start, end), ...]`` speech intervals of ``src`` in seconds.

    Silences of at least ``SILENCE_MIN_SECONDS`` below ``SILENCE_NOISE`` are
    excluded; each speech interval is padded by ``SPEECH_PADDING_SECONDS`` so
    soft word onsets are not clipped. If nothing is detected the whole file is
    returned as a single interval.
    """
    duration = _probe_duration_seconds(src)
    proc = subprocess.run(
        [
            "ffmpeg",
            "-i",
            str(src),
            "-af",
            f"silencedetect=noise={SILENCE_NOISE}:d={SILENCE_MIN_SECONDS}",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )

    # silencedetect logs start/end pairs to stderr; a trailing silence_start
    # without an end means the file ends in silence.
    silences: list[tuple[float, float]] = []
    pending_start: float | None = None
    for line in proc.stderr.splitlines():
        m = _SILENCE_START_RE.search(line)
        if m:
            pending_start = max(0.0, float(m.group(1)))
            continue
        m = _SILENCE_END_RE.search(line)
        if m and pending_start is not None:
            silences.append((pending_start, float(m.group(1))))
            pending_start = None
    if pending_start is not None:
        silences.append((pending_start, duration))

    speech: list[tuple[float, float]] = []
    pos = 0.0
    for s_start, s_end in silences:
        if s_start > pos:
            speech.append((pos, s_start))
        pos = max(pos, s_end)
    if pos < duration:
        speech.append((pos, duration))

    padded = [
        (max(0.0, a - SPEECH_PADDING_SECONDS), min(duration, b + SPEECH_PADDING_SECONDS))
        for a, b in speech
    ]
    merged: list[tuple[float, float]] = []
    for a, b in padded:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return merged or [(0.0, duration)]


def chunk_for_whisper(src: Path, out_dir: Path) -> list[tuple[Path, float]]:
    """Return ``[(chunk_path, chunk_offset_seconds), ...]`` covering the speech
    in ``src``.

    Long silences are skipped entirely (they are never sent to Whisper). Each
    chunk's offset is the absolute start of its speech interval in the original
    audio, so segment timestamps can be re-aligned against the full timeline.
    Speech intervals longer than the Whisper size cap are split into roughly
    equal pieces. If the file fits under the cap and has no silence worth
    trimming, it is returned as-is at offset 0.
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    duration = _probe_duration_seconds(src)
    intervals = detect_speech_intervals(src)

    trimmed = duration - sum(b - a for a, b in intervals)
    if trimmed < SILENCE_MIN_SECONDS and src.stat().st_size <= WHISPER_MAX_BYTES:
        return [(src, 0.0)]

    chunks: list[tuple[Path, float]] = []
    index = 0
    for a, b in intervals:
        n_pieces = max(1, math.ceil((b - a) / MAX_CHUNK_SECONDS))
        piece_seconds = (b - a) / n_pieces
        for j in range(n_pieces):
            start = a + j * piece_seconds
            chunk_path = out_dir / f"{src.stem}.chunk{index:02d}.mp3"
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-loglevel",
                    "error",
                    "-ss",
                    f"{start:.3f}",
                    "-t",
                    f"{piece_seconds:.3f}",
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
            index += 1
    return chunks
