"""
Unit tests for IndexBuilder.

Sprint:
    Sprint 6 - D3
"""

from src.embeddings.embedding_result import EmbeddingResult
from src.indexing.index_builder import IndexBuilder
from src.processing.document_chunk import DocumentChunk
from src.vectorstore.mock_vector_store import MockVectorStore


class FakeEmbeddingProvider:
    """
    Simple embedding provider used for testing.
    """

    def embed(
        self,
        chunk: DocumentChunk,
    ) -> EmbeddingResult:
        return EmbeddingResult(
            chunk_id=chunk.chunk_id,
            vector=[1.0, 2.0, 3.0],
            dimension=3,
            model_name="fake-model",
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


def make_chunk(
    chunk_id: str,
) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=chunk_id,
        text=f"Content for {chunk_id}",
        page_start=1,
        page_end=1,
        section_title="Section",
        metadata={},
    )


def test_index_single_chunk():
    provider = FakeEmbeddingProvider()
    store = MockVectorStore()

    builder = IndexBuilder(
        provider,
        store,
    )

    builder.index_chunk(
        make_chunk("chunk-1"),
    )

    assert store.count() == 1


def test_index_multiple_chunks():
    provider = FakeEmbeddingProvider()
    store = MockVectorStore()

    builder = IndexBuilder(
        provider,
        store,
    )

    builder.index_chunks(
        [
            make_chunk("1"),
            make_chunk("2"),
            make_chunk("3"),
        ]
    )

    assert store.count() == 3


def test_index_preserves_chunk_ids():
    provider = FakeEmbeddingProvider()
    store = MockVectorStore()

    builder = IndexBuilder(
        provider,
        store,
    )

    builder.index_chunks(
        [
            make_chunk("A"),
            make_chunk("B"),
        ]
    )

    results = store.search(
        [1.0, 2.0, 3.0],
        k=2,
    )

    ids = {
        result.chunk_id
        for result in results
    }

    assert ids == {"A", "B"}


def test_index_empty_chunk_list():
    provider = FakeEmbeddingProvider()
    store = MockVectorStore()

    builder = IndexBuilder(
        provider,
        store,
    )

    builder.index_chunks([])

    assert store.count() == 0


def test_embedding_metadata_preserved():
    provider = FakeEmbeddingProvider()
    store = MockVectorStore()

    builder = IndexBuilder(
        provider,
        store,
    )

    chunk = DocumentChunk(
        chunk_id="meta",
        text="EDD requirements",
        page_start=1,
        page_end=1,
        section_title="Recommendation 10",
        metadata={
            "jurisdiction": "FATF",
            "document": "Recommendations",
        },
    )

    builder.index_chunk(chunk)

    result = store.search(
        [1.0, 2.0, 3.0],
        k=1,
    )[0]

    assert result.metadata["jurisdiction"] == "FATF"
    assert result.metadata["document"] == "Recommendations"