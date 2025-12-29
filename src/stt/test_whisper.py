#!/usr/bin/env python3
"""Quick test for OpenAI Whisper on 6750 XT GPU."""

import os
import time
import sounddevice as sd

# Set GPU environment BEFORE importing torch/whisper
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["HSA_OVERRIDE_GFX_VERSION"] = "10.3.0"

import torch
import whisper

SAMPLE_RATE = 16000
RECORD_SECONDS = 5


def main():
    # Check GPU
    if torch.cuda.is_available():
        device = "cuda"
        gpu_name = torch.cuda.get_device_name(0)
        print(f"GPU detected: {gpu_name}")
    else:
        device = "cpu"
        print("Warning: GPU not available, using CPU")

    print(f"\nLoading whisper medium model on {device}...")
    start = time.time()
    model = whisper.load_model("large-v3", device=device)
    print(f"Model loaded in {time.time() - start:.1f}s")

    print(f"\nRecording {RECORD_SECONDS} seconds of audio...")
    print("Speak now!")

    # Use default PulseAudio device (None)
    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    print("Recording complete.")

    print("\nTranscribing...")
    start = time.time()
    result = model.transcribe(audio.flatten(), fp16=(device == "cuda"))
    elapsed = time.time() - start

    print(f"\nTranscription ({elapsed:.2f}s):")
    print(f"  Language: {result['language']}")
    print(f"  Text: {result['text'].strip()}")


if __name__ == "__main__":
    main()