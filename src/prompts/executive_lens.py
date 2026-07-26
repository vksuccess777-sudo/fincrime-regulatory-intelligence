"""
Executive Lens

Sprint:
    Sprint 7 - D5

Builds executive-level reasoning guidance that is injected
into every LLM prompt.

Responsibilities
----------------
- Focus on governance implications.
- Summarise business impact.
- Highlight material financial crime risks.
- Support concise reporting for senior management.
"""

from __future__ import annotations


class ExecutiveLens:
    """
    Produces executive-level guidance.
    """

    def build(self) -> str:
        """
        Build the Executive Lens guidance.
        """

        return """
=== EXECUTIVE LENS ===

Analyse the topic from the perspective of senior management and
the Board.

Where appropriate:

• Summarise the regulatory expectation in plain business language.

• Explain why the topic matters to the organisation.

• Highlight material financial crime risks.

• Explain governance implications.

• Explain possible regulatory, financial and reputational impacts.

• Identify the most important management actions.

• Keep executive summaries concise and evidence-based.

• Clearly distinguish:
    - Regulatory requirements
    - Retrieved evidence
    - Professional observations
    - Recommended management actions

Do not exaggerate risks.

Do not speculate.

If retrieved evidence is limited, clearly state the limitation.
""".strip()