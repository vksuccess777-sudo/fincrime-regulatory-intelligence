"""
Question Answering Service

Coordinates the complete Retrieval-Augmented Generation (RAG) workflow.

Sprint:
    Sprint 7 - D4
"""

from __future__ import annotations

from src.llm.llm_provider import LLMProvider
from src.llm.llm_response import LLMResponse
from src.prompts.prompt_builder import PromptBuilder
from src.rag.context_builder import ContextBuilder
from src.retrieval.retrieval_engine import RetrievalEngine


class QuestionAnsweringService:
    """
    High-level service that orchestrates the complete
    Retrieval-Augmented Generation (RAG) pipeline.

    Workflow
    --------
        User Question
              │
              ▼
        Retrieval Engine
              │
              ▼
        Context Builder
              │
              ▼
        Prompt Builder
              │
              ▼
          LLM Provider
              │
              ▼
         LLM Response
    """

    def __init__(
        self,
        retrieval_engine: RetrievalEngine,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        llm_provider: LLMProvider,
    ) -> None:
        """
        Initialise the Question Answering Service.
        """

        self._retrieval_engine = retrieval_engine
        self._context_builder = context_builder
        self._prompt_builder = prompt_builder
        self._llm_provider = llm_provider

    def answer(
        self,
        question: str,
        k: int = 5,
    ) -> LLMResponse:
        """
        Execute the complete Retrieval-Augmented Generation workflow.

        Parameters
        ----------
        question:
            User question.

        k:
            Number of semantic retrieval results.

        Returns
        -------
        LLMResponse
        """

        retrieval_results = self._retrieval_engine.search(
            question=question,
            k=k,
        )

        context = self._context_builder.build(
            retrieval_results,
        )

        prompt = self._prompt_builder.build(
            question=question,
            context=context,
        )

        return self._llm_provider.generate(
            prompt,
        )