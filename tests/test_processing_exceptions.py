import pytest

from src.processing.exceptions import (
    ParserError,
    ProcessingError,
    UnsupportedDocumentTypeError,
)


def test_processing_error_is_exception():
    assert issubclass(ProcessingError, Exception)


def test_parser_error_inherits_processing_error():
    assert issubclass(ParserError, ProcessingError)


def test_unsupported_document_type_inherits_processing_error():
    assert issubclass(
        UnsupportedDocumentTypeError,
        ProcessingError,
    )


def test_processing_error_message():

    with pytest.raises(ProcessingError) as exc:
        raise ProcessingError("Processing failed.")

    assert str(exc.value) == "Processing failed."


def test_parser_error_message():

    with pytest.raises(ParserError) as exc:
        raise ParserError("Parser failed.")

    assert str(exc.value) == "Parser failed."


def test_unsupported_document_type_message():

    with pytest.raises(
        UnsupportedDocumentTypeError
    ) as exc:
        raise UnsupportedDocumentTypeError(
            "Unsupported document type."
        )

    assert (
        str(exc.value)
        == "Unsupported document type."
    )