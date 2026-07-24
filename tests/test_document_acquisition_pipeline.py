"""
test_document_acquisition_pipeline.py

Sprint 4 D5 (Catalogue Integration)

Targeted unit tests for DocumentAcquisitionPipeline.

Each collaborator (DownloadEngine, StorageManager, IntegrityVerifier,
CatalogueManager) is already covered by its own test suite, so these
tests mock all four and verify only the orchestration: correct call
order, correct data hand-off between steps, and correct propagation
of the final result / exceptions.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import MagicMock, call

from src.acquisition.document_acquisition_pipeline import (
    DocumentAcquisitionPipeline,
)
from src.download.download_result import DownloadResult
from src.download.exceptions import DownloadFailedException
from src.integrity.integrity_record import IntegrityRecord
from src.models.document_metadata import DocumentMetadata
from src.storage.exceptions import StorageWriteError
from src.storage.storage_result import StorageResult


class TestDocumentAcquisitionPipeline(unittest.TestCase):

    def setUp(self) -> None:
        self.download_engine = MagicMock()
        self.storage_manager = MagicMock()
        self.integrity_verifier = MagicMock()
        self.catalogue_manager = MagicMock()

        self.pipeline = DocumentAcquisitionPipeline(
            download_engine=self.download_engine,
            storage_manager=self.storage_manager,
            integrity_verifier=self.integrity_verifier,
            catalogue_manager=self.catalogue_manager,
        )

        self.document = DocumentMetadata(
            document_id="fatf-2026-001",
            source_identifier="fatf",
            title="FATF Guidance on Virtual Assets",
            authority="FATF",
            jurisdiction="International",
            publication_url="https://www.fatf-gafi.org/doc.pdf",
        )

        self.download_result = DownloadResult(
            url=self.document.publication_url,
            status_code=200,
            content=b"pdf-bytes-here",
            content_type="application/pdf",
            content_length=14,
        )

        self.storage_result = StorageResult(
            file_path=Path("/data/fatf/fatf-2026-001.pdf"),
            file_size=14,
            created=True,
        )

        self.integrity_record = IntegrityRecord(
            file_hash="b" * 64,
            algorithm="SHA256",
            byte_count=14,
        )

        self.download_engine.download.return_value = self.download_result
        self.storage_manager.save.return_value = self.storage_result
        self.integrity_verifier.compute_bytes.return_value = (
            self.integrity_record
        )
        self.catalogue_manager.update_after_download.return_value = (
            self.document
        )

    def test_process_calls_each_collaborator_exactly_once(self) -> None:
        self.pipeline.process(self.document)

        self.download_engine.download.assert_called_once_with(
            self.document
        )
        self.storage_manager.save.assert_called_once()
        self.integrity_verifier.compute_bytes.assert_called_once_with(
            self.download_result.content
        )
        self.catalogue_manager.update_after_download.assert_called_once()

    def test_process_passes_downloaded_content_to_storage(self) -> None:
        self.pipeline.process(self.document)

        _, kwargs = self.storage_manager.save.call_args
        self.assertEqual(kwargs["content"], self.download_result.content)

    def test_process_uses_deterministic_filename_from_document_id(
        self,
    ) -> None:
        self.pipeline.process(self.document)

        _, kwargs = self.storage_manager.save.call_args
        self.assertEqual(kwargs["filename"], "fatf-2026-001.pdf")

    def test_process_saves_with_overwrite_true(self) -> None:
        self.pipeline.process(self.document)

        _, kwargs = self.storage_manager.save.call_args
        self.assertTrue(kwargs["overwrite"])

    def test_process_passes_storage_and_integrity_results_to_catalogue(
        self,
    ) -> None:
        self.pipeline.process(self.document)

        self.catalogue_manager.update_after_download.assert_called_once_with(
            document_id="fatf-2026-001",
            storage_result=self.storage_result,
            integrity_record=self.integrity_record,
        )

    def test_process_returns_updated_document_from_catalogue(self) -> None:
        result = self.pipeline.process(self.document)

        self.assertIs(result, self.document)

    def test_process_propagates_download_failure_and_stops_pipeline(
        self,
    ) -> None:
        self.download_engine.download.side_effect = DownloadFailedException(
            "boom"
        )

        with self.assertRaises(DownloadFailedException):
            self.pipeline.process(self.document)

        self.storage_manager.save.assert_not_called()
        self.integrity_verifier.compute_bytes.assert_not_called()
        self.catalogue_manager.update_after_download.assert_not_called()

    def test_process_propagates_storage_failure_and_stops_pipeline(
        self,
    ) -> None:
        self.storage_manager.save.side_effect = StorageWriteError("boom")

        with self.assertRaises(StorageWriteError):
            self.pipeline.process(self.document)

        self.integrity_verifier.compute_bytes.assert_not_called()
        self.catalogue_manager.update_after_download.assert_not_called()

    def test_build_filename_uses_url_extension(self) -> None:
        filename = DocumentAcquisitionPipeline._build_filename(
            self.document
        )
        self.assertEqual(filename, "fatf-2026-001.pdf")

    def test_build_filename_falls_back_to_default_extension(self) -> None:
        no_ext_document = DocumentMetadata(
            document_id="fatf-2026-002",
            source_identifier="fatf",
            title="Query-string driven download",
            authority="FATF",
            jurisdiction="International",
            publication_url="https://www.fatf-gafi.org/download?id=2",
        )

        filename = DocumentAcquisitionPipeline._build_filename(
            no_ext_document
        )
        self.assertEqual(filename, "fatf-2026-002.bin")


if __name__ == "__main__":
    unittest.main()