"""
integrity_verifier.py

Orchestrates integrity verification: computes a hash via
HashCalculator and compares it against an expected value, raising
IntegrityMismatchError on failure.

IntegrityVerifier contains no hashing logic itself (that belongs to
HashCalculator) and no file-writing logic (that belongs to
StorageManager). It is a pure comparison/orchestration layer, same
role DownloadEngine plays over HTTPDownloader.
"""

from __future__ import annotations

from pathlib import Path

from src.integrity.exceptions import IntegrityMismatchError
from src.integrity.hash_calculator import HashCalculator
from src.integrity.integrity_record import IntegrityRecord


class IntegrityVerifier:
    """
    Verifies content integrity by comparing computed hashes against
    expected values.
    """

    def __init__(self, hash_calculator: HashCalculator | None = None) -> None:
        self._hash_calculator = hash_calculator or HashCalculator()

    def verify_bytes(
        self, content: bytes, expected_hash: str
    ) -> IntegrityRecord:
        """
        Compute the hash of `content` and verify it matches
        `expected_hash`.

        Args:
            content: Raw bytes to verify.
            expected_hash: The hash the content is expected to
                produce.

        Returns:
            IntegrityRecord for the verified content.

        Raises:
            IntegrityMismatchError: The computed hash does not
                match expected_hash.
        """
        record = self._hash_calculator.calculate_from_bytes(content)
        self._assert_match(record, expected_hash)
        return record

    def verify_file(
        self, file_path: Path | str, expected_hash: str
    ) -> IntegrityRecord:
        """
        Compute the hash of the file at `file_path` and verify it
        matches `expected_hash`.

        Args:
            file_path: Path to the file to verify.
            expected_hash: The hash the file is expected to
                produce.

        Returns:
            IntegrityRecord for the verified file.

        Raises:
            HashCalculationError: The file could not be read.
            IntegrityMismatchError: The computed hash does not
                match expected_hash.
        """
        record = self._hash_calculator.calculate_from_path(file_path)
        self._assert_match(record, expected_hash)
        return record

    def compute_bytes(self, content: bytes) -> IntegrityRecord:
        """
        Compute the hash of `content` with no comparison — used
        when there is no expected hash yet (e.g. first time a
        document is seen).
        """
        return self._hash_calculator.calculate_from_bytes(content)

    def compute_file(self, file_path: Path | str) -> IntegrityRecord:
        """
        Compute the hash of the file at `file_path` with no
        comparison — used when there is no expected hash yet.
        """
        return self._hash_calculator.calculate_from_path(file_path)

    @staticmethod
    def _assert_match(record: IntegrityRecord, expected_hash: str) -> None:
        if not record.matches(expected_hash):
            raise IntegrityMismatchError(
                f"Integrity check failed: expected "
                f"'{expected_hash}', got '{record.file_hash}'."
            )