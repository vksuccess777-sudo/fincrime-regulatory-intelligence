"""
Question Answering Integration Test

Sprint:
    Sprint 7 - Final

Exercises the complete RAG pipeline using the project's
mock implementations.
"""

from __future__ import annotations

from src.embeddings.embedding_result import EmbeddingResult
from src.embeddings.mock_embedding_provider import (
    MockEmbeddingProvider,
)
from src.llm.mock_llm_provider import MockLLMProvider
from src.processing.document_chunk import DocumentChunk
from src.prompts.prompt_builder import PromptBuilder
from src.rag.context_builder import ContextBuilder
from src.retrieval.retrieval_engine import RetrievalEngine
from src.services.question_answering_service import (
    QuestionAnsweringService,
)
from src.vectorstore.mock_vector_store import MockVectorStore


def test_complete_question_answering_pipeline():

    embedding_provider = MockEmbeddingProvider()

    vector_store = MockVectorStore()

    chunk = DocumentChunk(
        chunk_id="chunk-1",
        text="Customer Due Diligence is required before establishing a business relationship.",
        page_start=1,
        page_end=2,
        section_title="Recommendation 10",
        metadata={
            "source": "FATF",
        },
    )

    embedding = embedding_provider.embed(chunk)

    embedding = EmbeddingResult(
        chunk_id=embedding.chunk_id,
        vector=embedding.vector,
        model_name=embedding.model_name,
        dimension=embedding.dimension,
        metadata={
            "text": chunk.text,
            "source": chunk.metadata["source"],
            "section_title": chunk.section_title,
            "page_start": chunk.page_start,
            "page_end": chunk.page_end,
        },
    )

    vector_store.add(embedding)

    retrieval_engine = RetrievalEngine(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    qa = QuestionAnsweringService(
        retrieval_engine=retrieval_engine,
        context_builder=ContextBuilder(),
        prompt_builder=PromptBuilder(),
        llm_provider=MockLLMProvider(),
    )

    response = qa.answer(
        "What is Customer Due Diligence?"
    )

    assert response is not None

    assert "MOCK RESPONSE" in response.text

    assert response.metadata["provider"] == "Mock"

    assert response.metadata["model"] == "mock-llm-v1"

    assert response.metadata["retrieved_chunks"] == 1