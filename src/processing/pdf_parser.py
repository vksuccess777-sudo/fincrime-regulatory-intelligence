"""
PDF Parser

Concrete implementation of the BaseParser for PDF documents.

Sprint:
    Sprint 5 - D1

Notes:
    - D1 validates input only.
    - Actual PDF text extraction is implemented in Sprint 5 D2.
"""

from pathlib import Path

from src.processing.base_parser import BaseParser
from src.processing.exceptions import ParserError
from src.processing.parser_result import ParserResult


class PDFParser(BaseParser):
    """
    Parser implementation for PDF documents.
    """

    @property
    def parser_name(self) -> str:
        return "PDFParser"

    @property
    def parser_version(self) -> str:
        return "1.0"

    def parse(
        self,
        document_id: str,
        file_path: Path,
    ) -> ParserResult:

        if not file_path.exists():
            raise ParserError(
                f"Document does not exist: {file_path}"
            )

        if file_path.suffix.lower() != ".pdf":
            raise ParserError(
                f"Unsupported file type: {file_path.suffix}"
            )

        return ParserResult(
            document_id=document_id,
            local_path=file_path,
            parser_name=self.parser_name,
            parser_version=self.parser_version,
            page_count=0,
            extracted_pages=[],
            success=True,
        )