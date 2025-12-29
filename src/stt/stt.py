"""Whisper STT wrapper using OpenAI Whisper on AMD GPU."""

import os
import tempfile
import sounddevice as sd
import soundfile as sf
import torch
import whisper

# Set GPU environment before importing torch
# 6750 XT is device 0, needs gfx1030 override for ROCm compatibility
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["HSA_OVERRIDE_GFX_VERSION"] = "10.3.0"

SAMPLE_RATE = 16000


class WhisperSTT:
    """Speech-to-text using OpenAI Whisper on 6750 XT GPU."""

    def __init__(self, model_size: str = "large-v3"):
        # Check if ROCm/CUDA is available
        if torch.cuda.is_available():
            self.device = "cuda"
            gpu_name = torch.cuda.get_device_name(0)
            print(f"  Using GPU: {gpu_name}")
        else:
            self.device = "cpu"
            print("  Warning: GPU not available, falling back to CPU")

        self.model = whisper.load_model(model_size, device=self.device)

    def record(self, seconds: float = 5.0):
        """Record audio from microphone. Returns numpy array."""
        # Use default PulseAudio device
        audio = sd.rec(
            int(seconds * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        return audio.flatten()

    def transcribe_audio(self, audio) -> str:
        """Transcribe audio data to text."""
        # Whisper expects float32 numpy array
        result = self.model.transcribe(audio, fp16=(self.device == "cuda"))
        return result["text"].strip()

    def listen(self, seconds: float = 5.0) -> str:
        """Record and transcribe in one call."""
        audio = self.record(seconds)
        return self.transcribe_audio(audio)