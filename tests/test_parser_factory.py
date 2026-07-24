from pathlib import Path

import pytest

from src.processing.exceptions import UnsupportedDocumentTypeError
from src.processing.parser_factory import ParserFactory
from src.processing.pdf_parser import PDFParser


def test_returns_pdf_parser():

    parser = ParserFactory.get_parser(
        Path("document.pdf")
    )

    assert isinstance(parser, PDFParser)


def test_pdf_extension_case_insensitive():

    parser = ParserFactory.get_parser(
        Path("document.PDF")
    )

    assert isinstance(parser, PDFParser)


def test_unknown_extension_raises():

    with pytest.raises(
        UnsupportedDocumentTypeError
    ):
        ParserFactory.get_parser(
            Path("document.docx")
        )


def test_no_extension_raises():

    with pytest.raises(
        UnsupportedDocumentTypeError
    ):
        ParserFactory.get_parser(
            Path("document")
        )