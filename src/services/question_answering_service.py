"""
Question Answering Service

Coordinates the complete Retrieval-Augmented Generation (RAG) workflow.

Sprint:
    Sprint 7 - D5
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
      Evidence Available?
          │           │
         No          Yes
          │           │
          ▼           ▼
  Return System   Context Builder
     Response           │
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
        """

        retrieval_results = self._retrieval_engine.search(
            question=question,
            k=k,
        )

        # ----------------------------------------------------------
        # Evidence Guard
        #
        # Never call the LLM when no regulatory evidence exists.
        # ----------------------------------------------------------

        if not retrieval_results:

            message = (
                "No supporting regulatory evidence was found in the "
                "indexed knowledge base.\n\n"
                "An evidence-based answer cannot be generated at this time.\n\n"
                "Please populate the regulatory knowledge base before "
                "querying.\n\n"
                "Disclaimer:\n"
                "AI-generated content may contain errors.\n"
                "Always verify against the cited regulatory source and "
                "apply professional judgement."
            )

            return LLMResponse(
                text=message,
                citations=[],
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
                metadata={
                    "provider": "System",
                    "model": "Evidence Guard",
                    "retrieved_chunks": 0,
                    "confidence": "None",
                },
            )

        context = self._context_builder.build(
            retrieval_results,
        )

        prompt = self._prompt_builder.build(
            question=question,
            context=context,
        )

        response = self._llm_provider.generate(
            prompt,
        )

        response.metadata["retrieved_chunks"] = len(
            retrieval_results,
        )

        return response