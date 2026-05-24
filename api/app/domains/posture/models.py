import enum

from sqlalchemy import Enum as SAEnum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.proposal.models import Proposal


class ConfidenceLevel(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CoderType(str, enum.Enum):
    LLM = "llm"
    HUMAN = "human"


class Posture(Base, TimestampMixin):
    __tablename__ = "postures"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    proposal_id: Mapped[int] = mapped_column(
        ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False
    )
    axis_value: Mapped[float] = mapped_column(Float, nullable=False)

    proposal: Mapped[Proposal] = relationship(back_populates="postures")

    confidence: Mapped[ConfidenceLevel] = mapped_column(
        SAEnum(
            ConfidenceLevel,
            name="confidence_level",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    )

    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    ambiguities: Mapped[str | None] = mapped_column(Text, nullable=True)

    coder_type: Mapped[CoderType] = mapped_column(
        SAEnum(
            CoderType,
            name="coder_type",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    )

    coder_name: Mapped[str] = mapped_column(String(255), nullable=False)
