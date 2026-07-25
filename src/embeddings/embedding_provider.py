"""
Embedding Provider

Defines the abstraction for embedding generation.

Sprint:
    Sprint 6 - D1
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.embeddings.embedding_result import EmbeddingResult
from src.processing.document_chunk import DocumentChunk


class EmbeddingProvider(ABC):
    """
    Abstract base class for embedding providers.

    Concrete implementations may use:

    - SentenceTransformers
    - OpenAI
    - Voyage AI
    - BGE
    - E5

    The remainder of the application should depend only
    on this abstraction.
    """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Return the embedding model name.
        """

    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Return the embedding dimension.
        """

    @abstractmethod
    def embed(
        self,
        chunk: DocumentChunk,
    ) -> EmbeddingResult:
        """
        Generate an embedding for a single document chunk.
        """

    @abstractmethod
    def embed_many(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddingResult]:
        """
        Generate embeddings for multiple document chunks.
        """