"""Gemini query embedder (gemini-embedding-001), in-process singleton.

Embeds search queries through Google's embedding API so no local model is
loaded into memory. Must mirror the analysis-side indexing: same model,
``output_dimensionality`` and L2-normalization, with task_type
``RETRIEVAL_QUERY`` for queries, so query vectors live in the same space as
the indexed chunks.
"""

import math

from google import genai
from google.genai import types

from app.core.config import get_settings

MODEL_NAME = "gemini-embedding-001"
EMBEDDING_DIM = 1536


def _l2_normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(v * v for v in vector))
    if norm == 0.0:
        return vector
    return [v / norm for v in vector]


class Embedder:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self._client: genai.Client | None = None

    @property
    def client(self) -> genai.Client:
        if self._client is None:
            self._client = genai.Client(api_key=get_settings().GEMINI_API_KEY)
        return self._client

    def embed_query(self, text: str) -> list[float]:
        response = self.client.models.embed_content(
            model=self.model_name,
            contents=[text],
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=EMBEDDING_DIM,
            ),
        )
        return _l2_normalize(response.embeddings[0].values)


_instance: Embedder | None = None


def get_embedder() -> Embedder:
    """Return the process-wide Embedder singleton."""
    global _instance
    if _instance is None:
        _instance = Embedder()
    return _instance
