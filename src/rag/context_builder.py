"""
Context Builder

Builds structured retrieval context for LLM prompts.

Sprint:
    Sprint 7 - D2

Responsibilities
----------------
- Convert retrieval results into readable context.
- Preserve source attribution.
- Preserve section titles.
- Preserve page references.
"""

from __future__ import annotations

from src.embeddings.embedding_result import EmbeddingResult


class ContextBuilder:
    """
    Converts retrieval results into prompt-ready context.
    """

    def build(
        self,
        results: list[EmbeddingResult],
    ) -> str:
        """
        Build formatted context from retrieval results.
        """

        if not results:
            return "No supporting context available."

        blocks: list[str] = []

        for result in results:

            metadata = result.metadata

            source = metadata.get(
                "source",
                "Unknown",
            )

            section = metadata.get(
                "section_title",
                "Unknown Section",
            )

            page_start = metadata.get(
                "page_start",
                "?",
            )

            page_end = metadata.get(
                "page_end",
                page_start,
            )

            text = metadata.get(
                "text",
                "",
            ).strip()

            block = (
                f"Source: {source}\n"
                f"Section: {section}\n"
                f"Pages: {page_start}-{page_end}\n\n"
                f"{text}"
            )

            blocks.append(block)

        return "\n\n" + ("\n" + "-" * 60 + "\n\n").join(blocks)