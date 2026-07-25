"""
End-to-End Indexing Pipeline

Sprint:
    Sprint 6 - D5

Coordinates semantic indexing of processed document chunks.
"""

from __future__ import annotations

from src.embeddings.embedding_provider import EmbeddingProvider
from src.indexing.index_builder import IndexBuilder
from src.processing.document_chunk import DocumentChunk
from src.vectorstore.vector_store import VectorStore


class IndexingPipeline:
    """
    High-level indexing pipeline.

    Coordinates converting document chunks into embeddings
    and storing them inside the configured vector store.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self._builder = IndexBuilder(
            embedding_provider,
            vector_store,
        )

    def index_chunk(
        self,
        chunk: DocumentChunk,
    ) -> None:
        """
        Index a single document chunk.
        """
        self._builder.index_chunk(chunk)

    def index_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        """
        Index multiple document chunks.
        """
        self._builder.index_chunks(chunks)