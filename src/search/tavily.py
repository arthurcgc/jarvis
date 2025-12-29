"""Tavily web search client."""

import os
import httpx

TAVILY_API_URL = "https://api.tavily.com/search"


class TavilySearch:
    """Async client for Tavily search API."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not set")
        self._client = httpx.AsyncClient(timeout=30.0)

    async def search(
        self,
        query: str,
        max_results: int = 5,
        search_depth: str = "basic",
        include_answer: bool = True,
    ) -> dict:
        """
        Search the web using Tavily.

        Args:
            query: Search query
            max_results: Number of results (1-10)
            search_depth: "basic" or "advanced" (advanced uses more API credits)
            include_answer: Whether to include AI-generated answer summary

        Returns:
            Dict with 'answer' (str) and 'results' (list of dicts with title, url, content)
        """
        resp = await self._client.post(
            TAVILY_API_URL,
            json={
                "api_key": self.api_key,
                "query": query,
                "max_results": max_results,
                "search_depth": search_depth,
                "include_answer": include_answer,
            },
        )
        resp.raise_for_status()
        data = resp.json()

        return {
            "answer": data.get("answer", ""),
            "results": [
                {
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", ""),
                }
                for r in data.get("results", [])
            ],
        }

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()