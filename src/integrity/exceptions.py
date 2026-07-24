"""
exceptions.py

Exception hierarchy for the Integrity module.

Mirrors the design used for Catalogue, Downloads, and Storage:
low-level errors are translated into domain-specific exceptions
so the rest of the FRI platform never needs to catch generic
OSError, ValueError, or hashlib-related errors directly.
"""

from __future__ import annotations


class IntegrityError(Exception):
    """
    Base class for all integrity-related exceptions.
    """


class HashCalculationError(IntegrityError):
    """
    Raised when a SHA256 hash cannot be computed, typically due to
    an unreadable file or invalid input.
    """


class IntegrityMismatchError(IntegrityError):
    """
    Raised when a computed hash does not match the expected hash,
    indicating the file was corrupted, truncated, or tampered with.
    """


class DuplicateContentError(IntegrityError):
    """
    Raised when content matching an existing hash is detected where
    duplicates are not permitted.
    """