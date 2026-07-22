"""
FRI - Catalogue Exceptions

Sprint 2
Deliverable D2
"""


class CatalogueError(Exception):
    """Base class for catalogue exceptions."""


class DuplicateSourceError(CatalogueError):
    """Raised when a source already exists."""


class DuplicateDocumentError(CatalogueError):
    """Raised when a document already exists."""


class UnknownSourceError(CatalogueError):
    """Raised when a referenced source does not exist."""