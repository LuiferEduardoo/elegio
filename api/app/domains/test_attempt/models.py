import enum
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.test.models import Test
from app.domains.visitor.models import Visitor


class TestStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    TIMED_OUT = "timed_out"


class TestAttempt(Base, TimestampMixin):
    __tablename__ = "test_attempts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    visitor_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("visitors.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    test_id: Mapped[int] = mapped_column(
        ForeignKey("tests.id", ondelete="CASCADE"), nullable=False, index=True
    )

    status: Mapped[TestStatus] = mapped_column(
        Enum(TestStatus, name="test_status"),
        default=TestStatus.IN_PROGRESS,
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)

    visitor: Mapped[Visitor] = relationship()
    test: Mapped[Test] = relationship()
