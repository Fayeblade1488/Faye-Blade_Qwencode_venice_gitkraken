# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

---

## Essential Commands and Workflows

All workflows are managed either by Makefile targets, shell scripts, or the Python CLI entry point. Use these patterns for most tasks:

### Setup & Installation
- **Initial project setup (virtualenv and deps):**
  ```sh
  make setup         # create .venv and install Python dependencies
  make install       # install deps into current Python environment
  ./install.sh       # bash script: checks env, installs deps, runs tests
  ```
- **Python dependencies:** `requirements.txt` (must exist in repo root)

### Build/Test/Lint
- **Run all checks sequentially:**
  ```sh
  make all           # setup, test, and check environments
  ```
- **Run integration/unit tests:**
  ```sh
  make test          # runs test_integration.py using .venv
  python test_integration.py  # (if dependencies installed)
  ```
- **Lint & format code:**
  ```sh
  make lint          # uses flake8 if available in .venv
  make format        # formats code with black if available
  ```
- **Basic system checks (CLI/tools/API):**
  ```sh
  make check         # validates Python, GitKraken CLI, and Venice API key
  make validate      # includes security string/secret checks
  ```
- **Clean environment:**
  ```sh
  make clean         # removes .venv, __pycache__, *.pyc, generated/
  ```

### CLI — Main Python Entry Point
- Use:
  ```sh
  python qwen_cli_integrator.py --help
  ```
- Example GitKraken commands:
  ```sh
  python qwen_cli_integrator.py gitkraken ai_commit            # AI commit gen
  python qwen_cli_integrator.py gitkraken workspace_list       # list workspaces
  python qwen_cli_integrator.py gitkraken work_start "title" --issue "ID"
  ```
- Example Venice AI commands:
  ```sh
  python qwen_cli_integrator.py venice generate --prompt "description here"
  python qwen_cli_integrator.py venice upscale --input input.png --scale 4
  python qwen_cli_integrator.py venice list-models
  ```
- To chat with an LLM model:
  ```sh
  python qwen_cli_integrator.py external chat --provider venice --model venice-uncensored --message "Hello!"
  ```
- Auto-configure Raycast-style providers file (optional):
  ```sh
  python auto_config.py --auto  # verify Venice API, update model config
  ```

### Typical Environment Variables
- **VENICE_API_KEY** — required for all Venice AI image and chat features: export before running commands.
- The API key is always read from your shell `export` (never stored in config by default).
- Optional: adjust `PATH` to include `gk`/GitKraken CLI (`/opt/homebrew/bin`, etc.)

### Troubleshooting
- To verify everything is ready:
  ```sh
  make check
  make test
  python qwen_cli_integrator.py --help
  ```
- Typical issues:
    - GitKraken CLI not found: install from https://www.gitkraken.com/cli
    - Python dependencies: check `requirements.txt`, run `make install`
    - Venice AI key not set: export as shell variable
    - Provider/model config not updated: run `python auto_config.py --auto`
    - See README.md and QUICKSTART_GUIDE.md for more detail

---

## Project Structure & Architecture (High Level)

    / (root)
    ├── qwen_cli_integrator.py
    ├── gitkraken_integration.py
    ├── venice_integration.py
    ├── external_api_integrator.py
    ├── auto_config.py
    ├── test_integration.py
    ├── Makefile, install.sh, requirements.txt
    └── Venice_gitkraken_llm/

- **qwen_cli_integrator.py** — Main CLI. Orchestrates GitKraken, Venice AI, and external provider integrations. Accepts subcommands and dispatches to respective modules.
- **gitkraken_integration.py** — Python wrapper for the GitKraken CLI. Handles all git operations, workspace/issue management, AI-driven workflows, auth provider ops, and status queries via subprocess.
- **venice_integration.py** — Handles all Venice AI API comms: image generation, upscaling, model listing, API key verification, and Raycast config generation. Offers robust session handling, retries, and environment configuration.
- **external_api_integrator.py** — Loads Raycast YAML provider config if present. Enables listing external LLM/image providers and models, and runs completions/chats via configurable endpoints.
- **auto_config.py** — Standalone utility: verifies Venice credentials and updates Raycast config on demand.

### Key Integration Points
- All functionality is CLI accessible; main Python modules expose classes for programmatic use and scripts.
- Venice and GitKraken integrations both require correct binaries/API keys available in environment.
- Provider support expands via Raycast format-compatible configs, updatable via included utilities.

### Model/Extensibility Patterns
- Adding new AI providers: augment provider YAML, re-run auto_config.py; pluggable architecture supports new endpoints.
- AI/LLM chat: use `external_api_integrator.py` for new provider/model endpoints as needed.

### Notes for macOS and Apple Silicon
- All workflows are tested for Python 3.7+ on macOS (tested on Apple Silicon M4, memory-optimized workflows)
- For Homebrew installations, use `/opt/homebrew/bin` in PATH
- Bash and zsh shells are both supported; tested on zsh 5.9

---

## Further Documentation
- See `README.md` for deep-dive on features, config, and usage
- For environment-sync and provider config, review details in QUICKSTART_GUIDE.md
- For provider automation see `auto_config.py` and related CLI help

_Last updated: 2025-09-28_
