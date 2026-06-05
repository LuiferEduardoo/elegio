"""Persist extracted news into MySQL.

The extracted article JSON (``news/<slug>.json``) carries the content, title,
url, dates and source_type; the YAML (``scripts/news.yaml``) carries the
per-candidate metadata (slug, name, publishing_house). This module joins the
two by ``new_id`` and upserts one row per article into the ``news`` table.

Idempotent on ``news.uuid`` (== the JSON ``new_id``): articles already loaded
are skipped, so re-running after adding new URLs only inserts the new ones.
"""

from datetime import date, datetime
from typing import Any

from sqlalchemy import Connection, select

from app.core.database import candidates_table, news_table


def candidate_id_by_name(conn: Connection) -> dict[str, int]:
    """Map ``presidential_candidate`` → ``id`` for non-deleted candidates."""
    rows = conn.execute(
        select(candidates_table.c.id, candidates_table.c.presidential_candidate)
        .where(candidates_table.c.deleted_at.is_(None))
    ).all()
    return {r.presidential_candidate: r.id for r in rows}


def existing_uuids(conn: Connection) -> set[str]:
    """UUIDs already present in the ``news`` table (any state)."""
    rows = conn.execute(select(news_table.c.uuid)).all()
    return {r.uuid for r in rows}


def _published_date(article: dict[str, Any]) -> date:
    """``published_date`` is NOT NULL; fall back to the processed date."""
    raw = article.get("published_date") or article.get("processed_at")
    return datetime.fromisoformat(str(raw).replace("Z", "")).date()


def build_news_row(
    article: dict[str, Any], *, candidate_id: int, publishing_house: str, url: str
) -> dict[str, Any]:
    """Combine one extracted article with its YAML metadata into a DB row."""
    return {
        "uuid": article["new_id"],
        "candidate_id": candidate_id,
        "source_type": article.get("source_type", "news_article"),
        "publishing_house": publishing_house,
        "title": article.get("title") or "(sin título)",
        "url": url or article.get("url", ""),
        "published_date": _published_date(article),
        "content_raw": article.get("content", ""),
    }


def insert_news(conn: Connection, rows: list[dict[str, Any]]) -> int:
    """Insert news rows in one transaction. Returns the number inserted."""
    if not rows:
        return 0
    conn.execute(news_table.insert(), rows)
    conn.commit()
    return len(rows)
