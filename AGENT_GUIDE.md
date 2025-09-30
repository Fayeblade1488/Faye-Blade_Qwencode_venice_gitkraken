# CLI Agent Guide for Qwen Venice Integration

**Purpose**: This guide is specifically designed for AI CLI agents (like Qwen) to understand and use this codebase efficiently.

---

## 🎯 What This Project Does

This is a **unified CLI tool** that integrates:
1. **Venice AI** - Uncensored image generation and upscaling (`lustify-sdxl` model)
2. **GitKraken CLI** - AI-powered Git workflow operations
3. **External APIs** - Generic provider integration via Raycast-format configs

---

## 📁 File Structure (Essential Files Only)

```
/Faye-Blade_Qwencode_venice_gitkraken/
├── qwen_cli_integrator.py        # MAIN ENTRY POINT - Start here
├── venice_integration.py         # Venice AI module (image generation)
├── gitkraken_integration.py      # GitKraken CLI wrapper  
├── external_api_integrator.py    # External API provider support
├── auto_config.py                # Config verification/update utility
├── requirements.txt              # Python dependencies
├── Makefile                      # Build/test automation
├── install.sh                    # Installation script
├── test_integration.py           # Integration tests
├── README.md                     # Human-readable documentation
├── QUICKSTART_GUIDE.md           # Getting started guide
└── AGENT_GUIDE.md                # This file (for AI agents)
```

---

## 🚀 Quick Start for CLI Agents

### 1. Installation Check
```bash
# Verify dependencies
python3 -m pip list | grep -E "requests|pyyaml"

# Install if needed
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
# Required: Venice API key
export VENICE_API_KEY="your_key_here"

# Optional: GitKraken CLI path (if not in PATH)
export PATH="/opt/homebrew/bin:$PATH"
```

### 3. Basic Usage
```bash
# Get help
python qwen_cli_integrator.py --help

# Generate image (uses lustify-sdxl by default)
python qwen_cli_integrator.py venice generate --prompt "description"

# GitKraken operations
python qwen_cli_integrator.py gitkraken ai_commit
```

---

## 📚 Module Reference

### qwen_cli_integrator.py
**Purpose**: Main CLI orchestrator  
**Usage**: Entry point for all commands  
**Key Class**: `QwenCLIIntegrator`  
**Commands**: 
- `gitkraken` - Git operations
- `venice` - Image generation
- `external` - External API calls

### venice_integration.py
**Purpose**: Venice AI API integration  
**Key Classes**:
- `VeniceAIImageGenerator` - Generate/upscale images
- `VeniceAIVerifier` - Verify API keys
- `VeniceAIConfigUpdater` - Update Raycast configs

**Default Settings**:
- Model: `lustify-sdxl`
- Steps: 50
- Safe Mode: Disabled (uncensored)
- CFG Scale: 5.0

**Key Methods**:
```python
generator = VeniceAIImageGenerator(api_key)
result = generator.generate_image(prompt="...", model="lustify-sdxl")
result = generator.upscale_image_file(image_path="...", scale=4)
models = generator.list_models()
```

### gitkraken_integration.py
**Purpose**: GitKraken CLI wrapper  
**Key Class**: `GitKrakenCLI`  
**Commands**: ai_commit, ai_resolve, workspace_list, work_start, etc.

**Key Methods**:
```python
gk = GitKrakenCLI()
result = gk.ai_commit(path="/repo/path")
result = gk.workspace_list()
```

### external_api_integrator.py
**Purpose**: Generic external API provider support  
**Key Class**: `ExternalAPIIntegrator`  
**Config Format**: Raycast YAML (optional)  
**Config Path**: `~/.config/raycast/ai/providers.yaml`

### auto_config.py
**Purpose**: Standalone config verification utility  
**Usage**:
```bash
python auto_config.py --verify      # Check API key
python auto_config.py --auto        # Verify & update config
```

---

## 🔧 Environment Variables

| Variable | Required | Purpose | Example |
|----------|----------|---------|---------|
| `VENICE_API_KEY` | **Yes** | Venice AI authentication | `export VENICE_API_KEY="key123"` |
| `PATH` | No | GitKraken CLI location | Ensure `gk` command is accessible |

---

## 💡 Common Agent Tasks

### Task: Generate an image
```python
from qwen_cli_integrator import QwenCLIIntegrator

integrator = QwenCLIIntegrator()
result = integrator.venice_generate_image(
    prompt="cyberpunk cityscape",
    model="lustify-sdxl",
    aspect_ratio="wide",
    steps=50,
    auto_upscale=True
)
print(result["generated_image_path"])
```

### Task: Create AI commit message
```python
integrator = QwenCLIIntegrator()
result = integrator.gitkraken_command("ai_commit", path="/path/to/repo")
print(result)
```

### Task: List available models
```python
integrator = QwenCLIIntegrator()
result = integrator.list_available_models()
print(f"Found {len(result['uncensored_models'])} uncensored models")
```

---

## 🐛 Troubleshooting for Agents

### Issue: "Venice AI not initialized"
**Solution**: Ensure `VENICE_API_KEY` environment variable is set
```bash
export VENICE_API_KEY="your_key_here"
```

### Issue: "GitKraken CLI not found"
**Solution**: Install GitKraken CLI or add to PATH
```bash
# macOS Homebrew
brew install --cask gitkraken-cli
```

### Issue: Import errors
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "No module named 'yaml'"
**Solution**: Install PyYAML (optional but recommended)
```bash
pip install pyyaml
```

---

## 📊 Agent Decision Tree

```
START
  │
  ├─ Need to generate images? 
  │   └─ Use: qwen_cli_integrator.py venice generate
  │
  ├─ Need Git operations?
  │   └─ Use: qwen_cli_integrator.py gitkraken [command]
  │
  ├─ Need to verify Venice API?
  │   └─ Use: auto_config.py --verify
  │
  ├─ Need to configure providers?
  │   └─ Use: auto_config.py --auto
  │
  └─ Need custom integration?
      └─ Import modules directly (see Module Reference)
```

---

## 🔍 Code Navigation Tips for Agents

1. **Start with**: `qwen_cli_integrator.py` - Contains main() and all CLI routing
2. **For Venice AI**: Look at `VeniceAIImageGenerator` class in `venice_integration.py`
3. **For Git ops**: Look at `GitKrakenCLI` class in `gitkraken_integration.py`
4. **For examples**: Check `test_integration.py` for usage patterns
5. **For setup**: Review `Makefile` targets (`make check`, `make test`, `make install`)

---

## 🎓 Key Concepts for Agents

### 1. Default Model
- **Current**: `lustify-sdxl` (uncensored image generation)
- **Steps**: 50 (optimal for this model)
- **Override**: Pass `--model` flag or `model=` parameter

### 2. CLI Architecture
- Single entry point (`qwen_cli_integrator.py`)
- Subcommands for each integration (`venice`, `gitkraken`, `external`)
- Consistent JSON output for programmatic parsing

### 3. API Key Security
- **Never logged** or stored in configs
- **Always** read from environment variables
- **Redacted** in all output/logs automatically

### 4. Error Handling
- All functions return dicts with `success` boolean
- Check `result['success']` before using data
- Error details in `result['error']` if failed

---

## 📝 Example Agent Workflow

```python
#!/usr/bin/env python3
"""Example workflow for CLI agents"""

import os
from qwen_cli_integrator import QwenCLIIntegrator

# 1. Verify environment
if not os.getenv("VENICE_API_KEY"):
    print("ERROR: VENICE_API_KEY not set")
    exit(1)

# 2. Initialize integrator
integrator = QwenCLIIntegrator()

# 3. Generate image
result = integrator.venice_generate_image(
    prompt="futuristic city at night",
    model="lustify-sdxl",
    steps=50,
    auto_upscale=True,
    verbose=True
)

# 4. Check result
if result.get("success"):
    print(f"✅ Image generated: {result['generated_image_path']}")
    if result.get("upscaled_image_path"):
        print(f"✅ Upscaled: {result['upscaled_image_path']}")
else:
    print(f"❌ Error: {result.get('error', 'Unknown error')}")
```

---

## 🔗 Integration Points

### With Other Systems
- **Raycast**: Can read/write Raycast provider configs (optional)
- **Git**: Requires GitKraken CLI binary for Git operations
- **APIs**: Supports OpenAI-compatible API endpoints

### Python Integration
```python
# Import as library
from venice_integration import VeniceAIImageGenerator
from gitkraken_integration import GitKrakenCLI

# Use directly
generator = VeniceAIImageGenerator(api_key="key")
gk = GitKrakenCLI()
```

---

## 📌 Important Notes for Agents

1. **Flat Structure**: All essential files are in root directory for easy access
2. **No Subdirectories**: Simplified structure - no nested module directories
3. **Self-Contained**: Each module is independent and can be imported separately
4. **CLI-First**: Designed for command-line usage, library usage is secondary
5. **Default Model**: Always use `lustify-sdxl` unless user specifies otherwise
6. **Steps**: Default 50 steps for lustify-sdxl (don't use 30 from old configs)

---

## 🚦 Status Indicators

When parsing output, look for these indicators:

```python
result = {
    "success": True/False,      # Operation succeeded?
    "error": "message",          # Error details (if failed)
    "generated_image_path": "",  # Output file path
    "metadata": {},              # Additional info
}
```

---

**Last Updated**: 2025-09-30  
**Optimized For**: AI CLI agents (Qwen, etc.)  
**Model**: lustify-sdxl (default)  
**Structure**: Flat, essential files only