import unittest

from src.models.document_metadata import DocumentMetadata
from src.models.source_definition import SourceDefinition


class TestDomainModels(unittest.TestCase):

    def setUp(self):

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
                "html"
            ],
            connector_class="FATFConnector",
            sync_schedule="daily",
        )

        self.document = DocumentMetadata(
            document_id="FATF-2026-001",
            source_identifier=self.source.identifier,
            title="Guidance on Beneficial Ownership",
            authority=self.source.name,
            jurisdiction=self.source.jurisdiction,
            publication_url=self.source.publication_urls[0],
        )

    # -----------------------------------------------------
    # Integration
    # -----------------------------------------------------

    def test_document_matches_source(self):

        self.assertEqual(
            self.document.source_identifier,
            self.source.identifier,
        )

        self.assertEqual(
            self.document.authority,
            self.source.name,
        )

        self.assertEqual(
            self.document.jurisdiction,
            self.source.jurisdiction,
        )

    def test_source_serialization(self):

        data = self.source.to_dict()

        recreated = SourceDefinition.from_dict(data)

        self.assertEqual(
            recreated,
            self.source,
        )

    def test_document_serialization(self):

        data = self.document.to_dict()

        recreated = DocumentMetadata.from_dict(data)

        self.assertEqual(
            recreated,
            self.document,
        )

    def test_source_json_roundtrip(self):

        json_data = self.source.to_json()

        recreated = SourceDefinition.from_json(json_data)

        self.assertEqual(
            recreated,
            self.source,
        )

    def test_document_json_roundtrip(self):

        json_data = self.document.to_json()

        recreated = DocumentMetadata.from_json(json_data)

        self.assertEqual(
            recreated,
            self.document,
        )

    def test_document_uses_source_publication_url(self):

        self.assertEqual(
            self.document.publication_url,
            self.source.publication_urls[0],
        )

    def test_default_processing_state(self):

        self.assertEqual(
            self.document.processing_status,
            "DISCOVERED",
        )

        self.assertEqual(
            self.document.status,
            "ACTIVE",
        )


if __name__ == "__main__":
    unittest.main()