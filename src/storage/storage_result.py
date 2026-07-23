"""
storage_result.py

Immutable value object representing the result of a successful
storage operation.

The StorageResult contains information about where a downloaded
document was stored and basic metadata about the stored file.

It intentionally contains no business logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class StorageResult:
    """
    Represents the outcome of a successful storage operation.
    """

    file_path: Path
    file_size: int
    created: bool = True

    @property
    def file_name(self) -> str:
        """
        Return the stored filename.
        """
        return self.file_path.name

    @property
    def directory(self) -> Path:
        """
        Return the directory containing the stored file.
        """
        return self.file_path.parent

    def __str__(self) -> str:
        return (
            f"StorageResult("
            f"file='{self.file_name}', "
            f"size={self.file_size} bytes)"
        )