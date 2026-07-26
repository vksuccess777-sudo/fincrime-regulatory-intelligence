"""
Knowledge Indexer

Sprint:
    Sprint 8 - D1

Coordinates processing a document and indexing the resulting
semantic chunks into the configured vector store.
"""

from __future__ import annotations

from pathlib import Path

from src.indexing.indexing_pipeline import IndexingPipeline
from src.indexing.knowledge_build_result import KnowledgeBuildResult
from src.processing.chunk_generator import ChunkGenerator
from src.processing.processing_pipeline import ProcessingPipeline


class KnowledgeIndexer:
    """
    End-to-end document indexing pipeline.
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
    ) -> KnowledgeBuildResult:
        """
        Process a document and index every semantic chunk.
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

        return KnowledgeBuildResult(
            documents_processed=1,
            sections_detected=len(processing_result.sections),
            chunks_generated=len(chunks),
            embeddings_created=len(chunks),
            vectors_stored=len(chunks),
            errors=[],
        )