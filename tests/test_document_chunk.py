from dataclasses import FrozenInstanceError

import pytest

from src.processing.document_chunk import DocumentChunk


def create_chunk(**kwargs):
    defaults = {
        "chunk_id": "chunk-001",
        "text": "This is a sample chunk.",
        "page_start": 1,
        "page_end": 1,
        "section_title": "Introduction",
        "metadata": {
            "source_id": "fatf-rec-01",
            "jurisdiction": "Global",
            "regulation": "FATF Recommendations",
        },
    }

    defaults.update(kwargs)
    return DocumentChunk(**defaults)


def test_document_chunk_creation():
    chunk = create_chunk()

    assert chunk.chunk_id == "chunk-001"
    assert chunk.text == "This is a sample chunk."
    assert chunk.page_start == 1
    assert chunk.page_end == 1
    assert chunk.section_title == "Introduction"
    assert chunk.metadata["source_id"] == "fatf-rec-01"


def test_document_chunk_is_frozen():
    chunk = create_chunk()

    with pytest.raises(FrozenInstanceError):
        chunk.text = "Modified"


def test_document_chunk_equality():
    chunk1 = create_chunk()
    chunk2 = create_chunk()

    assert chunk1 == chunk2


def test_document_chunk_inequality():
    chunk1 = create_chunk()
    chunk2 = create_chunk(chunk_id="chunk-002")

    assert chunk1 != chunk2


def test_document_chunk_multi_page():
    chunk = create_chunk(page_start=4, page_end=7)

    assert chunk.page_start == 4
    assert chunk.page_end == 7
    assert chunk.page_range == (4, 7)


def test_document_chunk_long_text():
    text = "AML " * 1000

    chunk = create_chunk(text=text)

    assert chunk.text == text


def test_document_chunk_metadata():
    metadata = {
        "source_id": "uk-mlr",
        "jurisdiction": "United Kingdom",
        "regulation": "Money Laundering Regulations",
    }

    chunk = create_chunk(metadata=metadata)

    assert chunk.metadata == metadata


def test_document_chunk_page_range():
    chunk = create_chunk(page_start=2, page_end=5)

    assert chunk.page_range == (2, 5)