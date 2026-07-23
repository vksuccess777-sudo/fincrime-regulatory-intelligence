"""
Unit tests for the HTTP Downloader.
"""

import unittest
from unittest.mock import Mock, patch

import requests

from src.download.download_result import DownloadResult
from src.download.exceptions import (
    ConnectionFailedException,
    DownloadFailedException,
    DownloadTimeoutException,
    HTTPStatusException,
)
from src.download.http_downloader import HTTPDownloader


class TestHTTPDownloader(unittest.TestCase):
    """Tests for HTTPDownloader."""

    def setUp(self):
        self.downloader = HTTPDownloader()
        self.url = "https://example.com/document.pdf"

    @patch("src.download.http_downloader.requests.get")
    def test_successful_download(self, mock_get):
        """A successful download should return DownloadResult."""

        response = Mock()
        response.ok = True
        response.status_code = 200
        response.content = b"Sample PDF Content"
        response.headers = {
            "Content-Type": "application/pdf"
        }

        mock_get.return_value = response

        result = self.downloader.download(self.url)

        self.assertIsInstance(result, DownloadResult)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, b"Sample PDF Content")
        self.assertEqual(
            result.content_type,
            "application/pdf",
        )
        self.assertEqual(
            result.content_length,
            len(b"Sample PDF Content"),
        )

    @patch("src.download.http_downloader.requests.get")
    def test_http_404(self, mock_get):
        """HTTP 404 should raise HTTPStatusException."""

        response = Mock()
        response.ok = False
        response.status_code = 404

        mock_get.return_value = response

        with self.assertRaises(HTTPStatusException):
            self.downloader.download(self.url)

    @patch("src.download.http_downloader.requests.get")
    def test_http_500(self, mock_get):
        """HTTP 500 should raise HTTPStatusException."""

        response = Mock()
        response.ok = False
        response.status_code = 500

        mock_get.return_value = response

        with self.assertRaises(HTTPStatusException):
            self.downloader.download(self.url)

    @patch("src.download.http_downloader.requests.get")
    def test_connection_error(self, mock_get):
        """Connection failures should raise ConnectionFailedException."""

        mock_get.side_effect = requests.exceptions.ConnectionError()

        with self.assertRaises(ConnectionFailedException):
            self.downloader.download(self.url)

    @patch("src.download.http_downloader.requests.get")
    def test_timeout(self, mock_get):
        """Timeouts should raise DownloadTimeoutException."""

        mock_get.side_effect = requests.exceptions.Timeout()

        with self.assertRaises(DownloadTimeoutException):
            self.downloader.download(self.url)

    @patch("src.download.http_downloader.requests.get")
    def test_request_exception(self, mock_get):
        """Unexpected request exceptions should raise DownloadFailedException."""

        mock_get.side_effect = requests.exceptions.RequestException(
            "Unexpected error"
        )

        with self.assertRaises(DownloadFailedException):
            self.downloader.download(self.url)


if __name__ == "__main__":
    unittest.main()