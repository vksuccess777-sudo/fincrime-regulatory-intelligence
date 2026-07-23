"""
exceptions.py

Exception hierarchy for the Storage module.

The StorageManager converts low-level filesystem errors
into domain-specific exceptions that are easier for the
rest of the FRI platform to understand.
"""

from __future__ import annotations


class StorageError(Exception):
    """
    Base class for all storage-related exceptions.
    """


class StoragePathError(StorageError):
    """
    Raised when a storage path is invalid.
    """


class StorageWriteError(StorageError):
    """
    Raised when a file cannot be written.
    """


class StorageReadError(StorageError):
    """
    Raised when a file cannot be read.
    """


class StorageAlreadyExistsError(StorageError):
    """
    Raised when overwrite is disabled and
    the destination file already exists.
    """