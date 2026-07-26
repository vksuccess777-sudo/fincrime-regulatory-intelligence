"""
Knowledge Build Result

Represents the outcome of a knowledge indexing run.

Sprint:
    Sprint 8 - D1
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class KnowledgeBuildResult:
    """
    Summary of one indexing operation.
    """

    documents_processed: int

    sections_detected: int

    chunks_generated: int

    embeddings_created: int

    vectors_stored: int

    errors: list[str] = field(default_factory=list)

    @property
    def successful(self) -> bool:
        return len(self.errors) == 0

    @property
    def failed(self) -> bool:
        return not self.successful