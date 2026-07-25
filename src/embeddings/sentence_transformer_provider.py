"""
Sentence Transformer embedding provider.

Sprint:
    Sprint 6
"""

from __future__ import annotations

from sentence_transformers import SentenceTransformer

from src.embeddings.embedding_provider import EmbeddingProvider
from src.embeddings.embedding_result import EmbeddingResult
from src.processing.document_chunk import DocumentChunk


class SentenceTransformerProvider(EmbeddingProvider):
    """
    Embedding provider backed by Sentence Transformers.
    """

    DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
    ) -> None:
        self._model_name = model_name
        self._model = SentenceTransformer(model_name)

    @property
    def model_name(self) -> str:
        """
        Return the embedding model name.
        """
        return self._model_name

    @property
    def dimension(self) -> int:
        """
        Return the embedding dimension.
        """
        return self._model.get_sentence_embedding_dimension()

    def embed(
        self,
        chunk: DocumentChunk,
    ) -> EmbeddingResult:
        """
        Embed a single document chunk.
        """

        vector = self._model.encode(
            chunk.text,
            normalize_embeddings=True,
        )

        return EmbeddingResult(
            chunk_id=chunk.chunk_id,
            vector=vector.tolist(),
            dimension=self.dimension,
            model_name=self.model_name,
            metadata={
                "provider": "sentence-transformers",
                **chunk.metadata,
            },
        )

    def embed_many(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddingResult]:
        """
        Embed multiple document chunks.
        """

        if not chunks:
            return []

        vectors = self._model.encode(
            [chunk.text for chunk in chunks],
            normalize_embeddings=True,
        )

        return [
            EmbeddingResult(
                chunk_id=chunk.chunk_id,
                vector=vector.tolist(),
                dimension=self.dimension,
                model_name=self.model_name,
                metadata={
                    "provider": "sentence-transformers",
                    **chunk.metadata,
                },
            )
            for chunk, vector in zip(chunks, vectors)
        ]

    def embed_query(
        self,
        question: str,
    ) -> list[float]:
        """
        Embed a natural-language search query.
        """

        vector = self._model.encode(
            question,
            normalize_embeddings=True,
        )

        return vector.tolist()