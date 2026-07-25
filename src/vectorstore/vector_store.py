"""
Abstract vector store interface.

Sprint:
    Sprint 6 - D3

Defines the contract that all vector database
implementations must satisfy.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.embeddings.embedding_result import EmbeddingResult


class VectorStore(ABC):
    """
    Abstract interface for semantic vector storage.

    Implementations are responsible for storing,
    retrieving and deleting embedding vectors.
    """

    @abstractmethod
    def add(
        self,
        embedding: EmbeddingResult,
    ) -> None:
        """
        Store a single embedding.
        """
        raise NotImplementedError

    @abstractmethod
    def add_many(
        self,
        embeddings: list[EmbeddingResult],
    ) -> None:
        """
        Store multiple embeddings.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query_vector: list[float],
        k: int = 5,
    ) -> list[EmbeddingResult]:
        """
        Return the k most similar embeddings.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        chunk_id: str,
    ) -> None:
        """
        Remove a stored embedding.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """
        Remove every stored embedding.
        """
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        """
        Return the number of stored embeddings.
        """
        raise NotImplementedError