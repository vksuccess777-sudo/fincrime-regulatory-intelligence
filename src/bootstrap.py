"""
Application Bootstrap

Creates and wires together the complete Financial Crime
Regulatory Intelligence application.

Sprint:
    Sprint 7 - Final
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
    Composition root for the application.

    Responsible for constructing all dependencies.
    """

    @staticmethod
    def build_question_answering_service() -> (
        QuestionAnsweringService
    ):
        """
        Build the complete Question Answering Service.
        """

        embedding_provider = (
            SentenceTransformerProvider()
        )

        vector_store = ChromaVectorStore()

        retrieval_engine = RetrievalEngine(
            embedding_provider=embedding_provider,
            vector_store=vector_store,
        )

        context_builder = ContextBuilder()

        prompt_builder = PromptBuilder()

        llm_provider = GroqProvider()

        return QuestionAnsweringService(
            retrieval_engine=retrieval_engine,
            context_builder=context_builder,
            prompt_builder=prompt_builder,
            llm_provider=llm_provider,
        )