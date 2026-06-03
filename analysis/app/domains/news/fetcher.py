"""Fetch raw HTML for a news article, caching it on disk.

We cache the raw HTML (not just the extracted JSON) so we can iterate on the
extractor without re-hitting the source — same idea as ``audio_cache/`` for
videos. Caching is also polite: avoids repeatedly hammering news sites.
"""

from pathlib import Path

import trafilatura


def fetch_html(url: str, cache_path: Path) -> str:
    """Return the page HTML for ``url``, reading from ``cache_path`` if present."""
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")

    html = trafilatura.fetch_url(url)
    if not html:
        raise RuntimeError(f"Could not fetch {url}")

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(html, encoding="utf-8")
    return html
