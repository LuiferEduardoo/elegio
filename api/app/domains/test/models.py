import enum

from sqlalchemy import Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class TestType(str, enum.Enum):
    POLITICAL_SPECTRUM = "political_spectrum"
    PROGRAMMATIC_ALIGNMENT = "programmatic_alignment"


class Test(Base, TimestampMixin):
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(2048))
    type: Mapped[TestType | None] = mapped_column(Enum(TestType, name="test_type"))
