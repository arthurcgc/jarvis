"""Piper TTS wrapper."""

import subprocess
import tempfile

DEFAULT_MODEL = "/home/samsepiol/Documents/jarvis/models/piper/en_US-lessac-high.onnx"
PIPER_BIN = "piper-tts"


class PiperTTS:
    """Text-to-speech using Piper on CPU."""

    def __init__(self, model_path: str = DEFAULT_MODEL):
        self.model_path = model_path

    def synthesize(self, text: str) -> str:
        """Synthesize text to audio file. Returns path to wav file."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            subprocess.run(
                [PIPER_BIN, "--model", self.model_path, "--output_file", f.name],
                input=text.encode(),
                capture_output=True,
                check=True,
            )
            return f.name

    def speak(self, text: str):
        """Synthesize and play audio directly."""
        wav_path = self.synthesize(text)
        subprocess.run(["aplay", "-q", wav_path], check=True)

    def speak_stream(self, text: str):
        """Synthesize and play without intermediate file."""
        piper = subprocess.Popen(
            [PIPER_BIN, "--model", self.model_path, "--output-raw"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        aplay = subprocess.Popen(
            ["aplay", "-q", "-r", "22050", "-f", "S16_LE", "-t", "raw", "-"],
            stdin=piper.stdout,
            stderr=subprocess.DEVNULL,
        )
        piper.stdin.write(text.encode())
        piper.stdin.close()
        aplay.wait()