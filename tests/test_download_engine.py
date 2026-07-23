"""
Unit tests for DownloadEngine.

The DownloadEngine is responsible for:

- validating DocumentMetadata
- selecting the correct downloader
- delegating the download

It is NOT responsible for:

- HTTP communication
- file storage
- hashing
"""

import unittest
from unittest.mock import patch

from src.download.download_engine import DownloadEngine
from src.download.download_result import DownloadResult
from src.download.exceptions import (
    DownloadError,
    DownloadNotSupportedException,
    InvalidDownloadURLException,
)
from src.models.document_metadata import DocumentMetadata


class TestDownloadEngine(unittest.TestCase):

    def setUp(self):

        self.engine = DownloadEngine()

        self.document = DocumentMetadata(
            document_id="DOC-001",
            source_identifier="fatf",
            title="Recommendation 10",
            authority="FATF",
            jurisdiction="Global",
            publication_url="https://www.fatf-gafi.org/document.pdf",
        )

    @patch("src.download.http_downloader.HTTPDownloader.download")
    def test_download_delegates_to_http_downloader(self, mock_download):
        """
        DownloadEngine should delegate downloading
        to HTTPDownloader.
        """

        expected = DownloadResult(
            url=self.document.publication_url,
            status_code=200,
            content=b"PDF",
            content_type="application/pdf",
            content_length=3,
        )

        mock_download.return_value = expected

        result = self.engine.download(self.document)

        mock_download.assert_called_once_with(
            self.document.publication_url
        )

        self.assertEqual(result, expected)

    def test_invalid_document_type(self):
        """
        Only DocumentMetadata is accepted.
        """

        with self.assertRaises(DownloadError):
            self.engine.download("invalid")

    def test_empty_publication_url(self):
        """
        Empty URLs are rejected before attempting
        any download.
        """

        self.document.publication_url = ""

        with self.assertRaises(
            InvalidDownloadURLException
        ):
            self.engine.download(self.document)

    def test_unsupported_protocol(self):
        """
        FTP is not yet supported.
        """

        self.document.publication_url = (
            "ftp://example.com/file.pdf"
        )

        with self.assertRaises(
            DownloadNotSupportedException
        ):
            self.engine.download(self.document)


if __name__ == "__main__":
    unittest.main()