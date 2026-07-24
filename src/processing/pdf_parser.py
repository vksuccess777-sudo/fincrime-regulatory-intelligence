"""
PDF Parser

Concrete implementation of the BaseParser for PDF documents.

Sprint:
    Sprint 5 - D2

Responsibilities:
    - Validate PDF input.
    - Extract text from each page.
    - Preserve page order.
    - Return ParserResult.

Notes:
    - Cleaning is performed in Sprint 5 D3.
    - Structure detection is performed in Sprint 5 D4.
    - Chunk generation is performed in Sprint 5 D5.
"""

from pathlib import Path

from pypdf import PdfReader

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
        return "2.0"

    def parse(
        self,
        document_id: str,
        file_path: Path,
    ) -> ParserResult:
        """
        Parses a PDF document and extracts text from each page.
        """

        if not file_path.exists():
            raise ParserError(
                f"Document does not exist: {file_path}"
            )

        if file_path.suffix.lower() != ".pdf":
            raise ParserError(
                f"Unsupported file type: {file_path.suffix}"
            )

        try:
            reader = PdfReader(file_path)

            extracted_pages: list[str] = []

            for page in reader.pages:
                text = page.extract_text()

                if text is None:
                    text = ""

                extracted_pages.append(text)

            return ParserResult(
                document_id=document_id,
                local_path=file_path,
                parser_name=self.parser_name,
                parser_version=self.parser_version,
                page_count=len(extracted_pages),
                extracted_pages=extracted_pages,
                success=True,
            )

        except Exception as exc:
            raise ParserError(
                f"Unable to parse PDF '{file_path}': {exc}"
            ) from exc