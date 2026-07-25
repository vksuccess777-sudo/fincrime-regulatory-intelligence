"""
Embedding Result

Represents the output produced by an embedding model for a single
DocumentChunk.

Sprint:
    Sprint 6 - D1
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class EmbeddingResult:
    """
    Immutable embedding result.

    Attributes
    ----------
    chunk_id:
        Identifier of the source DocumentChunk.

    vector:
        Numerical embedding vector.

    model_name:
        Name of the embedding model that generated the vector.

    dimension:
        Number of elements in the embedding vector.

    metadata:
        Optional extensible metadata.
    """

    chunk_id: str
    vector: list[float]
    model_name: str
    dimension: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate the embedding result."""

        if not self.chunk_id.strip():
            raise ValueError("chunk_id cannot be empty.")

        if not self.vector:
            raise ValueError("vector cannot be empty.")

        if not self.model_name.strip():
            raise ValueError("model_name cannot be empty.")

        if self.dimension <= 0:
            raise ValueError(
                "dimension must be greater than zero."
            )

        if len(self.vector) != self.dimension:
            raise ValueError(
                "dimension does not match vector length."
            )

        if self.metadata is None:
            raise ValueError("metadata cannot be None.")

        for value in self.vector:
            if not isinstance(value, (float, int)):
                raise ValueError(
                    "vector must contain only numeric values."
                )

    @property
    def vector_length(self) -> int:
        """Return the vector length."""

        return len(self.vector)