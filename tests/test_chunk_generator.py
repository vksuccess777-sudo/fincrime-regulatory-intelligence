from pathlib import Path

from src.processing.chunk_generator import ChunkGenerator
from src.processing.document_section import DocumentSection
from src.processing.parser_result import ParserResult
from src.processing.processing_result import ProcessingResult


def make_parser_result() -> ParserResult:
    return ParserResult(
        document_id="fatf-test",
        local_path=Path("knowledge/fatf.pdf"),
        parser_name="PDFParser",
        parser_version="1.0",
        page_count=2,
        extracted_pages=[
            "Page 1",
            "Page 2",
        ],
    )


def make_processing_result(
    sections: list[DocumentSection],
) -> ProcessingResult:
    return ProcessingResult(
        parser_result=make_parser_result(),
        sections=sections,
    )


def make_section(
    title: str,
    content: str,
    start_page: int,
    end_page: int | None = None,
    level: int = 1,
) -> DocumentSection:
    if end_page is None:
        end_page = start_page

    return DocumentSection(
        title=title,
        content=content,
        start_page=start_page,
        end_page=end_page,
        level=level,
    )


def test_empty_processing_result():
    generator = ChunkGenerator()

    result = make_processing_result([])

    chunks = generator.generate(result)

    assert chunks == []


def test_single_section_generates_single_chunk():
    generator = ChunkGenerator()

    result = make_processing_result(
        [
            make_section(
                "Recommendation 10",
                "Enhanced Due Diligence is required.",
                4,
            )
        ]
    )

    chunks = generator.generate(result)

    assert len(chunks) == 1

    chunk = chunks[0]

    assert chunk.chunk_id == "fatf-test-1"
    assert chunk.section_title == "Recommendation 10"
    assert chunk.text == "Enhanced Due Diligence is required."
    assert chunk.page_start == 4
    assert chunk.page_end == 4


def test_multiple_sections_generate_multiple_chunks():
    generator = ChunkGenerator()

    result = make_processing_result(
        [
            make_section("One", "AAA", 1),
            make_section("Two", "BBB", 2),
            make_section("Three", "CCC", 3),
        ]
    )

    chunks = generator.generate(result)

    assert len(chunks) == 3


def test_chunk_ids_are_unique():
    generator = ChunkGenerator()

    result = make_processing_result(
        [
            make_section("One", "AAA", 1),
            make_section("Two", "BBB", 2),
        ]
    )

    chunks = generator.generate(result)

    ids = [chunk.chunk_id for chunk in chunks]

    assert len(ids) == len(set(ids))


def test_page_numbers_preserved():
    generator = ChunkGenerator()

    result = make_processing_result(
        [
            make_section(
                "Recommendation 10",
                "EDD",
                start_page=7,
                end_page=9,
            )
        ]
    )

    chunk = generator.generate(result)[0]

    assert chunk.page_start == 7
    assert chunk.page_end == 9


def test_section_titles_preserved():
    generator = ChunkGenerator()

    result = make_processing_result(
        [
            make_section("Recommendation 20", "SAR", 5),
            make_section("Recommendation 24", "Beneficial Ownership", 6),
        ]
    )

    chunks = generator.generate(result)

    titles = [chunk.section_title for chunk in chunks]

    assert titles == [
        "Recommendation 20",
        "Recommendation 24",
    ]


def test_metadata_preserved():
    generator = ChunkGenerator()

    result = make_processing_result(
        [
            make_section(
                "Recommendation 10",
                "EDD",
                4,
                level=2,
            )
        ]
    )

    chunk = generator.generate(result)[0]

    assert chunk.metadata["document_id"] == "fatf-test"
    assert chunk.metadata["level"] == 2