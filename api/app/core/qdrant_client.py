from qdrant_client import QdrantClient

from app.core.config import get_settings

COLLECTION_NAME = "proposal_chunks"


_instance: QdrantClient | None = None


def get_qdrant_client() -> QdrantClient:
    """Return the process-wide Qdrant client singleton."""
    global _instance
    if _instance is None:
        settings = get_settings()
        _instance = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY or None,
        )
    return _instance
