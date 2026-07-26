"""
Prompt Builder

Constructs prompts for the Large Language Model.

Sprint:
    Sprint 7 - D5

Responsibilities
----------------
- Build Retrieval-Augmented Generation prompts.
- Inject reasoning lenses.
- Keep prompt construction independent of the LLM.
- Enforce evidence-based responses.
"""

from __future__ import annotations

from src.prompts.auditor_lens import AuditorLens
from src.prompts.control_lens import ControlLens
from src.prompts.executive_lens import ExecutiveLens
from src.prompts.risk_lens import RiskLens


class PromptBuilder:
    """
    Builds prompts for Financial Crime Regulatory Intelligence.
    """

    def __init__(self) -> None:
        self._auditor_lens = AuditorLens()
        self._risk_lens = RiskLens()
        self._control_lens = ControlLens()
        self._executive_lens = ExecutiveLens()

    def build(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Build the complete prompt.
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
        Build the default Financial Crime prompt.
        """

        auditor = self._auditor_lens.build()
        risk = self._risk_lens.build()
        control = self._control_lens.build()
        executive = self._executive_lens.build()

        return f"""
You are the Financial Crime Regulatory Intelligence Assistant.

Your purpose is to provide accurate, evidence-based answers using ONLY
the retrieved regulatory information.

Never invent regulations.

Never fabricate citations.

Never speculate.

If the retrieved context is insufficient, clearly state the limitation.

Always distinguish between:

• Regulatory requirements

• Retrieved evidence

• Professional observations

• Recommendations

==================================================
RETRIEVED REGULATORY CONTEXT
==================================================

{context}

==================================================
AUDITOR LENS
==================================================

{auditor}

==================================================
RISK LENS
==================================================

{risk}

==================================================
CONTROL LENS
==================================================

{control}

==================================================
EXECUTIVE LENS
==================================================

{executive}

==================================================
USER QUESTION
==================================================

{question}

==================================================
RESPONSE REQUIREMENTS
==================================================

Structure the answer using the following headings whenever appropriate:

1. Regulatory Summary

2. Financial Crime Risks

3. Expected Controls

4. Suggested Audit Procedures

5. Executive Summary

6. References

7. Confidence

8. Disclaimer

The Disclaimer must always state:

"This response was generated using retrieved regulatory information.
AI-generated content may contain errors.
Always verify against the cited regulatory source and apply professional
judgement before relying on this response."

==================================================
ANSWER
==================================================
""".strip()