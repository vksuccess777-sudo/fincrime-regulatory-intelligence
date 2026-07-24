"""
hash_calculator.py

Computes SHA256 hashes over raw bytes or files on disk.

HashCalculator has one job: turn content into an IntegrityRecord.
It does not compare hashes, does not raise on mismatch, and does
not know about storage paths, downloads, or the catalogue. That
keeps it trivially reusable anywhere a hash is needed.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from src.integrity.exceptions import HashCalculationError
from src.integrity.integrity_record import IntegrityRecord

_ALGORITHM = "sha256"
_CHUNK_SIZE = 65536  # 64 KB, keeps memory flat for large PDFs


class HashCalculator:
    """
    Computes SHA256 hashes and returns IntegrityRecord instances.
    """

    def calculate_from_bytes(self, content: bytes) -> IntegrityRecord:
        """
        Compute the SHA256 hash of in-memory bytes.

        Args:
            content: Raw bytes to hash.

        Returns:
            IntegrityRecord describing the computed hash.

        Raises:
            HashCalculationError: content is not bytes-like.
        """
        if not isinstance(content, (bytes, bytearray)):
            raise HashCalculationError(
                f"content must be bytes, got {type(content).__name__}."
            )

        digest = hashlib.sha256(content).hexdigest()

        return IntegrityRecord(
            file_hash=digest,
            algorithm=_ALGORITHM,
            byte_count=len(content),
        )

    def calculate_from_path(self, file_path: Path | str) -> IntegrityRecord:
        """
        Compute the SHA256 hash of a file on disk, streaming it in
        fixed-size chunks so large documents don't need to be
        loaded fully into memory.

        Args:
            file_path: Path to the file to hash.

        Returns:
            IntegrityRecord describing the computed hash.

        Raises:
            HashCalculationError: The file does not exist or cannot
                be read.
        """
        path = Path(file_path)

        if not path.is_file():
            raise HashCalculationError(
                f"Cannot hash '{path}': file does not exist."
            )

        hasher = hashlib.sha256()
        byte_count = 0

        try:
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(_CHUNK_SIZE), b""):
                    hasher.update(chunk)
                    byte_count += len(chunk)
        except OSError as exc:
            raise HashCalculationError(
                f"Failed to read '{path}' for hashing: {exc}"
            ) from exc

        return IntegrityRecord(
            file_hash=hasher.hexdigest(),
            algorithm=_ALGORITHM,
            byte_count=byte_count,
        )