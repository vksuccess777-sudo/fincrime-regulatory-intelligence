from langchain_groq import ChatGroq
from config import (
    GROQ_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS
)


class GroqClient:
    """
    Handles all communication with the Groq API.

    This class should not contain any business logic.
    It is responsible only for sending prompts to the LLM
    and returning responses.
    """

    def __init__(self):
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

    def ask(self, prompt: str) -> str:
        """
        Send a prompt to the LLM and return the response.
        """

        response = self.llm.invoke(prompt)

        return response.content