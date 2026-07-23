"""
Custom exceptions for the FRI Download Engine.

Sprint 4 D1 introduces the framework only.
These exceptions provide a clean contract between the
Download Engine and future download components.
"""


class DownloadError(Exception):
    """
    Base exception for all download-related errors.
    """
    pass


class InvalidDownloadURLException(DownloadError):
    """
    Raised when a document does not contain a valid download URL.
    """
    pass


class DownloadNotSupportedException(DownloadError):
    """
    Raised when the download protocol is not currently supported.
    Example:
        ftp://
        file://
    """
    pass