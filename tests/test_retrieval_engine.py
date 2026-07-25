"""
Unit tests for RetrievalEngine.

Sprint:
    Sprint 6 - D4
"""

from src.embeddings.embedding_result import EmbeddingResult
from src.processing.document_chunk import DocumentChunk
from src.retrieval.retrieval_engine import RetrievalEngine
from src.vectorstore.mock_vector_store import MockVectorStore


class FakeEmbeddingProvider:
    """
    Fake embedding provider used for RetrievalEngine tests.
    """

    @property
    def model_name(self) -> str:
        return "fake-model"

    @property
    def dimension(self) -> int:
        return 3

    def embed(
        self,
        chunk: DocumentChunk,
    ) -> EmbeddingResult:
        return EmbeddingResult(
            chunk_id=chunk.chunk_id,
            vector=[1.0, 2.0, 3.0],
            dimension=3,
            model_name=self.model_name,
            metadata=chunk.metadata,
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
        return [1.0, 2.0, 3.0]


def make_embedding(
    chunk_id: str,
    metadata: dict | None = None,
) -> EmbeddingResult:
    return EmbeddingResult(
        chunk_id=chunk_id,
        vector=[1.0, 2.0, 3.0],
        dimension=3,
        model_name="fake-model",
        metadata=metadata or {},
    )


def test_search_returns_single_result():
    provider = FakeEmbeddingProvider()
    store = MockVectorStore()

    store.add(
        make_embedding("chunk-1")
    )

    engine = RetrievalEngine(
        provider,
        store,
    )

    results = engine.search(
        "What is EDD?",
        k=1,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-1"


def test_search_returns_multiple_results():
    provider = FakeEmbeddingProvider()
    store = MockVectorStore()

    store.add_many(
        [
            make_embedding("A"),
            make_embedding("B"),
            make_embedding("C"),
        ]
    )

    engine = RetrievalEngine(
        provider,
        store,
    )

    results = engine.search(
        "AML",
        k=2,
    )

    assert len(results) == 2


def test_search_empty_store():
    provider = FakeEmbeddingProvider()
    store = MockVectorStore()

    engine = RetrievalEngine(
        provider,
        store,
    )

    results = engine.search(
        "Sanctions",
        k=5,
    )

    assert results == []


def test_metadata_preserved():
    provider = FakeEmbeddingProvider()
    store = MockVectorStore()

    store.add(
        make_embedding(
            "meta",
            metadata={
                "jurisdiction": "FATF",
                "section": "Recommendation 10",
            },
        )
    )

    engine = RetrievalEngine(
        provider,
        store,
    )

    result = engine.search(
        "CDD",
        k=1,
    )[0]

    assert result.metadata["jurisdiction"] == "FATF"
    assert result.metadata["section"] == "Recommendation 10"


def test_k_limit_respected():
    provider = FakeEmbeddingProvider()
    store = MockVectorStore()

    store.add_many(
        [
            make_embedding("1"),
            make_embedding("2"),
            make_embedding("3"),
            make_embedding("4"),
        ]
    )

    engine = RetrievalEngine(
        provider,
        store,
    )

    results = engine.search(
        "Financial Crime",
        k=3,
    )

    assert len(results) == 3