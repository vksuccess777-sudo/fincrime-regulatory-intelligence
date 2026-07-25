"""
Unit tests for MockVectorStore.

Sprint:
    Sprint 6 - D3
"""

from src.embeddings.embedding_result import EmbeddingResult
from src.vectorstore.mock_vector_store import MockVectorStore


def make_embedding(
    chunk_id: str,
    vector: list[float],
) -> EmbeddingResult:
    """
    Create a test embedding.
    """
    return EmbeddingResult(
        chunk_id=chunk_id,
        vector=vector,
        dimension=len(vector),
        model_name="mock",
        metadata={},
    )


def test_add_single_embedding():
    store = MockVectorStore()

    store.add(
        make_embedding(
            "1",
            [1.0, 0.0],
        )
    )

    assert store.count() == 1


def test_add_many_embeddings():
    store = MockVectorStore()

    store.add_many(
        [
            make_embedding("1", [1.0, 0.0]),
            make_embedding("2", [0.0, 1.0]),
        ]
    )

    assert store.count() == 2


def test_search_returns_best_match():
    store = MockVectorStore()

    store.add_many(
        [
            make_embedding("A", [1.0, 0.0]),
            make_embedding("B", [0.0, 1.0]),
        ]
    )

    results = store.search(
        [1.0, 0.0],
        k=1,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "A"


def test_delete_embedding():
    store = MockVectorStore()

    store.add(
        make_embedding(
            "1",
            [1.0, 0.0],
        )
    )

    store.delete("1")

    assert store.count() == 0


def test_clear_store():
    store = MockVectorStore()

    store.add_many(
        [
            make_embedding("1", [1.0, 0.0]),
            make_embedding("2", [0.0, 1.0]),
        ]
    )

    store.clear()

    assert store.count() == 0


def test_search_empty_store():
    store = MockVectorStore()

    results = store.search(
        [1.0, 0.0],
    )

    assert results == []


def test_search_returns_k_results():
    store = MockVectorStore()

    store.add_many(
        [
            make_embedding("1", [1.0, 0.0]),
            make_embedding("2", [0.9, 0.1]),
            make_embedding("3", [0.0, 1.0]),
        ]
    )

    results = store.search(
        [1.0, 0.0],
        k=2,
    )

    assert len(results) == 2