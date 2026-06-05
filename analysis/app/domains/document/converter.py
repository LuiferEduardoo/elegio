"""Convert a PDF into structured Markdown using `Docling <https://docling-project.github.io/docling/>`__.

Docling parses the PDF layout (headings, paragraphs, lists, tables, reading
order) and exports clean Markdown. Keeping that structure — instead of a flat
text blob — is what makes the output good for RAG: the chunker splits on blank
lines, so headings and paragraphs survive as natural chunk boundaries.

The :class:`docling.document_converter.DocumentConverter` is created once and
reused: building it loads the layout/OCR models, which is the expensive part.
"""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from docling.document_converter import DocumentConverter


@dataclass(slots=True)
class ConvertedDocument:
    title: str | None
    page_count: int
    markdown: str


@lru_cache(maxsize=1)
def _converter() -> DocumentConverter:
    """Lazily build (and cache) the Docling converter; loading models is slow."""
    return DocumentConverter()


def first_heading(markdown: str) -> str | None:
    """Use the first Markdown ATX heading as a title fallback, if any."""
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            if title:
                return title
    return None


def convert_pdf(path: Path) -> ConvertedDocument:
    """Run Docling over ``path`` and return its Markdown plus light metadata."""
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    result = _converter().convert(str(path))
    doc = result.document
    markdown = doc.export_to_markdown()

    title = first_heading(markdown) or (doc.name or None)
    page_count = len(getattr(doc, "pages", {}) or {})

    return ConvertedDocument(title=title, page_count=page_count, markdown=markdown)
