from datetime import datetime

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    DateTime,
    Integer,
    Numeric,
    SmallInteger,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class Visitor(Base, TimestampMixin):
    __tablename__ = "visitors"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    visitor_uid: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    browser_name: Mapped[str | None] = mapped_column(String(50))
    browser_version: Mapped[str | None] = mapped_column(String(30))
    engine_name: Mapped[str | None] = mapped_column(String(50))
    os_name: Mapped[str | None] = mapped_column(String(50))
    os_version: Mapped[str | None] = mapped_column(String(30))
    device_type: Mapped[str | None] = mapped_column(String(20), index=True)
    device_vendor: Mapped[str | None] = mapped_column(String(50))
    device_model: Mapped[str | None] = mapped_column(String(50))
    is_mobile: Mapped[bool | None] = mapped_column(Boolean)
    is_bot: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    screen_width: Mapped[int | None] = mapped_column(Integer)
    screen_height: Mapped[int | None] = mapped_column(Integer)
    pixel_ratio: Mapped[float | None] = mapped_column(Numeric(3, 2))
    color_depth: Mapped[int | None] = mapped_column(SmallInteger)
    cpu_cores: Mapped[int | None] = mapped_column(SmallInteger)
    device_memory: Mapped[int | None] = mapped_column(SmallInteger)
    touch_support: Mapped[bool | None] = mapped_column(Boolean)

    primary_language: Mapped[str | None] = mapped_column(String(20), index=True)
    languages: Mapped[list[str] | None] = mapped_column(JSON)
    timezone: Mapped[str | None] = mapped_column(String(64))

    total_sessions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_events: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_page_views: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_time_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    consent_given: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    consent_at: Mapped[datetime | None] = mapped_column(DateTime)
    consent_version: Mapped[str | None] = mapped_column(String(20))

    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, index=True
    )
