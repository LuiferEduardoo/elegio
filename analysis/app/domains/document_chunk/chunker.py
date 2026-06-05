"""Markdown- and structure-aware chunking for legal/PDF documents.

Unlike the flat news/proposal chunker, Docling Markdown carries structure that
matters for retrieval, so this splitter:

  - breaks at heading boundaries (a chunk never spans two sections) and prefixes
    every chunk with its active heading path, so each chunk knows its section.
    Nesting follows the heading's leading numbering (``3`` > ``3.1``) and falls
    back to the Markdown ``#`` level for unnumbered titles;
  - keeps tables (``| ... |`` blocks) whole — never split, always their own chunk;
  - splits a long bullet list *between items* (each ``-`` line is a "hecho"),
    never mid-item;
  - groups continuous paragraphs (the dense prose of a legal document) up to a
    target size, breaking only on blank lines; a single oversized paragraph is
    windowed with overlap.

Sizes are word-based, mirroring the Gemini ratio used elsewhere (~1.33 tokens
per Spanish word).
"""

import re

TARGET_WORDS = 200       # group continuous paragraphs/facts up to here
MAX_WORDS = 400          # hard ceiling per chunk
OVERLAP_WORDS = 30       # only applied when windowing an oversized paragraph

_NUM_PREFIX_RE = re.compile(r"\d+(?:\.\d+)*")


def _is_heading(block: str) -> bool:
    return block.lstrip().startswith("#")


def _is_table(block: str) -> bool:
    lines = [ln for ln in block.splitlines() if ln.strip()]
    return len(lines) >= 2 and all("|" in ln for ln in lines)


def _is_bullet_list(block: str) -> bool:
    lines = [ln for ln in block.splitlines() if ln.strip()]
    return bool(lines) and all(ln.lstrip().startswith(("-", "*")) for ln in lines)


def _heading_depth(block: str) -> int:
    """Nesting depth: numbering wins (``3.1`` → 2), else the Markdown ``#`` level."""
    level = len(block) - len(block.lstrip("#"))
    text = block.lstrip("#").strip()
    match = _NUM_PREFIX_RE.match(text)
    if match:
        return match.group(0).count(".") + 1
    return level or 1


def _word_count(text: str) -> int:
    return len(text.split())


def _split_paragraph(text: str, target: int, overlap: int) -> list[str]:
    """Window an oversized paragraph into ``target``-word pieces with overlap."""
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


def _bullet_items(block: str) -> list[str]:
    """Split a bullet block into items; non-marker lines attach to the prior item."""
    items: list[str] = []
    current: list[str] = []
    for line in block.splitlines():
        if line.lstrip().startswith(("-", "*")):
            if current:
                items.append("\n".join(current))
            current = [line]
        elif current:
            current.append(line)
        else:
            current = [line]
    if current:
        items.append("\n".join(current))
    return items


def _split_list(block: str, target: int) -> list[str]:
    """Group bullet items up to ``target`` words, never splitting an item."""
    groups: list[str] = []
    buf: list[str] = []
    buf_words = 0
    for item in _bullet_items(block):
        words = _word_count(item)
        if buf and buf_words + words > target:
            groups.append("\n".join(buf))
            buf, buf_words = [], 0
        buf.append(item)
        buf_words += words
    if buf:
        groups.append("\n".join(buf))
    return groups


def chunk_markdown(
    text: str,
    *,
    target_words: int = TARGET_WORDS,
    max_words: int = MAX_WORDS,
    overlap_words: int = OVERLAP_WORDS,
) -> list[str]:
    text = (text or "").strip()
    if not text:
        return []

    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]

    chunks: list[str] = []
    heading_path: list[tuple[int, str]] = []
    buf: list[str] = []

    def prefix() -> str:
        return "\n\n".join(h for _, h in heading_path)

    def emit(body_blocks: list[str]) -> None:
        if not body_blocks:
            return
        body = "\n\n".join(body_blocks)
        head = prefix()
        chunks.append(f"{head}\n\n{body}" if head else body)

    def flush() -> None:
        nonlocal buf
        emit(buf)
        buf = []

    def buf_words() -> int:
        return sum(_word_count(b) for b in buf)

    for block in blocks:
        if _is_heading(block):
            flush()
            depth = _heading_depth(block)
            while heading_path and heading_path[-1][0] >= depth:
                heading_path.pop()
            heading_path.append((depth, block))
            continue

        if _is_table(block):
            flush()
            emit([block])  # tables stay whole, on their own
            continue

        if _is_bullet_list(block) and _word_count(block) > target_words:
            flush()
            for group in _split_list(block, target_words):
                emit([group])
            continue

        words = _word_count(block)
        if words > max_words:
            flush()
            for piece in _split_paragraph(block, target_words, overlap_words):
                emit([piece])
            continue

        if buf and buf_words() + words > max_words:
            flush()
        buf.append(block)
        if buf_words() >= target_words:
            flush()

    flush()
    return chunks
