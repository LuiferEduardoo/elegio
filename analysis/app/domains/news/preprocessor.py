"""Cleanup heuristics for the raw text returned by trafilatura.

Trafilatura already strips ads, sidebars, and the page chrome, but the body
text it returns can still carry:
  - encoding garbage (mojibake from sites that double-encoded UTF-8 or served
    pages with the wrong charset),
  - stray URLs that survived the link-removal pass (image captions, social
    share blurbs, footer references),
  - newlines, tabs, and repeated spaces inherited from the source HTML.

This module is applied in :func:`app.domains.news.service.process_article`
so the JSON the pipeline emits is always one well-encoded, single-spaced
paragraph per article.
"""

import re

import ftfy

# http(s)://… or www.…  — broad enough to catch trailing URLs in captions
# without nuking surrounding punctuation.
_URL_RE = re.compile(r"https?://\S+|www\.\S+")

_WHITESPACE_RE = re.compile(r"\s+")


def clean_content(text: str | None) -> str:
    """Fix encoding, strip URLs, and collapse all whitespace to single spaces."""
    if not text:
        return ""
    fixed = ftfy.fix_text(text)
    no_urls = _URL_RE.sub(" ", fixed)
    collapsed = _WHITESPACE_RE.sub(" ", no_urls)
    return collapsed.strip()


def clean_title(text: str | None) -> str | None:
    """Same fixes as :func:`clean_content` but preserves ``None`` for missing titles."""
    if text is None:
        return None
    cleaned = clean_content(text)
    return cleaned or None
