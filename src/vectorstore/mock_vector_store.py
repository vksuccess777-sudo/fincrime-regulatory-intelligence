"""
In-memory vector store.

Sprint:
    Sprint 6 - D3

Provides an in-memory implementation of the VectorStore
interface for testing and development.
"""

from __future__ import annotations

from math import sqrt

from src.embeddings.embedding_result import EmbeddingResult
from src.vectorstore.vector_store import VectorStore


class MockVectorStore(VectorStore):
    """
    Simple in-memory vector store.
    """

    def __init__(self) -> None:
        self._embeddings: dict[str, EmbeddingResult] = {}

    def add(
        self,
        embedding: EmbeddingResult,
    ) -> None:
        self._embeddings[embedding.chunk_id] = embedding

    def add_many(
        self,
        embeddings: list[EmbeddingResult],
    ) -> None:
        for embedding in embeddings:
            self.add(embedding)

    def search(
        self,
        query_vector: list[float],
        k: int = 5,
    ) -> list[EmbeddingResult]:
        scored = []

        for embedding in self._embeddings.values():
            score = self._cosine_similarity(
                query_vector,
                embedding.vector,
            )
            scored.append((score, embedding))

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            embedding
            for _, embedding in scored[:k]
        ]

    def delete(
        self,
        chunk_id: str,
    ) -> None:
        self._embeddings.pop(chunk_id, None)

    def clear(self) -> None:
        self._embeddings.clear()

    def count(self) -> int:
        return len(self._embeddings)

    @staticmethod
    def _cosine_similarity(
        left: list[float],
        right: list[float],
    ) -> float:
        if len(left) != len(right):
            raise ValueError("Vector dimensions must match.")

        dot = sum(a * b for a, b in zip(left, right))
        left_norm = sqrt(sum(a * a for a in left))
        right_norm = sqrt(sum(b * b for b in right))

        if left_norm == 0 or right_norm == 0:
            return 0.0

        return dot / (left_norm * right_norm)