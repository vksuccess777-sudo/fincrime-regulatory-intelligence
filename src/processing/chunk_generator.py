"""
Semantic document chunk generator.

Transforms DocumentSection objects into immutable DocumentChunk
instances suitable for embedding and semantic retrieval.
"""

from __future__ import annotations

from typing import Iterable

from src.processing.document_chunk import DocumentChunk
from src.processing.document_section import DocumentSection


class ChunkGenerator:
    """Generate semantic chunks from document sections."""

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 0,
    ) -> None:

        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")

        if overlap < 0:
            raise ValueError("overlap cannot be negative.")

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size."
            )

        self._chunk_size = chunk_size
        self._overlap = overlap

    def generate(
        self,
        sections: Iterable[DocumentSection],
    ) -> list[DocumentChunk]:

        chunks: list[DocumentChunk] = []

        counter = 1

        for section in sections:

            text = section.content.strip()

            if not text:
                continue

            start = 0

            while start < len(text):

                end = min(
                    start + self._chunk_size,
                    len(text),
                )

                chunks.append(
                    DocumentChunk(
                        chunk_id=f"chunk-{counter:05d}",
                        text=text[start:end],
                        page_start=section.start_page,
                        page_end=section.end_page,
                        section_title=section.title,
                        metadata={},
                    )
                )

                counter += 1

                if end == len(text):
                    break

                start = end - self._overlap

        return chunks