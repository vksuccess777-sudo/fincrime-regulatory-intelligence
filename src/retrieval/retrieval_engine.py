"""
Semantic Retrieval Engine.

Sprint:
    Sprint 6 - D4

Coordinates semantic retrieval from the vector store.
"""

from __future__ import annotations

from src.embeddings.embedding_provider import EmbeddingProvider
from src.embeddings.embedding_result import EmbeddingResult
from src.vectorstore.vector_store import VectorStore


class RetrievalEngine:
    """
    Performs semantic retrieval using an embedding provider
    and a vector store.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    def search(
        self,
        question: str,
        k: int = 5,
    ) -> list[EmbeddingResult]:
        """
        Retrieve the k most relevant document embeddings
        for a natural-language question.
        """

        query_embedding = self._embedding_provider.embed_query(
            question,
        )

        return self._vector_store.search(
            query_vector=query_embedding,
            k=k,
        )