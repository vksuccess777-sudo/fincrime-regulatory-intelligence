from pathlib import Path

from src.indexing.knowledge_build_result import KnowledgeBuildResult
from src.indexing.knowledge_indexer import KnowledgeIndexer


class MockProcessingResult:
    def __init__(self):
        self.sections = [
            object(),
            object(),
        ]


class MockProcessingPipeline:
    def process(
        self,
        document_id,
        file_path,
    ):
        return MockProcessingResult()


class MockChunkGenerator:
    def generate(
        self,
        processing_result,
    ):
        return [
            object(),
            object(),
            object(),
        ]


class MockIndexingPipeline:
    def __init__(self):
        self.received_chunks = None

    def index_chunks(
        self,
        chunks,
    ):
        self.received_chunks = chunks


def create_indexer():

    indexing_pipeline = MockIndexingPipeline()

    return (
        KnowledgeIndexer(
            processing_pipeline=MockProcessingPipeline(),
            chunk_generator=MockChunkGenerator(),
            indexing_pipeline=indexing_pipeline,
        ),
        indexing_pipeline,
    )


def test_returns_build_result():

    indexer, _ = create_indexer()

    result = indexer.index_document(
        document_id="doc-1",
        file_path=Path("dummy.pdf"),
    )

    assert isinstance(
        result,
        KnowledgeBuildResult,
    )


def test_documents_processed():

    indexer, _ = create_indexer()

    result = indexer.index_document(
        "doc-1",
        Path("dummy.pdf"),
    )

    assert result.documents_processed == 1


def test_sections_detected():

    indexer, _ = create_indexer()

    result = indexer.index_document(
        "doc-1",
        Path("dummy.pdf"),
    )

    assert result.sections_detected == 2


def test_chunks_generated():

    indexer, _ = create_indexer()

    result = indexer.index_document(
        "doc-1",
        Path("dummy.pdf"),
    )

    assert result.chunks_generated == 3


def test_embeddings_created():

    indexer, _ = create_indexer()

    result = indexer.index_document(
        "doc-1",
        Path("dummy.pdf"),
    )

    assert result.embeddings_created == 3


def test_vectors_stored():

    indexer, _ = create_indexer()

    result = indexer.index_document(
        "doc-1",
        Path("dummy.pdf"),
    )

    assert result.vectors_stored == 3


def test_successful():

    indexer, _ = create_indexer()

    result = indexer.index_document(
        "doc-1",
        Path("dummy.pdf"),
    )

    assert result.successful is True


def test_chunks_sent_to_indexing_pipeline():

    indexer, indexing_pipeline = create_indexer()

    indexer.index_document(
        "doc-1",
        Path("dummy.pdf"),
    )

    assert len(indexing_pipeline.received_chunks) == 3