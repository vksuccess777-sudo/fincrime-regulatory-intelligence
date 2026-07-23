"""
Download Engine for FRI.

Sprint 4 D1 introduces the orchestration framework only.

Responsibilities:
    - Validate DocumentMetadata objects
    - Validate publication URLs
    - Provide a stable public API for future download components

Future Sprint 4 Deliverables:
    D2 - HTTP Downloader
    D3 - File Storage Manager
    D4 - Integrity Validation
    D5 - Catalogue Integration
"""

from urllib.parse import urlparse

from src.models.document_metadata import DocumentMetadata

from src.download.exceptions import (
    DownloadError,
    InvalidDownloadURLException,
    DownloadNotSupportedException,
)


class DownloadEngine:
    """
    Orchestrates the document download workflow.

    At Sprint 4 D1 this engine performs validation only.
    Actual downloading will be implemented in later deliverables.
    """

    SUPPORTED_SCHEMES = {"http", "https"}

    def download(self, document: DocumentMetadata) -> DocumentMetadata:
        """
        Validate a document before download.

        Parameters
        ----------
        document : DocumentMetadata
            Metadata describing the document.

        Returns
        -------
        DocumentMetadata
            The validated document metadata.

        Raises
        ------
        DownloadError
            If the supplied object is not a DocumentMetadata instance.
        InvalidDownloadURLException
            If the publication URL is missing or invalid.
        DownloadNotSupportedException
            If the URL scheme is unsupported.
        """

        self._validate_document(document)
        self._validate_publication_url(document.publication_url)

        # Sprint 4 D2 will perform the actual download.
        return document

    def _validate_document(self, document: DocumentMetadata) -> None:
        """
        Validate the supplied DocumentMetadata object.
        """

        if not isinstance(document, DocumentMetadata):
            raise DownloadError(
                "Expected a DocumentMetadata instance."
            )

    def _validate_publication_url(self, publication_url: str) -> None:
        """
        Validate the publication URL.
        """

        if publication_url is None:
            raise InvalidDownloadURLException(
                "Publication URL is missing."
            )

        if not publication_url.strip():
            raise InvalidDownloadURLException(
                "Publication URL cannot be empty."
            )

        parsed = urlparse(publication_url)

        if parsed.scheme.lower() not in self.SUPPORTED_SCHEMES:
            raise DownloadNotSupportedException(
                f"Unsupported download protocol: '{parsed.scheme}'."
            )

        if not parsed.netloc:
            raise InvalidDownloadURLException(
                "Publication URL is invalid."
            )