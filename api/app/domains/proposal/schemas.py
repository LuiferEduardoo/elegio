from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CategoryInProposal(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    weight: float


class CandidateInProposal(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    presidential_candidate: str
    vice_presidential_candidate: str
    political_group: str
    political_spectrum: str | None
    photo_president: str | None
    photo_vice_president: str | None
    photo_of_political_group: str | None


class PostureInProposal(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    axis_value: float


class TaggingInProposal(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class SourceInProposal(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str


class ProposalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    summary: str | None
    full_text: str | None
    category: CategoryInProposal
    candidate: CandidateInProposal
    postures: list[PostureInProposal]
    taggings: list[TaggingInProposal]
    sources: list[SourceInProposal]
    created_at: datetime


class ProposalList(BaseModel):
    items: list[ProposalRead]
    total: int
    limit: int
    offset: int
