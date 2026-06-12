from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domains.chat.models import ChatMessageRole


class ChatCreate(BaseModel):
    title: str | None = Field(default=None, max_length=150)


class ChatRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    is_active: bool
    created_at: datetime


class ChatList(BaseModel):
    items: list[ChatRead]
    total: int
    limit: int
    offset: int


class ChatMessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


class ChatMessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chat_id: int
    role: ChatMessageRole
    content: str
    tokens_used: int
    latency_ms: int
    created_at: datetime


class ChatMessageList(BaseModel):
    items: list[ChatMessageRead]
    total: int
    limit: int
    offset: int
