"""
Structure Detector

Detects logical document sections from cleaned text.

Sprint:
    Sprint 5 - D4
"""

from src.processing.document_section import DocumentSection


class StructureDetector:
    """
    Detects document sections using simple rule-based logic.

    Current implementation:
    - One DocumentSection per page.

    Future versions will detect:
    - Numbered headings
    - Multi-level sections
    - Tables
    - Appendices
    """

    def detect(
        self,
        pages: list[str],
    ) -> list[DocumentSection]:

        sections: list[DocumentSection] = []

        for page_number, page_text in enumerate(
            pages,
            start=1,
        ):

            text = page_text.strip()

            if not text:
                title = f"Page {page_number}"
            else:
                first_line = text.splitlines()[0].strip()
                title = first_line if first_line else f"Page {page_number}"

            sections.append(
                DocumentSection(
                    title=title,
                    content=page_text,
                    start_page=page_number,
                    end_page=page_number,
                    level=1,
                )
            )

        return sections