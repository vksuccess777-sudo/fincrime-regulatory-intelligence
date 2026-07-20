# Application configuration
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# ----------------------------
# Groq Configuration
# ----------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ----------------------------
# Model Configuration
# ----------------------------

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama-3.3-70b-versatile"
)

TEMPERATURE = float(
    os.getenv(
        "TEMPERATURE",
        "0"
    )
)

MAX_TOKENS = int(
    os.getenv(
        "MAX_TOKENS",
        "4096"
    )
)