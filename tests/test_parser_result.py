from pathlib import Path

import pytest

from src.processing.parser_result import ParserResult


def test_create_parser_result_success():
    result = ParserResult(
        document_id="DOC001",
        local_path=Path("knowledge/test.pdf"),
        parser_name="PDFParser",
        parser_version="1.0",
        page_count=2,
        extracted_pages=[
            "Page One",
            "Page Two",
        ],
        success=True,
    )

    assert result.document_id == "DOC001"
    assert result.page_count == 2
    assert result.success is True
    assert len(result.extracted_pages) == 2


def test_empty_document_id_raises():
    with pytest.raises(ValueError):
        ParserResult(
            document_id="",
            local_path=Path("test.pdf"),
            parser_name="PDFParser",
            parser_version="1.0",
            page_count=0,
            extracted_pages=[],
        )


def test_negative_page_count_raises():
    with pytest.raises(ValueError):
        ParserResult(
            document_id="DOC001",
            local_path=Path("test.pdf"),
            parser_name="PDFParser",
            parser_version="1.0",
            page_count=-1,
            extracted_pages=[],
        )


def test_page_count_mismatch_raises():
    with pytest.raises(ValueError):
        ParserResult(
            document_id="DOC001",
            local_path=Path("test.pdf"),
            parser_name="PDFParser",
            parser_version="1.0",
            page_count=2,
            extracted_pages=["Only one page"],
        )


def test_failure_requires_error_message():
    with pytest.raises(ValueError):
        ParserResult(
            document_id="DOC001",
            local_path=Path("test.pdf"),
            parser_name="PDFParser",
            parser_version="1.0",
            page_count=0,
            extracted_pages=[],
            success=False,
        )


def test_failure_with_error_message():
    result = ParserResult(
        document_id="DOC001",
        local_path=Path("test.pdf"),
        parser_name="PDFParser",
        parser_version="1.0",
        page_count=0,
        extracted_pages=[],
        success=False,
        error_message="Unable to parse document.",
    )

    assert result.success is False
    assert result.error_message == "Unable to parse document."


def test_empty_document_is_valid():
    result = ParserResult(
        document_id="DOC001",
        local_path=Path("empty.pdf"),
        parser_name="PDFParser",
        parser_version="1.0",
        page_count=0,
        extracted_pages=[],
    )

    assert result.page_count == 0
    assert result.extracted_pages == []