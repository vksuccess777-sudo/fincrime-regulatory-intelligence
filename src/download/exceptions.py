"""
Custom exceptions for the FRI Download Engine.

Sprint 4 D1 introduced the framework.

Sprint 4 D2 extends the exception hierarchy to support
HTTP download operations.
"""


class DownloadError(Exception):
    """
    Base exception for all download-related errors.
    """
    pass


class InvalidDownloadURLException(DownloadError):
    """
    Raised when a document does not contain a valid
    publication URL.
    """
    pass


class DownloadNotSupportedException(DownloadError):
    """
    Raised when the download protocol is not supported.

    Example:
        ftp://
        file://
    """
    pass


class DownloadFailedException(DownloadError):
    """
    Raised when a document download fails.
    """
    pass


class HTTPStatusException(DownloadFailedException):
    """
    Raised when an HTTP request returns a non-success
    status code.
    """

    def __init__(self, status_code: int, url: str):
        self.status_code = status_code
        self.url = url

        super().__init__(
            f"HTTP request failed with status "
            f"{status_code} for '{url}'."
        )


class ConnectionFailedException(DownloadFailedException):
    """
    Raised when a connection to the remote server
    cannot be established.
    """
    pass


class DownloadTimeoutException(DownloadFailedException):
    """
    Raised when an HTTP request exceeds the configured
    timeout.
    """
    pass