import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_client() -> OpenAI:
    """
    Get an OpenAI client using the API key from the environment variable.
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    return OpenAI(api_key=key)
