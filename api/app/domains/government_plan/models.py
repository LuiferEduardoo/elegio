from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.candidate.models import Candidate


class GovernmentPlan(Base, TimestampMixin):
    __tablename__ = "government_plans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False
    )

    url: Mapped[str] = mapped_column(String(255), nullable=False)

    candidate: Mapped[Candidate] = relationship()
