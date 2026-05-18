from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
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

categories_table = Table(
    "categories",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("weight", Float, nullable=False),
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

proposals_table = Table(
    "proposals",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("summary", Text),
    Column("full_text", Text),
    Column("category_id", Integer, ForeignKey("categories.id"), nullable=False),
    Column("candidate_id", Integer, ForeignKey("candidates.id"), nullable=False),
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

proposal_chunks_table = Table(
    "proposal_chunks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "proposal_id",
        Integer,
        ForeignKey("proposals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("chunk_index", Integer, nullable=False),
    Column("total_chunks", Integer, nullable=False),
    Column("content", Text, nullable=False),
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

postures_table = Table(
    "postures",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "proposal_id",
        Integer,
        ForeignKey("proposals.id", ondelete="CASCADE"),
        nullable=False,
    ),
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
