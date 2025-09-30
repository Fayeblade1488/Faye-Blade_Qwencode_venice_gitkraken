# WARP.md

This file provides comprehensive guidance to WARP AI agents when working with this repository.

---

## Project Overview

**Qwen CLI Integration: GitKraken & Venice AI**

This repository provides a comprehensive integration between Qwen CLI and powerful tools for developers. The system combines GitKraken's AI-powered Git workflow capabilities with Venice AI's uncensored image generation features, all accessible through a unified command-line interface.

### Key Components

1. **GitKraken CLI Integration** - AI-assisted Git operations including commit generation, conflict resolution, PR creation, and workspace management
2. **Venice AI Integration** - Uncensored image generation and upscaling using the `lustify-sdxl` model
3. **External API Integration** - Support for multiple AI providers with Raycast-format configuration (Raycast installation is optional)

### Current Status

- **Latest Commit**: 6498a45 - "Add comprehensive test coverage for critical code paths"
- **Branch**: main
- **Default Image Model**: `lustify-sdxl` (updated from flux-dev-uncensored)
- **Default Steps**: 50 (optimized for lustify-sdxl)
- **Repository**: https://github.com/Fayeblade1488/Faye-Blade_Qwencode_venice_gitkraken

---

## Essential Commands and Workflows

All workflows are managed through Makefile targets, shell scripts, or the Python CLI entry point.

### Setup & Installation

**Initial project setup:**
```sh
make setup         # create .venv and install Python dependencies
make install       # install deps into current Python environment
./install.sh       # bash script: checks env, installs deps, runs tests
```

**Python dependencies:** `requirements.txt` (must exist in repo root)

### Build/Test/Lint

**Run all checks sequentially:**
```sh
make all           # setup, test, and check environments
```

**Run integration/unit tests:**
```sh
make test          # runs test_integration.py using .venv
python test_integration.py  # (if dependencies installed)
```

**Lint & format code:**
```sh
make lint          # uses flake8 if available in .venv
make format        # formats code with black if available
```

**Basic system checks:**
```sh
make check         # validates Python, GitKraken CLI, and Venice API key
make validate      # includes security string/secret checks
```

**Clean environment:**
```sh
make clean         # removes .venv, __pycache__, *.pyc, generated/
```

### CLI — Main Python Entry Point

**Help and basic usage:**
```sh
python qwen_cli_integrator.py --help
```

**GitKraken Commands:**
```sh
python qwen_cli_integrator.py gitkraken ai_commit            # AI commit gen
python qwen_cli_integrator.py gitkraken workspace_list       # list workspaces
python qwen_cli_integrator.py gitkraken work_start "title" --issue "ID"
python qwen_cli_integrator.py gitkraken ai_resolve           # resolve conflicts
```

**Venice AI Commands:**
```sh
# Generate image with default lustify-sdxl model
python qwen_cli_integrator.py venice generate --prompt "description here"

# Generate with specific parameters
python qwen_cli_integrator.py venice generate \
  --prompt "cyberpunk cityscape" \
  --model lustify-sdxl \
  --aspect-ratio wide \
  --steps 50 \
  --cfg-scale 7.0 \
  --upscale

# Upscale existing image
python qwen_cli_integrator.py venice upscale --input input.png --scale 4

# List available models
python qwen_cli_integrator.py venice list-models
```

**External API Commands:**
```sh
# Chat with an LLM model
python qwen_cli_integrator.py external chat \
  --provider venice \
  --model venice-uncensored \
  --message "Hello!"
```

**Auto-Configuration:**
```sh
python auto_config.py --auto  # verify Venice API, update model config
python auto_config.py --verify  # verify API key only
```

### Typical Environment Variables

- **VENICE_API_KEY** — required for all Venice AI image and chat features: export before running commands
- The API key is always read from your shell `export` (never stored in config by default)
- Optional: adjust `PATH` to include `gk`/GitKraken CLI (`/opt/homebrew/bin`, etc.)

### Troubleshooting

**Verify everything is ready:**
```sh
make check
make test
python qwen_cli_integrator.py --help
```

**Typical issues:**
- GitKraken CLI not found: install from https://www.gitkraken.com/cli
- Python dependencies: check `requirements.txt`, run `make install`
- Venice AI key not set: export as shell variable (`export VENICE_API_KEY="your_key"`)
- Provider/model config not updated: run `python auto_config.py --auto`
- See README.md and QUICKSTART_GUIDE.md for more detail

---

## Project Structure & Architecture

```
/ (root)
├── qwen_cli_integrator.py        # Main CLI orchestrator
├── gitkraken_integration.py      # GitKraken CLI wrapper
├── venice_integration.py         # Venice AI API integration
├── external_api_integrator.py    # External provider integration
├── auto_config.py                # Auto-configuration utility
├── test_integration.py           # Integration tests
├── test_bug_fixes.py             # Bug fix tests
├── test_comprehensive_coverage.py # Coverage tests
├── Makefile, install.sh          # Build and setup scripts
├── requirements.txt              # Python dependencies
├── AGENT.md                      # Agent-specific documentation
├── WARP.md                       # This file (Warp AI guidance)
├── README.md                     # Comprehensive user documentation
├── QUICKSTART_GUIDE.md           # Beginner-friendly guide
├── Venice_gitkraken_llm/         # Legacy/alternative implementations
├── tests/                        # Test suite directory
├── docs/                         # Documentation and logs
├── patches/                      # Archived patches
└── tools/                        # Utility scripts
```

### Core Modules

**qwen_cli_integrator.py** — Main CLI orchestrator
- Accepts subcommands and dispatches to appropriate integration modules
- Handles argument parsing and command routing
- Unified interface for all functionality

**gitkraken_integration.py** — GitKraken CLI wrapper
- Python wrapper for all `gk` commands
- Handles git operations, workspace/issue management
- AI-driven workflows, auth provider operations, status queries via subprocess

**venice_integration.py** — Venice AI integration
- Handles all Venice AI API communications
- Image generation, upscaling, model listing, API key verification
- Raycast config generation
- Robust session handling, retries, environment configuration
- **Default model: `lustify-sdxl`** (50 steps recommended)

**external_api_integrator.py** — External provider integration
- Loads Raycast YAML provider config if present
- Lists external LLM/image providers and models
- Runs completions/chats via configurable endpoints

**auto_config.py** — Auto-configuration utility
- Verifies Venice credentials
- Updates Raycast config on demand
- Standalone utility for setup automation

### Key Integration Points

- All functionality is CLI accessible
- Main Python modules expose classes for programmatic use
- Venice and GitKraken integrations require correct binaries/API keys in environment
- Provider support expands via Raycast format-compatible configs

### Model/Extensibility Patterns

- **Adding new AI providers**: augment provider YAML, re-run auto_config.py
- **AI/LLM chat**: use `external_api_integrator.py` for new provider/model endpoints
- **Image generation defaults**: modify `venice_integration.py` VeniceAIImageGenerator class

### Notes for macOS and Apple Silicon

- All workflows tested on Python 3.7+ on macOS (Apple Silicon M4)
- Memory-optimized workflows for 16GB systems
- Homebrew installations: use `/opt/homebrew/bin` in PATH
- Bash and zsh shells supported; tested on zsh 5.9

---

## Important Configuration Details

### Default Image Generation Settings

The Venice AI integration uses the following defaults (optimized for `lustify-sdxl`):

- **Model**: `lustify-sdxl` (uncensored model)
- **Steps**: 50 (optimized for lustify-sdxl)
- **CFG Scale**: 5.0
- **Aspect Ratio**: tall (768x1024)
- **Output Format**: PNG
- **Safe Mode**: Disabled (for uncensored generation)
- **Watermark**: Hidden by default

These can be overridden via CLI arguments or function parameters.

### Security Features

- **Sensitive Data Redaction**: All API responses containing API keys, tokens, passwords are automatically redacted before logging
- **Environment Variable Only**: API keys must be provided via environment variables, never in code or config files
- **Secure Retry Logic**: Built-in retry mechanisms with exponential backoff for API calls
- **Timeout Protection**: All API calls have connection and read timeouts to prevent hanging
- **No Cleartext Logging**: Sensitive information is never logged in cleartext (fixed in recent commits)

### Git Workflow Integration

- Configured for SSH-based commit signing
- Conventional commits enforced globally via commit-msg hook
- VS Code integration for Git operations
- GitHub CLI authenticated with appropriate scopes
- Lefthook for Git hooks management

---

## Recent Changes and Improvements

### September 2025 Updates

1. **Model Change**: Replaced `flux-dev-uncensored` with `lustify-sdxl` as default model
   - Updated all code, documentation, and tests
   - Adjusted default steps from 30 to 50 for optimal quality
   - Updated uncensored_keywords arrays to include lustify-sdxl

2. **Bug Fixes**: 
   - Fixed cleartext logging of sensitive information (PR #4)
   - Resolved merge conflicts in README.md and qwen_cli_integrator.py
   - Enhanced test coverage for critical code paths

3. **Documentation**: 
   - Comprehensive README updates with Raycast-independent usage instructions
   - Created QUICKSTART_GUIDE.md for beginners
   - Added AGENT.md for AI agent-specific guidance
   - Created this WARP.md for Warp AI agents

4. **Testing**: 
   - Added comprehensive test coverage
   - Created test_bug_fixes.py for regression testing
   - Enhanced test_comprehensive_coverage.py

---

## Development Guidelines

### Code Style

- **Python PEP 8** style guidelines
- **Google-style docstrings** for all public functions/methods/classes
- **Type hints** where applicable
- **Security-first approach**: API keys are never logged or stored in configs

### Testing

```sh
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=. --cov-report=html

# Run specific test file
python -m pytest test_integration.py
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes with tests
4. Follow existing code style and docstring conventions
5. Ensure all tests pass
6. Commit with conventional commit format: `git commit -m "type: description"`
7. Push to your fork and open a Pull Request

### Conventional Commits

This repository uses conventional commit messages:
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `refactor:` code refactoring
- `test:` test additions or modifications
- `chore:` maintenance tasks

---

## Further Documentation

- **README.md** — Comprehensive user documentation with all features, configuration, and usage
- **QUICKSTART_GUIDE.md** — Beginner-friendly guide with step-by-step instructions
- **AGENT.md** — AI agent-specific commands and workflows (similar to this file)
- **PROJECT_SUMMARY.md** — Project goals, recent actions, and current plan
- **docs/** directory — Additional documentation, logs, and API inventories

---

## Support and Resources

- **GitHub Issues**: https://github.com/Fayeblade1488/Faye-Blade_Qwencode_venice_gitkraken/issues
- **GitHub Discussions**: https://github.com/Fayeblade1488/Faye-Blade_Qwencode_venice_gitkraken/discussions
- **GitKraken CLI**: https://www.gitkraken.com/cli
- **Venice AI**: https://venice.ai

---

_Last updated: 2025-09-30_
_Default model: lustify-sdxl_
_Maintained for: Warp AI agents and human contributors_