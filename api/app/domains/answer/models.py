from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.question.models import Question
from app.domains.response_option.models import ResponseOption
from app.domains.visitor.models import Visitor


class Answer(Base, TimestampMixin):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    visitor_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("visitors.id", ondelete="CASCADE"),
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

    visitor: Mapped[Visitor] = relationship()
    question: Mapped[Question] = relationship()
    response_option: Mapped[ResponseOption | None] = relationship()
