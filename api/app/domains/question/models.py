import enum

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.category.models import Category
from app.domains.test.models import Test


class QuestionType(str, enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    BOOLEAN = "boolean"
    ONLY_OPTION = "only_option"
    OPEN_QUESTION = "open_question"


class Question(Base, TimestampMixin):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_id: Mapped[int] = mapped_column(
        ForeignKey("tests.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT")
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    type_question: Mapped[QuestionType] = mapped_column(
        Enum(QuestionType, name="question_type"), nullable=False
    )
    question_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    test: Mapped[Test] = relationship()
    category: Mapped[Category | None] = relationship()
