"""Persist interview transcripts into MySQL.

Each video in ``transcripts/<slug>.json`` becomes one ``interviews`` row, and
its ``transcript_segments`` are collapsed into ``interview_segments`` by merging
*consecutive segments from the same speaker* into a single turn — keeping the
first segment's start_time and the last segment's end_time and concatenating the
text. Idempotent on ``interviews.uuid`` (== the video_id).

Note: transcript dates are stored as ``YYYY-DD-MM`` (day before month), so they
are parsed accordingly.
"""

from datetime import date, datetime, time
from typing import Any

from sqlalchemy import Connection, select

from app.core.database import (
    candidates_table,
    interview_segments_table,
    interviews_table,
)


def candidate_id_by_name(conn: Connection) -> dict[str, int]:
    """Map ``presidential_candidate`` → ``id`` for non-deleted candidates."""
    rows = conn.execute(
        select(candidates_table.c.id, candidates_table.c.presidential_candidate)
        .where(candidates_table.c.deleted_at.is_(None))
    ).all()
    return {r.presidential_candidate: r.id for r in rows}


def existing_uuids(conn: Connection) -> set[str]:
    """UUIDs already present in the ``interviews`` table (any state)."""
    rows = conn.execute(select(interviews_table.c.uuid)).all()
    return {r.uuid for r in rows}


def _parse_interview_date(raw: Any) -> date:
    """Transcript dates are ``YYYY-DD-MM``; fall back to ISO if that fails."""
    text = str(raw).strip()
    for fmt in ("%Y-%d-%m", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unparseable interview date: {raw!r}")


def _parse_dt(raw: Any) -> datetime | None:
    if not raw:
        return None
    return datetime.fromisoformat(str(raw).replace("Z", ""))


def _parse_time(raw: str) -> time:
    return datetime.strptime(raw.strip(), "%H:%M:%S").time()


def build_interview_row(video: dict[str, Any], *, candidate_id: int) -> dict[str, Any]:
    """Turn one transcript video object into an ``interviews`` row."""
    meta = video.get("metadata") or {}
    media_outlet = (
        meta.get("organized_by")
        or meta.get("host_or_interviewer")
        or video.get("platform")
        or ""
    )
    row = {
        "uuid": video["video_id"],
        "candidate_id": candidate_id,
        "source_type": video.get("source_type") or "video_broadcast",
        "format_type": meta.get("format_type"),
        "title": (video.get("title") or "(sin título)")[:255],
        "media_outlet": media_outlet[:100],
        "organized_by": meta.get("organized_by"),
        "host_or_interviewer": meta.get("host_or_interviewer"),
        "participants": meta.get("participants"),
        "interview_date": _parse_interview_date(video["published_date"]),
        "url_video_audio": video.get("url"),
    }
    processed_at = _parse_dt(video.get("processed_at"))
    if processed_at is not None:
        row["processed_at"] = processed_at
    return row


def merge_segments(segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge consecutive segments from the same speaker into one turn."""
    merged: list[dict[str, Any]] = []
    for seg in segments:
        speaker = seg.get("speaker", "")
        text = (seg.get("text") or "").strip()
        if merged and merged[-1]["speaker"] == speaker:
            merged[-1]["end_time"] = seg["end_time"]
            if text:
                merged[-1]["text"] = f"{merged[-1]['text']} {text}".strip()
        else:
            merged.append(
                {
                    "speaker": speaker,
                    "start_time": seg["start_time"],
                    "end_time": seg["end_time"],
                    "text": text,
                }
            )
    return merged


def insert_interview(conn: Connection, video: dict[str, Any], *, candidate_id: int) -> int:
    """Insert one interview and its merged segments. Returns the segment count."""
    row = build_interview_row(video, candidate_id=candidate_id)
    result = conn.execute(interviews_table.insert(), row)
    interview_id = result.inserted_primary_key[0]

    merged = merge_segments(video.get("transcript_segments") or [])
    if merged:
        conn.execute(
            interview_segments_table.insert(),
            [
                {
                    "interview_id": interview_id,
                    "start_time": _parse_time(m["start_time"]),
                    "end_time": _parse_time(m["end_time"]),
                    "speaker": m["speaker"][:100],
                    "text_segment": m["text"],
                }
                for m in merged
            ],
        )
    conn.commit()
    return len(merged)
