"""
Processing Pipeline

Coordinates the document processing workflow.

Sprint:
    Sprint 6 - D5
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from src.processing.parser_factory import ParserFactory
from src.processing.processing_result import ProcessingResult
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
    ) -> ProcessingResult:
        """
        Process a document.

        Workflow

        Parse
            ↓
        Clean
            ↓
        Detect Structure
            ↓
        Return ProcessingResult
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

        cleaned_result = replace(
            raw_result,
            extracted_pages=cleaned_pages,
        )

        sections = self._structure_detector.detect(
            cleaned_pages,
        )

        return ProcessingResult(
            parser_result=cleaned_result,
            sections=sections,
        )