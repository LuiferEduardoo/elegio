"""Extract clean article content + headline + publication date from raw HTML.

Uses `trafilatura <https://trafilatura.readthedocs.io>`__, which strips ads,
boilerplate, navigation, comments, sidebars, and cookie banners. We favor
precision over recall so we never include unrelated text from the page.
"""

from dataclasses import dataclass

import trafilatura
from trafilatura.metadata import extract_metadata


@dataclass(slots=True)
class ExtractedArticle:
    title: str | None
    published_date: str | None  # "YYYY-MM-DD" when trafilatura can parse it
    content: str


def extract_article(html: str, url: str) -> ExtractedArticle:
    text = trafilatura.extract(
        html,
        url=url,
        include_comments=False,
        include_tables=False,
        include_links=False,
        favor_precision=True,
    ) or ""

    meta = extract_metadata(html, default_url=url)
    title = meta.title if meta else None
    published_date = meta.date if meta else None

    return ExtractedArticle(title=title, published_date=published_date, content=text)
