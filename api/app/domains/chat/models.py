import enum

from sqlalchemy import BigInteger, Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin
from app.domains.visitor.models import Visitor


class ChatMessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"


class MessageFeedbackRating(str, enum.Enum):
    LIKE = "like"
    DISLIKE = "dislike"


class Chat(Base, TimestampMixin):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    visitor_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("visitors.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(150),
        default="Nueva conversación",
        server_default="Nueva conversación",
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Conversational memory: old messages get folded into `summary` once the
    # history exceeds the token budget; `last_summarized_message_id` marks how
    # far the summary reaches, so only newer messages are sent verbatim.
    summary: Mapped[str | None] = mapped_column(Text)
    last_summarized_message_id: Mapped[int | None] = mapped_column(Integer)

    visitor: Mapped[Visitor] = relationship()
    messages: Mapped[list["ChatMessage"]] = relationship(back_populates="chat")


class ChatMessage(Base, TimestampMixin):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[ChatMessageRole] = mapped_column(
        Enum(
            ChatMessageRole,
            name="chat_message_role",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    tokens_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    chat: Mapped[Chat] = relationship(back_populates="messages")
    feedback: Mapped["MessageFeedback | None"] = relationship(
        back_populates="message"
    )


class MessageFeedback(Base, TimestampMixin):
    __tablename__ = "message_feedback"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(
        ForeignKey("chat_messages.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    rating: Mapped[MessageFeedbackRating] = mapped_column(
        Enum(
            MessageFeedbackRating,
            name="message_feedback_rating",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    )
    feedback_reason: Mapped[str | None] = mapped_column(String(255))
    comment: Mapped[str | None] = mapped_column(Text)

    message: Mapped[ChatMessage] = relationship(back_populates="feedback")
