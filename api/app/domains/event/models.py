from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.session.models import Session
from app.domains.visitor.models import Visitor


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    visitor_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("visitors.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    event_name: Mapped[str | None] = mapped_column(String(100))

    page_url: Mapped[str | None] = mapped_column(Text)
    page_path: Mapped[str | None] = mapped_column(String(500), index=True)
    page_title: Mapped[str | None] = mapped_column(String(255))

    element_tag: Mapped[str | None] = mapped_column(String(50))
    element_id: Mapped[str | None] = mapped_column(String(255))
    element_class: Mapped[str | None] = mapped_column(String(255))
    element_text: Mapped[str | None] = mapped_column(String(500))

    scroll_depth: Mapped[int | None] = mapped_column(SmallInteger)
    duration_ms: Mapped[int | None] = mapped_column(Integer)

    properties: Mapped[dict[str, Any] | None] = mapped_column(JSON)

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, index=True
    )

    session: Mapped[Session] = relationship()
    visitor: Mapped[Visitor] = relationship()
