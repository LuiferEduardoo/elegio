"""Multilingual E5 embedder.

The E5 family requires task-specific prefixes:
    - documents/chunks  →  "passage: <text>"
    - search queries    →  "query: <text>"

Outputs are L2-normalized so cosine similarity equals dot product (the metric
Qdrant should be configured with — `Distance.COSINE`).
"""

from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-large"
EMBEDDING_DIM = 1024


class Embedder:
    def __init__(
        self,
        model_name: str = MODEL_NAME,
        device: str | None = None,
        batch_size: int = 16,
    ):
        self.model_name = model_name
        self._device = device
        self.batch_size = batch_size
        self._model: SentenceTransformer | None = None

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.model_name, device=self._device)
        return self._model

    def embed_passages(self, texts: list[str]) -> list[list[float]]:
        """Embed documents/chunks for storage. Adds the ``passage:`` prefix."""
        if not texts:
            return []
        prefixed = [f"passage: {t}" for t in texts]
        embeddings = self.model.encode(
            prefixed,
            batch_size=self.batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        """Embed a single search query. Adds the ``query:`` prefix."""
        embedding = self.model.encode(
            [f"query: {text}"],
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return embedding[0].tolist()
