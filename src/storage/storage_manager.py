"""
storage_manager.py

StorageManager persists downloaded document bytes to local disk and
returns a StorageResult describing what was written.

Responsibilities:
    - Create destination directories automatically
    - Write downloaded bytes to disk
    - Generate deterministic, filesystem-safe filenames
    - Translate low-level OS errors into StorageError subclasses
    - Prevent path traversal outside the configured storage root

StorageManager does not download files and does not compute
integrity hashes (SHA256 is Sprint 4 D4). It is a pure storage
abstraction with a single responsibility: getting bytes onto disk
safely and predictably.
"""

from __future__ import annotations

import string
from pathlib import Path

from src.storage.exceptions import (
    StorageAlreadyExistsError,
    StoragePathError,
    StorageWriteError,
)
from src.storage.storage_result import StorageResult

_SAFE_FILENAME_CHARS = set(string.ascii_letters + string.digits + "-_")


class StorageManager:
    """
    Persists downloaded document bytes to a local storage root.

    All paths are resolved relative to `base_directory`. Callers
    supply raw bytes and a filename (or an identifier to derive one
    from); StorageManager handles directory creation, collision
    checks, and error translation.
    """

    def __init__(self, base_directory: Path | str) -> None:
        self._base_directory = Path(base_directory)

    @property
    def base_directory(self) -> Path:
        """Return the root directory this manager writes under."""
        return self._base_directory

    def save(
        self,
        content: bytes,
        filename: str,
        subdirectory: str | None = None,
        overwrite: bool = False,
    ) -> StorageResult:
        """
        Write `content` to disk under `filename`.

        Args:
            content: Raw bytes to persist.
            filename: Target filename (not a path).
            subdirectory: Optional path segment under base_directory.
            overwrite: If False (default), raises when the target
                file already exists.

        Returns:
            StorageResult describing the written file.

        Raises:
            StoragePathError: Invalid filename/subdirectory, or a
                directory could not be created.
            StorageAlreadyExistsError: File exists and overwrite is
                False.
            StorageWriteError: The write itself failed.
        """
        if not filename or not filename.strip():
            raise StoragePathError("filename must not be empty.")

        if any(sep in filename for sep in ("/", "\\")):
            raise StoragePathError(
                f"filename must not contain path separators: '{filename}'"
            )

        target_dir = self._resolve_directory(subdirectory)
        self._ensure_directory(target_dir)

        target_path = target_dir / filename

        if target_path.exists() and not overwrite:
            raise StorageAlreadyExistsError(
                f"File already exists and overwrite is disabled: {target_path}"
            )

        try:
            target_path.write_bytes(content)
        except OSError as exc:
            raise StorageWriteError(
                f"Failed to write file '{target_path}': {exc}"
            ) from exc

        try:
            file_size = target_path.stat().st_size
        except OSError as exc:
            raise StorageWriteError(
                f"File written but could not be stat'd: '{target_path}': {exc}"
            ) from exc

        return StorageResult(
            file_path=target_path,
            file_size=file_size,
            created=True,
        )

    @staticmethod
    def generate_filename(identifier: str, extension: str) -> str:
        """
        Build a deterministic, filesystem-safe filename from an
        identifier (e.g. a catalogue key or document ID).

        Same identifier + extension always produces the same
        filename, which is what makes downstream duplicate
        detection (D4) reliable.
        """
        if not identifier or not identifier.strip():
            raise StoragePathError("identifier must not be empty.")

        safe_id = StorageManager._sanitize(identifier.strip())
        ext = extension.strip().lstrip(".")

        return f"{safe_id}.{ext}" if ext else safe_id

    def _resolve_directory(self, subdirectory: str | None) -> Path:
        base_resolved = self._base_directory.resolve()

        if not subdirectory:
            return base_resolved

        candidate = (self._base_directory / subdirectory).resolve()

        try:
            candidate.relative_to(base_resolved)
        except ValueError as exc:
            raise StoragePathError(
                f"subdirectory '{subdirectory}' escapes the storage root."
            ) from exc

        return candidate

    def _ensure_directory(self, directory: Path) -> None:
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise StoragePathError(
                f"Failed to create storage directory '{directory}': {exc}"
            ) from exc

    @staticmethod
    def _sanitize(value: str) -> str:
        return "".join(
            c if c in _SAFE_FILENAME_CHARS else "_" for c in value
        )