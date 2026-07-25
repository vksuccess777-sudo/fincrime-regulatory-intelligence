"""
Index Builder

Sprint:
    Sprint 6 - D3

Coordinates semantic indexing of document chunks.
"""

from __future__ import annotations

from src.embeddings.embedding_provider import EmbeddingProvider
from src.processing.document_chunk import DocumentChunk
from src.vectorstore.vector_store import VectorStore


class IndexBuilder:
    """
    Builds a semantic index from document chunks.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    def index_chunk(
        self,
        chunk: DocumentChunk,
    ) -> None:
        """
        Index a single document chunk.
        """

        embedding = self._embedding_provider.embed(chunk)

        self._vector_store.add(embedding)

    def index_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        """
        Index multiple document chunks.
        """

        embeddings = self._embedding_provider.embed_many(
            chunks,
        )

        self._vector_store.add_many(
            embeddings,
        )