"""
Integration tests for DocumentIndexingService.

Sprint:
    Sprint 6 - D5
"""

from pathlib import Path

from src.embeddings.mock_embedding_provider import MockEmbeddingProvider
from src.indexing.document_indexing_service import DocumentIndexingService
from src.indexing.indexing_pipeline import IndexingPipeline
from src.processing.chunk_generator import ChunkGenerator
from src.processing.processing_pipeline import ProcessingPipeline
from src.vectorstore.mock_vector_store import MockVectorStore


def test_document_indexing_service_creation():
    service = DocumentIndexingService(
        processing_pipeline=ProcessingPipeline(),
        chunk_generator=ChunkGenerator(),
        indexing_pipeline=IndexingPipeline(
            embedding_provider=MockEmbeddingProvider(),
            vector_store=MockVectorStore(),
        ),
    )

    assert service is not None


def test_index_document_method_exists():
    service = DocumentIndexingService(
        processing_pipeline=ProcessingPipeline(),
        chunk_generator=ChunkGenerator(),
        indexing_pipeline=IndexingPipeline(
            embedding_provider=MockEmbeddingProvider(),
            vector_store=MockVectorStore(),
        ),
    )

    assert hasattr(service, "index_document")


def test_index_document_signature():
    service = DocumentIndexingService(
        processing_pipeline=ProcessingPipeline(),
        chunk_generator=ChunkGenerator(),
        indexing_pipeline=IndexingPipeline(
            embedding_provider=MockEmbeddingProvider(),
            vector_store=MockVectorStore(),
        ),
    )

    assert callable(service.index_document)