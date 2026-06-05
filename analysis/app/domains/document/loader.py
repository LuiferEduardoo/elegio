"""Persist extracted documents into MySQL.

The document JSON (``documents/<slug>.json``) is self-contained — it already
carries source_type, type, title, url, content, publishing_house,
published_date and page_count. The only thing it lacks is ``candidate_id``,
which we resolve from the YAML candidate name. One row per PDF is upserted into
the ``documents`` table, idempotent on ``documents.uuid`` (== JSON ``doc_id``).
"""

from datetime import date, datetime
from typing import Any

from sqlalchemy import Connection, select

from app.core.database import candidates_table, documents_table


def candidate_id_by_name(conn: Connection) -> dict[str, int]:
    """Map ``presidential_candidate`` → ``id`` for non-deleted candidates."""
    rows = conn.execute(
        select(candidates_table.c.id, candidates_table.c.presidential_candidate)
        .where(candidates_table.c.deleted_at.is_(None))
    ).all()
    return {r.presidential_candidate: r.id for r in rows}


def existing_uuids(conn: Connection) -> set[str]:
    """UUIDs already present in the ``documents`` table (any state)."""
    rows = conn.execute(select(documents_table.c.uuid)).all()
    return {r.uuid for r in rows}


def _parse_date(raw: Any) -> date | None:
    if not raw:
        return None
    return datetime.fromisoformat(str(raw).replace("Z", "")).date()


def _parse_dt(raw: Any) -> datetime | None:
    if not raw:
        return None
    return datetime.fromisoformat(str(raw).replace("Z", ""))


def build_document_row(doc: dict[str, Any], *, candidate_id: int) -> dict[str, Any]:
    """Turn one extracted document JSON object into a ``documents`` row."""
    row = {
        "uuid": doc["doc_id"],
        "candidate_id": candidate_id,
        "source_type": doc.get("source_type", "pdf_document"),
        "type": doc.get("type"),
        "title": doc.get("title"),
        "url": doc.get("url"),
        "content": doc.get("content", ""),
        "publishing_house": doc.get("publishing_house"),
        "published_date": _parse_date(doc.get("published_date")),
        "page_count": doc.get("page_count"),
    }
    processed_at = _parse_dt(doc.get("processed_at"))
    if processed_at is not None:
        row["processed_at"] = processed_at
    return row


def insert_documents(conn: Connection, rows: list[dict[str, Any]]) -> int:
    """Insert document rows in one transaction. Returns the number inserted."""
    if not rows:
        return 0
    conn.execute(documents_table.insert(), rows)
    conn.commit()
    return len(rows)
