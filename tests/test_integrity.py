"""
test_integrity.py

Unit tests for HashCalculator and IntegrityVerifier.
"""

from __future__ import annotations

import hashlib

import pytest

from src.integrity.exceptions import (
    HashCalculationError,
    IntegrityMismatchError,
)
from src.integrity.hash_calculator import HashCalculator
from src.integrity.integrity_record import IntegrityRecord
from src.integrity.integrity_verifier import IntegrityVerifier


class TestIntegrityRecord:
    def test_valid_record_constructs(self):
        record = IntegrityRecord(
            file_hash="abc123", algorithm="sha256", byte_count=10
        )
        assert record.file_hash == "abc123"
        assert record.byte_count == 10

    def test_rejects_empty_hash(self):
        with pytest.raises(ValueError):
            IntegrityRecord(file_hash="", algorithm="sha256", byte_count=10)

    def test_rejects_empty_algorithm(self):
        with pytest.raises(ValueError):
            IntegrityRecord(file_hash="abc123", algorithm="", byte_count=10)

    def test_rejects_negative_byte_count(self):
        with pytest.raises(ValueError):
            IntegrityRecord(
                file_hash="abc123", algorithm="sha256", byte_count=-1
            )

    def test_matches_is_case_insensitive(self):
        record = IntegrityRecord(
            file_hash="ABC123", algorithm="sha256", byte_count=10
        )
        assert record.matches("abc123") is True
        assert record.matches(" ABC123 ") is True

    def test_matches_returns_false_on_mismatch(self):
        record = IntegrityRecord(
            file_hash="abc123", algorithm="sha256", byte_count=10
        )
        assert record.matches("def456") is False


class TestHashCalculator:
    def test_calculate_from_bytes_matches_hashlib(self):
        calculator = HashCalculator()
        content = b"hello world"

        record = calculator.calculate_from_bytes(content)

        assert record.file_hash == hashlib.sha256(content).hexdigest()
        assert record.algorithm == "sha256"
        assert record.byte_count == len(content)

    def test_calculate_from_bytes_rejects_non_bytes(self):
        calculator = HashCalculator()

        with pytest.raises(HashCalculationError):
            calculator.calculate_from_bytes("not bytes")

    def test_calculate_from_path_matches_hashlib(self, tmp_path):
        calculator = HashCalculator()
        content = b"regulatory document content" * 1000
        file_path = tmp_path / "doc.pdf"
        file_path.write_bytes(content)

        record = calculator.calculate_from_path(file_path)

        assert record.file_hash == hashlib.sha256(content).hexdigest()
        assert record.byte_count == len(content)

    def test_calculate_from_path_raises_when_file_missing(self, tmp_path):
        calculator = HashCalculator()
        missing_path = tmp_path / "does_not_exist.pdf"

        with pytest.raises(HashCalculationError):
            calculator.calculate_from_path(missing_path)

    def test_calculate_from_path_raises_when_path_is_directory(
        self, tmp_path
    ):
        calculator = HashCalculator()

        with pytest.raises(HashCalculationError):
            calculator.calculate_from_path(tmp_path)


class TestIntegrityVerifier:
    def test_verify_bytes_succeeds_on_match(self):
        verifier = IntegrityVerifier()
        content = b"hello world"
        expected_hash = hashlib.sha256(content).hexdigest()

        record = verifier.verify_bytes(content, expected_hash)

        assert record.file_hash == expected_hash

    def test_verify_bytes_raises_on_mismatch(self):
        verifier = IntegrityVerifier()
        content = b"hello world"

        with pytest.raises(IntegrityMismatchError):
            verifier.verify_bytes(content, "wrong_hash")

    def test_verify_file_succeeds_on_match(self, tmp_path):
        verifier = IntegrityVerifier()
        content = b"regulatory document content"
        file_path = tmp_path / "doc.pdf"
        file_path.write_bytes(content)
        expected_hash = hashlib.sha256(content).hexdigest()

        record = verifier.verify_file(file_path, expected_hash)

        assert record.file_hash == expected_hash

    def test_verify_file_raises_on_mismatch(self, tmp_path):
        verifier = IntegrityVerifier()
        file_path = tmp_path / "doc.pdf"
        file_path.write_bytes(b"actual content")

        with pytest.raises(IntegrityMismatchError):
            verifier.verify_file(file_path, "wrong_hash")

    def test_verify_file_propagates_hash_calculation_error(self, tmp_path):
        verifier = IntegrityVerifier()
        missing_path = tmp_path / "does_not_exist.pdf"

        with pytest.raises(HashCalculationError):
            verifier.verify_file(missing_path, "any_hash")

    def test_compute_bytes_returns_record_without_comparison(self):
        verifier = IntegrityVerifier()
        content = b"first time seeing this document"

        record = verifier.compute_bytes(content)

        assert record.file_hash == hashlib.sha256(content).hexdigest()

    def test_compute_file_returns_record_without_comparison(self, tmp_path):
        verifier = IntegrityVerifier()
        content = b"first time seeing this document"
        file_path = tmp_path / "doc.pdf"
        file_path.write_bytes(content)

        record = verifier.compute_file(file_path)

        assert record.file_hash == hashlib.sha256(content).hexdigest()

    def test_verify_bytes_accepts_injected_calculator(self):
        calculator = HashCalculator()
        verifier = IntegrityVerifier(hash_calculator=calculator)
        content = b"hello world"
        expected_hash = hashlib.sha256(content).hexdigest()

        record = verifier.verify_bytes(content, expected_hash)

        assert record.file_hash == expected_hash