"""
Parser Factory

Responsible for returning the correct parser implementation
for a supported document type.

Sprint:
    Sprint 5 - D1
"""

from pathlib import Path

from src.processing.base_parser import BaseParser
from src.processing.exceptions import UnsupportedDocumentTypeError
from src.processing.pdf_parser import PDFParser


class ParserFactory:
    """
    Factory for creating document parser instances.
    """

    @staticmethod
    def get_parser(file_path: Path) -> BaseParser:
        """
        Returns the appropriate parser based on the
        file extension.
        """

        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            return PDFParser()

        raise UnsupportedDocumentTypeError(
            f"No parser available for '{suffix}' files."
        )