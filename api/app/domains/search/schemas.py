from pydantic import BaseModel, Field

from app.domains.proposal.schemas import CandidateInProposal, CategoryInProposal


class SearchHit(BaseModel):
    proposal_id: int
    title: str
    summary: str | None
    candidate: CandidateInProposal
    category: CategoryInProposal
    score: float = Field(description="RRF fusion score (higher = better)")
    semantic_rank: int | None = Field(
        default=None,
        description="1-based rank in the dense list; null if not retrieved by semantic search",
    )
    semantic_score: float | None = Field(
        default=None, description="Cosine similarity from Qdrant"
    )
    lexical_rank: int | None = Field(
        default=None,
        description="1-based rank in the BM25 list; null if not retrieved by lexical search",
    )
    lexical_score: float | None = Field(default=None, description="Raw BM25 score")
    excerpt: str | None = Field(
        default=None, description="Content of the best-matching chunk"
    )


class SearchResponse(BaseModel):
    query: str
    total: int
    items: list[SearchHit]
