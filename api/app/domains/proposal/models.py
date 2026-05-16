from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.candidate.models import Candidate
from app.domains.category.models import Category

if TYPE_CHECKING:
    from app.domains.posture.models import Posture
    from app.domains.proposal_chunk.models import ProposalChunk
    from app.domains.source.models import Source
    from app.domains.tagging.models import Tagging


class Proposal(Base, TimestampMixin):
    __tablename__ = "proposals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    full_text: Mapped[str | None] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False
    )
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False
    )

    category: Mapped[Category] = relationship()
    candidate: Mapped[Candidate] = relationship()
    postures: Mapped[list["Posture"]] = relationship(back_populates="proposal")
    taggings: Mapped[list["Tagging"]] = relationship(back_populates="proposal")
    sources: Mapped[list["Source"]] = relationship(back_populates="proposal")
    chunks: Mapped[list["ProposalChunk"]] = relationship(back_populates="proposal")
