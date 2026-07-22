"""
Tests for Base Connector Framework
"""


import unittest

from src.connectors.base_connector import BaseConnector



class DummyConnector(BaseConnector):
    """
    Test implementation
    """

    def __init__(self):
        super().__init__("dummy")


    def discover_documents(self):
        return []



class TestBaseConnector(unittest.TestCase):


    def test_connector_requires_source_name(self):

        connector = DummyConnector()

        self.assertEqual(
            connector.get_source_name(),
            "dummy"
        )


    def test_discover_documents_contract(self):

        connector = DummyConnector()

        result = connector.discover_documents()

        self.assertEqual(
            result,
            []
        )


    def test_empty_source_name_not_allowed(self):

        with self.assertRaises(ValueError):

            DummyConnectorWithEmptyName()



class DummyConnectorWithEmptyName(BaseConnector):


    def __init__(self):

        super().__init__("")


    def discover_documents(self):

        return []