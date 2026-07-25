"""
Integration tests for ChromaVectorStore.

Sprint:
    Sprint 6 - D3
"""

from pathlib import Path

from src.embeddings.embedding_result import EmbeddingResult
from src.vectorstore.chroma_vector_store import ChromaVectorStore


TEST_DB = Path("tests/temp_chroma_db")


def make_embedding(
    chunk_id: str,
    vector: list[float],
    metadata: dict | None = None,
) -> EmbeddingResult:
    return EmbeddingResult(
        chunk_id=chunk_id,
        vector=vector,
        dimension=len(vector),
        model_name="test-model",
        metadata=metadata or {},
    )


def make_store() -> ChromaVectorStore:
    store = ChromaVectorStore(
        persist_directory=TEST_DB,
    )
    store.clear()
    return store


def test_add_single_embedding():
    store = make_store()

    store.add(
        make_embedding(
            "chunk-1",
            [1.0, 0.0],
        )
    )

    assert store.count() == 1


def test_add_many_embeddings():
    store = make_store()

    store.add_many(
        [
            make_embedding("a", [1.0, 0.0]),
            make_embedding("b", [0.0, 1.0]),
        ]
    )

    assert store.count() == 2


def test_search_returns_best_match():
    store = make_store()

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
    store = make_store()

    store.add(
        make_embedding(
            "delete-me",
            [1.0, 0.0],
        )
    )

    store.delete("delete-me")

    assert store.count() == 0


def test_clear_store():
    store = make_store()

    store.add_many(
        [
            make_embedding("1", [1.0, 0.0]),
            make_embedding("2", [0.0, 1.0]),
        ]
    )

    store.clear()

    assert store.count() == 0


def test_metadata_preserved():
    store = make_store()

    store.add(
        make_embedding(
            "meta",
            [1.0, 0.0],
            metadata={
                "jurisdiction": "FATF",
                "section": "Recommendation 10",
            },
        )
    )

    result = store.search(
        [1.0, 0.0],
        k=1,
    )[0]

    assert result.metadata["jurisdiction"] == "FATF"
    assert result.metadata["section"] == "Recommendation 10"


def test_search_returns_k_results():
    store = make_store()

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