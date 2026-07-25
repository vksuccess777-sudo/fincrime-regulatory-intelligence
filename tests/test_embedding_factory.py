"""
Unit tests for EmbeddingFactory.
"""

import pytest

from src.embeddings.embedding_factory import EmbeddingFactory
from src.embeddings.embedding_provider import EmbeddingProvider
from src.embeddings.mock_embedding_provider import MockEmbeddingProvider


def test_default_provider():
    """
    The default provider should be the mock provider.
    """

    provider = EmbeddingFactory.get_provider()

    assert isinstance(provider, MockEmbeddingProvider)


def test_mock_provider():
    """
    Explicitly requesting the mock provider should return
    a MockEmbeddingProvider instance.
    """

    provider = EmbeddingFactory.get_provider("mock")

    assert isinstance(provider, MockEmbeddingProvider)


def test_provider_is_embedding_provider():
    """
    Returned providers must implement the EmbeddingProvider
    abstraction.
    """

    provider = EmbeddingFactory.get_provider()

    assert isinstance(provider, EmbeddingProvider)


def test_provider_model_name():
    """
    Provider should expose its configured model name.
    """

    provider = EmbeddingFactory.get_provider()

    assert provider.model_name == "mock-embedding-model"


def test_provider_dimension():
    """
    Provider should expose its embedding dimension.
    """

    provider = EmbeddingFactory.get_provider()

    assert provider.dimension == 8


def test_provider_name_case_insensitive():
    """
    Factory should accept provider names regardless of case.
    """

    provider = EmbeddingFactory.get_provider("MOCK")

    assert isinstance(provider, MockEmbeddingProvider)


def test_unknown_provider():
    """
    Unsupported providers should raise ValueError.
    """

    with pytest.raises(ValueError):
        EmbeddingFactory.get_provider("unknown")


def test_empty_provider_name():
    """
    Empty provider names should raise ValueError.
    """

    with pytest.raises(ValueError):
        EmbeddingFactory.get_provider("")


def test_whitespace_provider_name():
    """
    Whitespace-only provider names should raise ValueError.
    """

    with pytest.raises(ValueError):
        EmbeddingFactory.get_provider("   ")