"""
LLM Response

Represents the response returned by a Large Language Model (LLM).

Sprint:
    Sprint 7 - D1

Responsibilities
----------------
- Store generated answer.
- Store supporting citations.
- Store token usage.
- Store provider metadata.
- Remain immutable.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class LLMResponse:
    """
    Immutable response returned by an LLM provider.
    """

    text: str

    citations: list[str] = field(default_factory=list)

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    metadata: dict[str, str] = field(default_factory=dict)