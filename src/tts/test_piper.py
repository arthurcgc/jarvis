#!/usr/bin/env python3
"""Quick test for Piper TTS on CPU."""

import subprocess
import tempfile
import time

# Piper config
PIPER_BIN = "piper-tts"
VOICE_MODEL = "/usr/share/piper-voices/en/en_US/lessac/medium/en_US-lessac-medium.onnx"

# Test phrases
PHRASES = [
    "Hello, I am Jarvis, your local voice assistant.",
    "The quick brown fox jumps over the lazy dog.",
    "Running on CPU with AMD GPUs handling the language model.",
]


def synthesize(text: str, output_path: str) -> float:
    """Synthesize text to audio file. Returns elapsed time."""
    start = time.time()
    subprocess.run(
        [PIPER_BIN, "--model", VOICE_MODEL, "--output_file", output_path],
        input=text.encode(),
        capture_output=True,
        check=True,
    )
    return time.time() - start


def play(path: str):
    """Play audio file using aplay."""
    subprocess.run(["aplay", "-q", path], check=True)


def main():
    print(f"Testing Piper TTS")
    print(f"Voice: lessac (medium)")
    print(f"Model: {VOICE_MODEL}")
    print()

    for i, phrase in enumerate(PHRASES, 1):
        print(f"[{i}/{len(PHRASES)}] \"{phrase[:50]}{'...' if len(phrase) > 50 else ''}\"")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            elapsed = synthesize(phrase, f.name)
            print(f"  Synthesized in {elapsed:.2f}s")

            print("  Playing...")
            play(f.name)
            print()


if __name__ == "__main__":
    main()