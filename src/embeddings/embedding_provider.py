"""
Embedding provider abstraction.

Sprint:
    Sprint 6 - D4
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.embeddings.embedding_result import EmbeddingResult
from src.processing.document_chunk import DocumentChunk


class EmbeddingProvider(ABC):
    """
    Abstract interface for embedding providers.
    """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Name of the embedding model.
        """

    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Embedding vector dimension.
        """

    @abstractmethod
    def embed(
        self,
        chunk: DocumentChunk,
    ) -> EmbeddingResult:
        """
        Embed a single document chunk.
        """

    @abstractmethod
    def embed_many(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddingResult]:
        """
        Embed multiple document chunks.
        """

    @abstractmethod
    def embed_query(
        self,
        question: str,
    ) -> list[float]:
        """
        Embed a natural-language query.
        """