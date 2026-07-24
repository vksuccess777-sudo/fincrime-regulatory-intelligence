"""
Immutable document chunk model.

A DocumentChunk represents a semantic unit of text extracted from a
DocumentSection. It is the smallest retrieval unit that will later be
embedded into the vector database for semantic search.

Instances are immutable and validated on creation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class DocumentChunk:
    """
    Immutable semantic document chunk.

    Attributes:
        chunk_id:
            Unique identifier for the chunk.

        text:
            Chunk content.

        page_start:
            First page represented by the chunk.

        page_end:
            Last page represented by the chunk.

        section_title:
            Parent document section title.

        metadata:
            Extensible metadata associated with the chunk.
    """

    chunk_id: str
    text: str
    page_start: int
    page_end: int
    section_title: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate the document chunk."""

        if not self.chunk_id or not self.chunk_id.strip():
            raise ValueError("chunk_id cannot be empty.")

        if not self.text or not self.text.strip():
            raise ValueError("text cannot be empty.")

        if self.page_start < 1:
            raise ValueError(
                "page_start must be greater than or equal to 1."
            )

        if self.page_end < self.page_start:
            raise ValueError(
                "page_end must be greater than or equal to page_start."
            )

        if not self.section_title or not self.section_title.strip():
            raise ValueError("section_title cannot be empty.")

        if self.metadata is None:
            raise ValueError("metadata cannot be None.")

    @property
    def page_range(self) -> tuple[int, int]:
        """
        Return the page range represented by this chunk.

        Returns:
            Tuple containing (page_start, page_end).
        """
        return (self.page_start, self.page_end)