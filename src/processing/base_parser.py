"""
Base Parser

Defines the abstract interface that every document parser
must implement.

Sprint:
    Sprint 5 - D1 (Knowledge Processing Framework)

Architecture:
    Single Responsibility Principle (SRP)

Notes:
    - This class contains no parsing logic.
    - Concrete parsers (PDF, DOCX, HTML, etc.) inherit from this class.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from src.processing.parser_result import ParserResult


class BaseParser(ABC):
    """
    Abstract base class for all document parsers.
    """

    @property
    @abstractmethod
    def parser_name(self) -> str:
        """
        Returns the parser name.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def parser_version(self) -> str:
        """
        Returns the parser version.
        """
        raise NotImplementedError

    @abstractmethod
    def parse(
        self,
        document_id: str,
        file_path: Path,
    ) -> ParserResult:
        """
        Parses a document and returns a ParserResult.
        """
        raise NotImplementedError