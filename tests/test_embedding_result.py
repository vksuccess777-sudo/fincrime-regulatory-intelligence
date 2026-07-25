"""
Unit tests for EmbeddingResult.
"""

from dataclasses import FrozenInstanceError

import pytest

from src.embeddings.embedding_result import EmbeddingResult


def create_embedding(**kwargs):
    defaults = {
        "chunk_id": "chunk-00001",
        "vector": [0.1, 0.2, 0.3, 0.4],
        "model_name": "bge-small-en-v1.5",
        "dimension": 4,
        "metadata": {
            "provider": "SentenceTransformers",
            "source": "FATF",
        },
    }

    defaults.update(kwargs)

    return EmbeddingResult(**defaults)


def test_embedding_creation():
    embedding = create_embedding()

    assert embedding.chunk_id == "chunk-00001"
    assert embedding.model_name == "bge-small-en-v1.5"
    assert embedding.dimension == 4
    assert embedding.vector == [0.1, 0.2, 0.3, 0.4]


def test_embedding_is_frozen():
    embedding = create_embedding()

    with pytest.raises(FrozenInstanceError):
        embedding.dimension = 10


def test_embedding_equality():
    e1 = create_embedding()
    e2 = create_embedding()

    assert e1 == e2


def test_embedding_inequality():
    e1 = create_embedding()
    e2 = create_embedding(chunk_id="chunk-00002")

    assert e1 != e2


def test_vector_length_property():
    embedding = create_embedding()

    assert embedding.vector_length == 4


def test_empty_chunk_id():
    with pytest.raises(ValueError):
        create_embedding(chunk_id="")


def test_empty_vector():
    with pytest.raises(ValueError):
        create_embedding(vector=[], dimension=0)


def test_empty_model_name():
    with pytest.raises(ValueError):
        create_embedding(model_name="")


def test_dimension_mismatch():
    with pytest.raises(ValueError):
        create_embedding(
            vector=[0.1, 0.2],
            dimension=5,
        )


def test_negative_dimension():
    with pytest.raises(ValueError):
        create_embedding(
            dimension=-1,
        )


def test_non_numeric_vector():
    with pytest.raises(ValueError):
        create_embedding(
            vector=[0.1, "abc", 0.3],
            dimension=3,
        )


def test_metadata():
    metadata = {
        "provider": "OpenAI",
        "version": "1.0",
    }

    embedding = create_embedding(metadata=metadata)

    assert embedding.metadata == metadata