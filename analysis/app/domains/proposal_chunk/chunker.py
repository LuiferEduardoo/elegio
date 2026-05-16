"""Paragraph-aware chunking with controlled overlap.

Token sizes follow Gemini's rough ratio for Spanish text: ~1.33 tokens per word.
Defaults below map to the spec target/max/overlap (200/400/30 tokens).
"""

TARGET_WORDS = 150       # ~200 tokens
MAX_WORDS = 300          # ~400 tokens
OVERLAP_WORDS = 20       # ~30 tokens
MIN_SPLIT_WORDS = 150    # shorter inputs are returned as a single chunk


def chunk_text(
    text: str,
    *,
    target_words: int = TARGET_WORDS,
    max_words: int = MAX_WORDS,
    overlap_words: int = OVERLAP_WORDS,
    min_split_words: int = MIN_SPLIT_WORDS,
) -> list[str]:
    """Split ``text`` into chunks respecting paragraph boundaries when possible.

    - Inputs shorter than ``min_split_words`` are returned as a single chunk.
    - Paragraphs (separated by blank lines) are packed greedily until the buffer
      reaches ``target_words``; the next chunk is seeded with the last
      ``overlap_words`` of the previous one to preserve context.
    - A single paragraph longer than ``max_words`` is split standalone into
      windows of ``target_words`` with the same overlap.
    - The hard ceiling per chunk is ``max_words``.
    """
    text = (text or "").strip()
    if not text:
        return []

    all_words = text.split()
    if len(all_words) < min_split_words:
        return [text]

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [text]

    chunks: list[str] = []
    buf: list[str] = []

    def flush() -> None:
        nonlocal buf
        if not buf:
            return
        chunks.append(" ".join(buf))
        buf = buf[-overlap_words:] if len(buf) > overlap_words else []

    for paragraph in paragraphs:
        words = paragraph.split()

        if len(words) > max_words:
            flush()
            buf = []
            step = max(1, target_words - overlap_words)
            last_window: list[str] = []
            i = 0
            while i < len(words):
                window = words[i : i + target_words]
                chunks.append(" ".join(window))
                last_window = window
                if i + target_words >= len(words):
                    break
                i += step
            buf = last_window[-overlap_words:] if last_window else []
            continue

        if buf and len(buf) + len(words) > max_words:
            flush()

        buf.extend(words)

        if len(buf) >= target_words:
            flush()

    if buf and len(buf) > overlap_words:
        chunks.append(" ".join(buf))

    return chunks
