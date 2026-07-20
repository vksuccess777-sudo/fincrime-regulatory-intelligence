"""
document_metadata.py

Domain model representing a regulatory publication.

This module defines the DocumentMetadata class, which is the canonical
metadata representation for every regulatory document discovered by
the FRI platform.

The class stores metadata only.
It does not contain document content.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import List, Optional
from urllib.parse import urlparse


@dataclass(slots=True)
class DocumentMetadata:
    """
    Represents a regulatory publication.

    This object is exchanged between all major platform components:
        - Knowledge Agent
        - Catalogue Manager
        - Processing Pipeline
        - Vector Database
        - Regulatory Intelligence
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    document_id: str
    source_identifier: str
    title: str

    # ------------------------------------------------------------------
    # Source
    # ------------------------------------------------------------------

    authority: str
    jurisdiction: str
    publication_url: str

    # ------------------------------------------------------------------
    # Publication
    # ------------------------------------------------------------------

    publication_date: Optional[str] = None
    effective_date: Optional[str] = None
    version: str = "1.0"
    status: str = "ACTIVE"

    # ------------------------------------------------------------------
    # Storage
    # ------------------------------------------------------------------

    file_name: Optional[str] = None
    file_type: Optional[str] = None
    local_path: Optional[str] = None
    file_size: Optional[int] = None

    # ------------------------------------------------------------------
    # Integrity
    # ------------------------------------------------------------------

    sha256_hash: Optional[str] = None

    # ------------------------------------------------------------------
    # Processing
    # ------------------------------------------------------------------

    processing_status: str = "DISCOVERED"

    # ------------------------------------------------------------------
    # Audit
    # ------------------------------------------------------------------

    first_seen: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    last_checked: Optional[str] = None
    last_downloaded: Optional[str] = None
    last_updated: Optional[str] = None

    processing_errors: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:

        self.document_id = self.document_id.strip()
        self.source_identifier = self.source_identifier.strip().lower()
        self.title = self.title.strip()
        self.authority = self.authority.strip()
        self.jurisdiction = self.jurisdiction.strip()

        if not self.document_id:
            raise ValueError("document_id cannot be empty")

        if not self.source_identifier:
            raise ValueError("source_identifier cannot be empty")

        if not self.title:
            raise ValueError("title cannot be empty")

        if not self.authority:
            raise ValueError("authority cannot be empty")

        if not self.jurisdiction:
            raise ValueError("jurisdiction cannot be empty")

        self._validate_url(self.publication_url)

        if self.file_size is not None and self.file_size < 0:
            raise ValueError("file_size cannot be negative")

    @staticmethod
    def _validate_url(url: str) -> None:

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            raise ValueError("publication_url must use http or https")

        if not parsed.netloc:
            raise ValueError("publication_url is invalid")

    def to_dict(self) -> dict:
        """Return dictionary representation."""

        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "DocumentMetadata":
        """Create object from dictionary."""

        return cls(**data)

    def to_json(self) -> str:
        """Serialize object to formatted JSON."""

        return json.dumps(
            self.to_dict(),
            indent=4,
            sort_keys=True,
        )

    @classmethod
    def from_json(cls, json_string: str) -> "DocumentMetadata":
        """Deserialize object from JSON."""

        data = json.loads(json_string)

        return cls.from_dict(data)

    def add_processing_error(self, message: str) -> None:
        """Record a processing error."""

        self.processing_errors.append(message)

    def __str__(self) -> str:
        return (
            f"DocumentMetadata("
            f"document_id='{self.document_id}', "
            f"title='{self.title}', "
            f"status='{self.processing_status}')"
        )