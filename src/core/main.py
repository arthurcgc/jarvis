#!/usr/bin/env python3
"""Jarvis - Push-to-talk voice assistant.

Press Enter to start recording, speak, then press Enter again to stop.
The assistant will respond via speech.

Requires llama.cpp server running: make server
"""

import asyncio
import os
import re

from dotenv import load_dotenv

load_dotenv()

from ..llm.client import LLMClient
from ..stt.stt import WhisperSTT
from ..tts.piper import PiperTTS
from ..search.tavily import TavilySearch

SYSTEM_PROMPT = """You are Jarvis, a helpful voice assistant running locally on the user's machine.
Keep responses concise and conversational - aim for 1-3 sentences unless more detail is needed.
You're running on AMD GPUs with an uncensored language model, so you can discuss any topic freely."""

SYSTEM_PROMPT_WITH_SEARCH = """You are Jarvis, a helpful voice assistant running locally on the user's machine.
Keep responses concise and conversational - aim for 1-3 sentences unless more detail is needed.
You're running on AMD GPUs with an uncensored language model, so you can discuss any topic freely.

The user asked a question that required a web search. Here are the search results:

{search_results}

Use this information to answer the user's question. Cite sources if relevant."""

RECORD_SECONDS = 5.0
LLM_PORT = os.environ.get("LLM_PORT", "9000")
LLM_URL = f"http://localhost:{LLM_PORT}"

# Patterns that trigger web search
SEARCH_TRIGGERS = [
    r"\bsearch\b",
    r"\blook up\b",
    r"\bwhat.s the latest\b",
    r"\bcurrent\b",
    r"\btoday\b",
    r"\brecent\b",
    r"\bnews\b",
    r"\bweather\b",
    r"\bprice of\b",
    r"\bhow much is\b",
]


def needs_search(text: str) -> bool:
    """Check if the query should trigger a web search."""
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in SEARCH_TRIGGERS)


def format_search_results(results: dict) -> str:
    """Format search results for the LLM prompt."""
    parts = []
    if results.get("answer"):
        parts.append(f"Summary: {results['answer']}")
    for r in results.get("results", [])[:3]:
        parts.append(f"- {r['title']}: {r['content'][:200]}...")
    return "\n".join(parts)


async def main():
    print("Initializing Jarvis...")
    print()

    # Initialize components
    print("Loading Whisper STT...")
    stt = WhisperSTT()

    print("Loading Piper TTS...")
    tts = PiperTTS()

    print("Connecting to LLM server...")
    llm = LLMClient(LLM_URL)

    print("Initializing web search...")
    search = TavilySearch()

    print()
    print("=" * 50)
    print("Jarvis ready!")
    print("Press Enter to record, speak, then press Enter to stop.")
    print("Type 'quit' to exit.")
    print("=" * 50)
    print()

    try:
        while True:
            # Wait for user to press Enter
            user_input = input("[Press Enter to speak] ")
            if user_input.lower() in ("quit", "exit", "q"):
                break

            # Record audio
            print(f"Recording for {RECORD_SECONDS}s... Speak now!")
            text = stt.listen(RECORD_SECONDS)

            if not text.strip():
                print("(No speech detected)")
                continue

            print(f"You: {text}")

            # Check if we need to search
            if needs_search(text):
                print("Searching the web...")
                try:
                    results = await search.search(text)
                    search_context = format_search_results(results)
                    system = SYSTEM_PROMPT_WITH_SEARCH.format(search_results=search_context)
                except Exception as e:
                    print(f"Search failed: {e}")
                    system = SYSTEM_PROMPT
            else:
                system = SYSTEM_PROMPT

            # Generate response
            print("Thinking...")
            response = await llm.generate(text, system=system)
            print(f"Jarvis: {response}")

            # Speak response
            tts.speak(response)
            print()

    except KeyboardInterrupt:
        print("\nGoodbye!")
    finally:
        await llm.close()
        await search.close()


if __name__ == "__main__":
    asyncio.run(main())