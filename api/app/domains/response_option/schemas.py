from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResponseOptionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    title: str
    value: float
    created_at: datetime


class ResponseOptionList(BaseModel):
    items: list[ResponseOptionRead]
    total: int
    limit: int
    offset: int
