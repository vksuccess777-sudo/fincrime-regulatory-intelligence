"""
FRI - Catalogue Store Integration Tests

Sprint 2
Deliverable D5

Validates persistence between CatalogueManager and CatalogueStore.
"""

import os
import tempfile
import unittest

from src.catalogue.catalogue_manager import CatalogueManager
from src.catalogue.catalogue_store import CatalogueStore
from src.models.document_metadata import DocumentMetadata
from src.models.source_definition import SourceDefinition


class TestCatalogueStore(unittest.TestCase):
    """
    Integration tests for catalogue persistence.
    """

    def setUp(self):

        self.temp_directory = tempfile.TemporaryDirectory()

        self.catalogue_path = os.path.join(
            self.temp_directory.name,
            "catalogue.json",
        )

        self.store = CatalogueStore(self.catalogue_path)

    def tearDown(self):

        self.temp_directory.cleanup()

    # ---------------------------------------------------------
    # Test Data
    # ---------------------------------------------------------

    def _create_source(self):

        return SourceDefinition(
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
            enabled=True,
        )

    def _create_document(self):

        return DocumentMetadata(
            document_id="fatf-rec-2025",
            source_identifier="fatf",
            title="FATF Recommendations",
            authority="Financial Action Task Force",
            jurisdiction="Global",
            publication_url="https://www.fatf-gafi.org/en/publications.html",
        )

    # ---------------------------------------------------------
    # Tests
    # ---------------------------------------------------------

    def test_catalogue_created(self):

        self.assertTrue(self.store.exists())

    def test_empty_catalogue(self):

        sources, documents = self.store.load()

        self.assertEqual(len(sources), 0)
        self.assertEqual(len(documents), 0)

    def test_save_and_load(self):

        source = self._create_source()
        document = self._create_document()

        self.store.save(
            [source],
            [document],
        )

        sources, documents = self.store.load()

        self.assertEqual(len(sources), 1)
        self.assertEqual(len(documents), 1)

        self.assertEqual(
            sources[0].identifier,
            "fatf",
        )

        self.assertEqual(
            documents[0].document_id,
            "fatf-rec-2025",
        )

    def test_manager_persistence(self):

        manager = CatalogueManager(self.store)

        manager.register_source(
            self._create_source()
        )

        manager.register_document(
            self._create_document()
        )

        reloaded_manager = CatalogueManager(self.store)

        self.assertEqual(
            reloaded_manager.source_count,
            1,
        )

        self.assertEqual(
            reloaded_manager.document_count,
            1,
        )


if __name__ == "__main__":
    unittest.main()