from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: str | None
    created_at: datetime


class TestList(BaseModel):
    items: list[TestRead]
    total: int
    limit: int
    offset: int
