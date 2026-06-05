"""CLI: read scripts/documents.yaml and produce documents/<slug>.json per candidate.

Each PDF is associated with a candidate. Docling parses the PDF into structured
Markdown (headings, paragraphs, tables) and we emit one RAG-ready record per
document, aggregated per candidate — mirroring the news pipeline.

Usage:
    python -m scripts.extract_documents                        # default paths
    python -m scripts.extract_documents path/to/documents.yaml # custom input

Per-document JSON is cached at documents/_files/<doc_id>.json so re-runs skip
PDFs that already succeeded. The raw Docling Markdown is also cached at
document_cache/<doc_id>.md so we can re-clean cheaply if the preprocessor
improves. Delete either cache file to force re-processing of one document.
"""

import json
import sys
from pathlib import Path

import yaml

from app.domains.document.service import DocumentSpec, process_document

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_YAML = REPO_ROOT / "scripts" / "documents.yaml"
DOCS_DIR = REPO_ROOT / "documents"
MD_CACHE_DIR = REPO_ROOT / "document_cache"
PER_DOC_DIR = DOCS_DIR / "_files"


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _resolve_path(raw_path: str) -> Path:
    """PDF paths in the YAML are relative to the repo root unless absolute."""
    p = Path(raw_path)
    return p if p.is_absolute() else (REPO_ROOT / p)


def _document_spec(raw: dict) -> DocumentSpec:
    return DocumentSpec(
        doc_id=raw["doc_id"],
        path=_resolve_path(raw["path"]),
        type=raw.get("type"),
        url=raw.get("url"),
        title=raw.get("title"),
        publishing_house=raw.get("publishing_house", ""),
        authors=tuple(raw.get("authors", [])),
        published_date=raw.get("published_date"),
    )


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _insert_after(document: dict, field: str, value, after: str) -> None:
    """Set ``document[field] = value`` positioned right after key ``after``."""
    ordered: dict = {}
    for key, val in document.items():
        if key == field:
            continue
        ordered[key] = val
        if key == after:
            ordered[field] = value
    ordered.setdefault(field, value)
    document.clear()
    document.update(ordered)


def _backfill_fields(document: dict, spec: DocumentSpec) -> bool:
    """Inject fields added to the schema after a document was already cached,
    each in canonical position, without touching its content or re-running
    Docling. Returns ``True`` if the document was modified.
    """
    # (field, value, key to sit after)
    wanted = [
        ("type", spec.type, "source_type"),
        ("url", spec.url, "source_path"),
    ]
    changed = False
    for field, value, after in wanted:
        if document.get(field) == value:
            continue
        _insert_after(document, field, value, after)
        changed = True
    return changed


def main(yaml_path: Path = DEFAULT_YAML) -> None:
    config = _load_yaml(yaml_path)
    candidates = config.get("candidates", [])
    if not candidates:
        print(f"No candidates in {yaml_path}")
        return

    PER_DOC_DIR.mkdir(parents=True, exist_ok=True)

    total = sum(len(c.get("documents", [])) for c in candidates)
    cached = sum(
        1
        for c in candidates
        for raw in c.get("documents", [])
        if (PER_DOC_DIR / f"{raw['doc_id']}.json").exists()
    )
    print(
        f"Total documents: {total} — cached (will skip): {cached}, "
        f"pending (will process): {total - cached}"
    )

    for candidate in candidates:
        slug = candidate["slug"]
        name = candidate.get("name", slug)
        documents = candidate.get("documents", [])
        print(f"\n=== {name} ({len(documents)} document(s)) ===")

        outputs: list[dict] = []
        for raw in documents:
            spec = _document_spec(raw)
            cache_path = PER_DOC_DIR / f"{spec.doc_id}.json"
            if cache_path.exists():
                cached_doc = json.loads(cache_path.read_text(encoding="utf-8"))
                if _backfill_fields(cached_doc, spec):
                    _write_json(cache_path, cached_doc)
                    print(f"  · {spec.doc_id}: cached (backfilled new fields)")
                else:
                    print(f"  · {spec.doc_id}: cached, skipping")
                outputs.append(cached_doc)
                continue

            print(f"  · {spec.doc_id}: processing {spec.path}")
            try:
                result = process_document(spec, MD_CACHE_DIR)
            except Exception as e:
                print(f"    ! failed: {e!r}")
                continue
            _write_json(cache_path, result)
            outputs.append(result)
            title = result.get("title") or "(no title)"
            print(
                f"    ✓ {len(result['content'])} chars, "
                f"{result['page_count']} page(s) — {title[:80]}"
            )

        if not outputs:
            print(f"  (no documents extracted for {slug})")
            continue

        out_path = DOCS_DIR / f"{slug}.json"
        _write_json(out_path, outputs)
        print(f"  → wrote {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    arg = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_YAML
    main(arg)
