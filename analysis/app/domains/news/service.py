"""Orchestrates news article extraction for one URL.

Pipeline:
    fetch HTML (cached) → trafilatura extract (title, date, clean text)
    → output dict matching the user-facing JSON schema

Cache layout under ``cache_root/<new_id>.html``: raw HTML kept so we can
re-extract cheaply if the extractor changes.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.domains.news import extractor, fetcher
from app.domains.news.preprocessor import clean_content, clean_title


@dataclass(slots=True)
class NewsSpec:
    new_id: str
    url: str
    publishing_house: str
    authors: list[str]


def process_article(spec: NewsSpec, cache_root: Path) -> dict[str, Any]:
    html_cache = cache_root / f"{spec.new_id}.html"
    html = fetcher.fetch_html(spec.url, html_cache)
    article = extractor.extract_article(html, spec.url)

    return {
        "new_id": spec.new_id,
        "source_type": "news_article",
        "title": clean_title(article.title),
        "url": spec.url,
        "published_date": article.published_date,
        "processed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "content": clean_content(article.content),
    }
