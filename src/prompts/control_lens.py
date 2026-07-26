"""
Control Lens

Sprint:
    Sprint 7 - D5

Builds financial crime control guidance that is injected
into every LLM prompt.
"""

from __future__ import annotations


class ControlLens:
    """
    Produces structured control-focused guidance.
    """

    def build(self) -> str:
        """
        Build the Control Lens guidance.
        """

        return """
=== CONTROL LENS ===

Analyse the regulatory requirement from an internal control perspective.

Where appropriate:

• Identify preventive controls.

• Identify detective controls.

• Identify corrective controls.

• Explain governance and oversight expectations.

• Explain ownership and accountability.

• Identify manual and automated controls.

• Highlight key control evidence an auditor should inspect.

• Explain how control weaknesses increase financial crime risk.

Where possible distinguish:

- Design effectiveness
- Operating effectiveness

Never invent controls that are unsupported by the retrieved evidence.

Clearly distinguish mandatory regulatory requirements from recommended good practices.
""".strip()