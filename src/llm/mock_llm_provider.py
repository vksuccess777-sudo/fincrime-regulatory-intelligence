"""
Mock LLM Provider

Deterministic mock implementation of the LLMProvider interface.

Sprint:
    Sprint 7 - D1

Responsibilities
----------------
- Provide deterministic responses for testing.
- Avoid external API dependencies.
- Support unit and integration tests.
"""

from __future__ import annotations

from src.llm.llm_provider import LLMProvider
from src.llm.llm_response import LLMResponse


class MockLLMProvider(LLMProvider):
    """
    Deterministic mock implementation of an LLM provider.
    """

    @property
    def provider_name(self) -> str:
        return "Mock"

    @property
    def model_name(self) -> str:
        return "mock-llm-v1"

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:
        """
        Return a deterministic response based on the supplied prompt.
        """

        prompt = prompt.strip()

        response_text = (
            "MOCK RESPONSE\n\n"
            f"Prompt received:\n{prompt}"
        )

        prompt_tokens = len(prompt.split())
        completion_tokens = len(response_text.split())

        return LLMResponse(
            text=response_text,
            citations=[],
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            metadata={
                "provider": self.provider_name,
                "model": self.model_name,
                "mock": "true",
            },
        )