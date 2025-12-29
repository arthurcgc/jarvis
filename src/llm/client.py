"""Async client for llama.cpp server."""

import httpx
from typing import AsyncIterator

DEFAULT_URL = "http://localhost:8080"


class LLMClient:
    """Async wrapper for llama.cpp server API."""

    def __init__(self, base_url: str = DEFAULT_URL):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(timeout=120.0)

    async def generate(
        self,
        prompt: str,
        system: str | None = None,
        max_tokens: int = 512,
        temperature: float = 0.7,
    ) -> str:
        """Generate a response (non-streaming)."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        resp = await self._client.post(
            f"{self.base_url}/v1/chat/completions",
            json={
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    async def generate_stream(
        self,
        prompt: str,
        system: str | None = None,
        max_tokens: int = 512,
        temperature: float = 0.7,
    ) -> AsyncIterator[str]:
        """Generate a response with streaming."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        async with self._client.stream(
            "POST",
            f"{self.base_url}/v1/chat/completions",
            json={
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": True,
            },
        ) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    import json
                    chunk = json.loads(data)
                    delta = chunk["choices"][0].get("delta", {})
                    if "content" in delta:
                        yield delta["content"]

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()