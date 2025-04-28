import os
from dotenv import load_dotenv


def load_api_keys():
    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    claude_key = os.getenv("CLAUDE_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not openai_key and not claude_key and not gemini_key:
        raise EnvironmentError(
            "❗ API keys are not set.\n"
            "Please create a .env file or set environment variables.\n"
            "Required: OPENAI_API_KEY or CLAUDE_API_KEY or GEMINI_API_KEY."
        )
