"""Conversation-aware chunking for interview transcripts.

Input is the ordered list of speaker turns (the merged ``interview_segments``).
This groups consecutive turns into chunks of ~target size so a question and its
answer stay together, labelling each turn with its speaker and tracking the time
span of the chunk:

    [Westcol] ¿Asamblea constituyente?
    [Abelardo de la Espriella] No, lo que yo propongo es...

  - turns are kept whole; a single turn longer than ``max_words`` is windowed
    with overlap (each window keeps the turn's speaker and time span);
  - each chunk carries ``start_time`` of its first turn and ``end_time`` of its
    last turn.
"""

from dataclasses import dataclass
from datetime import time

TARGET_WORDS = 200
MAX_WORDS = 400
OVERLAP_WORDS = 30


@dataclass(slots=True)
class Turn:
    start_time: time
    end_time: time
    speaker: str
    text: str


@dataclass(slots=True)
class InterviewChunk:
    start_time: time
    end_time: time
    content: str


def _window(text: str, target: int, overlap: int) -> list[str]:
    words = text.split()
    step = max(1, target - overlap)
    pieces: list[str] = []
    i = 0
    while i < len(words):
        pieces.append(" ".join(words[i : i + target]))
        if i + target >= len(words):
            break
        i += step
    return pieces


def chunk_turns(
    turns: list[Turn],
    *,
    target_words: int = TARGET_WORDS,
    max_words: int = MAX_WORDS,
    overlap_words: int = OVERLAP_WORDS,
) -> list[InterviewChunk]:
    chunks: list[InterviewChunk] = []
    buf: list[str] = []
    buf_words = 0
    buf_start: time | None = None
    buf_end: time | None = None

    def flush() -> None:
        nonlocal buf, buf_words, buf_start, buf_end
        if buf:
            chunks.append(InterviewChunk(buf_start, buf_end, "\n".join(buf)))
        buf, buf_words, buf_start, buf_end = [], 0, None, None

    for turn in turns:
        text = turn.text.strip()
        if not text:
            continue
        words = len(text.split())

        if words > max_words:
            flush()
            for piece in _window(text, target_words, overlap_words):
                chunks.append(
                    InterviewChunk(turn.start_time, turn.end_time, f"[{turn.speaker}] {piece}")
                )
            continue

        if buf and buf_words + words > max_words:
            flush()
        if not buf:
            buf_start = turn.start_time
        buf.append(f"[{turn.speaker}] {text}")
        buf_words += words
        buf_end = turn.end_time
        if buf_words >= target_words:
            flush()

    flush()
    return chunks
