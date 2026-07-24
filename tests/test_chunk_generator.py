import pytest

from src.processing.chunk_generator import ChunkGenerator
from src.processing.document_section import DocumentSection


def create_section(content: str, **kwargs):
    defaults = {
        "title": "Introduction",
        "content": content,
        "start_page": 1,
        "end_page": 1,
        "level": 1,
    }

    defaults.update(kwargs)

    return DocumentSection(**defaults)


def test_single_chunk_generation():
    generator = ChunkGenerator(chunk_size=100)

    chunks = generator.generate(
        [create_section("Hello World")]
    )

    assert len(chunks) == 1
    assert chunks[0].text == "Hello World"


def test_multiple_chunk_generation():
    generator = ChunkGenerator(
        chunk_size=10,
        overlap=0,
    )

    chunks = generator.generate(
        [create_section("A" * 35)]
    )

    assert len(chunks) == 4


def test_overlap_generation():
    generator = ChunkGenerator(
        chunk_size=10,
        overlap=2,
    )

    chunks = generator.generate(
        [create_section("A" * 25)]
    )

    assert len(chunks) > 2


def test_empty_section_skipped():
    generator = ChunkGenerator()

    chunks = generator.generate([])

    assert chunks == []


def test_chunk_ids_are_unique():
    generator = ChunkGenerator(
        chunk_size=10,
        overlap=0,
    )

    chunks = generator.generate(
        [create_section("A" * 50)]
    )

    ids = [c.chunk_id for c in chunks]

    assert len(ids) == len(set(ids))


def test_page_numbers_preserved():
    generator = ChunkGenerator(
        chunk_size=10,
        overlap=0,
    )

    chunks = generator.generate(
        [
            create_section(
                "A" * 30,
                start_page=4,
                end_page=6,
            )
        ]
    )

    for chunk in chunks:
        assert chunk.page_start == 4
        assert chunk.page_end == 6


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        ChunkGenerator(chunk_size=0)


def test_invalid_overlap():
    with pytest.raises(ValueError):
        ChunkGenerator(
            chunk_size=100,
            overlap=100,
        )


def test_negative_overlap():
    with pytest.raises(ValueError):
        ChunkGenerator(
            chunk_size=100,
            overlap=-1,
        )


def test_multiple_sections():
    generator = ChunkGenerator(
        chunk_size=20,
        overlap=0,
    )

    sections = [
        create_section("A" * 25, title="One"),
        create_section("B" * 25, title="Two"),
    ]

    chunks = generator.generate(sections)

    titles = {c.section_title for c in chunks}

    assert titles == {"One", "Two"}