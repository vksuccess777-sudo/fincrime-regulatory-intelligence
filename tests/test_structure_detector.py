from src.processing.document_section import DocumentSection
from src.processing.structure_detector import StructureDetector


def test_empty_document():

    detector = StructureDetector()

    sections = detector.detect([])

    assert sections == []


def test_single_page():

    detector = StructureDetector()

    sections = detector.detect(
        [
            "Customer Due Diligence\nCDD requirements..."
        ]
    )

    assert len(sections) == 1
    assert isinstance(
        sections[0],
        DocumentSection,
    )
    assert sections[0].title == "Customer Due Diligence"
    assert sections[0].start_page == 1
    assert sections[0].end_page == 1


def test_multiple_pages():

    detector = StructureDetector()

    sections = detector.detect(
        [
            "Introduction\nWelcome",
            "Sanctions\nRules",
            "Monitoring\nDetails",
        ]
    )

    assert len(sections) == 3

    assert sections[0].title == "Introduction"
    assert sections[1].title == "Sanctions"
    assert sections[2].title == "Monitoring"


def test_blank_page():

    detector = StructureDetector()

    sections = detector.detect([""])

    assert sections[0].title == "Page 1"


def test_page_numbers():

    detector = StructureDetector()

    sections = detector.detect(
        [
            "A",
            "B",
            "C",
        ]
    )

    assert sections[0].start_page == 1
    assert sections[1].start_page == 2
    assert sections[2].start_page == 3


def test_content_preserved():

    detector = StructureDetector()

    text = (
        "Customer Due Diligence\n"
        "Financial institutions should..."
    )

    sections = detector.detect([text])

    assert sections[0].content == text