from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import GROQ_API_KEY
from langchain_groq import ChatGroq


def get_groq_llm(model_name: str = "openai/gpt-oss-120b",temperature: float = 0.2):
    """
    Returns an initialized Groq LLM instance.

    This function should be used by all agents
    to ensure consistent LLM configuration.
    """


    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found. Please set it in your .env file."
        )

    llm = ChatGroq(
        model=model_name,
        api_key=GROQ_API_KEY,
        temperature=temperature,
    )

    return llm


