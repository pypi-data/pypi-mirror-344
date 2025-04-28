from readme_generator.ai_client.openai_client import OpenAIClient
from readme_generator.ai_client.claude_client import ClaudeClient
from readme_generator.ai_client.gemini_client import GeminiClient

def get_client(provider: str):
    if provider == "openai":
        return OpenAIClient()
    elif provider == "claude":
        return ClaudeClient()
    elif provider == "gemini":
        return GeminiClient()
    else:
        raise ValueError(f"Unsupported provider: {provider}")