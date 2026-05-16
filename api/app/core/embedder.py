"""Multilingual E5 embedder, in-process singleton for query embeddings.

Mirrors the analysis-side embedder so query vectors live in the same space
as the indexed chunks. E5 requires task-specific prefixes:
    - documents/chunks  →  "passage: <text>"
    - search queries    →  "query: <text>"

The model is lazily loaded on first call (~2.2 GB download on first start,
~1.5 GB RAM per worker). Outputs are L2-normalized so cosine == dot product.
"""

from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-large"
EMBEDDING_DIM = 1024


class Embedder:
    def __init__(
        self,
        model_name: str = MODEL_NAME,
        device: str | None = None,
    ):
        self.model_name = model_name
        self._device = device
        self._model: SentenceTransformer | None = None

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.model_name, device=self._device)
        return self._model

    def embed_query(self, text: str) -> list[float]:
        embedding = self.model.encode(
            [f"query: {text}"],
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return embedding[0].tolist()


_instance: Embedder | None = None


def get_embedder() -> Embedder:
    """Return the process-wide Embedder singleton (lazy-loaded)."""
    global _instance
    if _instance is None:
        _instance = Embedder()
    return _instance
