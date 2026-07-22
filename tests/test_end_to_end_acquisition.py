"""
End-to-End Acquisition Pipeline Test

Validates complete FRI regulatory acquisition flow:

Connector
    |
Discovery Engine
    |
Acquisition Service
    |
Catalogue Manager
    |
Catalogue Store
"""


import unittest


from src.acquisition.acquisition_service import (
    AcquisitionService,
)

from src.catalogue.catalogue_manager import (
    CatalogueManager,
)

from src.connectors.fatf_connector import (
    FATFConnector,
)

from src.discovery.discovery_engine import (
    DiscoveryEngine,
)

from src.models.source_definition import (
    SourceDefinition,
)



class TestEndToEndAcquisition(unittest.TestCase):


    def setUp(self):

        self.catalogue = CatalogueManager()


        self.catalogue.register_source(
            SourceDefinition(
                identifier="fatf",
                name="Financial Action Task Force",
                jurisdiction="Global",
                base_url="https://www.fatf-gafi.org/",
                publication_urls=[
                    "https://www.fatf-gafi.org/"
                ],
                supported_file_types=[
                    "pdf",
                    "html"
                ],
                connector_class="FATFConnector",
                sync_schedule="monthly",
            )
        )


        self.acquisition_service = AcquisitionService(
            DiscoveryEngine(),
            self.catalogue,
        )


    def test_complete_fatf_acquisition_pipeline(self):

        documents = (
            self.acquisition_service.acquire(
                FATFConnector()
            )
        )


        self.assertEqual(
            len(documents),
            1
        )


        document = (
            self.catalogue.get_document(
                "fatf-recommendations"
            )
        )


        self.assertIsNotNone(
            document
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
            document.processing_status,
            "DISCOVERED"
        )



if __name__ == "__main__":

    unittest.main()