"""
Processing Pipeline

Coordinates the document processing workflow.

Sprint:
    Sprint 5 - D3

Responsibilities
----------------
- Select the correct parser.
- Parse the document.
- Clean extracted text.
- Return a cleaned ParserResult.

Notes
-----
This class orchestrates processing only.

It intentionally performs NO:

- PDF parsing
- Text cleaning
- Structure detection
- Chunk generation

Those responsibilities belong to dedicated classes.
"""

from pathlib import Path
from dataclasses import replace

from src.processing.parser_factory import ParserFactory
from src.processing.parser_result import ParserResult
from src.processing.text_cleaner import TextCleaner


class ProcessingPipeline:
    """
    Coordinates the complete processing workflow.
    """

    def __init__(self) -> None:
        self._cleaner = TextCleaner()

    def process(
        self,
        document_id: str,
        file_path: Path,
    ) -> ParserResult:
        """
        Processes a document and returns a cleaned ParserResult.
        """

        parser = ParserFactory.get_parser(file_path)

        raw_result = parser.parse(
            document_id=document_id,
            file_path=file_path,
        )

        cleaned_pages = [
            self._cleaner.clean(page)
            for page in raw_result.extracted_pages
        ]

        return replace(
            raw_result,
            extracted_pages=cleaned_pages,
        )