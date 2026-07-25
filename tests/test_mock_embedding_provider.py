"""
Unit tests for MockEmbeddingProvider.
"""

from src.embeddings.embedding_result import EmbeddingResult
from src.embeddings.mock_embedding_provider import MockEmbeddingProvider
from src.processing.document_chunk import DocumentChunk


def create_chunk(**kwargs):
    defaults = {
        "chunk_id": "chunk-00001",
        "text": "Know Your Customer requirements under FATF Recommendation 10.",
        "page_start": 1,
        "page_end": 1,
        "section_title": "Customer Due Diligence",
        "metadata": {},
    }

    defaults.update(kwargs)

    return DocumentChunk(**defaults)


def test_model_name():
    provider = MockEmbeddingProvider()

    assert provider.model_name == "mock-embedding-model"


def test_dimension():
    provider = MockEmbeddingProvider()

    assert provider.dimension == 8


def test_embed_returns_embedding_result():
    provider = MockEmbeddingProvider()

    chunk = create_chunk()

    result = provider.embed(chunk)

    assert isinstance(result, EmbeddingResult)


def test_embed_chunk_id_preserved():
    provider = MockEmbeddingProvider()

    chunk = create_chunk(chunk_id="chunk-123")

    result = provider.embed(chunk)

    assert result.chunk_id == "chunk-123"


def test_vector_dimension():
    provider = MockEmbeddingProvider()

    chunk = create_chunk()

    result = provider.embed(chunk)

    assert len(result.vector) == provider.dimension
    assert result.dimension == provider.dimension


def test_embed_is_deterministic():
    provider = MockEmbeddingProvider()

    chunk = create_chunk()

    first = provider.embed(chunk)
    second = provider.embed(chunk)

    assert first.vector == second.vector


def test_different_text_produces_different_embedding():
    provider = MockEmbeddingProvider()

    chunk1 = create_chunk(text="AML")
    chunk2 = create_chunk(text="AML regulations covering customer due diligence.")

    result1 = provider.embed(chunk1)
    result2 = provider.embed(chunk2)

    assert result1.vector != result2.vector


def test_embed_many_returns_list():
    provider = MockEmbeddingProvider()

    chunks = [
        create_chunk(chunk_id="1"),
        create_chunk(chunk_id="2"),
        create_chunk(chunk_id="3"),
    ]

    results = provider.embed_many(chunks)

    assert len(results) == 3
    assert all(isinstance(r, EmbeddingResult) for r in results)


def test_embed_many_preserves_order():
    provider = MockEmbeddingProvider()

    chunks = [
        create_chunk(chunk_id="A"),
        create_chunk(chunk_id="B"),
        create_chunk(chunk_id="C"),
    ]

    results = provider.embed_many(chunks)

    assert [r.chunk_id for r in results] == ["A", "B", "C"]


def test_metadata_contains_provider():
    provider = MockEmbeddingProvider()

    chunk = create_chunk()

    result = provider.embed(chunk)

    assert result.metadata["provider"] == "mock"