from sqlalchemy import Connection

from app.core.database import postures_table
from app.core.gemini_client import GeminiClassifier
from app.domains.posture_proposal.prompt import build_prompt
from app.domains.posture_proposal.schemas import (
    ConfidenceLevel,
    CoderType,
    ProposalRead,
)


CONFIDENCE_MAP = {
    "high": ConfidenceLevel.HIGH,
    "medium": ConfidenceLevel.MEDIUM,
    "low": ConfidenceLevel.LOW,
}


class PostureService:
    def __init__(self, conn: Connection, classifier: GeminiClassifier):
        self.conn = conn
        self.classifier = classifier

    def rate_proposal(self, proposal: ProposalRead) -> int:
        """Classify a proposal with the LLM and insert the resulting posture."""
        prompt = build_prompt(
            category_slug=proposal.category.name,
            category_name=proposal.category.name,
            proposal_text=proposal.full_text or proposal.summary or proposal.title,
        )

        result = self.classifier.classify(prompt)

        stmt = postures_table.insert().values(
            proposal_id=proposal.id,
            axis_value=result.score,
            confidence=CONFIDENCE_MAP[result.confidence].value,
            reasoning=result.reasoning,
            ambiguities=result.ambiguities,
            coder_type=CoderType.LLM.value,
            coder_name=self.classifier.model,
        )

        cursor = self.conn.execute(stmt)
        self.conn.commit()
        return cursor.inserted_primary_key[0]
