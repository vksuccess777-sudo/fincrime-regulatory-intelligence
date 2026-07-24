import pytest

from src.processing.document_section import DocumentSection


def test_document_section_creation():

    section = DocumentSection(
        title="Customer Due Diligence",
        content="CDD requirements...",
        start_page=10,
        end_page=12,
        level=2,
    )

    assert section.title == "Customer Due Diligence"
    assert section.content == "CDD requirements..."
    assert section.start_page == 10
    assert section.end_page == 12
    assert section.level == 2


def test_default_level():

    section = DocumentSection(
        title="Introduction",
        content="Welcome",
        start_page=1,
        end_page=2,
    )

    assert section.level == 1


def test_immutable():

    section = DocumentSection(
        title="Test",
        content="Example",
        start_page=1,
        end_page=1,
    )

    with pytest.raises(AttributeError):
        section.title = "Changed"


def test_equality():

    a = DocumentSection(
        title="A",
        content="Text",
        start_page=1,
        end_page=2,
    )

    b = DocumentSection(
        title="A",
        content="Text",
        start_page=1,
        end_page=2,
    )

    assert a == b


def test_repr_contains_title():

    section = DocumentSection(
        title="Sanctions",
        content="Sanctions guidance",
        start_page=5,
        end_page=6,
    )

    assert "Sanctions" in repr(section)