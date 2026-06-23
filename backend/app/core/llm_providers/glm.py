from openai import AsyncOpenAI

from app.core.llm import LLMProvider
from app.config import settings


class GLMProvider(LLMProvider):
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.glm_api_key,
            base_url="https://open.bigmodel.cn/api/paas/v4/",
        )
        self.model = settings.glm_model

    async def chat(self, messages: list[dict], system_prompt: str = "") -> str:
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            temperature=0.7,
            max_tokens=2048,
        )
        return response.choices[0].message.content or ""

    async def chat_with_json(self, messages: list[dict], system_prompt: str = "") -> dict:
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            temperature=0.3,
            max_tokens=4096,
            response_format={"type": "json_object"},
        )
        import json
        return json.loads(response.choices[0].message.content or "{}")
