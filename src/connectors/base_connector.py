"""
Base Connector Framework

Defines the standard contract that all regulatory
source connectors must implement.

Examples:
- FATF Connector
- FCA Connector
- FinCEN Connector
- RBI Connector
"""


from abc import ABC, abstractmethod


class BaseConnector(ABC):
    """
    Abstract base class for regulatory connectors.

    Every connector must provide:
    - source_name
    - discover_documents()
    """

    def __init__(self, source_name: str):
        if not source_name:
            raise ValueError(
                "Source name cannot be empty"
            )

        self.source_name = source_name


    @abstractmethod
    def discover_documents(self):
        """
        Discover regulatory documents.

        Returns:
            List[DocumentMetadata]

        Must be implemented by
        regulator-specific connectors.
        """

        pass


    def get_source_name(self):
        """
        Return connector source name.
        """

        return self.source_name