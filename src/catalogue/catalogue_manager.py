"""
FRI - Knowledge Catalogue Manager

Sprint 2
Deliverable D5 (original — Catalogue Manager)

Updated: Sprint 4 D5 (Catalogue Integration) — added
update_after_download(), which is the final step of the automated
acquisition pipeline: Download -> Storage -> SHA256 -> Catalogue Update.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Dict, List

from src.catalogue.catalogue_store import CatalogueStore
from src.catalogue.exceptions import (
    DocumentNotFoundError,
    DuplicateDocumentError,
    DuplicateSourceError,
    UnknownSourceError,
)
from src.integrity.integrity_record import IntegrityRecord
from src.models.document_metadata import DocumentMetadata
from src.models.source_definition import SourceDefinition
from src.storage.storage_result import StorageResult


class CatalogueManager:
    """
    Central registry for regulatory knowledge.
    """

    def __init__(self, store: CatalogueStore | None = None) -> None:

        self._store = store

        self._sources: Dict[str, SourceDefinition] = {}
        self._documents: Dict[str, DocumentMetadata] = {}

        if self._store is not None:
            sources, documents = self._store.load()

            self._sources = {
                source.identifier: source
                for source in sources
            }

            self._documents = {
                document.document_id: document
                for document in documents
            }

    # ---------------------------------------------------------
    # Source Management
    # ---------------------------------------------------------

    def register_source(self, source: SourceDefinition) -> None:

        if source.identifier in self._sources:
            raise DuplicateSourceError(
                f"Source '{source.identifier}' already exists."
            )

        self._sources[source.identifier] = source

        self._save()

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

        self._save()

    def get_document(self, document_id: str) -> DocumentMetadata | None:
        return self._documents.get(document_id)

    def list_documents(self) -> List[DocumentMetadata]:
        return list(self._documents.values())

    # ---------------------------------------------------------
    # Post-Download Update (Sprint 4 D5)
    # ---------------------------------------------------------

    def update_after_download(
        self,
        document_id: str,
        storage_result: StorageResult,
        integrity_record: IntegrityRecord,
        processing_status: str = "DOWNLOADED",
    ) -> DocumentMetadata:
        """
        Update a catalogued document after a successful
        download -> storage -> integrity verification cycle.

        This is the final step of the Sprint 4 acquisition pipeline:
            Download -> Storage -> SHA256 -> Catalogue Update

        Raises:
            DocumentNotFoundError: if document_id is not already
                registered in the catalogue. A document must exist
                (via register_document, from discovery/acquisition)
                before it can be updated post-download — this is not
                an implicit-create path.
        """

        document = self._documents.get(document_id)

        if document is None:
            raise DocumentNotFoundError(
                f"Cannot update document '{document_id}': not found "
                f"in catalogue. It must be registered before download."
            )

        now = datetime.now(UTC).isoformat()

        document.file_name = storage_result.file_name
        document.file_type = (
            storage_result.file_path.suffix.lstrip(".") or None
        )
        document.local_path = str(storage_result.file_path)
        document.file_size = storage_result.file_size
        document.sha256_hash = integrity_record.file_hash
        document.processing_status = processing_status
        document.last_downloaded = now
        document.last_updated = now

        self._save()

        return document

    # ---------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------

    def _save(self) -> None:

        if self._store is None:
            return

        self._store.save(
            self.list_sources(),
            self.list_documents(),
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @property
    def source_count(self) -> int:
        return len(self._sources)

    @property
    def document_count(self) -> int:
        return len(self._documents)