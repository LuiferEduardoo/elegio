from google import genai
from google.genai import types

from app.config import settings
from app.posture_proposal.schemas import LLMRating


class GeminiClassifier:
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = model

    def classify(self, prompt: str) -> LLMRating:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LLMRating,
                temperature=0.1,
            ),
        )
        return response.parsed
