"""
FATF Regulatory Connector

Provides FATF-specific document discovery.

This connector currently implements controlled discovery.
Live web crawling and downloading are handled in later sprints.
"""


from typing import List

from src.connectors.base_connector import BaseConnector
from src.models.document_metadata import DocumentMetadata


class FATFConnector(BaseConnector):
    """
    Connector for Financial Action Task Force (FATF).

    Responsible for discovering FATF regulatory publications.
    """

    SOURCE_IDENTIFIER = "fatf"

    AUTHORITY = "Financial Action Task Force"

    JURISDICTION = "Global"


    def __init__(self):

        super().__init__(
            self.SOURCE_IDENTIFIER
        )


    def discover_documents(self) -> List[DocumentMetadata]:
        """
        Discover FATF publications.

        Returns:
            List of DocumentMetadata objects.
        """

        return [
            DocumentMetadata(
                document_id="fatf-recommendations",
                source_identifier=self.SOURCE_IDENTIFIER,
                title=(
                    "FATF Recommendations "
                    "International Standards on AML/CFT"
                ),
                authority=self.AUTHORITY,
                jurisdiction=self.JURISDICTION,
                publication_url=(
                    "https://www.fatf-gafi.org/"
                ),
                version="1.0",
                processing_status="DISCOVERED",
            )
        ]