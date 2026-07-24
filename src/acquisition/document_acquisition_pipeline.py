"""
document_acquisition_pipeline.py

Sprint 4 D5 (Catalogue Integration)

Orchestrates the full post-discovery acquisition pipeline for a single
document: Download -> Storage -> SHA256 -> Catalogue Update.

This is the missing link described in Section 7 of the FRI status
report — the standalone, individually-tested D1-D4 components
(DownloadEngine, StorageManager, IntegrityVerifier) were never
previously chained together or connected to the catalogue.

Responsibilities:
    - Download document content via DownloadEngine
    - Persist it via StorageManager
    - Compute its integrity hash via IntegrityVerifier
    - Update the catalogue record via CatalogueManager

DocumentAcquisitionPipeline does NOT:
    - Discover documents (AcquisitionService's job)
    - Perform HTTP requests directly (HTTPDownloader's job)
    - Write bytes to disk directly (StorageManager's job)
    - Calculate hashes directly (HashCalculator's job)
    - Decide catalogue business rules (CatalogueManager's job)

It only sequences these existing, already-tested components — each
of which retains sole responsibility for its own concern.
"""

from __future__ import annotations

from pathlib import PurePosixPath
from urllib.parse import urlparse

from src.catalogue.catalogue_manager import CatalogueManager
from src.download.download_engine import DownloadEngine
from src.integrity.integrity_verifier import IntegrityVerifier
from src.models.document_metadata import DocumentMetadata
from src.storage.storage_manager import StorageManager

_DEFAULT_EXTENSION = "bin"


class DocumentAcquisitionPipeline:
    """
    Sequences Download -> Storage -> Integrity -> Catalogue Update
    for a single already-catalogued document.
    """

    def __init__(
        self,
        download_engine: DownloadEngine,
        storage_manager: StorageManager,
        integrity_verifier: IntegrityVerifier,
        catalogue_manager: CatalogueManager,
    ) -> None:
        self._download_engine = download_engine
        self._storage_manager = storage_manager
        self._integrity_verifier = integrity_verifier
        self._catalogue_manager = catalogue_manager

    def process(self, document: DocumentMetadata) -> DocumentMetadata:
        """
        Run the full acquisition pipeline for a document that has
        already been registered in the catalogue (via
        AcquisitionService / discovery).

        Args:
            document: Catalogued document to download, store, verify,
                and update.

        Returns:
            The updated DocumentMetadata, as returned by
            CatalogueManager.update_after_download().

        Raises:
            DownloadError (and subclasses): the download failed.
            StorageError (and subclasses): the write to disk failed.
            HashCalculationError: hash computation failed.
            DocumentNotFoundError: document_id is not registered in
                the catalogue. Should not occur in the normal flow
                since AcquisitionService registers documents before
                this pipeline runs on them.
        """

        download_result = self._download_engine.download(document)

        filename = self._build_filename(document)

        storage_result = self._storage_manager.save(
            content=download_result.content,
            filename=filename,
            overwrite=True,
        )

        integrity_record = self._integrity_verifier.compute_bytes(
            download_result.content
        )

        return self._catalogue_manager.update_after_download(
            document_id=document.document_id,
            storage_result=storage_result,
            integrity_record=integrity_record,
        )

    @staticmethod
    def _build_filename(document: DocumentMetadata) -> str:
        """
        Derive a deterministic, filesystem-safe filename for the
        document using StorageManager.generate_filename(), keyed on
        document_id so repeated downloads of the same document
        overwrite the same file rather than accumulating duplicates.

        Extension is taken from the publication_url's path; falls
        back to 'bin' when the URL has no discernible extension
        (e.g. a query-string-driven download endpoint).
        """

        url_path = PurePosixPath(urlparse(document.publication_url).path)
        extension = url_path.suffix.lstrip(".") or _DEFAULT_EXTENSION

        return StorageManager.generate_filename(
            identifier=document.document_id,
            extension=extension,
        )