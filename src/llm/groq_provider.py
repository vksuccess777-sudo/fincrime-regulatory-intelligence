"""
Groq Provider

Production implementation of the LLMProvider interface using the Groq API.

Sprint:
    Sprint 7 - D1

Responsibilities
----------------
- Connect to Groq.
- Generate responses using the configured model.
- Return provider-independent LLMResponse objects.
"""

from __future__ import annotations

from groq import Groq

import config
from src.llm.llm_provider import LLMProvider
from src.llm.llm_response import LLMResponse


class GroqProvider(LLMProvider):
    """
    Production Groq implementation.
    """

    def __init__(self) -> None:
        if not config.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not configured. "
                "Please set it in your .env file."
            )

        self._client = Groq(
            api_key=config.GROQ_API_KEY,
        )

    @property
    def provider_name(self) -> str:
        return "Groq"

    @property
    def model_name(self) -> str:
        return config.MODEL_NAME

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:
        """
        Generate a response from Groq.
        """

        response = self._client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=config.TEMPERATURE,
            max_completion_tokens=config.MAX_TOKENS,
        )

        usage = response.usage

        return LLMResponse(
            text=response.choices[0].message.content or "",
            citations=[],
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
            metadata={
                "provider": self.provider_name,
                "model": self.model_name,
            },
        )