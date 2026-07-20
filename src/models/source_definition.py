"""
source_definition.py

Domain model representing a regulatory authority.

This module defines the SourceDefinition class, which is the canonical
representation of a regulator within the FRI platform.

The class contains only metadata and configuration.
It contains no business logic.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import List
from urllib.parse import urlparse


@dataclass(slots=True)
class SourceDefinition:
    """
    Represents a regulatory authority.

    Example:
        FATF
        RBI
        FCA
        OFAC
    """

    identifier: str
    name: str
    jurisdiction: str
    base_url: str
    publication_urls: List[str]
    supported_file_types: List[str]
    connector_class: str
    sync_schedule: str
    enabled: bool = True

    def __post_init__(self) -> None:
        """Validate the object after construction."""

        self.identifier = self.identifier.strip().lower()
        self.name = self.name.strip()
        self.jurisdiction = self.jurisdiction.strip()
        self.connector_class = self.connector_class.strip()
        self.sync_schedule = self.sync_schedule.strip()

        if not self.identifier:
            raise ValueError("identifier cannot be empty")

        if not self.name:
            raise ValueError("name cannot be empty")

        if not self.jurisdiction:
            raise ValueError("jurisdiction cannot be empty")

        if not self.connector_class:
            raise ValueError("connector_class cannot be empty")

        if not self.sync_schedule:
            raise ValueError("sync_schedule cannot be empty")

        self._validate_url(self.base_url, "base_url")

        if not self.publication_urls:
            raise ValueError("publication_urls cannot be empty")

        for url in self.publication_urls:
            self._validate_url(url, "publication_url")

        if not self.supported_file_types:
            raise ValueError("supported_file_types cannot be empty")

    @staticmethod
    def _validate_url(url: str, field_name: str) -> None:
        """Validate that a URL is syntactically correct."""

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"{field_name} must use http or https")

        if not parsed.netloc:
            raise ValueError(f"{field_name} is invalid")

    def to_dict(self) -> dict:
        """Convert object to dictionary."""

        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SourceDefinition":
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
    def from_json(cls, json_string: str) -> "SourceDefinition":
        """Deserialize object from JSON."""

        data = json.loads(json_string)
        return cls.from_dict(data)

    def __str__(self) -> str:
        return (
            f"SourceDefinition("
            f"identifier='{self.identifier}', "
            f"name='{self.name}', "
            f"jurisdiction='{self.jurisdiction}')"
        )