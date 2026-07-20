import json
import unittest

from src.models.document_metadata import DocumentMetadata


class TestDocumentMetadata(unittest.TestCase):

    def setUp(self):
        self.document = DocumentMetadata(
            document_id="FATF-2026-001",
            source_identifier="fatf",
            title="Guidance on Beneficial Ownership",
            authority="Financial Action Task Force",
            jurisdiction="Global",
            publication_url="https://www.fatf-gafi.org/en/publications.html",
        )

    # ---------------------------------------------------------
    # Object Creation
    # ---------------------------------------------------------

    def test_create_document(self):
        self.assertEqual(self.document.document_id, "FATF-2026-001")
        self.assertEqual(self.document.source_identifier, "fatf")
        self.assertEqual(
            self.document.title,
            "Guidance on Beneficial Ownership"
        )

    # ---------------------------------------------------------
    # Default Values
    # ---------------------------------------------------------

    def test_default_processing_status(self):
        self.assertEqual(
            self.document.processing_status,
            "DISCOVERED"
        )

    def test_default_status(self):
        self.assertEqual(
            self.document.status,
            "ACTIVE"
        )

    def test_default_version(self):
        self.assertEqual(
            self.document.version,
            "1.0"
        )

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def test_to_dict(self):
        data = self.document.to_dict()

        self.assertEqual(
            data["document_id"],
            "FATF-2026-001"
        )

        self.assertEqual(
            data["authority"],
            "Financial Action Task Force"
        )

    def test_to_json(self):
        json_string = self.document.to_json()

        data = json.loads(json_string)

        self.assertEqual(
            data["source_identifier"],
            "fatf"
        )

    def test_from_dict(self):
        data = self.document.to_dict()

        obj = DocumentMetadata.from_dict(data)

        self.assertEqual(
            obj,
            self.document
        )

    def test_from_json(self):
        json_string = self.document.to_json()

        obj = DocumentMetadata.from_json(json_string)

        self.assertEqual(
            obj,
            self.document
        )

    # ---------------------------------------------------------
    # Processing Errors
    # ---------------------------------------------------------

    def test_add_processing_error(self):

        self.document.add_processing_error("Download failed")

        self.assertEqual(
            len(self.document.processing_errors),
            1
        )

        self.assertEqual(
            self.document.processing_errors[0],
            "Download failed"
        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def test_empty_document_id(self):

        with self.assertRaises(ValueError):
            DocumentMetadata(
                document_id="",
                source_identifier="fatf",
                title="Title",
                authority="FATF",
                jurisdiction="Global",
                publication_url="https://example.com",
            )

    def test_empty_title(self):

        with self.assertRaises(ValueError):
            DocumentMetadata(
                document_id="DOC001",
                source_identifier="fatf",
                title="",
                authority="FATF",
                jurisdiction="Global",
                publication_url="https://example.com",
            )

    def test_invalid_url(self):

        with self.assertRaises(ValueError):
            DocumentMetadata(
                document_id="DOC001",
                source_identifier="fatf",
                title="Title",
                authority="FATF",
                jurisdiction="Global",
                publication_url="invalid-url",
            )

    def test_negative_file_size(self):

        with self.assertRaises(ValueError):
            DocumentMetadata(
                document_id="DOC001",
                source_identifier="fatf",
                title="Title",
                authority="FATF",
                jurisdiction="Global",
                publication_url="https://example.com",
                file_size=-10,
            )


if __name__ == "__main__":
    unittest.main()