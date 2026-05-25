from sqlalchemy import CheckConstraint, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.candidate.models import Candidate
from app.domains.category.models import Category


class RhetoricalWeight(Base, TimestampMixin):
    __tablename__ = "rhetorical_weights"
    __table_args__ = (
        CheckConstraint("value >= 0.0 AND value <= 5.0", name="ck_rhetorical_weights_value_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False
    )
    value: Mapped[float] = mapped_column(Float, nullable=False)
    editorial_justification: Mapped[str | None] = mapped_column(Text, nullable=True)

    category: Mapped[Category] = relationship()
    candidate: Mapped[Candidate] = relationship()
