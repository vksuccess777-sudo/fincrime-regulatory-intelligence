"""
Parser Result Model

Represents the output produced by a document parser.

Sprint:
    Sprint 5 - D1 (Knowledge Processing Framework)

Author:
    Karthik Varadharajan Project

Architecture:
    Single Responsibility Principle (SRP)

Notes:
    - Represents parser output only.
    - Contains no parsing logic.
    - Generic enough to support PDF, DOCX, HTML, XML and future formats.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ParserResult:
    """
    Represents the result returned by a document parser.
    """

    document_id: str
    local_path: Path
    parser_name: str
    parser_version: str
    page_count: int
    extracted_pages: list[str] = field(default_factory=list)
    success: bool = True
    error_message: str | None = None

    def __post_init__(self) -> None:
        if not self.document_id:
            raise ValueError("document_id cannot be empty.")

        if not self.parser_name:
            raise ValueError("parser_name cannot be empty.")

        if not self.parser_version:
            raise ValueError("parser_version cannot be empty.")

        if self.page_count < 0:
            raise ValueError("page_count cannot be negative.")

        if self.page_count != len(self.extracted_pages):
            raise ValueError(
                "page_count must equal the number of extracted pages."
            )

        if not self.success and not self.error_message:
            raise ValueError(
                "error_message must be provided when success=False."
            )