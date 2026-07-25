"""
Sentence Transformer Provider

Embedding provider backed by Sentence Transformers.

Sprint:
    Sprint 6 - D2
"""

from __future__ import annotations

from sentence_transformers import SentenceTransformer

from src.embeddings.embedding_provider import EmbeddingProvider
from src.embeddings.embedding_result import EmbeddingResult
from src.processing.document_chunk import DocumentChunk


class SentenceTransformerProvider(EmbeddingProvider):
    """
    Embedding provider using Sentence Transformers.
    """

    DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"

    def __init__(
        self,
        model_name: str | None = None,
    ) -> None:
        """
        Initialise the embedding model.

        Args:
            model_name:
                Optional Sentence Transformer model name.
        """

        self._model_name = model_name or self.DEFAULT_MODEL
        self._model = SentenceTransformer(self._model_name)

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimension(self) -> int:
        return self._model.get_sentence_embedding_dimension()

    def embed(
        self,
        chunk: DocumentChunk,
    ) -> EmbeddingResult:
        """
        Generate an embedding for a single document chunk.
        """

        vector = self._model.encode(
            chunk.text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).tolist()

        return EmbeddingResult(
            chunk_id=chunk.chunk_id,
            vector=vector,
            model_name=self.model_name,
            dimension=len(vector),
            metadata={
                "provider": "sentence-transformers",
            },
        )

    def embed_many(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddingResult]:
        """
        Generate embeddings for multiple chunks.
        """

        texts = [chunk.text for chunk in chunks]

        vectors = self._model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return [
            EmbeddingResult(
                chunk_id=chunk.chunk_id,
                vector=vector.tolist(),
                model_name=self.model_name,
                dimension=len(vector),
                metadata={
                    "provider": "sentence-transformers",
                },
            )
            for chunk, vector in zip(chunks, vectors)
        ]