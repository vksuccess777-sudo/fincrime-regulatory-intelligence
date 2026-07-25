"""
Prompt Builder

Constructs prompts for the Large Language Model.

Sprint:
    Sprint 7 - D3
"""

from __future__ import annotations


class PromptBuilder:
    """
    Builds prompts for different reasoning modes.

    Currently implemented:

    - Standard Regulatory QA

    Future Sprint 8:

    - Audit Lens
    - Risk Lens
    - Control Lens
    - Executive Summary
    - Regulatory Comparison
    """

    def build(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Build the default prompt.
        """

        return self._build_standard_prompt(
            question=question,
            context=context,
        )

    def _build_standard_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Standard Retrieval-Augmented Generation prompt.
        """

        return f"""You are the Financial Crime Regulatory Intelligence Assistant.

You are answering questions ONLY from the supplied regulatory material.

Rules:

- Answer ONLY using the supplied regulatory context.
- Never invent regulations.
- Never fabricate citations.
- If the answer cannot be found, clearly state that the supplied material does not contain the answer.
- Keep answers factual and concise.
- Quote regulatory wording only when necessary.

==============================
REGULATORY CONTEXT
==============================

{context}

==============================
USER QUESTION
==============================

{question}

==============================
ANSWER
==============================
"""