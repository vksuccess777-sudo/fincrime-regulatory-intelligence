"""
FRI - Knowledge Catalogue Manager

Sprint 2
Deliverable D2
"""

from __future__ import annotations

from typing import Dict, List

from src.catalogue.exceptions import (
    DuplicateDocumentError,
    DuplicateSourceError,
    UnknownSourceError,
)
from src.models.document_metadata import DocumentMetadata
from src.models.source_definition import SourceDefinition


class CatalogueManager:
    """
    Central registry for regulatory knowledge.
    """

    def __init__(self) -> None:
        self._sources: Dict[str, SourceDefinition] = {}
        self._documents: Dict[str, DocumentMetadata] = {}

    # ---------------------------------------------------------
    # Source Management
    # ---------------------------------------------------------

    def register_source(self, source: SourceDefinition) -> None:

        if source.identifier in self._sources:
            raise DuplicateSourceError(
                f"Source '{source.identifier}' already exists."
            )

        self._sources[source.identifier] = source

    def get_source(self, identifier: str) -> SourceDefinition | None:
        return self._sources.get(identifier)

    def list_sources(self) -> List[SourceDefinition]:
        return list(self._sources.values())

    # ---------------------------------------------------------
    # Document Management
    # ---------------------------------------------------------

    def register_document(self, document: DocumentMetadata) -> None:

        if document.document_id in self._documents:
            raise DuplicateDocumentError(
                f"Document '{document.document_id}' already exists."
            )

        if document.source_identifier not in self._sources:
            raise UnknownSourceError(
                f"Unknown source '{document.source_identifier}'."
            )

        self._documents[document.document_id] = document

    def get_document(self, document_id: str) -> DocumentMetadata | None:
        return self._documents.get(document_id)

    def list_documents(self) -> List[DocumentMetadata]:
        return list(self._documents.values())

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @property
    def source_count(self) -> int:
        return len(self._sources)

    @property
    def document_count(self) -> int:
        return len(self._documents)