from abc import ABC, abstractmethod
from typing import Optional

from app.config import settings


class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, messages: list[dict], system_prompt: str = "") -> str:
        ...

    @abstractmethod
    async def chat_with_json(self, messages: list[dict], system_prompt: str = "") -> dict:
        ...


def get_llm_provider(provider_name: Optional[str] = None) -> LLMProvider:
    name = (provider_name or settings.llm_provider).lower()

    if name == "deepseek":
        from app.core.llm_providers.deepseek import DeepSeekProvider
        return DeepSeekProvider()
    elif name == "glm":
        from app.core.llm_providers.glm import GLMProvider
        return GLMProvider()
    elif name == "groq":
        from app.core.llm_providers.groq import GroqProvider
        return GroqProvider()
    elif name == "ollama":
        from app.core.llm_providers.ollama import OllamaProvider
        return OllamaProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {name}")
