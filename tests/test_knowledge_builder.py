from pathlib import Path

from src.indexing.knowledge_build_result import KnowledgeBuildResult
from src.indexing.knowledge_builder import KnowledgeBuilder


class MockKnowledgeIndexer:
    """
    Mock KnowledgeIndexer used for testing.
    """

    def __init__(self):
        self.documents = []

    def index_document(
        self,
        document_id: str,
        file_path: Path,
    ) -> KnowledgeBuildResult:

        self.documents.append(
            (
                document_id,
                file_path,
            )
        )

        return KnowledgeBuildResult(
            documents_processed=1,
            sections_detected=5,
            chunks_generated=20,
            embeddings_created=20,
            vectors_stored=20,
            errors=[],
        )


def test_empty_folder(tmp_path):

    builder = KnowledgeBuilder(
        MockKnowledgeIndexer(),
    )

    result = builder.build(
        tmp_path,
    )

    assert result.documents_processed == 0
    assert result.sections_detected == 0
    assert result.chunks_generated == 0
    assert result.embeddings_created == 0
    assert result.vectors_stored == 0
    assert result.errors == []


def test_single_pdf(tmp_path):

    pdf = tmp_path / "fatf.pdf"
    pdf.write_bytes(b"dummy")

    builder = KnowledgeBuilder(
        MockKnowledgeIndexer(),
    )

    result = builder.build(
        tmp_path,
    )

    assert result.documents_processed == 1
    assert result.sections_detected == 5
    assert result.chunks_generated == 20
    assert result.embeddings_created == 20
    assert result.vectors_stored == 20


def test_multiple_pdfs(tmp_path):

    for i in range(3):
        (tmp_path / f"doc{i}.pdf").write_bytes(
            b"dummy"
        )

    builder = KnowledgeBuilder(
        MockKnowledgeIndexer(),
    )

    result = builder.build(
        tmp_path,
    )

    assert result.documents_processed == 3
    assert result.sections_detected == 15
    assert result.chunks_generated == 60
    assert result.embeddings_created == 60
    assert result.vectors_stored == 60


def test_non_pdf_files_ignored(tmp_path):

    (tmp_path / "notes.txt").write_text(
        "ignore"
    )

    (tmp_path / "fatf.pdf").write_bytes(
        b"dummy"
    )

    builder = KnowledgeBuilder(
        MockKnowledgeIndexer(),
    )

    result = builder.build(
        tmp_path,
    )

    assert result.documents_processed == 1


def test_nested_directories(tmp_path):

    nested = tmp_path / "fatf"
    nested.mkdir()

    (nested / "recommendation10.pdf").write_bytes(
        b"dummy"
    )

    builder = KnowledgeBuilder(
        MockKnowledgeIndexer(),
    )

    result = builder.build(
        tmp_path,
    )

    assert result.documents_processed == 1


def test_errors_are_recorded(tmp_path):

    class FailingIndexer:

        def index_document(
            self,
            document_id,
            file_path,
        ):
            raise RuntimeError(
                "Index failed"
            )

    (tmp_path / "bad.pdf").write_bytes(
        b"dummy"
    )

    builder = KnowledgeBuilder(
        FailingIndexer(),
    )

    result = builder.build(
        tmp_path,
    )

    assert result.documents_processed == 0
    assert len(result.errors) == 1
    assert "Index failed" in result.errors[0]