from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domains.test_attempt.models import TestStatus


class TestAttemptInitialize(BaseModel):
    test_id: int = Field(gt=0)


class TestAttemptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: str
    visitor_id: int
    test_id: int
    status: TestStatus
    started_at: datetime
    finished_at: datetime | None
    created_at: datetime


class TestAttemptList(BaseModel):
    items: list[TestAttemptRead]
    total: int
    limit: int
    offset: int
