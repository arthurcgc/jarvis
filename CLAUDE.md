# CLAUDE.md

Context file for Claude Code. This document describes the project so you can pick up where we left off.

## Project: Jarvis

A local voice assistant running on AMD GPUs with uncensored LLMs.

## How to Communicate

I'm new to the LLM/AI world. When explaining concepts:

- Skip marketing buzzwords and hype
- Give me the plain-English version first, then details if needed
- Keep explanations short — don't derail the main task
- If a term is important, define it briefly inline

## Hardware Context

- **Main Rig:** Arch Linux, Ryzen 9 5900X, 32GB RAM
- **GPU 1:** AMD RX 7800 XT (16GB VRAM) — Vulkan0
- **GPU 2:** AMD RX 6750 XT (12GB VRAM) — Vulkan1
- **Total VRAM:** 28GB for LLM inference
- **Future satellites:** 2x old Android phones, 1x RPi 4B

## Tech Stack

| Component   | Tool                      | Notes                   |
| ----------- | ------------------------- | ----------------------- |
| LLM Runtime | llama.cpp + Vulkan        | Dual GPU, tensor split  |
| STT         | faster-whisper (large-v3) | GPU via CUDA or CPU     |
| TTS         | Piper (high quality)      | CPU                     |
| Web Search  | Tavily API                | For current events      |
| Glue        | Python 3.11+              | httpx for async calls   |

## Current Phase: 1 (Core Loop) ✅ WORKING

- Vulkan dual-GPU inference working
- Whisper STT working (large-v3)
- Piper TTS working (high quality voice)
- Web search integration working
- Push-to-talk loop working

## Key Design Decisions

- **Vulkan over ROCm:** Mixed RDNA2+RDNA3 GPUs don't work with ROCm/HIP. Vulkan handles mixed architectures natively.
- **llama.cpp over Ollama:** Ollama can't do multi-GPU with different architectures.
- **Personality profiles:** System prompt + voice model bundled together, hot-swappable
- **Distributed architecture:** Main rig does heavy compute, satellites just stream audio

## Directory Structure

- `src/core/` — Main assistant loop, orchestration
- `src/stt/` — Whisper wrapper
- `src/tts/` — TTS engines (Piper)
- `src/llm/` — llama.cpp client (OpenAI-compatible API)
- `src/search/` — Tavily web search client
- `models/` — GGUF models and Piper voices
- `docs/setup/` — Installation guides

## Commands

```bash
cd ~/Documents/jarvis

# Start the LLM server (run in separate terminal)
make server PORT=9000
make server PORT=9000 MODEL=Qwen2.5-32B-Instruct-abliterated-Q4_K_M.gguf

# Run the voice assistant
make jarvis

# Rebuild llama.cpp
make build

# Check GPU VRAM usage
rocm-smi
```

## Models

Located in `~/Documents/jarvis/models/`:

- `Qwen2.5-32B-Instruct-abliterated-Q4_K_M.gguf` (~20GB) — Main model
- `qwen2.5-abliterate-14b.gguf` (8GB) — Fallback/testing

## Environment Variables

`.env` file (not committed):

- `TAVILY_API_KEY` — For web search
- `LLM_PORT` — Override default port (9000)

## Next Steps

1. ~~ROCm/Vulkan GPU setup~~ ✅
2. ~~llama.cpp dual-GPU inference~~ ✅
3. ~~Whisper STT~~ ✅
4. ~~Piper TTS~~ ✅
5. ~~Web search integration~~ ✅
6. Test 32B model performance
7. Phase 2: Better TTS (XTTS/F5), VAD, continuous listening
