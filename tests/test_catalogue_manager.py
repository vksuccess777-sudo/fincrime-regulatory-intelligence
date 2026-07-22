"""
FRI - Catalogue Manager Tests

Sprint 2
Deliverable D3
"""

import unittest

from src.catalogue.catalogue_manager import CatalogueManager
from src.catalogue.exceptions import (
    DuplicateDocumentError,
    DuplicateSourceError,
    UnknownSourceError,
)
from src.models.document_metadata import DocumentMetadata
from src.models.source_definition import SourceDefinition


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

        self.assertEqual(
            self.manager.source_count,
            0,
        )

        self.assertEqual(
            self.manager.document_count,
            0,
        )


if __name__ == "__main__":
    unittest.main()