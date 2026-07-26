"""
Financial Crime Regulatory Intelligence
Interactive CLI

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
from src.vectorstore.chroma_vector_store import ChromaVectorStore


def main() -> None:

    print("=" * 70)
    print("Financial Crime Regulatory Intelligence (FRI)")
    print("Version 1.0")
    print("=" * 70)
    print()

    embedding_provider = SentenceTransformerProvider()

    vector_store = ChromaVectorStore()

    retrieval_engine = RetrievalEngine(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    qa_service = QuestionAnsweringService(
        retrieval_engine=retrieval_engine,
        context_builder=ContextBuilder(),
        prompt_builder=PromptBuilder(),
        llm_provider=GroqProvider(),
    )

    while True:

        question = input(
            "\nAsk a regulatory question ('exit' to quit):\n> "
        ).strip()

        if question.lower() in {
            "exit",
            "quit",
            "q",
        }:
            break

        if not question:
            continue

        print("\nSearching regulatory knowledge base...\n")

        response = qa_service.answer(
            question=question,
        )

        print("=" * 70)

        print(response.text)

        print("=" * 70)

        retrieved_chunks = response.metadata.get(
            "retrieved_chunks",
            "Unknown",
        )

        print(f"Retrieved Chunks : {retrieved_chunks}")

        provider = response.metadata.get(
            "provider",
            "",
        )

        if provider == "System":
            print("Knowledge Source : None")
            print("Status           : No regulatory evidence found.")
        else:
            print("Knowledge Source : Indexed Regulatory Corpus")

    print("\nGoodbye.")


if __name__ == "__main__":
    main()