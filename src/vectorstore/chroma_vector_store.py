"""
ChromaDB-backed vector store.

Sprint:
    Sprint 6 - D3
"""

from __future__ import annotations

from pathlib import Path

import chromadb

from src.embeddings.embedding_result import EmbeddingResult
from src.vectorstore.vector_store import VectorStore


class ChromaVectorStore(VectorStore):
    """
    Production vector store backed by ChromaDB.
    """

    COLLECTION_NAME = "document_chunks"

    def __init__(
        self,
        persist_directory: str | Path = "data/database/chroma",
    ) -> None:
        self._persist_directory = str(persist_directory)

        self._client = chromadb.PersistentClient(
            path=self._persist_directory,
        )

        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
        )

    def add(
        self,
        embedding: EmbeddingResult,
    ) -> None:
        self._collection.add(
            ids=[embedding.chunk_id],
            embeddings=[embedding.vector],
            metadatas=[
                {
                    "model_name": embedding.model_name,
                    "dimension": embedding.dimension,
                    **embedding.metadata,
                }
            ],
        )

    def add_many(
        self,
        embeddings: list[EmbeddingResult],
    ) -> None:
        if not embeddings:
            return

        self._collection.add(
            ids=[e.chunk_id for e in embeddings],
            embeddings=[e.vector for e in embeddings],
            metadatas=[
                {
                    "model_name": e.model_name,
                    "dimension": e.dimension,
                    **e.metadata,
                }
                for e in embeddings
            ],
        )

    def search(
        self,
        query_vector: list[float],
        k: int = 5,
    ) -> list[EmbeddingResult]:
        """
        Search for the most similar embeddings.
        """

        results = self._collection.query(
            query_embeddings=[query_vector],
            n_results=k,
            include=[
                "embeddings",
                "metadatas",
            ],
        )

        ids = results["ids"][0]

        embeddings = results.get("embeddings")
        metadatas = results.get("metadatas")

        if embeddings is None or metadatas is None:
            return []

        vectors = embeddings[0]
        metadata_list = metadatas[0]

        output: list[EmbeddingResult] = []

        for chunk_id, vector, metadata in zip(
            ids,
            vectors,
            metadata_list,
        ):
            metadata = dict(metadata)

            output.append(
                EmbeddingResult(
                    chunk_id=chunk_id,
                    vector=list(vector),
                    dimension=int(metadata.pop("dimension")),
                    model_name=str(metadata.pop("model_name")),
                    metadata=metadata,
                )
            )

        return output

    def delete(
        self,
        chunk_id: str,
    ) -> None:
        self._collection.delete(
            ids=[chunk_id],
        )

    def clear(self) -> None:
        try:
            self._client.delete_collection(
                self.COLLECTION_NAME,
            )
        except Exception:
            pass

        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
        )

    def count(self) -> int:
        return self._collection.count()