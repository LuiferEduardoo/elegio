from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    func,
)

from app.config import settings

engine = create_engine(settings.database_url, future=True)

metadata = MetaData()

postures_table = Table(
    "postures",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("proposal_id", Integer, nullable=False),
    Column("axis_value", Float, nullable=False),
    Column(
        "confidence",
        Enum("high", "medium", "low", name="confidence_level"),
        nullable=False,
    ),
    Column("reasoning", Text),
    Column("ambiguities", Text),
    Column(
        "coder_type",
        Enum("llm", "human", name="coder_type"),
        nullable=False,
    ),
    Column("coder_name", String(255), nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column(
        "updated_at",
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
    Column("deleted_at", DateTime, nullable=True),
)
