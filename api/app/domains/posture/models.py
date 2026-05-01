from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.proposal.models import Proposal


class Posture(Base, TimestampMixin):
    __tablename__ = "postures"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    proposal_id: Mapped[int] = mapped_column(
        ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False
    )
    axis_value: Mapped[float] = mapped_column(Float, nullable=False)

    proposal: Mapped[Proposal] = relationship(back_populates="postures")
