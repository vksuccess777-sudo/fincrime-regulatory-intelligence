"""
integrity_record.py

Immutable value object representing the result of a successful
integrity hash computation.

IntegrityRecord contains only what was computed and how — it does
not know about files being downloaded, stored, or catalogued, and
it does not perform any comparison or verification itself. That
responsibility belongs to IntegrityVerifier.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IntegrityRecord:
    """
    Represents the outcome of a successful hash computation.
    """

    file_hash: str
    algorithm: str
    byte_count: int

    def __post_init__(self) -> None:
        if not self.file_hash:
            raise ValueError("file_hash must not be empty.")
        if not self.algorithm:
            raise ValueError("algorithm must not be empty.")
        if self.byte_count < 0:
            raise ValueError("byte_count must not be negative.")

    def matches(self, other_hash: str) -> bool:
        """
        Case-insensitive comparison against another hash string.
        """
        return self.file_hash.lower() == other_hash.strip().lower()

    def __str__(self) -> str:
        return (
            f"IntegrityRecord("
            f"algorithm={self.algorithm}, "
            f"hash={self.file_hash[:12]}..., "
            f"bytes={self.byte_count})"
        )