from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class Candidate(Base, TimestampMixin):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    presidential_candidate: Mapped[str] = mapped_column(String(255), nullable=False)
    vice_presidential_candidate: Mapped[str] = mapped_column(String(255), nullable=False)
    political_group: Mapped[str] = mapped_column(String(255), nullable=False)
    photo_of_political_group: Mapped[str | None] = mapped_column(String(500))
    photo_president: Mapped[str | None] = mapped_column(String(500))
    photo_vice_president: Mapped[str | None] = mapped_column(String(500))
    troubles_questions: Mapped[str | None] = mapped_column(Text)
    political_spectrum: Mapped[str | None] = mapped_column(String(50))
