"""
End-to-End Retrieval Pipeline

Sprint:
    Sprint 6 - D5

Coordinates semantic retrieval from the vector store.
"""

from __future__ import annotations

from src.embeddings.embedding_provider import EmbeddingProvider
from src.embeddings.embedding_result import EmbeddingResult
from src.retrieval.retrieval_engine import RetrievalEngine
from src.vectorstore.vector_store import VectorStore


class RetrievalPipeline:
    """
    High-level semantic retrieval pipeline.

    This class provides the entry point for searching the indexed
    regulatory corpus.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:

        self._engine = RetrievalEngine(
            embedding_provider,
            vector_store,
        )

    def search(
        self,
        question: str,
        k: int = 5,
    ) -> list[EmbeddingResult]:
        """
        Retrieve the top-k most relevant chunks.
        """

        return self._engine.search(
            question=question,
            k=k,
        )