import os
from typing import Any, Dict
import httpx

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")


class AIProvider:
    async def chat(self, messages: list[dict[str, str]], tools: list[dict[str, Any]] | None = None) -> str:
        raise NotImplementedError


class OpenAIProvider(AIProvider):
    async def chat(self, messages: list[dict[str, str]], tools: list[dict[str, Any]] | None = None) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "temperature": 0.7,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()


class ClaudeProvider(AIProvider):
    async def chat(self, messages: list[dict[str, str]], tools: list[dict[str, Any]] | None = None) -> str:
        url = "https://api.anthropic.com/v1/chat/completions"
        headers = {
            "x-api-key": CLAUDE_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "model": "claude-3.5-realtime-preview",
            "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
            "temperature": 0.7,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["completion"]


def get_provider() -> AIProvider:
    provider = os.getenv("AI_PROVIDER", "openai")
    if provider == "claude":
        return ClaudeProvider()
    return OpenAIProvider()
