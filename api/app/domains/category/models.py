from sqlalchemy import Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)

    # Negative pole (-1.0 end of the axis)
    negative_pole_name: Mapped[str] = mapped_column(String(64), nullable=False)
    negative_pole_description: Mapped[str] = mapped_column(Text, nullable=False)

    # Positive pole (+1.0 end of the axis)
    positive_pole_name: Mapped[str] = mapped_column(String(64), nullable=False)
    positive_pole_description: Mapped[str] = mapped_column(Text, nullable=False)
