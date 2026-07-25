"""
LLM Factory

Creates LLM provider implementations.

Sprint:
    Sprint 7 - D1
"""

from __future__ import annotations

from src.llm.groq_provider import GroqProvider
from src.llm.llm_provider import LLMProvider
from src.llm.mock_llm_provider import MockLLMProvider


class LLMFactory:
    """
    Factory for creating LLM providers.
    """

    @staticmethod
    def create(
        provider: str = "groq",
    ) -> LLMProvider:
        """
        Create an LLM provider.
        """

        provider = provider.lower()

        if provider == "groq":
            return GroqProvider()

        if provider == "mock":
            return MockLLMProvider()

        raise ValueError(
            f"Unknown LLM provider: {provider}"
        )