"""
LLM Provider

Abstract interface for all Large Language Model providers.

Sprint:
    Sprint 7 - D1

Responsibilities
----------------
- Define the contract for all LLM providers.
- Keep the application independent of any specific vendor.
- Support single and future conversational interactions.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.llm.llm_response import LLMResponse


class LLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Human-readable provider name.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Name of the underlying model.
        """
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:
        """
        Generate a response from a prompt.
        """
        raise NotImplementedError