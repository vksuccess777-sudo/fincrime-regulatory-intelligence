"""
Unit tests for the FRI Download Engine.
"""

import unittest

from src.download.download_engine import DownloadEngine
from src.download.exceptions import (
    DownloadError,
    DownloadNotSupportedException,
    InvalidDownloadURLException,
)
from src.models.document_metadata import DocumentMetadata


class TestDownloadEngine(unittest.TestCase):
    """Tests for DownloadEngine."""

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

    def test_valid_document_returns_document(self):
        """Valid document should be returned unchanged."""

        result = self.engine.download(self.document)

        self.assertIs(result, self.document)

    def test_invalid_object_raises_download_error(self):
        """Non-DocumentMetadata object should raise DownloadError."""

        with self.assertRaises(DownloadError):
            self.engine.download("not a document")

    def test_none_publication_url_raises_exception(self):
        """Missing publication URL should raise InvalidDownloadURLException."""

        self.document.publication_url = None

        with self.assertRaises(InvalidDownloadURLException):
            self.engine.download(self.document)

    def test_empty_publication_url_raises_exception(self):
        """Empty publication URL should raise InvalidDownloadURLException."""

        self.document.publication_url = ""

        with self.assertRaises(InvalidDownloadURLException):
            self.engine.download(self.document)

    def test_whitespace_publication_url_raises_exception(self):
        """Whitespace publication URL should raise InvalidDownloadURLException."""

        self.document.publication_url = "    "

        with self.assertRaises(InvalidDownloadURLException):
            self.engine.download(self.document)

    def test_unsupported_protocol_raises_exception(self):
        """Unsupported protocol should raise DownloadNotSupportedException."""

        self.document.publication_url = "ftp://example.com/file.pdf"

        with self.assertRaises(DownloadNotSupportedException):
            self.engine.download(self.document)

    def test_http_url_is_valid(self):
        """HTTP URLs should be accepted."""

        self.document.publication_url = "http://example.com/file.pdf"

        result = self.engine.download(self.document)

        self.assertIs(result, self.document)

    def test_https_url_is_valid(self):
        """HTTPS URLs should be accepted."""

        self.document.publication_url = "https://example.com/file.pdf"

        result = self.engine.download(self.document)

        self.assertIs(result, self.document)


if __name__ == "__main__":
    unittest.main()