# GPU Setup on Arch Linux

## Overview

Setting up dual AMD GPUs for LLM inference using Vulkan.

**GPUs:**

- AMD RX 7800 XT (RDNA3, NAVI32) — 16GB VRAM
- AMD RX 6750 XT (RDNA2, NAVI22) — 12GB VRAM
- **Total: 28GB VRAM**

## Status: ✅ COMPLETE

Both GPUs working together via llama.cpp with Vulkan backend and tensor splitting.

## Why Vulkan Instead of ROCm?

We tried ROCm/HIP first but hit a wall with mixed GPU architectures:

1. **ROCm requires matching gfx versions** - The 7800 XT is gfx1101 (RDNA3) and 6750 XT is gfx1031 (RDNA2). ROCm can't handle both simultaneously.

2. **HSA_OVERRIDE_GFX_VERSION doesn't work per-device** - You can spoof one GPU's architecture, but not independently for each card. Setting a global override crashes during multi-GPU tensor operations.

3. **rocBLAS missing kernels for gfx1031** - Even with overrides, the HIP backend segfaults during warmup because rocBLAS doesn't have precompiled kernels for gfx1031.

4. **Vulkan just works** - The RADV Vulkan driver handles mixed architectures natively. No spoofing, no crashes, both GPUs detected and usable immediately.

**Bottom line:** ROCm is great for single-GPU or matching GPU pairs. For mixed RDNA2+RDNA3, use Vulkan.

## Prerequisites

```bash
# Ensure user is in video group
sudo usermod -aG video $USER
sudo usermod -aG render $USER
# Log out and back in after this
```

## Installation Steps

### 1. Install Vulkan packages

```bash
# AMD Vulkan driver (RADV - Mesa's open source driver)
sudo pacman -S vulkan-radeon

# Vulkan tools (optional, for debugging)
sudo pacman -S vulkan-tools
```

### 2. Verify GPU detection

```bash
# Check Vulkan sees both GPUs
vulkaninfo --summary

# Should show both:
# - AMD Radeon RX 7800 XT (RADV NAVI32)
# - AMD Radeon RX 6750 XT (RADV NAVI22)
```

### 3. Build llama.cpp with Vulkan

```bash
cd ~/Documents
git clone https://github.com/ggerganov/llama.cpp.git

# Use the Makefile in jarvis/ to build
cd ~/Documents/jarvis
make build
```

Or manually:

```bash
cd ~/Documents/llama.cpp
mkdir -p build && cd build
cmake .. -DGGML_VULKAN=ON -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

### 4. Verify Vulkan devices in llama.cpp

```bash
~/Documents/llama.cpp/build/bin/llama-server --list-devices

# Should show:
# Vulkan0: AMD Radeon RX 7800 XT (RADV NAVI32) (16368 MiB)
# Vulkan1: AMD Radeon RX 6750 XT (RADV NAVI22) (12272 MiB)
```

### 5. Set up models

Models live in `~/Documents/jarvis/models/`. Download GGUF files there:

```bash
# Example: download 32B abliterated model (~20GB)
huggingface-cli download tensorblock/Qwen2.5-32B-Instruct-abliterated-GGUF \
  Qwen2.5-32B-Instruct-abliterated-Q4_K_M.gguf \
  --local-dir ~/Documents/jarvis/models
```

## Usage

From the jarvis directory:

```bash
cd ~/Documents/jarvis

# API server (default port 8080)
make server

# API server on custom port
make server PORT=9000

# Use a specific model
make server MODEL=Qwen2.5-32B-Instruct-abliterated-Q4_K_M.gguf PORT=9000
```

## Current State

**Models:** `~/Documents/jarvis/models/`

- Qwen2.5-32B-Instruct-abliterated-Q4_K_M.gguf (~20GB)
- qwen2.5-abliterate-14b.gguf (8GB, symlinked from Ollama)

**llama.cpp:** `~/Documents/llama.cpp/build/bin/`

- Built with: `-DGGML_VULKAN=ON`
- Both GPUs working with tensor split (57%/43% based on VRAM ratio)
- 14B model: ~29 tokens/sec
- 32B model: ~16.5 tokens/sec

## GPU Monitoring

```bash
# ROCm SMI shows VRAM usage (works for Vulkan too)
rocm-smi

# radeontop shows GPU activity per card
# Use -b flag for specific GPU by PCI bus
radeontop -b 0b:00.0  # 7800 XT
radeontop -b 06:00.0  # 6750 XT
```

Note: `rocm-smi` won't show GPU compute % for Vulkan workloads (only HIP), but VRAM usage is accurate.

## Troubleshooting

### "No Vulkan devices found"

- Install `vulkan-radeon` package
- Check with `vulkaninfo --summary`

### Only one GPU detected

- Both GPUs must have the Vulkan driver loaded
- Check `ls /dev/dri/` for both render nodes

### Model doesn't fit in VRAM

- Use `--tensor-split` to control distribution (e.g., `16,12` for 16GB/12GB split)
- Try a smaller quantization (Q3_K_M instead of Q4_K_M)

## Next Steps

1. ~~Install Vulkan driver~~ ✅
2. ~~Build llama.cpp with Vulkan~~ ✅
3. ~~Test dual GPU inference~~ ✅
4. ~~Download 32B model~~ ✅
5. Move on to `02-whisper.md` for STT setup
