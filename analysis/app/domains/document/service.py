"""Orchestrates structuring one candidate PDF for RAG.

Pipeline:
    Docling convert (cached Markdown) → preprocess (encoding + whitespace)
    → output dict matching the user-facing JSON schema

Cache layout under ``cache_root/<doc_id>.md``: the raw Docling Markdown is kept
so we can re-clean cheaply if the preprocessor changes, without re-running the
(expensive) layout models — same idea as ``news_cache/`` for articles.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.domains.document import converter
from app.domains.document.preprocessor import clean_markdown, clean_title


@dataclass(slots=True)
class DocumentSpec:
    doc_id: str
    path: Path
    type: str | None = None  # e.g. "legal_document", "campaign_document"
    url: str | None = None  # remote source of the PDF, if any
    title: str | None = None
    publishing_house: str = ""
    authors: tuple[str, ...] = ()
    published_date: str | None = None


def _markdown_for(spec: DocumentSpec, cache_root: Path) -> tuple[str, int]:
    """Return ``(markdown, page_count)``, using the cached Markdown when present.

    Page count is only known when Docling actually runs, so a cache hit reports
    ``0`` — the conversion metadata isn't re-derived from cached Markdown.
    """
    md_cache = cache_root / f"{spec.doc_id}.md"
    if md_cache.exists():
        return md_cache.read_text(encoding="utf-8"), 0

    converted = converter.convert_pdf(spec.path)
    md_cache.parent.mkdir(parents=True, exist_ok=True)
    md_cache.write_text(converted.markdown, encoding="utf-8")
    # Carry Docling's detected title forward only if the spec didn't pin one.
    if spec.title is None:
        spec.title = converted.title
    return converted.markdown, converted.page_count


def process_document(spec: DocumentSpec, cache_root: Path) -> dict[str, Any]:
    markdown, page_count = _markdown_for(spec, cache_root)

    return {
        "doc_id": spec.doc_id,
        "source_type": "pdf_document",
        "type": spec.type,
        "title": clean_title(spec.title),
        "source_path": str(spec.path),
        "url": spec.url,
        "publishing_house": spec.publishing_house,
        "authors": list(spec.authors),
        "published_date": spec.published_date,
        "page_count": page_count,
        "processed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "content": clean_markdown(markdown),
    }
