"""
Tests for Acquisition Service
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


class TestAcquisitionService(unittest.TestCase):


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


        self.service = AcquisitionService(
            DiscoveryEngine(),
            self.catalogue,
        )


    def test_acquire_registers_documents(self):

        documents = self.service.acquire(
            FATFConnector()
        )


        self.assertEqual(
            len(documents),
            1
        )


        self.assertEqual(
            self.catalogue.document_count,
            1
        )


    def test_document_available_in_catalogue(self):

        self.service.acquire(
            FATFConnector()
        )


        document = (
            self.catalogue.get_document(
                "fatf-recommendations"
            )
        )


        self.assertIsNotNone(
            document
        )


if __name__ == "__main__":

    unittest.main()