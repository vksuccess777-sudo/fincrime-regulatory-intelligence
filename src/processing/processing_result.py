"""
Processing Result

Sprint:
    Sprint 6 - D5

Represents the output of the processing pipeline while maintaining
backward compatibility with the Sprint 5 API.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.processing.document_section import DocumentSection
from src.processing.parser_result import ParserResult


@dataclass(slots=True)
class ProcessingResult:
    """
    Complete processing result.

    New API:
        parser_result
        sections

    Backward-compatible API:
        success
        document_id
        parser_name
        parser_version
        page_count
        extracted_pages
    """

    parser_result: ParserResult
    sections: list[DocumentSection]

    @property
    def success(self) -> bool:
        return self.parser_result.success

    @property
    def document_id(self) -> str:
        return self.parser_result.document_id

    @property
    def parser_name(self) -> str:
        return self.parser_result.parser_name

    @property
    def parser_version(self) -> str:
        return self.parser_result.parser_version

    @property
    def page_count(self) -> int:
        return self.parser_result.page_count

    @property
    def extracted_pages(self) -> list[str]:
        return self.parser_result.extracted_pages