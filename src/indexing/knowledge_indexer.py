"""
Knowledge Indexer

Sprint:
    Sprint 6 - D5

Coordinates processing a document and indexing the resulting
semantic chunks into the configured vector store.
"""

from __future__ import annotations

from pathlib import Path

from src.indexing.indexing_pipeline import IndexingPipeline
from src.processing.processing_pipeline import ProcessingPipeline
from src.processing.semantic_chunker import SemanticChunker


class KnowledgeIndexer:
    """
    End-to-end document indexing pipeline.
    """

    def __init__(
        self,
        processing_pipeline: ProcessingPipeline,
        chunker: SemanticChunker,
        indexing_pipeline: IndexingPipeline,
    ) -> None:
        self._processing_pipeline = processing_pipeline
        self._chunker = chunker
        self._indexing_pipeline = indexing_pipeline

    def index_document(
        self,
        document_id: str,
        file_path: Path,
    ) -> None:
        """
        Process a document and index every semantic chunk.
        """

        parser_result = self._processing_pipeline.process(
            document_id=document_id,
            file_path=file_path,
        )

        chunks = self._chunker.chunk(parser_result)

        self._indexing_pipeline.index_chunks(chunks)