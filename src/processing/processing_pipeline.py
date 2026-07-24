"""
Processing Pipeline

Coordinates the document processing workflow.

Sprint:
    Sprint 5 - D5
"""

from dataclasses import replace
from pathlib import Path

from src.processing.chunk_generator import ChunkGenerator
from src.processing.parser_factory import ParserFactory
from src.processing.parser_result import ParserResult
from src.processing.structure_detector import StructureDetector
from src.processing.text_cleaner import TextCleaner


class ProcessingPipeline:
    """
    Coordinates the complete document processing workflow.

    Workflow

        Parse
          ↓
        Clean
          ↓
        Detect Structure
          ↓
        Generate Semantic Chunks
          ↓
        Return cleaned ParserResult
    """

    def __init__(self) -> None:
        self._cleaner = TextCleaner()
        self._structure_detector = StructureDetector()
        self._chunk_generator = ChunkGenerator()

    def process(
        self,
        document_id: str,
        file_path: Path,
    ) -> ParserResult:
        """
        Process a document through the complete pipeline.
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

        sections = self._structure_detector.detect(
            cleaned_pages
        )

        #
        # Generate semantic chunks.
        #
        # Sprint 5 stores the generated chunks only within the
        # pipeline execution. Sprint 6 will persist these chunks
        # into the embedding/vector database.
        #
        _chunks = self._chunk_generator.generate(
            sections
        )

        return replace(
            raw_result,
            extracted_pages=cleaned_pages,
        )