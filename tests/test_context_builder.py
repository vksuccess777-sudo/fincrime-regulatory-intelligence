"""
Tests for ContextBuilder

Sprint:
    Sprint 7 - D2
"""

from src.embeddings.embedding_result import EmbeddingResult
from src.rag.context_builder import ContextBuilder


def make_result(
    text: str,
    source: str = "FATF",
    section: str = "Recommendation 10",
    page_start: int = 1,
    page_end: int = 1,
) -> EmbeddingResult:
    return EmbeddingResult(
        chunk_id="chunk-1",
        vector=[0.1, 0.2, 0.3],
        model_name="mock-model",
        dimension=3,
        metadata={
            "text": text,
            "source": source,
            "section_title": section,
            "page_start": page_start,
            "page_end": page_end,
        },
    )


def test_empty_results():
    builder = ContextBuilder()

    context = builder.build([])

    assert context == "No supporting context available."


def test_single_result():
    builder = ContextBuilder()

    context = builder.build(
        [
            make_result(
                "Enhanced Due Diligence is required."
            )
        ]
    )

    assert "Enhanced Due Diligence" in context
    assert "FATF" in context
    assert "Recommendation 10" in context


def test_multiple_results():
    builder = ContextBuilder()

    context = builder.build(
        [
            make_result(
                "AAA",
            ),
            make_result(
                "BBB",
                source="FCA",
                section="Customer Risk Assessment",
            ),
        ]
    )

    assert "AAA" in context
    assert "BBB" in context
    assert "FATF" in context
    assert "FCA" in context


def test_missing_metadata():
    builder = ContextBuilder()

    result = EmbeddingResult(
        chunk_id="chunk-1",
        vector=[0.1],
        model_name="mock-model",
        dimension=1,
        metadata={
            "text": "Example",
        },
    )

    context = builder.build([result])

    assert "Unknown" in context
    assert "Example" in context


def test_page_numbers():
    builder = ContextBuilder()

    context = builder.build(
        [
            make_result(
                "EDD",
                page_start=4,
                page_end=6,
            )
        ]
    )

    assert "4-6" in context


def test_separator_between_results():
    builder = ContextBuilder()

    context = builder.build(
        [
            make_result("AAA"),
            make_result("BBB"),
        ]
    )

    assert context.count("----------------------------------------") == 1


def test_section_title_preserved():
    builder = ContextBuilder()

    context = builder.build(
        [
            make_result(
                "SAR",
                section="Recommendation 20",
            )
        ]
    )

    assert "Recommendation 20" in context