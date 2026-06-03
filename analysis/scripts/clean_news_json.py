"""One-off: re-apply the news preprocessor to every JSON already produced.

Use this after changing the preprocessor (or to retrofit older runs) without
re-fetching anything. Walks ``news/`` and rewrites each file in place,
cleaning ``title`` and ``content`` on every article it finds. Both the
per-article cache (``news/_articles/<new_id>.json``) and the per-candidate
aggregates (``news/<slug>.json``) are handled.

Usage:
    python -m scripts.clean_news_json                # default: ./news
    python -m scripts.clean_news_json path/to/dir    # custom root
"""

import json
import sys
from pathlib import Path

from app.domains.news.preprocessor import clean_content, clean_title

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = REPO_ROOT / "news"


def _clean_article(article: dict) -> tuple[dict, bool]:
    """Return ``(article, changed)`` with title/content cleaned in-place."""
    changed = False
    if "title" in article:
        new_title = clean_title(article["title"])
        if new_title != article["title"]:
            article["title"] = new_title
            changed = True
    if "content" in article:
        new_content = clean_content(article["content"])
        if new_content != article["content"]:
            article["content"] = new_content
            changed = True
    return article, changed


def _clean_payload(payload):
    """Articles can be stored as one dict or a list of dicts; handle both."""
    if isinstance(payload, list):
        any_changed = False
        for i, item in enumerate(payload):
            if isinstance(item, dict):
                payload[i], changed = _clean_article(item)
                any_changed = any_changed or changed
        return payload, any_changed
    if isinstance(payload, dict):
        return _clean_article(payload)
    return payload, False


def main(root: Path = DEFAULT_ROOT) -> None:
    if not root.exists():
        print(f"Nothing to clean: {root} does not exist")
        return

    files = sorted(root.rglob("*.json"))
    if not files:
        print(f"No JSON files under {root}")
        return

    print(f"Cleaning {len(files)} file(s) under {root.relative_to(REPO_ROOT)}")
    touched = 0
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"  ! {path.relative_to(REPO_ROOT)}: invalid JSON ({e})")
            continue
        cleaned, changed = _clean_payload(payload)
        if changed:
            path.write_text(
                json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            touched += 1
            print(f"  ✓ {path.relative_to(REPO_ROOT)}")
        else:
            print(f"  · {path.relative_to(REPO_ROOT)} (unchanged)")

    print(f"\nDone. {touched}/{len(files)} file(s) updated.")


if __name__ == "__main__":
    arg = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROOT
    main(arg)
