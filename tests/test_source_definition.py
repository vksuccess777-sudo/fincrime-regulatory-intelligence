import json
import unittest

from src.models.source_definition import SourceDefinition


class TestSourceDefinition(unittest.TestCase):

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

    def test_create_source(self):
        self.assertEqual(self.source.identifier, "fatf")
        self.assertEqual(
            self.source.name,
            "Financial Action Task Force"
        )
        self.assertTrue(self.source.enabled)

    def test_to_dict(self):
        data = self.source.to_dict()

        self.assertEqual(data["identifier"], "fatf")
        self.assertEqual(data["jurisdiction"], "Global")
        self.assertEqual(
            data["connector_class"],
            "FATFConnector"
        )

    def test_to_json(self):
        json_string = self.source.to_json()

        data = json.loads(json_string)

        self.assertEqual(
            data["identifier"],
            "fatf"
        )

    def test_from_dict(self):
        data = self.source.to_dict()

        obj = SourceDefinition.from_dict(data)

        self.assertEqual(obj, self.source)

    def test_from_json(self):
        json_string = self.source.to_json()

        obj = SourceDefinition.from_json(json_string)

        self.assertEqual(obj, self.source)

    def test_invalid_base_url(self):
        with self.assertRaises(ValueError):
            SourceDefinition(
                identifier="fatf",
                name="FATF",
                jurisdiction="Global",
                base_url="invalid-url",
                publication_urls=[
                    "https://example.com"
                ],
                supported_file_types=[
                    "pdf"
                ],
                connector_class="FATFConnector",
                sync_schedule="daily",
            )

    def test_empty_identifier(self):
        with self.assertRaises(ValueError):
            SourceDefinition(
                identifier="",
                name="FATF",
                jurisdiction="Global",
                base_url="https://example.com",
                publication_urls=[
                    "https://example.com"
                ],
                supported_file_types=[
                    "pdf"
                ],
                connector_class="FATFConnector",
                sync_schedule="daily",
            )

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            SourceDefinition(
                identifier="fatf",
                name="",
                jurisdiction="Global",
                base_url="https://example.com",
                publication_urls=[
                    "https://example.com"
                ],
                supported_file_types=[
                    "pdf"
                ],
                connector_class="FATFConnector",
                sync_schedule="daily",
            )

    def test_invalid_publication_url(self):
        with self.assertRaises(ValueError):
            SourceDefinition(
                identifier="fatf",
                name="FATF",
                jurisdiction="Global",
                base_url="https://example.com",
                publication_urls=[
                    "bad-url"
                ],
                supported_file_types=[
                    "pdf"
                ],
                connector_class="FATFConnector",
                sync_schedule="daily",
            )


if __name__ == "__main__":
    unittest.main()