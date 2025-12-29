# Jarvis

A local, privacy-first voice assistant powered by uncensored LLMs. Think Alexa, but it's actually smart and runs on your hardware.

## Hardware

- **CPU:** AMD Ryzen 9 5900X
- **GPU 1:** AMD RX 7800 XT (16GB) — LLM inference
- **GPU 2:** AMD RX 6700 XT (12GB) — Whisper / auxiliary
- **RAM:** 32GB
- **OS:** Arch Linux (zen kernel)

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         MAIN RIG                                │
│                                                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│  │   VAD   │───▶│ Whisper │───▶│   LLM   │───▶│   TTS   │      │
│  │ Silero  │    │  (STT)  │    │ Ollama  │    │  Piper  │      │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘      │
│       ▲                             ▲              │            │
│       │                             │              ▼            │
│  ┌─────────┐                  ┌─────────┐    ┌─────────┐       │
│  │   Mic   │                  │Personality│   │ Speaker │       │
│  └─────────┘                  │ Profiles │    └─────────┘       │
│                               └─────────┘                       │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ WebSocket (future)
                              ▼
              ┌───────────────────────────────┐
              │      SATELLITE PODS           │
              │  (Phones / RPi / other mics)  │
              │                               │
              │  - Wake word detection        │
              │  - Audio streaming            │
              │  - TTS playback               │
              └───────────────────────────────┘
```

## Roadmap

### Phase 1: Core Loop ✨ *current*
- [ ] ROCm setup for AMD GPUs
- [ ] Ollama with uncensored LLM
- [ ] faster-whisper for STT
- [ ] Piper TTS
- [ ] Simple push-to-talk Python script

### Phase 2: Personality & Polish
- [ ] Personality profiles (system prompt + voice pairing)
- [ ] Coqui XTTS or F5-TTS for expressive voices
- [ ] VAD for hands-free on desktop
- [ ] Conversation memory / context

### Phase 3: Distributed Listening
- [ ] WebSocket server for audio streaming
- [ ] OpenWakeWord integration
- [ ] Web app client (PWA for phones)
- [ ] RPi satellite support

### Phase 4: Home Integration (someday)
- [ ] Home Assistant integration
- [ ] Device control
- [ ] Routines and automation

## Project Structure

```
jarvis/
├── src/
│   ├── core/           # Main assistant loop
│   ├── stt/            # Speech-to-text (Whisper)
│   ├── tts/            # Text-to-speech (Piper, XTTS)
│   ├── llm/            # LLM client (Ollama)
│   ├── vad/            # Voice activity detection
│   ├── personalities/  # System prompts + voice configs
│   └── server/         # WebSocket server (Phase 3)
├── clients/
│   ├── web/            # PWA for phone pods
│   └── desktop/        # Local desktop client
├── docs/
│   ├── setup/          # Installation guides
│   └── architecture/   # Design docs
├── scripts/            # Setup and utility scripts
└── tests/
```

## Quick Start

```bash
# TODO: After Phase 1 setup
```

## License

MIT
