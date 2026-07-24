from pathlib import Path

import pytest
from pypdf import PdfWriter

from src.processing.exceptions import (
    ParserError,
    UnsupportedDocumentTypeError,
)
from src.processing.processing_pipeline import ProcessingPipeline


def create_blank_pdf(path: Path, pages: int = 1) -> None:
    """
    Creates a valid blank PDF for testing.
    """
    writer = PdfWriter()

    for _ in range(pages):
        writer.add_blank_page(width=595, height=842)

    with path.open("wb") as file:
        writer.write(file)


def test_pipeline_processes_pdf(tmp_path):

    pipeline = ProcessingPipeline()

    pdf = tmp_path / "sample.pdf"

    create_blank_pdf(pdf)

    result = pipeline.process(
        "DOC001",
        pdf,
    )

    assert result.success is True
    assert result.page_count == 1
    assert len(result.extracted_pages) == 1


def test_metadata_preserved(tmp_path):

    pipeline = ProcessingPipeline()

    pdf = tmp_path / "sample.pdf"

    create_blank_pdf(pdf)

    result = pipeline.process(
        "DOC001",
        pdf,
    )

    assert result.document_id == "DOC001"
    assert result.parser_name == "PDFParser"
    assert result.parser_version == "2.0"


def test_page_count_preserved(tmp_path):

    pipeline = ProcessingPipeline()

    pdf = tmp_path / "multi.pdf"

    create_blank_pdf(pdf, pages=4)

    result = pipeline.process(
        "DOC001",
        pdf,
    )

    assert result.page_count == 4
    assert len(result.extracted_pages) == 4


def test_missing_file():

    pipeline = ProcessingPipeline()

    with pytest.raises(ParserError):
        pipeline.process(
            "DOC001",
            Path("missing.pdf"),
        )


def test_invalid_extension(tmp_path):

    pipeline = ProcessingPipeline()

    file = tmp_path / "document.docx"

    file.write_text("dummy")

    with pytest.raises(UnsupportedDocumentTypeError):
        pipeline.process(
            "DOC001",
            file,
        )


def test_empty_pages_preserved(tmp_path):

    pipeline = ProcessingPipeline()

    pdf = tmp_path / "blank.pdf"

    create_blank_pdf(pdf, pages=2)

    result = pipeline.process(
        "DOC001",
        pdf,
    )

    assert result.extracted_pages == ["", ""]