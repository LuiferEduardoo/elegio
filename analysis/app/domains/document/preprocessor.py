"""Cleanup heuristics for the Markdown that Docling returns.

Unlike the news preprocessor (which collapses everything into one paragraph),
PDFs are structured documents and that structure is *useful* for RAG: the
chunker splits on blank lines, so we keep headings and paragraph breaks intact.
We only fix what hurts retrieval:
  - encoding garbage (mojibake from PDFs with broken text encodings),
  - runs of spaces/tabs and trailing whitespace inherited from PDF layout,
  - excess blank lines (3+ collapsed to a single paragraph break).

Applied in :func:`app.domains.document.service.process_document` so the JSON
the pipeline emits is well-encoded, structure-preserving Markdown.
"""

import re

import ftfy

# Spaces/tabs only (never newlines) so paragraph structure survives.
_INLINE_WS_RE = re.compile(r"[ \t]+")
_TRAILING_WS_RE = re.compile(r"[ \t]+$", re.MULTILINE)
# 3+ newlines → one blank line (a single paragraph separator).
_BLANK_LINES_RE = re.compile(r"\n{3,}")


def clean_markdown(text: str | None) -> str:
    """Fix encoding and normalize whitespace while preserving Markdown structure."""
    if not text:
        return ""
    fixed = ftfy.fix_text(text)
    fixed = _INLINE_WS_RE.sub(" ", fixed)
    fixed = _TRAILING_WS_RE.sub("", fixed)
    fixed = _BLANK_LINES_RE.sub("\n\n", fixed)
    return fixed.strip()


def clean_title(text: str | None) -> str | None:
    """Fix encoding and collapse whitespace; preserves ``None`` for missing titles."""
    if text is None:
        return None
    fixed = ftfy.fix_text(text)
    cleaned = _INLINE_WS_RE.sub(" ", fixed.replace("\n", " ")).strip()
    return cleaned or None
