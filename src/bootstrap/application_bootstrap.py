"""
Application Bootstrap

Sprint:
    Sprint 8 - D2

Central composition root for the FRI application.
"""

from __future__ import annotations

from src.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)
from src.llm.groq_provider import GroqProvider
from src.prompts.prompt_builder import PromptBuilder
from src.rag.context_builder import ContextBuilder
from src.retrieval.retrieval_engine import RetrievalEngine
from src.services.question_answering_service import (
    QuestionAnsweringService,
)
from src.vectorstore.chroma_vector_store import (
    ChromaVectorStore,
)


class ApplicationBootstrap:
    """
    Creates singleton production services.
    """

    def __init__(self) -> None:

        self._embedding_provider = None
        self._vector_store = None
        self._retrieval_engine = None

        self._context_builder = None
        self._prompt_builder = None
        self._llm_provider = None
        self._question_answering_service = None

    def embedding_provider(self) -> SentenceTransformerProvider:

        if self._embedding_provider is None:
            self._embedding_provider = (
                SentenceTransformerProvider()
            )

        return self._embedding_provider

    def vector_store(self) -> ChromaVectorStore:

        if self._vector_store is None:
            self._vector_store = (
                ChromaVectorStore()
            )

        return self._vector_store

    def retrieval_engine(self) -> RetrievalEngine:

        if self._retrieval_engine is None:
            self._retrieval_engine = RetrievalEngine(
                embedding_provider=self.embedding_provider(),
                vector_store=self.vector_store(),
            )

        return self._retrieval_engine

    def context_builder(self) -> ContextBuilder:

        if self._context_builder is None:
            self._context_builder = ContextBuilder()

        return self._context_builder

    def prompt_builder(self) -> PromptBuilder:

        if self._prompt_builder is None:
            self._prompt_builder = PromptBuilder()

        return self._prompt_builder

    def llm_provider(self) -> GroqProvider:

        if self._llm_provider is None:
            self._llm_provider = GroqProvider()

        return self._llm_provider

    def question_answering_service(
        self,
    ) -> QuestionAnsweringService:

        if self._question_answering_service is None:

            self._question_answering_service = (
                QuestionAnsweringService(
                    retrieval_engine=self.retrieval_engine(),
                    context_builder=self.context_builder(),
                    prompt_builder=self.prompt_builder(),
                    llm_provider=self.llm_provider(),
                )
            )

        return self._question_answering_service