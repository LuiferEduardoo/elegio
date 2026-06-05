"""Cleanup heuristics for the Markdown that Docling returns.

Unlike the news preprocessor (which collapses everything into one paragraph),
PDFs are structured documents and that structure is *useful* for RAG: the
chunker splits on blank lines, so we keep headings and paragraph breaks intact.
We fix what hurts retrieval:
  - encoding garbage (mojibake from PDFs with broken text encodings),
  - orphan visual tags Docling emits for figures (``<!-- image -->``),
  - runs of spaces/tabs and trailing whitespace inherited from PDF layout,
  - excess blank lines (3+ collapsed to a single paragraph break),
  - running page headers/footers and redundant duplicate paragraphs that the
    PDF repeats on every page and that interrupt sentences mid-flow.

Applied in :func:`app.domains.document.service.process_document` so the JSON
the pipeline emits is well-encoded, structure-preserving Markdown.
"""

import re
from collections import Counter

import ftfy

# Spaces/tabs only (never newlines) so paragraph structure survives.
_INLINE_WS_RE = re.compile(r"[ \t]+")
_TRAILING_WS_RE = re.compile(r"[ \t]+$", re.MULTILINE)
# 3+ newlines → one blank line (a single paragraph separator).
_BLANK_LINES_RE = re.compile(r"\n{3,}")
# Docling emits HTML comments as placeholders for figures, e.g. "<!-- image -->".
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

# A paragraph repeated at least this many times is a running header/footer
# (structural noise the PDF stamps on every page), so every occurrence is
# dropped. A paragraph that appears exactly twice is treated as an accidental
# duplicate and kept once.
_RUNNING_BLOCK_MIN_REPEATS = 3

# Document-specific boilerplate to strip wherever it appears (e.g. campaign
# slogans that dilute semantic density). Extend as you spot recurring phrases;
# matching is case-insensitive. Left empty by default — only add phrases that
# are genuinely noise, since this removes them verbatim from the body.
_BOILERPLATE_PATTERNS: list[str] = []
_BOILERPLATE_RE = (
    re.compile("|".join(_BOILERPLATE_PATTERNS), re.IGNORECASE)
    if _BOILERPLATE_PATTERNS
    else None
)


def _strip_repeated_blocks(text: str) -> str:
    """Drop running headers/footers and redundant duplicate paragraphs.

    Paragraphs are blank-line separated. A block repeated
    ``_RUNNING_BLOCK_MIN_REPEATS`` times or more is treated as a running
    header/footer: every standalone occurrence is removed *and* any inline copy
    spliced into a sentence is stripped too (PDFs stamp the header mid-text when
    a sentence spans a page break). A block appearing exactly twice is an
    accidental duplicate and kept on its first occurrence only. Order is
    otherwise preserved.
    """
    paragraphs = [p.strip() for p in text.split("\n\n")]
    counts = Counter(p for p in paragraphs if p)
    running = {p for p, n in counts.items() if n >= _RUNNING_BLOCK_MIN_REPEATS}

    kept: list[str] = []
    seen: set[str] = set()
    for para in paragraphs:
        if not para or para in running:
            continue  # blank or standalone running header/footer
        if counts[para] >= 2:
            if para in seen:
                continue  # duplicate: keep only the first occurrence
            seen.add(para)
        kept.append(para)

    result = "\n\n".join(kept)

    # Strip inline copies of the running headers (longest first so a header that
    # contains another is removed whole), then collapse the gaps they leave.
    for header in sorted(running, key=len, reverse=True):
        result = result.replace(header, " ")
    return _INLINE_WS_RE.sub(" ", result)


def clean_markdown(text: str | None) -> str:
    """Fix encoding and structure-preserving noise while keeping Markdown intact."""
    if not text:
        return ""
    fixed = ftfy.fix_text(text)
    fixed = _HTML_COMMENT_RE.sub("", fixed)
    fixed = _INLINE_WS_RE.sub(" ", fixed)
    fixed = _TRAILING_WS_RE.sub("", fixed)
    fixed = _BLANK_LINES_RE.sub("\n\n", fixed)
    if _BOILERPLATE_RE is not None:
        fixed = _BOILERPLATE_RE.sub(" ", fixed)
    fixed = _strip_repeated_blocks(fixed)
    return fixed.strip()


def clean_title(text: str | None) -> str | None:
    """Fix encoding and collapse whitespace; preserves ``None`` for missing titles."""
    if text is None:
        return None
    fixed = ftfy.fix_text(text)
    cleaned = _INLINE_WS_RE.sub(" ", fixed.replace("\n", " ")).strip()
    return cleaned or None
