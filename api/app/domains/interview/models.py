from datetime import date, datetime
from typing import Any

from sqlalchemy import JSON, Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.candidate.models import Candidate


class Interview(Base, TimestampMixin):
    __tablename__ = "interviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # UUID for external/API/Qdrant use; the numeric id stays internal.
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True, index=True)
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id"), nullable=False, index=True
    )
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g. video_broadcast
    # Content format: interview | debate | pronouncing.
    format_type: Mapped[str | None] = mapped_column(String(50))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    media_outlet: Mapped[str] = mapped_column(String(100), nullable=False)
    organized_by: Mapped[str | None] = mapped_column(String(100))
    host_or_interviewer: Mapped[str | None] = mapped_column(String(100))
    participants: Mapped[list[Any] | None] = mapped_column(JSON)
    interview_date: Mapped[date] = mapped_column(Date, nullable=False)
    url_video_audio: Mapped[str | None] = mapped_column(Text)
    processed_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    candidate: Mapped[Candidate] = relationship()
