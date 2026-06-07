from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    JSON,
    MetaData,
    String,
    Table,
    Text,
    Time,
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

# Partial reflection: only the columns the analysis pipeline reads. The full
# candidates schema is owned by the API/Alembic; we never write to it here.
candidates_table = Table(
    "candidates",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("presidential_candidate", String(255), nullable=False),
    Column("deleted_at", DateTime, nullable=True),
)

news_table = Table(
    "news",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("uuid", String(36), nullable=False, unique=True, index=True),
    Column("candidate_id", Integer, ForeignKey("candidates.id"), nullable=False),
    Column("source_type", String(50), nullable=False),
    Column("publishing_house", String(100), nullable=False),
    Column("title", String(255), nullable=False),
    Column("url", Text, nullable=False),
    Column("published_date", Date, nullable=False),
    Column("processed_at", DateTime, server_default=func.now(), nullable=False),
    Column("content_raw", Text, nullable=False),
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

news_chunks_table = Table(
    "news_chunks",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column(
        "news_id",
        Integer,
        ForeignKey("news.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("chunk_index", Integer, nullable=False),
    Column("total_chunks", Integer, nullable=False),
    Column("content_chunk", Text, nullable=False),
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

documents_table = Table(
    "documents",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("uuid", String(36), nullable=False, unique=True, index=True),
    Column("candidate_id", Integer, ForeignKey("candidates.id"), nullable=False),
    Column("source_type", String(50), nullable=False),
    Column("type", String(50), nullable=True),
    Column("title", String(255), nullable=True),
    Column("url", Text, nullable=True),
    Column("content", Text, nullable=False),
    Column("publishing_house", String(100), nullable=True),
    Column("published_date", Date, nullable=True),
    Column("page_count", Integer, nullable=True),
    Column("processed_at", DateTime, server_default=func.now(), nullable=False),
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

document_chunks_table = Table(
    "document_chunks",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column(
        "document_id",
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("chunk_index", Integer, nullable=False),
    Column("total_chunks", Integer, nullable=False),
    Column("content_chunk", Text, nullable=False),
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

interviews_table = Table(
    "interviews",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("uuid", String(36), nullable=False, unique=True, index=True),
    Column("candidate_id", Integer, ForeignKey("candidates.id"), nullable=False),
    Column("source_type", String(50), nullable=False),
    Column("format_type", String(50), nullable=True),
    Column("title", String(255), nullable=False),
    Column("media_outlet", String(100), nullable=False),
    Column("organized_by", String(100), nullable=True),
    Column("host_or_interviewer", String(100), nullable=True),
    Column("participants", JSON, nullable=True),
    Column("interview_date", Date, nullable=False),
    Column("url_video_audio", Text, nullable=True),
    Column("processed_at", DateTime, server_default=func.now(), nullable=False),
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

interview_segments_table = Table(
    "interview_segments",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column(
        "interview_id",
        Integer,
        ForeignKey("interviews.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("start_time", Time, nullable=False),
    Column("end_time", Time, nullable=False),
    Column("speaker", String(100), nullable=False),
    Column("text_segment", Text, nullable=False),
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
