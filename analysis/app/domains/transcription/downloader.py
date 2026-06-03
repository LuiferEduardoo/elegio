"""Download a YouTube video as a compressed audio file via yt-dlp.

The pipeline uses two audio renditions of the same source:
  - mp3 64 kbps mono → fed to the OpenAI Whisper API (small, fits the 25 MB cap
    for ~50 minutes of speech).
  - wav 16 kHz mono → fed to pyannote.audio for diarization (see audio.py).

`download_audio` only produces the mp3; the wav is derived from it by
:func:`app.domains.transcription.audio.to_diarization_wav` to avoid downloading
twice.
"""

from pathlib import Path

import yt_dlp


def download_audio(url: str, out_dir: Path, basename: str = "audio") -> Path:
    """Download the audio track of ``url`` as ``out_dir/<basename>.mp3``.

    Idempotent: if the mp3 already exists, returns its path without re-downloading.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    mp3_path = out_dir / f"{basename}.mp3"
    if mp3_path.exists():
        return mp3_path

    template = str(out_dir / f"{basename}.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": template,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "64",
            }
        ],
        "postprocessor_args": ["-ac", "1"],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if not mp3_path.exists():
        raise RuntimeError(f"yt-dlp did not produce {mp3_path}")
    return mp3_path
