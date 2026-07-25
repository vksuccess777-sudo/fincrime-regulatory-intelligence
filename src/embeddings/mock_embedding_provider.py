"""
Mock Embedding Provider

Deterministic embedding provider used for testing.

Sprint:
    Sprint 6
"""

from __future__ import annotations

from src.embeddings.embedding_provider import EmbeddingProvider
from src.embeddings.embedding_result import EmbeddingResult
from src.processing.document_chunk import DocumentChunk


class MockEmbeddingProvider(EmbeddingProvider):
    """
    Deterministic embedding provider for unit testing.
    """

    @property
    def model_name(self) -> str:
        return "mock-embedding-model"

    @property
    def dimension(self) -> int:
        return 8

    def embed(
        self,
        chunk: DocumentChunk,
    ) -> EmbeddingResult:

        length = len(chunk.text)

        vector = [
            float((length + i) % 100) / 100.0
            for i in range(self.dimension)
        ]

        return EmbeddingResult(
            chunk_id=chunk.chunk_id,
            vector=vector,
            model_name=self.model_name,
            dimension=self.dimension,
            metadata={
                "provider": "mock",
            },
        )

    def embed_many(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddingResult]:

        return [
            self.embed(chunk)
            for chunk in chunks
        ]

    def embed_query(
        self,
        question: str,
    ) -> list[float]:
        """
        Produce a deterministic embedding for a search query.
        """

        length = len(question)

        return [
            float((length + i) % 100) / 100.0
            for i in range(self.dimension)
        ]