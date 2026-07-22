"""
Tests for FATF Connector
"""


import unittest

from src.connectors.fatf_connector import FATFConnector
from src.models.document_metadata import DocumentMetadata



class TestFATFConnector(unittest.TestCase):


    def setUp(self):

        self.connector = FATFConnector()


    def test_source_identifier(self):

        self.assertEqual(
            self.connector.get_source_name(),
            "fatf"
        )


    def test_discover_documents_returns_documents(self):

        documents = (
            self.connector.discover_documents()
        )

        self.assertEqual(
            len(documents),
            1
        )


    def test_document_metadata_structure(self):

        documents = (
            self.connector.discover_documents()
        )

        document = documents[0]


        self.assertIsInstance(
            document,
            DocumentMetadata
        )


        self.assertEqual(
            document.source_identifier,
            "fatf"
        )


        self.assertEqual(
            document.authority,
            "Financial Action Task Force"
        )


        self.assertEqual(
            document.jurisdiction,
            "Global"
        )


if __name__ == "__main__":

    unittest.main()