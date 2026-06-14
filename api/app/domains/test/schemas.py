from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domains.test.models import TestType


class TestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    image_url: str | None
    type: TestType | None
    created_at: datetime


class TestList(BaseModel):
    items: list[TestRead]
    total: int
    limit: int
    offset: int
