"""
Acquisition Service

Bridges discovery and catalogue layers.

Responsibilities:
- Execute discovery
- Register discovered documents

Does not:
- Download documents
- Process documents
- Manage catalogue rules
"""

from typing import List

from src.catalogue.catalogue_manager import CatalogueManager
from src.connectors.base_connector import BaseConnector
from src.discovery.discovery_engine import DiscoveryEngine
from src.models.document_metadata import DocumentMetadata


class AcquisitionService:
    """
    Regulatory document acquisition coordinator.
    """


    def __init__(
        self,
        discovery_engine: DiscoveryEngine,
        catalogue_manager: CatalogueManager,
    ) -> None:

        self._discovery_engine = discovery_engine
        self._catalogue_manager = catalogue_manager



    def acquire(
        self,
        connector: BaseConnector,
    ) -> List[DocumentMetadata]:
        """
        Discover and register documents.

        Returns:
            List of acquired documents
        """

        documents = (
            self._discovery_engine.discover(
                connector
            )
        )


        for document in documents:

            self._catalogue_manager.register_document(
                document
            )


        return documents