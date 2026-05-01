from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domains.test_attempt.models import TestStatus


class TestAttemptCreate(BaseModel):
    test_id: int = Field(gt=0)
    ip_address: str = Field(min_length=1, max_length=45)


class TestAttemptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    visitor_id: int
    test_id: int
    status: TestStatus
    started_at: datetime
    finished_at: datetime | None
    created_at: datetime
