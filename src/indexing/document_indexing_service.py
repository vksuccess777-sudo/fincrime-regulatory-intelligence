"""
Document Indexing Service

Sprint:
    Sprint 6 - D5

Coordinates the complete document indexing workflow.
"""

from __future__ import annotations

from pathlib import Path

from src.indexing.indexing_pipeline import IndexingPipeline
from src.processing.chunk_generator import ChunkGenerator
from src.processing.processing_pipeline import ProcessingPipeline


class DocumentIndexingService:
    """
    High-level orchestration for document indexing.
    """

    def __init__(
        self,
        processing_pipeline: ProcessingPipeline,
        chunk_generator: ChunkGenerator,
        indexing_pipeline: IndexingPipeline,
    ) -> None:
        self._processing_pipeline = processing_pipeline
        self._chunk_generator = chunk_generator
        self._indexing_pipeline = indexing_pipeline

    def index_document(
        self,
        document_id: str,
        file_path: Path,
    ) -> None:
        """
        Execute the complete indexing workflow.

        Parse
            ↓
        Clean
            ↓
        Detect Structure
            ↓
        Generate Chunks
            ↓
        Generate Embeddings
            ↓
        Store in Vector Database
        """

        processing_result = self._processing_pipeline.process(
            document_id=document_id,
            file_path=file_path,
        )

        chunks = self._chunk_generator.generate(
            processing_result,
        )

        self._indexing_pipeline.index_chunks(
            chunks,
        )