"""
Processing Exceptions

Defines the exception hierarchy for the document
processing package.

Sprint:
    Sprint 5 - D1

Architecture:
    Single Responsibility Principle (SRP)
"""


class ProcessingError(Exception):
    """
    Base exception for all processing-related errors.
    """

    pass


class ParserError(ProcessingError):
    """
    Raised when a parser cannot process a document.
    """

    pass


class UnsupportedDocumentTypeError(ProcessingError):
    """
    Raised when no parser exists for the requested
    document type.
    """

    pass