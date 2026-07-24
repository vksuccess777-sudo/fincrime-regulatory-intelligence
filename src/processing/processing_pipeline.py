"""
Processing Pipeline

Coordinates the document processing workflow.

Sprint:
    Sprint 5 - D4
"""

from dataclasses import replace
from pathlib import Path

from src.processing.parser_factory import ParserFactory
from src.processing.parser_result import ParserResult
from src.processing.structure_detector import StructureDetector
from src.processing.text_cleaner import TextCleaner


class ProcessingPipeline:
    """
    Coordinates the complete processing workflow.
    """

    def __init__(self) -> None:
        self._cleaner = TextCleaner()
        self._structure_detector = StructureDetector()

    def process(
        self,
        document_id: str,
        file_path: Path,
    ) -> ParserResult:
        """
        Processes a document.

        Workflow:
            Parse
            ↓
            Clean
            ↓
            Detect Structure
            ↓
            Return cleaned ParserResult
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

        # Structure detection
        #
        # The detected sections are intentionally not yet
        # returned. Sprint 5 D5 will consume them for
        # semantic chunk generation.
        _ = self._structure_detector.detect(cleaned_pages)

        return replace(
            raw_result,
            extracted_pages=cleaned_pages,
        )