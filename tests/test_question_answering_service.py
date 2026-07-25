import pytest

from src.embeddings.embedding_result import EmbeddingResult
from src.llm.llm_response import LLMResponse
from src.llm.mock_llm_provider import MockLLMProvider
from src.prompts.prompt_builder import PromptBuilder
from src.rag.context_builder import ContextBuilder
from src.services.question_answering_service import (
    QuestionAnsweringService,
)


class MockRetrievalEngine:
    """
    Deterministic retrieval engine for testing.
    """

    def __init__(self) -> None:
        self.last_question = None
        self.last_k = None

    def search(
        self,
        question: str,
        k: int = 5,
    ):
        self.last_question = question
        self.last_k = k

        return [
            EmbeddingResult(
                chunk_id="chunk-1",
                vector=[0.1, 0.2, 0.3],
                model_name="mock-embedding",
                dimension=3,
                metadata={
                    "text": "Enhanced Due Diligence is required.",
                    "source": "FATF",
                    "section_title": "Recommendation 10",
                    "page_start": 4,
                    "page_end": 5,
                },
            )
        ]


class EmptyRetrievalEngine:
    """
    Always returns no search results.
    """

    def search(
        self,
        question: str,
        k: int = 5,
    ):
        return []


def create_service(
    retrieval_engine,
):
    return QuestionAnsweringService(
        retrieval_engine=retrieval_engine,
        context_builder=ContextBuilder(),
        prompt_builder=PromptBuilder(),
        llm_provider=MockLLMProvider(),
    )


def test_answer_returns_llm_response():
    service = create_service(
        MockRetrievalEngine(),
    )

    response = service.answer(
        "What is Enhanced Due Diligence?",
    )

    assert isinstance(
        response,
        LLMResponse,
    )

    assert "MOCK RESPONSE" in response.text


def test_question_passed_to_retrieval_engine():
    retrieval = MockRetrievalEngine()

    service = create_service(
        retrieval,
    )

    question = "What is Recommendation 10?"

    service.answer(question)

    assert retrieval.last_question == question


def test_default_k_used():
    retrieval = MockRetrievalEngine()

    service = create_service(
        retrieval,
    )

    service.answer(
        "EDD",
    )

    assert retrieval.last_k == 5


def test_custom_k_used():
    retrieval = MockRetrievalEngine()

    service = create_service(
        retrieval,
    )

    service.answer(
        "EDD",
        k=3,
    )

    assert retrieval.last_k == 3


def test_prompt_contains_context():
    service = create_service(
        MockRetrievalEngine(),
    )

    response = service.answer(
        "Explain EDD",
    )

    assert "Enhanced Due Diligence" in response.text


def test_empty_retrieval_results():
    service = create_service(
        EmptyRetrievalEngine(),
    )

    response = service.answer(
        "Unknown regulation",
    )

    assert "No supporting context available." in response.text


def test_response_metadata():
    service = create_service(
        MockRetrievalEngine(),
    )

    response = service.answer(
        "EDD",
    )

    assert response.metadata["provider"] == "Mock"

    assert response.metadata["model"] == "mock-llm-v1"