"""
http_downloader.py

HTTP Downloader for the FRI platform.

Sprint 4 D2 introduces the capability to retrieve regulatory
documents over HTTP/HTTPS.

Responsibilities:
    - Download document content
    - Validate HTTP response
    - Return DownloadResult

This component DOES NOT:
    - Save files
    - Calculate hashes
    - Update the catalogue
"""

from __future__ import annotations

import requests
from requests.exceptions import ConnectionError, RequestException, Timeout

from src.download.download_result import DownloadResult
from src.download.exceptions import (
    ConnectionFailedException,
    DownloadFailedException,
    DownloadTimeoutException,
    HTTPStatusException,
)


class HTTPDownloader:
    """
    Downloads regulatory documents over HTTP/HTTPS.
    """

    DEFAULT_TIMEOUT = 30

    def download(
        self,
        url: str,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> DownloadResult:
        """
        Download a document from the supplied URL.

        Parameters
        ----------
        url : str
            Publication URL.

        timeout : int
            HTTP timeout in seconds.

        Returns
        -------
        DownloadResult

        Raises
        ------
        ConnectionFailedException
        DownloadTimeoutException
        HTTPStatusException
        DownloadFailedException
        """

        try:
            response = requests.get(
                url,
                timeout=timeout,
                allow_redirects=True,
            )

        except Timeout as ex:
            raise DownloadTimeoutException(
                f"Download timed out for '{url}'."
            ) from ex

        except ConnectionError as ex:
            raise ConnectionFailedException(
                f"Unable to connect to '{url}'."
            ) from ex

        except RequestException as ex:
            raise DownloadFailedException(
                str(ex)
            ) from ex

        if not response.ok:
            raise HTTPStatusException(
                response.status_code,
                url,
            )

        return DownloadResult(
            url=url,
            status_code=response.status_code,
            content=response.content,
            content_type=response.headers.get("Content-Type"),
            content_length=len(response.content),
        )