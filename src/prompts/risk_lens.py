"""
Risk Lens

Sprint:
    Sprint 7 - D5

Builds financial crime risk reasoning guidance that is injected
into every LLM prompt.
"""

from __future__ import annotations


class RiskLens:
    """
    Produces structured financial crime risk guidance.
    """

    def build(self) -> str:
        """
        Build the Risk Lens guidance.
        """

        return """
=== RISK LENS ===

Analyse the regulatory requirement from a financial crime risk perspective.

Where appropriate:

• Explain the inherent financial crime risk.

• Identify money laundering risks.

• Identify terrorist financing risks.

• Identify sanctions risks.

• Identify fraud risks.

• Identify beneficial ownership risks.

• Explain how failure of controls could be exploited.

• Consider customer, product, geographic and transaction risks.

Prioritise risks using a risk-based approach.

Clearly distinguish factual regulatory requirements from inferred risk analysis.

Never invent risks that are unsupported by the retrieved evidence.
""".strip()