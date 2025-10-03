# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Essential Development Commands

### Installation & Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up for Gemini environment (copies scripts to ~/.gemini)
make setup-gemini

# Set up for Qwen environment (copies scripts to ~/.qwen)
make setup-qwen

# Install development tools
pip install pytest pytest-cov pytest-mock flake8 black isort pylint
```

### Environment Configuration
```bash
# Required: Set Venice AI API key
export VENICE_API_KEY="your_api_key_here"

# Verify Venice API configuration
python auto_config.py --verify

# Check API key is set
echo $VENICE_API_KEY
```

### Running Tests
```bash
# Run all tests
pytest tests/

# Run tests quietly
pytest -q tests/

# Run with fail-fast and last-failed optimization
pytest -x --ff tests/

# Run with coverage report
pytest --cov=. --cov-report=term-missing tests/

# Run specific test file
pytest tests/test_integration.py -v
```

### Code Quality & Linting
```bash
# Run flake8 linter
flake8 . --max-line-length=120

# Format code with Black (120 char line length)
black . --line-length 120

# Sort imports with isort
isort . --profile black

# Check formatting without changes
black --check . --line-length 120
isort --check-only . --profile black
```

### CLI Usage
```bash
# Get help
python qwen_cli_integrator.py --help

# Generate image with Venice AI
python qwen_cli_integrator.py venice generate --prompt "description" --model lustify-sdxl

# GitKraken operations
python qwen_cli_integrator.py gitkraken ai_commit
python qwen_cli_integrator.py gitkraken workspace_list
```

## High-Level Architecture

### Unified CLI Integration
This is a **unified CLI tool** that bridges three distinct integrations:
- **Venice AI**: Uncensored image generation and upscaling
- **GitKraken CLI**: AI-powered Git workflow operations  
- **External API Providers**: Generic provider abstraction layer

### Core Entry Point
- **`qwen_cli_integrator.py`**: Main orchestrator providing the `QwenCLIIntegrator` class
  - Dispatches commands to appropriate integration modules
  - Handles cross-tool workflows
  - Provides unified CLI interface via argparse

### Integration Modules (Flat Structure)
All modules are in the repository root (no nested packages):

- **`venice_integration.py`**: Venice AI image generation
  - Default model: `lustify-sdxl` with 50 steps
  - Supports image generation, upscaling (4x), and model listing
  - Authentication: `VENICE_API_KEY` environment variable
  - Key classes: `VeniceAIImageGenerator`, `VeniceAIVerifier`, `VeniceAIConfigUpdater`

- **`gitkraken_integration.py`**: GitKraken CLI wrapper
  - Wraps `gk` command-line tool for Git operations
  - AI-powered features: commit generation, conflict resolution, PR creation
  - Standard operations: branch management, workspace operations, status queries
  - Key class: `GitKrakenCLI`

- **`external_api_integrator.py`**: External API provider support
  - Provider-agnostic abstraction layer
  - Loads configurations from Raycast YAML format (optional)
  - Centralizes authentication and configuration
  - Config path: `~/.config/raycast/ai/providers.yaml`
  - Key class: `ExternalAPIIntegrator`

- **`auto_config.py`**: Configuration verification utility
  - Standalone tool for API key verification
  - Can automatically update Raycast configurations
  - Usage: `python auto_config.py --verify` or `python auto_config.py --auto`

### Configuration Philosophy
- **No secrets in repository**: All API keys loaded from environment variables
- **Environment-based setup**: Uses `.gemini` or `.qwen` home directory structure
- **Settings file**: `setting_to_apply.json` copied during setup but contains no secrets

### Scripts Directory Structure
```
scripts/
├── gemini/     # Full set of modules for Gemini environment
└── qwen/       # Full set of modules for Qwen environment
```
Setup targets copy these to `~/.gemini/` or `~/.qwen/` respectively.

## Ongoing Improvement Work

### Current Development Context
- **Branch**: `chore/docs-tests-bugfix-qwen-cli`
- **Recent commit**: `dc78083` (fixed merge conflicts and test syntax errors)
- **Test baseline**: 60 tests passing, 5 tests failing (pre-existing issues, not regressions)
- **Repository state**: Clean working state on feature branch, ready for enhancement

### In-Progress Tasks
1. **Comprehensive Docstrings**: Adding complete docstrings across 5 core modules
2. **Test Coverage Expansion**: Creating new test files to cover high-risk code paths
3. **Security Hardening**: `yaml.safe_load()` already implemented (was security issue)
4. **Documentation Overhaul**: README enhancement, architecture guides, this WARP.md

### Priority Items (from previous session)
- **Critical bug fix**: Security issue with yaml loading (✓ already fixed)
- **Core module documentation**: Focus on `qwen_cli_integrator`, `venice_integration`, `external_api_integrator`
- **Essential test coverage**: New test files targeting highest-risk paths
- **Architecture documentation**: This WARP.md and README updates

## Important Development Notes

### Requirements
- **Python**: 3.7+ required
- **Optional**: GitKraken CLI (`gk` command) for Git operations
- **Required for image gen**: Venice AI API key

### Code Style & Standards
- **Commit format**: Conventional commits enforced (`feat:`, `fix:`, `docs:`, `chore:`, etc.)
- **Formatting**: Black with 120 character line length
- **Import sorting**: isort with black profile
- **Linting**: flake8 with max-complexity=10

### Security Best Practices
- Never commit API keys or secrets
- Always use environment variables for configuration
- API keys are automatically redacted in logs
- Client-side CSAM guard implemented (content filtering)

### Testing Stack
- **pytest**: Test framework
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking support
- Test files located in `tests/` directory

### GitHub Workflows
- **tests.yml**: Runs pytest on push/PR to main
- **linting.yml**: Runs flake8, black, isort checks
- **security.yml**: Security scanning

### Notable Defaults
- **Venice model**: `lustify-sdxl` (uncensored)
- **Generation steps**: 50 (optimal for lustify-sdxl)
- **Safe mode**: Disabled by default
- **CFG scale**: 5.0

### Module Dependencies
```
qwen_cli_integrator.py
├── gitkraken_integration.py (no external deps)
├── venice_integration.py (requires: requests, urllib3)
└── external_api_integrator.py (requires: requests, pyyaml [optional])
```
