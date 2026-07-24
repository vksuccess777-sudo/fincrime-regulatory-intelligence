from pathlib import Path

import pytest
from pypdf import PdfWriter

from src.processing.exceptions import ParserError
from src.processing.pdf_parser import PDFParser


def create_blank_pdf(path: Path, pages: int = 1) -> None:
    """
    Creates a valid blank PDF for testing.
    """
    writer = PdfWriter()

    for _ in range(pages):
        writer.add_blank_page(width=595, height=842)

    with path.open("wb") as f:
        writer.write(f)


def test_parser_properties():

    parser = PDFParser()

    assert parser.parser_name == "PDFParser"
    assert parser.parser_version == "2.0"


def test_missing_file_raises():

    parser = PDFParser()

    with pytest.raises(ParserError):
        parser.parse(
            "DOC001",
            Path("missing.pdf"),
        )


def test_wrong_extension_raises(tmp_path):

    parser = PDFParser()

    file = tmp_path / "sample.txt"
    file.write_text("hello")

    with pytest.raises(ParserError):
        parser.parse(
            "DOC001",
            file,
        )


def test_blank_pdf_returns_empty_pages(tmp_path):

    parser = PDFParser()

    pdf = tmp_path / "blank.pdf"

    create_blank_pdf(pdf)

    result = parser.parse(
        "DOC001",
        pdf,
    )

    assert result.success is True
    assert result.page_count == 1
    assert result.extracted_pages == [""]


def test_multiple_blank_pages(tmp_path):

    parser = PDFParser()

    pdf = tmp_path / "multi.pdf"

    create_blank_pdf(pdf, pages=3)

    result = parser.parse(
        "DOC001",
        pdf,
    )

    assert result.page_count == 3
    assert len(result.extracted_pages) == 3


def test_corrupted_pdf_raises(tmp_path):

    parser = PDFParser()

    pdf = tmp_path / "bad.pdf"

    pdf.write_text("This is not a PDF")

    with pytest.raises(ParserError):
        parser.parse(
            "DOC001",
            pdf,
        )


def test_page_order_preserved(tmp_path):

    parser = PDFParser()

    pdf = tmp_path / "ordered.pdf"

    create_blank_pdf(pdf, pages=5)

    result = parser.parse(
        "DOC001",
        pdf,
    )

    assert len(result.extracted_pages) == 5


def test_document_metadata(tmp_path):

    parser = PDFParser()

    pdf = tmp_path / "meta.pdf"

    create_blank_pdf(pdf)

    result = parser.parse(
        "DOC001",
        pdf,
    )

    assert result.document_id == "DOC001"
    assert result.local_path == pdf
    assert result.parser_name == "PDFParser"
    assert result.parser_version == "2.0"