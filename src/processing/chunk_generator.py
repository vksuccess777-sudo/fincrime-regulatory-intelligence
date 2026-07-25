"""
Chunk Generator

Converts detected document sections into semantic document chunks.

Sprint:
    Sprint 6 - D5
"""

from __future__ import annotations

from src.processing.document_chunk import DocumentChunk
from src.processing.processing_result import ProcessingResult


class ChunkGenerator:
    """
    Generates semantic chunks from a ProcessingResult.
    """

    def generate(
        self,
        processing_result: ProcessingResult,
    ) -> list[DocumentChunk]:
        """
        Convert detected sections into document chunks.
        """

        parser_result = processing_result.parser_result

        chunks: list[DocumentChunk] = []

        for index, section in enumerate(processing_result.sections):
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{parser_result.document_id}-{index + 1}",
                    text=section.content,
                    page_start=section.start_page,
                    page_end=section.end_page,
                    section_title=section.title,
                    metadata={
                        "document_id": parser_result.document_id,
                        "level": section.level,
                    },
                )
            )

        return chunks