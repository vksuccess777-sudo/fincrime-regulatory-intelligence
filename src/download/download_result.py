"""
download_result.py

Represents the result of a successful HTTP download.

This object contains the downloaded content together with
basic HTTP metadata. It deliberately does not perform any
file storage or integrity validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class DownloadResult:
    """
    Represents the result of downloading a regulatory document.

    This object is produced by the HTTPDownloader and will later
    be consumed by:

        - Storage Manager (Sprint 4 D3)
        - Integrity Validator (Sprint 4 D4)
        - Catalogue Integration (Sprint 4 D5)
    """

    # ------------------------------------------------------------------
    # Request Information
    # ------------------------------------------------------------------

    url: str

    # ------------------------------------------------------------------
    # HTTP Response
    # ------------------------------------------------------------------

    status_code: int
    content: bytes

    # ------------------------------------------------------------------
    # Optional Metadata
    # ------------------------------------------------------------------

    content_type: Optional[str] = None
    content_length: Optional[int] = None

    @property
    def is_success(self) -> bool:
        """
        Indicates whether the HTTP request was successful.
        """

        return 200 <= self.status_code < 300

    def __len__(self) -> int:
        """
        Returns the size of the downloaded content.
        """

        return len(self.content)

    def __str__(self) -> str:
        return (
            f"DownloadResult("
            f"status_code={self.status_code}, "
            f"bytes={len(self.content)}, "
            f"url='{self.url}')"
        )