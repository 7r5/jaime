import asyncio
import os
import pytest
from backend.ai import get_provider, OpenAIProvider, ClaudeProvider


def test_get_provider_default():
    os.environ.pop("AI_PROVIDER", None)
    provider = get_provider()
    assert isinstance(provider, OpenAIProvider)


def test_get_provider_claude():
    os.environ["AI_PROVIDER"] = "claude"
    provider = get_provider()
    assert isinstance(provider, ClaudeProvider)


class FakeResponse:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code
        self.reason_phrase = "OK"

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

    def json(self):
        return self._data


class FakeAsyncClient:
    def __init__(self, response):
        self._response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, url, json, headers):
        return self._response


@pytest.mark.asyncio
async def test_openai_provider_chat(monkeypatch):
    from backend.ai import OpenAIProvider

    fake_response = FakeResponse({"choices": [{"message": {"content": "Hola"}}]})
    monkeypatch.setattr("backend.ai.httpx.AsyncClient", lambda: FakeAsyncClient(fake_response))
    provider = OpenAIProvider()
    output = await provider.chat([{"role": "user", "content": "Hi"}])
    assert output == "Hola"


@pytest.mark.asyncio
async def test_claude_provider_chat(monkeypatch):
    from backend.ai import ClaudeProvider

    fake_response = FakeResponse({"completion": "Hola"})
    monkeypatch.setattr("backend.ai.httpx.AsyncClient", lambda: FakeAsyncClient(fake_response))
    provider = ClaudeProvider()
    output = await provider.chat([{"role": "user", "content": "Hi"}])
    assert output == "Hola"
