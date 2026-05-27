"""Gemini embedder (gemini-embedding-001).

Embeds chunks and queries through Google's embedding API, so no local model
is loaded into memory. Passages use task_type ``RETRIEVAL_DOCUMENT`` and
queries ``RETRIEVAL_QUERY`` so both live in the same retrieval space.

Outputs are L2-normalized (required for ``output_dimensionality`` < 3072) so
cosine similarity equals dot product — the metric Qdrant is configured with
(``Distance.COSINE``).
"""

import math

from google import genai
from google.genai import types

from app.config import settings

MODEL_NAME = "gemini-embedding-001"
EMBEDDING_DIM = 1536


def _l2_normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(v * v for v in vector))
    if norm == 0.0:
        return vector
    return [v / norm for v in vector]


class Embedder:
    def __init__(
        self,
        model_name: str = MODEL_NAME,
        batch_size: int = 100,
    ):
        self.model_name = model_name
        self.batch_size = batch_size
        self._client = genai.Client(api_key=settings.gemini_api_key)

    def _embed(self, texts: list[str], task_type: str) -> list[list[float]]:
        out: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            response = self._client.models.embed_content(
                model=self.model_name,
                contents=batch,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=EMBEDDING_DIM,
                ),
            )
            out.extend(_l2_normalize(e.values) for e in response.embeddings)
        return out

    def embed_passages(self, texts: list[str]) -> list[list[float]]:
        """Embed documents/chunks for storage (RETRIEVAL_DOCUMENT)."""
        if not texts:
            return []
        return self._embed(texts, "RETRIEVAL_DOCUMENT")

    def embed_query(self, text: str) -> list[float]:
        """Embed a single search query (RETRIEVAL_QUERY)."""
        return self._embed([text], "RETRIEVAL_QUERY")[0]
