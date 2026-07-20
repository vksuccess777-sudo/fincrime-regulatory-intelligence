"""
Business Service

Regulatory Intelligence Service

Purpose:
Receives an auditor question, builds a professional prompt
using the Prompt Library and obtains a response from Groq.

Version: 0.2
"""

from src.llm.groq_client import GroqClient
from src.prompts.regulatory_prompt import build_regulatory_prompt


class RegulatoryService:
    """
    Business Service responsible for regulatory intelligence.
    """

    def __init__(self):
        self.client = GroqClient()

    def ask(self, question: str) -> dict:
        """
        Ask a regulatory question.

        Parameters
        ----------
        question : str

        Returns
        -------
        dict
        """

        prompt = build_regulatory_prompt(question)

        response = self.client.ask(prompt)

        return {
            "status": "success",
            "question": question,
            "response": response
        }