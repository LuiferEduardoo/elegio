"""CLI: read scripts/news.yaml and produce news/<slug>.json per candidate.

Usage:
    python -m scripts.extract_news                       # default paths
    python -m scripts.extract_news path/to/news.yaml     # custom input

Per-article JSON is cached at news/_articles/<new_id>.json so re-runs skip
URLs that already succeeded. The raw HTML is also cached at
news_cache/<new_id>.html so we can re-extract cheaply if the extractor
improves. Delete either cache file to force re-processing of one article.
"""

import json
import sys
from pathlib import Path

import yaml

from app.domains.news.service import NewsSpec, process_article

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_YAML = REPO_ROOT / "scripts" / "news.yaml"
NEWS_DIR = REPO_ROOT / "news"
HTML_CACHE_DIR = REPO_ROOT / "news_cache"
PER_ARTICLE_DIR = NEWS_DIR / "_articles"


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _news_spec(raw: dict) -> NewsSpec:
    return NewsSpec(
        new_id=raw["new_id"],
        url=raw["url"],
        publishing_house=raw.get("publishing_house", ""),
        authors=list(raw.get("authors", [])),
    )


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _backfill_publishing_house(article: dict, spec: NewsSpec) -> bool:
    """Inject ``publishing_house`` into an older cached article in canonical
    position (right after ``source_type``), without touching its content.

    Returns ``True`` if the article was modified. This lets us add the field to
    JSON produced before it existed while preserving any manual content edits.
    """
    if article.get("publishing_house") == spec.publishing_house:
        return False
    ordered: dict = {}
    for key, value in article.items():
        ordered[key] = value
        if key == "source_type":
            ordered["publishing_house"] = spec.publishing_house
    ordered.setdefault("publishing_house", spec.publishing_house)
    article.clear()
    article.update(ordered)
    return True


def main(yaml_path: Path = DEFAULT_YAML) -> None:
    config = _load_yaml(yaml_path)
    candidates = config.get("candidates", [])
    if not candidates:
        print(f"No candidates in {yaml_path}")
        return

    PER_ARTICLE_DIR.mkdir(parents=True, exist_ok=True)

    total = sum(len(c.get("news", [])) for c in candidates)
    cached = sum(
        1
        for c in candidates
        for raw in c.get("news", [])
        if (PER_ARTICLE_DIR / f"{raw['new_id']}.json").exists()
    )
    print(
        f"Total articles: {total} — cached (will skip): {cached}, "
        f"pending (will process): {total - cached}"
    )

    for candidate in candidates:
        slug = candidate["slug"]
        name = candidate.get("name", slug)
        articles = candidate.get("news", [])
        print(f"\n=== {name} ({len(articles)} article(s)) ===")

        outputs: list[dict] = []
        for raw in articles:
            spec = _news_spec(raw)
            cache_path = PER_ARTICLE_DIR / f"{spec.new_id}.json"
            if cache_path.exists():
                cached_article = json.loads(cache_path.read_text(encoding="utf-8"))
                if _backfill_publishing_house(cached_article, spec):
                    _write_json(cache_path, cached_article)
                    print(f"  · {spec.new_id}: cached (backfilled publishing_house)")
                else:
                    print(f"  · {spec.new_id}: cached, skipping")
                outputs.append(cached_article)
                continue

            print(f"  · {spec.new_id}: processing {spec.url}")
            try:
                result = process_article(spec, HTML_CACHE_DIR)
            except Exception as e:
                print(f"    ! failed: {e!r}")
                continue
            _write_json(cache_path, result)
            outputs.append(result)
            title = result.get("title") or "(no title)"
            print(f"    ✓ {len(result['content'])} chars — {title[:80]}")

        if not outputs:
            print(f"  (no articles extracted for {slug})")
            continue

        out_path = NEWS_DIR / f"{slug}.json"
        _write_json(out_path, outputs)
        print(f"  → wrote {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    arg = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_YAML
    main(arg)
