"""
FRI - Knowledge Catalogue Store

Sprint 2
Deliverable D4

Responsible for persisting and loading the
Knowledge Catalogue from disk.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.models.document_metadata import DocumentMetadata
from src.models.source_definition import SourceDefinition


class CatalogueStore:
    """
    Handles persistence of the Knowledge Catalogue.
    """

    def __init__(self, catalogue_path: str):

        self._catalogue_path = Path(catalogue_path)

        # Create directory if required
        self._catalogue_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Create an empty catalogue if it doesn't exist
        if not self._catalogue_path.exists():
            with self._catalogue_path.open(
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    {
                        "sources": [],
                        "documents": [],
                    },
                    file,
                    indent=4,
                )

    def load(
        self,
    ) -> tuple[list[SourceDefinition], list[DocumentMetadata]]:

        with self._catalogue_path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        sources = [
            SourceDefinition.from_dict(item)
            for item in data.get("sources", [])
        ]

        documents = [
            DocumentMetadata.from_dict(item)
            for item in data.get("documents", [])
        ]

        return sources, documents

    def save(
        self,
        sources: list[SourceDefinition],
        documents: list[DocumentMetadata],
    ) -> None:

        data = {
            "sources": [
                source.to_dict()
                for source in sources
            ],
            "documents": [
                document.to_dict()
                for document in documents
            ],
        }

        with self._catalogue_path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                sort_keys=True,
            )

    def exists(self) -> bool:
        """
        Returns True if the catalogue file exists.
        """

        return self._catalogue_path.exists()