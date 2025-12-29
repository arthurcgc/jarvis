# Jarvis

A local, privacy-first voice assistant powered by uncensored LLMs. Think Alexa, but it's actually smart and runs on your hardware.

## Hardware

- **CPU:** AMD Ryzen 9 5900X
- **GPU 1:** AMD RX 7800 XT (16GB) — Vulkan0
- **GPU 2:** AMD RX 6750 XT (12GB) — Vulkan1
- **Total VRAM:** 28GB for LLM inference
- **RAM:** 32GB
- **OS:** Arch Linux (zen kernel)

## Tech Stack

| Component   | Tool                      | Notes                  |
| ----------- | ------------------------- | ---------------------- |
| LLM Runtime | llama.cpp + Vulkan        | Dual GPU, tensor split |
| STT         | faster-whisper (large-v3) | CPU                    |
| TTS         | Piper (high quality)      | CPU                    |
| Web Search  | Tavily API                | For current events     |
| Glue        | Python 3.11+              | httpx for async calls  |

## Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                         MAIN RIG                                │
│                                                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│  │   Mic   │───▶│ Whisper │───▶│llama.cpp│───▶│  Piper  │      │
│  │(Record) │    │  (STT)  │    │ (LLM)   │    │  (TTS)  │      │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘      │
│                                     │              │            │
│                               ┌─────────┐          ▼            │
│                               │ Tavily  │    ┌─────────┐       │
│                               │ Search  │    │ Speaker │       │
│                               └─────────┘    └─────────┘       │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ WebSocket (future)
                              ▼
              ┌───────────────────────────────────┐
              │      SATELLITE PODS               │
              │  (Phones / RPi / other mics)      │
              └───────────────────────────────────┘
```

## Quick Start

```bash
cd ~/Documents/jarvis

# Start the LLM server (terminal 1)
make server PORT=9000

# Run the voice assistant (terminal 2)
make jarvis
```

Press and hold Space to talk, release to get a response.

## Models

- **14B** (default): ~29 tok/s — fast, good for voice
- **32B**: ~16.5 tok/s — smarter, use for complex queries

```bash
# Use 32B model
make server PORT=9000 MODEL=Qwen2.5-32B-Instruct-abliterated-Q4_K_M.gguf
```

## Why Vulkan?

We have mixed RDNA2 + RDNA3 GPUs. ROCm/HIP can't handle different GPU architectures together — it crashes during multi-GPU tensor operations. Vulkan (via RADV) handles mixed architectures natively.

See [docs/setup/01-rocm.md](docs/setup/01-rocm.md) for the full story.

## Roadmap

### Phase 1: Core Loop ✅ COMPLETE

- [x] Dual GPU Vulkan setup
- [x] llama.cpp with tensor splitting
- [x] faster-whisper STT (large-v3)
- [x] Piper TTS (high quality)
- [x] Tavily web search
- [x] Push-to-talk voice loop

### Phase 2: Latency & Polish

- [ ] Streaming TTS (speak while generating)
- [ ] VAD for hands-free
- [ ] Better TTS (XTTS or F5-TTS)
- [ ] Conversation memory

### Phase 3: Distributed Listening

- [ ] WebSocket server
- [ ] Wake word detection
- [ ] Phone/RPi satellite clients

### Phase 4: Home Integration

- [ ] Home Assistant
- [ ] Device control

## Project Structure

```text
jarvis/
├── src/
│   ├── core/       # Main assistant loop
│   ├── stt/        # Speech-to-text (Whisper)
│   ├── tts/        # Text-to-speech (Piper)
│   ├── llm/        # llama.cpp client
│   └── search/     # Tavily web search
├── models/         # GGUF models and Piper voices
├── docs/setup/     # Installation guides
└── Makefile        # Build and run commands
```

## License

MIT
