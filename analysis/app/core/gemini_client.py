from google import genai
from google.genai import types

from app.config import settings
from app.domains.posture_proposal.schemas import QualificationLLM


class GeminiClassifier:
    def __init__(self, model: str = "gemini-2.5-pro"):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = model

    def classify(self, prompt: str) -> QualificationLLM:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=QualificationLLM,
                temperature=0.1,
            ),
        )
        return response.parsed
