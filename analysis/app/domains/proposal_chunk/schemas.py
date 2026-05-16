from pydantic import BaseModel


class ProposalText(BaseModel):
    id: int
    title: str
    summary: str | None
    full_text: str | None

    def to_chunkable(self) -> str:
        return self.full_text or self.summary or self.title
