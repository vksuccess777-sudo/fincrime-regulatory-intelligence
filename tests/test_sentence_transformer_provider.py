"""
Unit tests for SentenceTransformerProvider.
"""

from src.embeddings.embedding_result import EmbeddingResult
from src.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)
from src.processing.document_chunk import DocumentChunk


def create_chunk(**kwargs):
    defaults = {
        "chunk_id": "chunk-00001",
        "text": (
            "Customer Due Diligence requirements under "
            "FATF Recommendation 10."
        ),
        "page_start": 1,
        "page_end": 1,
        "section_title": "Customer Due Diligence",
        "metadata": {},
    }

    defaults.update(kwargs)

    return DocumentChunk(**defaults)


def test_model_name():
    provider = SentenceTransformerProvider()

    assert provider.model_name == "BAAI/bge-small-en-v1.5"


def test_dimension():
    provider = SentenceTransformerProvider()

    assert provider.dimension > 0


def test_embed_returns_embedding_result():
    provider = SentenceTransformerProvider()

    chunk = create_chunk()

    result = provider.embed(chunk)

    assert isinstance(result, EmbeddingResult)


def test_chunk_id_preserved():
    provider = SentenceTransformerProvider()

    chunk = create_chunk(chunk_id="abc123")

    result = provider.embed(chunk)

    assert result.chunk_id == "abc123"


def test_vector_dimension_matches_provider():
    provider = SentenceTransformerProvider()

    chunk = create_chunk()

    result = provider.embed(chunk)

    assert len(result.vector) == provider.dimension
    assert result.dimension == provider.dimension


def test_embedding_not_empty():
    provider = SentenceTransformerProvider()

    chunk = create_chunk()

    result = provider.embed(chunk)

    assert len(result.vector) > 0


def test_embed_many():
    provider = SentenceTransformerProvider()

    chunks = [
        create_chunk(chunk_id="1"),
        create_chunk(chunk_id="2"),
        create_chunk(chunk_id="3"),
    ]

    results = provider.embed_many(chunks)

    assert len(results) == 3
    assert all(isinstance(r, EmbeddingResult) for r in results)


def test_embed_many_preserves_order():
    provider = SentenceTransformerProvider()

    chunks = [
        create_chunk(chunk_id="A"),
        create_chunk(chunk_id="B"),
        create_chunk(chunk_id="C"),
    ]

    results = provider.embed_many(chunks)

    assert [r.chunk_id for r in results] == ["A", "B", "C"]


def test_provider_metadata():
    provider = SentenceTransformerProvider()

    chunk = create_chunk()

    result = provider.embed(chunk)

    assert result.metadata["provider"] == "sentence-transformers"


def test_same_text_same_dimension():
    provider = SentenceTransformerProvider()

    chunk = create_chunk()

    first = provider.embed(chunk)
    second = provider.embed(chunk)

    assert len(first.vector) == len(second.vector)
    assert first.dimension == second.dimension