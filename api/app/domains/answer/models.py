from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.question.models import Question
from app.domains.response_option.models import ResponseOption
from app.domains.test_attempt.models import TestAttempt


class Answer(Base, TimestampMixin):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_attempt_id: Mapped[int] = mapped_column(
        ForeignKey("test_attempts.id", ondelete="CASCADE"), 
        nullable=False,
        index=True,
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    response_option_id: Mapped[int | None] = mapped_column(
        ForeignKey("response_options.id", ondelete="SET NULL")
    )

    boolean_answer: Mapped[bool | None] = mapped_column(Boolean)
    open_text_answer: Mapped[str | None] = mapped_column(Text)

    response_time: Mapped[int | None] = mapped_column(Integer)

    question: Mapped[Question] = relationship()
    response_option: Mapped[ResponseOption | None] = relationship()
    test_attempt: Mapped[TestAttempt] = relationship()