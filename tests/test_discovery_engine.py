"""
Tests for Discovery Engine
"""


import unittest


from src.discovery.discovery_engine import DiscoveryEngine
from src.connectors.fatf_connector import FATFConnector
from src.connectors.base_connector import BaseConnector



class InvalidConnector:

    pass



class TestDiscoveryEngine(unittest.TestCase):


    def setUp(self):

        self.engine = DiscoveryEngine()



    def test_discovery_with_fatf_connector(self):

        documents = (
            self.engine.discover(
                FATFConnector()
            )
        )


        self.assertEqual(
            len(documents),
            1
        )


        self.assertEqual(
            documents[0].source_identifier,
            "fatf"
        )



    def test_invalid_connector_rejected(self):

        with self.assertRaises(TypeError):

            self.engine.discover(
                InvalidConnector()
            )



if __name__ == "__main__":

    unittest.main()