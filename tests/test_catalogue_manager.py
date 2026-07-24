"""
FRI - Catalogue Manager Tests

Sprint 2
Deliverable D3

Updated: Sprint 4 D5 (Catalogue Integration) — added
TestUpdateAfterDownload covering CatalogueManager.update_after_download().
"""

import unittest
from pathlib import Path

from src.catalogue.catalogue_manager import CatalogueManager
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


class TestCatalogueManager(unittest.TestCase):

    def setUp(self):

        self.manager = CatalogueManager()

        self.source = SourceDefinition(
            identifier="fatf",
            name="Financial Action Task Force",
            jurisdiction="Global",
            base_url="https://www.fatf-gafi.org",
            publication_urls=[
                "https://www.fatf-gafi.org/en/publications.html"
            ],
            supported_file_types=[
                "pdf",
                "html",
            ],
            connector_class="FATFConnector",
            sync_schedule="daily",
        )

        self.document = DocumentMetadata(
            document_id="DOC-001",
            source_identifier="fatf",
            title="Guidance on Beneficial Ownership",
            authority="Financial Action Task Force",
            jurisdiction="Global",
            publication_url="https://www.fatf-gafi.org/en/publications.html",
        )

    # ---------------------------------------------------------
    # Source Tests
    # ---------------------------------------------------------

    def test_register_source(self):

        self.manager.register_source(self.source)

        self.assertEqual(
            self.manager.source_count,
            1,
        )

    def test_duplicate_source(self):

        self.manager.register_source(self.source)

        with self.assertRaises(DuplicateSourceError):
            self.manager.register_source(self.source)

    def test_get_source(self):

        self.manager.register_source(self.source)

        result = self.manager.get_source("fatf")

        self.assertEqual(
            result,
            self.source,
        )

    def test_list_sources(self):

        self.manager.register_source(self.source)

        self.assertEqual(
            len(self.manager.list_sources()),
            1,
        )

    # ---------------------------------------------------------
    # Document Tests
    # ---------------------------------------------------------

    def test_register_document(self):

        self.manager.register_source(self.source)

        self.manager.register_document(self.document)

        self.assertEqual(
            self.manager.document_count,
            1,
        )

    def test_duplicate_document(self):

        self.manager.register_source(self.source)

        self.manager.register_document(self.document)

        with self.assertRaises(DuplicateDocumentError):
            self.manager.register_document(self.document)

    def test_unknown_source(self):

        bad_document = DocumentMetadata(
            document_id="DOC-999",
            source_identifier="unknown",
            title="Unknown Source",
            authority="Unknown",
            jurisdiction="Global",
            publication_url="https://example.com",
        )

        with self.assertRaises(UnknownSourceError):
            self.manager.register_document(bad_document)

    def test_get_document(self):

        self.manager.register_source(self.source)

        self.manager.register_document(self.document)

        result = self.manager.get_document("DOC-001")

        self.assertEqual(
            result,
            self.document,
        )

    def test_list_documents(self):

        self.manager.register_source(self.source)

        self.manager.register_document(self.document)

        self.assertEqual(
            len(self.manager.list_documents()),
            1,
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def test_initial_counts(self):
        # RECONSTRUCTED — verify against your original file/git history.
        # The paste of this method was corrupted/truncated; this is the
        # obvious intended content given the method name and section.

        self.assertEqual(
            self.manager.source_count,
            0,
        )

        self.assertEqual(
            self.manager.document_count,
            0,
        )


class TestUpdateAfterDownload(unittest.TestCase):

    def setUp(self) -> None:
        self.manager = CatalogueManager()  # no store -> in-memory only

        self.source = SourceDefinition(
            identifier="fatf",
            name="Financial Action Task Force",
            jurisdiction="International",
            base_url="https://www.fatf-gafi.org",
            publication_urls=["https://www.fatf-gafi.org/publications"],
            supported_file_types=["pdf"],
            connector_class="src.connectors.fatf_connector.FATFConnector",
            sync_schedule="daily",
        )
        self.manager.register_source(self.source)

        self.document = DocumentMetadata(
            document_id="fatf-2026-001",
            source_identifier="fatf",
            title="FATF Guidance on Virtual Assets",
            authority="FATF",
            jurisdiction="International",
            publication_url="https://www.fatf-gafi.org/doc.pdf",
        )
        self.manager.register_document(self.document)

        self.storage_result = StorageResult(
            file_path=Path("/data/fatf/fatf-2026-001.pdf"),
            file_size=204800,
            created=True,
        )
        self.integrity_record = IntegrityRecord(
            file_hash="a" * 64,
            algorithm="SHA256",
            byte_count=204800,
        )

    def test_updates_all_expected_fields(self) -> None:
        updated = self.manager.update_after_download(
            document_id="fatf-2026-001",
            storage_result=self.storage_result,
            integrity_record=self.integrity_record,
        )

        self.assertEqual(updated.file_name, "fatf-2026-001.pdf")
        self.assertEqual(updated.file_type, "pdf")
        self.assertEqual(
            updated.local_path, str(self.storage_result.file_path)
        )
        self.assertEqual(updated.file_size, 204800)
        self.assertEqual(updated.sha256_hash, "a" * 64)
        self.assertEqual(updated.processing_status, "DOWNLOADED")
        self.assertIsNotNone(updated.last_downloaded)
        self.assertIsNotNone(updated.last_updated)

    def test_default_processing_status_is_downloaded(self) -> None:
        updated = self.manager.update_after_download(
            document_id="fatf-2026-001",
            storage_result=self.storage_result,
            integrity_record=self.integrity_record,
        )
        self.assertEqual(updated.processing_status, "DOWNLOADED")

    def test_custom_processing_status_is_honoured(self) -> None:
        updated = self.manager.update_after_download(
            document_id="fatf-2026-001",
            storage_result=self.storage_result,
            integrity_record=self.integrity_record,
            processing_status="VERIFIED",
        )
        self.assertEqual(updated.processing_status, "VERIFIED")

    def test_unknown_document_raises_document_not_found_error(self) -> None:
        with self.assertRaises(DocumentNotFoundError):
            self.manager.update_after_download(
                document_id="does-not-exist",
                storage_result=self.storage_result,
                integrity_record=self.integrity_record,
            )

    def test_update_is_reflected_in_get_document(self) -> None:
        self.manager.update_after_download(
            document_id="fatf-2026-001",
            storage_result=self.storage_result,
            integrity_record=self.integrity_record,
        )

        fetched = self.manager.get_document("fatf-2026-001")
        self.assertEqual(fetched.sha256_hash, "a" * 64)
        self.assertEqual(fetched.processing_status, "DOWNLOADED")

    def test_file_type_none_when_no_extension(self) -> None:
        no_ext_result = StorageResult(
            file_path=Path("/data/fatf/fatf-2026-001"),
            file_size=100,
            created=True,
        )
        updated = self.manager.update_after_download(
            document_id="fatf-2026-001",
            storage_result=no_ext_result,
            integrity_record=self.integrity_record,
        )
        self.assertIsNone(updated.file_type)


if __name__ == "__main__":
    unittest.main()