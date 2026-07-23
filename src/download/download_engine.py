"""
download_engine.py

Download Engine for the FinCrime Regulatory Intelligence (FRI) platform.

The DownloadEngine orchestrates the document download workflow.

Responsibilities
----------------
1. Validate the supplied DocumentMetadata.
2. Select the appropriate downloader.
3. Delegate the download.
4. Return a DownloadResult.

The DownloadEngine intentionally does NOT:

- perform HTTP requests directly
- save files
- calculate hashes
- update the catalogue
"""

from __future__ import annotations

from urllib.parse import urlparse

from src.download.download_result import DownloadResult
from src.download.exceptions import (
    DownloadError,
    DownloadNotSupportedException,
    InvalidDownloadURLException,
)
from src.download.http_downloader import HTTPDownloader
from src.models.document_metadata import DocumentMetadata


class DownloadEngine:
    """
    Coordinates document downloads.
    """

    def __init__(self) -> None:
        self._http_downloader = HTTPDownloader()

    def download(self, document: DocumentMetadata) -> DownloadResult:
        """
        Download the supplied regulatory document.

        Parameters
        ----------
        document:
            Metadata describing the regulatory publication.

        Returns
        -------
        DownloadResult
        """

        self._validate_document(document)

        downloader = self._select_downloader(
            document.publication_url
        )

        return downloader.download(
            document.publication_url
        )

    @staticmethod
    def _validate_document(
        document: DocumentMetadata,
    ) -> None:
        """
        Validate the supplied document metadata.
        """

        if not isinstance(document, DocumentMetadata):
            raise DownloadError(
                "Expected a DocumentMetadata instance."
            )

        if not document.publication_url:
            raise InvalidDownloadURLException(
                "publication_url cannot be empty."
            )

    def _select_downloader(
        self,
        url: str,
    ) -> HTTPDownloader:
        """
        Select the downloader based on URL scheme.

        Currently supported:

            http
            https

        Future:

            ftp
            s3
            sharepoint
        """

        parsed = urlparse(url)

        scheme = parsed.scheme.lower()

        if scheme in ("http", "https"):
            return self._http_downloader

        raise DownloadNotSupportedException(
            f"Unsupported download protocol '{scheme}'."
        )