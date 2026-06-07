from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import settings
from app.core.embedder import EMBEDDING_DIM

COLLECTION_NAME = "proposal_chunks"
NEWS_COLLECTION_NAME = "news_chunks"
DOCUMENT_COLLECTION_NAME = "document_chunks"
INTERVIEW_COLLECTION_NAME = "interview_chunks"


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key or None,
    )


def ensure_collection(
    client: QdrantClient, name: str = COLLECTION_NAME
) -> None:
    """Create the collection if it doesn't exist (idempotent)."""
    if client.collection_exists(name):
        return
    client.create_collection(
        collection_name=name,
        vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
    )
