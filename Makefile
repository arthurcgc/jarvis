# Jarvis - Local Voice Assistant
# Makefile for llama.cpp inference on AMD GPU

LLAMA_DIR := $(HOME)/Documents/llama.cpp
LLAMA_BIN := $(LLAMA_DIR)/build/bin
MODELS_DIR := $(CURDIR)/models

# Default model (14B for faster voice responses, 32B available for complex queries)
MODEL ?= qwen2.5-abliterate-14b.gguf
MODEL_PATH := $(MODELS_DIR)/$(MODEL)

# GPU config: Dual GPU via Vulkan (RADV driver)
# Vulkan0: 7800 XT (NAVI32) - 16GB VRAM
# Vulkan1: 6750 XT (NAVI22) - 12GB VRAM
# Total: 28GB VRAM for LLM
GPU_LAYERS := 999
# Split proportional to VRAM: 7800 XT gets ~57%, 6750 XT gets ~43%
TENSOR_SPLIT := 16,12

# Server config
PORT ?= 8080
HOST := 0.0.0.0

.PHONY: chat server build clean verify help jarvis

help:
	@echo "Jarvis - llama.cpp on 7800 XT, Whisper on 6750 XT"
	@echo ""
	@echo "Usage:"
	@echo "  make chat              Interactive chat with 14B model"
	@echo "  make server            Start API server on port 8080"
	@echo "  make server PORT=9000  Start API server on custom port"
	@echo "  make build             Rebuild llama.cpp with GPU targets"
	@echo "  make verify            Check GPU targets in binary"
	@echo "  make clean             Clean llama.cpp build"
	@echo "  make jarvis            Run voice assistant (requires server running)"
	@echo ""
	@echo "Models: $(MODELS_DIR)"
	@echo "Current: $(MODEL)"

chat: $(MODEL_PATH)
	$(LLAMA_BIN)/llama-cli \
		--model $(MODEL_PATH) \
		--n-gpu-layers $(GPU_LAYERS)

server: $(MODEL_PATH)
	@echo "Starting server on $(HOST):$(PORT)"
	@echo "Model: $(MODEL)"
	@echo "GPUs: 7800 XT (16GB) + 6750 XT (12GB) = 28GB via Vulkan"
	$(LLAMA_BIN)/llama-server \
		--model $(MODEL_PATH) \
		--n-gpu-layers $(GPU_LAYERS) \
		--tensor-split $(TENSOR_SPLIT) \
		--host $(HOST) \
		--port $(PORT)

build:
	@echo "Building llama.cpp with Vulkan for dual GPU..."
	cd $(LLAMA_DIR) && mkdir -p build && cd build && \
		cmake .. -DGGML_VULKAN=ON -DCMAKE_BUILD_TYPE=Release && \
		make -j$$(nproc)

verify:
	@echo "GPU targets in libggml-hip.so:"
	@strings $(LLAMA_BIN)/libggml-hip.so | grep -E "amdgcn.*gfx10|amdgcn.*gfx11" | sort -u

clean:
	rm -rf $(LLAMA_DIR)/build

jarvis:
	.venv/bin/python -m src.core.main

$(MODEL_PATH):
	@echo "Model not found: $(MODEL_PATH)"
	@echo "Available models:"
	@ls -1 $(MODELS_DIR)/*.gguf 2>/dev/null || echo "  (none)"
	@exit 1