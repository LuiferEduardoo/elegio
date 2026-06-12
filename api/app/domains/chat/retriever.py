"""LangChain retriever over the four Qdrant chunk collections.

Embeds the query with gemini-embedding-001 (same space as the indexed chunks,
see app/core/embedder.py) and searches ``proposal_chunks``,
``document_chunks``, ``interview_chunks`` and ``news_chunks``. Hits from every
collection are merged by cosine score — comparable across collections because
all of them are indexed with the same model and normalization — and the global
top-k is returned as LangChain ``Document``s.
"""

import logging

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from app.core.embedder import get_embedder
from app.core.qdrant_client import get_qdrant_client

logger = logging.getLogger(__name__)

CHUNK_COLLECTIONS = (
    "proposal_chunks",
    "document_chunks",
    "interview_chunks",
    "news_chunks",
)

COLLECTION_LABELS = {
    "proposal_chunks": "Propuesta",
    "document_chunks": "Documento",
    "interview_chunks": "Entrevista",
    "news_chunks": "Noticia",
}


class ElegioRetriever(BaseRetriever):
    """Dense retriever across every Elegio chunk collection."""

    top_k_per_collection: int = 4
    top_k: int = 8

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> list[Document]:
        embedder = get_embedder()
        qdrant = get_qdrant_client()
        query_vec = embedder.embed_query(query)

        hits: list[tuple[str, float, dict]] = []
        for collection in CHUNK_COLLECTIONS:
            try:
                points = qdrant.search(
                    collection_name=collection,
                    query_vector=query_vec,
                    limit=self.top_k_per_collection,
                    with_payload=True,
                )
            except Exception:
                logger.warning("Qdrant search failed for %s; skipping", collection)
                continue
            for point in points:
                if point.payload and point.payload.get("content"):
                    hits.append((collection, float(point.score), point.payload))

        hits.sort(key=lambda hit: hit[1], reverse=True)

        return [
            Document(
                page_content=payload["content"],
                metadata={
                    "collection": collection,
                    "score": score,
                    **{k: v for k, v in payload.items() if k != "content"},
                },
            )
            for collection, score, payload in hits[: self.top_k]
        ]
