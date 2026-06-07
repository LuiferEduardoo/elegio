from datetime import time

from sqlalchemy import BigInteger, ForeignKey, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.interview.models import Interview


class InterviewSegment(Base, TimestampMixin):
    __tablename__ = "interview_segments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    interview_id: Mapped[int] = mapped_column(
        ForeignKey("interviews.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    speaker: Mapped[str] = mapped_column(String(100), nullable=False)
    text_segment: Mapped[str] = mapped_column(Text, nullable=False)

    interview: Mapped[Interview] = relationship()
