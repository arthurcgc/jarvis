# Whisper STT Setup

## Overview

Setting up OpenAI Whisper for speech-to-text on the 6750 XT GPU via ROCm.

## Status: COMPLETE

OpenAI Whisper installed with large-v3 model running on 6750 XT GPU.

## Architecture

| Component | Device | Notes |
|-----------|--------|-------|
| Whisper STT | 6750 XT (device 0) | ~3GB VRAM |
| LLM | 7800 XT (device 1) | Separate GPU |

The 6750 XT (gfx1031) requires `HSA_OVERRIDE_GFX_VERSION=10.3.0` to use gfx1030 kernels.

## Installation

```bash
cd ~/Documents/jarvis

# Create venv with Python 3.12 (pyenv)
~/.pyenv/versions/3.12.11/bin/python -m venv .venv
source .venv/bin/activate

# Install PyTorch ROCm
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.2

# Install OpenAI Whisper and audio deps
pip install openai-whisper sounddevice soundfile
```

## Model

Using `large-v3` for best accuracy.

| Model | VRAM | Speed | Notes |
|-------|------|-------|-------|
| tiny | ~1GB | fastest | basic accuracy |
| base | ~1GB | fast | decent |
| small | ~2GB | moderate | good |
| medium | ~2GB | slower | good |
| **large-v3** | ~3GB | slowest | **current** - best accuracy |

Model is auto-downloaded on first use to `~/.cache/whisper/`.

## GPU Environment

The STT wrapper sets these before importing torch:

```python
import os
os.environ["HIP_VISIBLE_DEVICES"] = "0"  # 6750 XT only
os.environ["HSA_OVERRIDE_GFX_VERSION"] = "10.3.0"  # gfx1031 -> gfx1030
```

## Test

```bash
cd ~/Documents/jarvis
source .venv/bin/activate
python src/stt/test_whisper.py
```

Speak when you see "Speak now!" - you have 5 seconds.

## Troubleshooting

### Audio returns silence

1. Check PulseAudio is running: `pactl list sources short`
2. Check mic isn't muted: `pavucontrol` -> Input Devices
3. Check for PipeWire conflict: `pgrep pipewire` - if running, stop it:
   ```bash
   systemctl --user stop pipewire pipewire.socket
   systemctl --user restart pulseaudio
   ```

### hipBLASLt warnings

Ignore these warnings:
```
Attempting to use hipBLASLt on an unsupported architecture!
```
ROCm falls back to hipBLAS automatically.