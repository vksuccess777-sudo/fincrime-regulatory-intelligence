"""
Document Section

Represents a logical section detected within a processed document.

Sprint:
    Sprint 5 - D4

Responsibilities
----------------
- Store section metadata.
- Store section content.
- Preserve page boundaries.
- Remain immutable.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DocumentSection:
    """
    Represents one logical document section.
    """

    title: str
    content: str

    start_page: int
    end_page: int

    level: int = 1