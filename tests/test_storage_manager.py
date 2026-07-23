"""
test_storage_manager.py

Unit tests for StorageManager.

Uses pytest's tmp_path fixture so every test runs against a real,
isolated filesystem location with no cleanup required.
"""

from __future__ import annotations

import pytest

from src.storage.exceptions import (
    StorageAlreadyExistsError,
    StoragePathError,
)
from src.storage.storage_manager import StorageManager
from src.storage.storage_result import StorageResult


class TestStorageManagerSave:
    def test_save_writes_file_and_returns_storage_result(self, tmp_path):
        manager = StorageManager(base_directory=tmp_path)

        result = manager.save(content=b"hello world", filename="doc.txt")

        assert isinstance(result, StorageResult)
        assert result.file_path == tmp_path / "doc.txt"
        assert result.file_path.read_bytes() == b"hello world"
        assert result.file_size == len(b"hello world")
        assert result.created is True

    def test_save_creates_missing_directories(self, tmp_path):
        manager = StorageManager(base_directory=tmp_path)

        result = manager.save(
            content=b"data",
            filename="doc.pdf",
            subdirectory="fatf/2026",
        )

        assert result.file_path == tmp_path / "fatf" / "2026" / "doc.pdf"
        assert result.file_path.exists()

    def test_save_rejects_empty_filename(self, tmp_path):
        manager = StorageManager(base_directory=tmp_path)

        with pytest.raises(StoragePathError):
            manager.save(content=b"data", filename="")

    def test_save_rejects_filename_with_path_separators(self, tmp_path):
        manager = StorageManager(base_directory=tmp_path)

        with pytest.raises(StoragePathError):
            manager.save(content=b"data", filename="../escape.txt")

    def test_save_raises_when_file_exists_and_overwrite_false(self, tmp_path):
        manager = StorageManager(base_directory=tmp_path)
        manager.save(content=b"v1", filename="doc.txt")

        with pytest.raises(StorageAlreadyExistsError):
            manager.save(content=b"v2", filename="doc.txt")

    def test_save_overwrites_when_overwrite_true(self, tmp_path):
        manager = StorageManager(base_directory=tmp_path)
        manager.save(content=b"v1", filename="doc.txt")

        result = manager.save(
            content=b"v2", filename="doc.txt", overwrite=True
        )

        assert result.file_path.read_bytes() == b"v2"

    def test_save_rejects_subdirectory_that_escapes_base(self, tmp_path):
        manager = StorageManager(base_directory=tmp_path)

        with pytest.raises(StoragePathError):
            manager.save(
                content=b"data",
                filename="doc.txt",
                subdirectory="../../etc",
            )


class TestGenerateFilename:
    def test_generate_filename_is_deterministic(self):
        first = StorageManager.generate_filename("doc-123", "pdf")
        second = StorageManager.generate_filename("doc-123", "pdf")

        assert first == second == "doc-123.pdf"

    def test_generate_filename_sanitizes_unsafe_characters(self):
        result = StorageManager.generate_filename("doc/123:v2", "pdf")

        assert result == "doc_123_v2.pdf"

    def test_generate_filename_strips_leading_dot_from_extension(self):
        result = StorageManager.generate_filename("doc-123", ".pdf")

        assert result == "doc-123.pdf"

    def test_generate_filename_without_extension(self):
        result = StorageManager.generate_filename("doc-123", "")

        assert result == "doc-123"

    def test_generate_filename_rejects_empty_identifier(self):
        with pytest.raises(StoragePathError):
            StorageManager.generate_filename("", "pdf")