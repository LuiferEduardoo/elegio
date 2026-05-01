from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EventCreate(BaseModel):
    ip_address: str = Field(min_length=1, max_length=45)

    event_type: str = Field(min_length=1, max_length=50)
    event_name: str | None = Field(default=None, max_length=100)

    page_url: str | None = None
    page_path: str | None = Field(default=None, max_length=500)
    page_title: str | None = Field(default=None, max_length=255)

    element_tag: str | None = Field(default=None, max_length=50)
    element_id: str | None = Field(default=None, max_length=255)
    element_class: str | None = Field(default=None, max_length=255)
    element_text: str | None = Field(default=None, max_length=500)

    scroll_depth: int | None = Field(default=None, ge=0, le=100)
    duration_ms: int | None = Field(default=None, ge=0)

    properties: dict[str, Any] | None = None


class EventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    visitor_id: int
    event_type: str
    event_name: str | None
    page_url: str | None
    page_path: str | None
    page_title: str | None
    element_tag: str | None
    element_id: str | None
    element_class: str | None
    element_text: str | None
    scroll_depth: int | None
    duration_ms: int | None
    properties: dict[str, Any] | None
    occurred_at: datetime
    created_at: datetime
