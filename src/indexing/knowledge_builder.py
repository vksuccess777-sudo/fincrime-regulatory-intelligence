"""
Knowledge Builder

Sprint:
    Sprint 8 - D1

Coordinates indexing an entire collection of regulatory
documents into the knowledge base.
"""

from __future__ import annotations

from pathlib import Path

from src.indexing.knowledge_build_result import (
    KnowledgeBuildResult,
)
from src.indexing.knowledge_indexer import KnowledgeIndexer


class KnowledgeBuilder:
    """
    Builds an entire regulatory knowledge base by indexing
    every supported document within a folder.
    """

    def __init__(
        self,
        knowledge_indexer: KnowledgeIndexer,
    ) -> None:
        self._knowledge_indexer = knowledge_indexer

    def build(
        self,
        folder: Path,
    ) -> KnowledgeBuildResult:
        """
        Index every PDF document found in the supplied folder.
        """

        pdf_files = sorted(folder.rglob("*.pdf"))

        documents_processed = 0
        sections_detected = 0
        chunks_generated = 0
        embeddings_created = 0
        vectors_stored = 0
        errors: list[str] = []

        for pdf in pdf_files:
            try:
                result = self._knowledge_indexer.index_document(
                    document_id=pdf.stem,
                    file_path=pdf,
                )

                documents_processed += result.documents_processed
                sections_detected += result.sections_detected
                chunks_generated += result.chunks_generated
                embeddings_created += result.embeddings_created
                vectors_stored += result.vectors_stored
                errors.extend(result.errors)

            except Exception as ex:
                errors.append(
                    f"{pdf.name}: {str(ex)}"
                )

        return KnowledgeBuildResult(
            documents_processed=documents_processed,
            sections_detected=sections_detected,
            chunks_generated=chunks_generated,
            embeddings_created=embeddings_created,
            vectors_stored=vectors_stored,
            errors=errors,
        )