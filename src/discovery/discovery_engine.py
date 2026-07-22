"""
Discovery Engine

Orchestrates regulatory document discovery
through source connectors.

Responsibilities:
- Execute connectors
- Validate discovery output
- Return DocumentMetadata objects

Non-responsibilities:
- Persistence
- Catalogue management
- Document downloading
"""


from typing import List

from src.connectors.base_connector import BaseConnector
from src.models.document_metadata import DocumentMetadata



class DiscoveryEngine:
    """
    Central discovery orchestration service.
    """


    def discover(
        self,
        connector: BaseConnector
    ) -> List[DocumentMetadata]:
        """
        Execute connector discovery.

        Args:
            connector:
                Regulatory source connector

        Returns:
            List of discovered documents
        """


        if not isinstance(
            connector,
            BaseConnector
        ):
            raise TypeError(
                "connector must inherit from BaseConnector"
            )


        documents = (
            connector.discover_documents()
        )


        self._validate_documents(
            documents
        )


        return documents



    @staticmethod
    def _validate_documents(
        documents: List[DocumentMetadata]
    ) -> None:
        """
        Validate discovery output.
        """


        if not isinstance(
            documents,
            list
        ):
            raise ValueError(
                "Connector must return a list"
            )


        for document in documents:

            if not isinstance(
                document,
                DocumentMetadata
            ):
                raise ValueError(
                    "Discovery output must contain DocumentMetadata objects"
                )