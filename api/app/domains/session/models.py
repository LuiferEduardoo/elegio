import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.visitor.models import Visitor


class Session(Base, TimestampMixin):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    session_uid: Mapped[str] = mapped_column(
        String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    visitor_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("visitors.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    ip_address: Mapped[str | None] = mapped_column(String(45), index=True)
    ip_hash: Mapped[str | None] = mapped_column(String(64))
    isp: Mapped[str | None] = mapped_column(String(255))
    asn: Mapped[int | None] = mapped_column(Integer)
    is_vpn: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_proxy: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_datacenter: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    country_code: Mapped[str | None] = mapped_column(String(2), index=True)
    country_name: Mapped[str | None] = mapped_column(String(100))
    region: Mapped[str | None] = mapped_column(String(100))
    city: Mapped[str | None] = mapped_column(String(100))
    postal_code: Mapped[str | None] = mapped_column(String(20))
    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6))
    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6))
    geo_accuracy: Mapped[str | None] = mapped_column(String(20))

    viewport_width: Mapped[int | None] = mapped_column(Integer)
    viewport_height: Mapped[int | None] = mapped_column(Integer)
    connection_type: Mapped[str | None] = mapped_column(String(20))
    connection_downlink: Mapped[float | None] = mapped_column(Numeric(6, 2))

    referer: Mapped[str | None] = mapped_column(Text)
    referer_domain: Mapped[str | None] = mapped_column(String(255), index=True)
    landing_page: Mapped[str | None] = mapped_column(Text)
    exit_page: Mapped[str | None] = mapped_column(Text)
    utm_source: Mapped[str | None] = mapped_column(String(100), index=True)
    utm_medium: Mapped[str | None] = mapped_column(String(100))
    utm_campaign: Mapped[str | None] = mapped_column(String(100))
    utm_term: Mapped[str | None] = mapped_column(String(100))
    utm_content: Mapped[str | None] = mapped_column(String(100))
    gclid: Mapped[str | None] = mapped_column(String(255))
    fbclid: Mapped[str | None] = mapped_column(String(255))

    page_views_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    events_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_bounce: Mapped[bool | None] = mapped_column(Boolean)

    started_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, index=True
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime)

    visitor: Mapped[Visitor] = relationship()
