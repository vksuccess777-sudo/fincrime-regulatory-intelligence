"""
Embedding Factory

Creates embedding provider instances.

Sprint:
    Sprint 6 - D2
"""

from __future__ import annotations

from src.embeddings.embedding_provider import EmbeddingProvider
from src.embeddings.mock_embedding_provider import MockEmbeddingProvider


class EmbeddingFactory:
    """
    Factory for creating embedding providers.

    The factory hides provider selection from the rest
    of the application.

    Sprint 6 currently returns the mock provider.

    Future providers:

    - SentenceTransformerProvider
    - OpenAIEmbeddingProvider
    - VoyageEmbeddingProvider
    """

    @staticmethod
    def get_provider(
        provider_name: str = "mock",
    ) -> EmbeddingProvider:
        """
        Return an embedding provider.

        Args:
            provider_name:
                Name of the provider.

        Returns:
            EmbeddingProvider implementation.
        """

        provider = provider_name.lower()

        if provider == "mock":
            return MockEmbeddingProvider()

        raise ValueError(
            f"Unsupported embedding provider: {provider_name}"
        )