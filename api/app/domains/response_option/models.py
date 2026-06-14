from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.question.models import Question


class ResponseOption(Base, TimestampMixin):
    __tablename__ = "response_options"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    programmatic_alignment_value: Mapped[float] = mapped_column(Float, nullable=True)

    question: Mapped[Question] = relationship()
