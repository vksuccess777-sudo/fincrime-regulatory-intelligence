from pathlib import Path

import pytest

from src.processing.exceptions import ParserError
from src.processing.pdf_parser import PDFParser


def test_parser_properties():

    parser = PDFParser()

    assert parser.parser_name == "PDFParser"
    assert parser.parser_version == "1.0"


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


def test_valid_pdf_returns_parser_result(tmp_path):

    parser = PDFParser()

    pdf = tmp_path / "sample.pdf"
    pdf.write_bytes(b"%PDF-1.4")

    result = parser.parse(
        "DOC001",
        pdf,
    )

    assert result.success is True
    assert result.page_count == 0
    assert result.document_id == "DOC001"
    assert result.local_path == pdf