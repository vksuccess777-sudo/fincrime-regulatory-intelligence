"""
Financial Crime Regulatory Intelligence
Interactive CLI

Sprint:
    Sprint 8 - D2
"""

from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------------
# Allow execution via:
#
#     python scripts/ask.py
#
# by adding the project root to sys.path.
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.bootstrap.application_bootstrap import (  # noqa: E402
    ApplicationBootstrap,
)


def main() -> None:

    print("=" * 70)
    print("Financial Crime Regulatory Intelligence (FRI)")
    print("Version 1.0")
    print("=" * 70)
    print()

    bootstrap = ApplicationBootstrap()

    qa_service = bootstrap.question_answering_service()

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
            print(
                "Status           : No regulatory evidence found."
            )

        else:

            print(
                "Knowledge Source : Indexed Regulatory Corpus"
            )

    print("\nGoodbye.")


if __name__ == "__main__":
    main()