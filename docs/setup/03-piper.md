# Piper TTS Setup

## Overview

Setting up Piper for text-to-speech on CPU.

## Status: COMPLETE

Piper installed with high-quality lessac voice running on CPU.

## Architecture

Piper uses ONNX Runtime which only supports CUDA/DirectML, not ROCm. Running on CPU is fast enough (~10x real-time) and frees GPU VRAM for LLM/STT.

## Installation

```bash
# From chaotic-aur
sudo pacman -S piper-tts-git

# When prompted for onnxruntime, choose:
# 1) onnxruntime-cpu (recommended - no GPU support anyway)
```

## Voice

Using `lessac` high-quality voice (downloaded to project).

```bash
cd ~/Documents/jarvis
mkdir -p models/piper
cd models/piper

# Download high-quality voice
curl -LO "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/high/en_US-lessac-high.onnx"
curl -LO "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/high/en_US-lessac-high.onnx.json"
```

| Voice | Quality | Size | Notes |
|-------|---------|------|-------|
| lessac | medium | ~60MB | system package |
| **lessac** | **high** | ~108MB | **current** |
| ryan | high | ~100MB | male voice |

## Usage

Command line:

```bash
# Direct playback
echo "Hello world" | piper-tts \
    --model ~/Documents/jarvis/models/piper/en_US-lessac-high.onnx \
    --output-raw | aplay -q -r 22050 -f S16_LE -t raw -
```

## Performance

- Voice load: ~0.7s
- Synthesis: ~10x real-time (3s audio in 0.3s)
- CPU only - no GPU VRAM usage