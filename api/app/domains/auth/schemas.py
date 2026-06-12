from pydantic import BaseModel, Field

from app.domains.visitor.schemas import SessionCreate, VisitorCreate


class AuthTokenRequest(BaseModel):
    visitor: VisitorCreate
    session: SessionCreate = Field(default_factory=SessionCreate)


class AuthTokenResponse(BaseModel):
    token: str
    visitor_id: int
