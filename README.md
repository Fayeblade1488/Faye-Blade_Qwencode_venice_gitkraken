# 🚀 Qwen CLI Integration: GitKraken & Venice AI 🎨
<img width="1536" height="1024" alt="image2 copy" src="https://github.com/user-attachments/assets/a23c49db-d0b8-4468-aa5a-a85e1b3ab0f3" />

```
╔══════════════════════════════════════════════════════════════════════╗
║                          Qwen CLI Integrator                         ║
║                GitKraken + Venice AI + External APIs                 ║
║                                                                      ║
║  🔐 Secure API Key Management     🧠 AI-Powered Workflows            ║
║  🖼️ Uncensored Image Generation   📡 Real-time Model Updates         ║
║  ⚡ Auto-Configuration             🛡️ Security-First Approach         ║
╚══════════════════════════════════════════════════════════════════════╝
```

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Security Considerations](#security-considerations)
- [Quick Start Guide](QUICKSTART_GUIDE.md) 
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

This repository provides a comprehensive integration between Qwen CLI and powerful tools:

1. **GitKraken CLI**: A complete, AI-powered Git workflow enhancement suite that allows for seamless Git operations with AI assistance
2. **Venice AI Integration**: An uncensored AI system that provides both image generation and chat capabilities
3. **External API Integration**: Support for multiple AI providers including Venice AI, with config loading from Raycast format

The integration is designed to work within the Qwen CLI ecosystem, allowing users to leverage advanced Git workflows and AI-powered services directly from their command line. **Note: While the system can read provider configurations from Raycast's format, Raycast is NOT required for usage.**

## Features

### GitKraken CLI Integration
- Full command-line access to GitKraken's features
- AI-powered commit generation, conflict resolution, and PR creation
- Workspace and issue management
- Authentication and provider token management

### Venice AI Integration
- Uncensored image generation using models like `flux-dev-uncensored`
- Image upscaling with enhancement capabilities
- Support for various aspect ratios and formats
- Automatic upscaling of generated images

## Prerequisites

1. GitKraken CLI installed on your system
2. Venice AI API key for image generation
3. Python 3.7+

## Installation

1. Clone or download this repository
2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your Venice API key:

```bash
export VENICE_API_KEY="your_api_key_here"
```

## Usage

### Command Line Interface

The main interface is through the `qwen_cli_integrator.py` script:

```bash
python qwen_cli_integrator.py --help
```

#### GitKraken Commands

Generate a commit message with AI:
```bash
python qwen_cli_integrator.py gitkraken ai_commit
```

List workspaces:
```bash
python qwen_cli_integrator.py gitkraken workspace_list
```

Start a new work item:
```bash
python qwen_cli_integrator.py gitkraken work_start "my-feature" --issue "ISS-123"
```

#### Venice AI Commands

Generate an uncensored image:
```bash
python qwen_cli_integrator.py venice generate --prompt "fantasy landscape at sunset"
```

Generate an image with specific parameters:
```bash
python qwen_cli_integrator.py venice generate \
  --prompt "cyberpunk cityscape" \
  --model flux-dev-uncensored \
  --aspect-ratio wide \
  --steps 30 \
  --cfg-scale 7.0 \
  --upscale
```

Upscale an existing image:
```bash
python qwen_cli_integrator.py venice upscale --input my_image.png --scale 4
```

List available models:
```bash
python qwen_cli_integrator.py venice list-models
```

### Python API

You can also use the integrations directly in Python:

```python
from qwen_cli_integrator import QwenCLIIntegrator

integrator = QwenCLIIntegrator()

# GitKraken example
result = integrator.gitkraken_command('workspace_list')
print(result)

# Venice example
result = integrator.venice_generate_image(
    prompt="abstract art with vibrant colors",
    model="flux-dev-uncensored",
    upscale=True
)
print(result)
```

## Configuration

### GitKraken CLI

Make sure the `gk` command is in your PATH. If GitKraken CLI is installed but not in PATH, you may need to add it:

```bash
# For macOS with Homebrew
export PATH="/opt/homebrew/bin:$PATH"

# For Linux with snap
export PATH="$HOME/snap/bin:$PATH"
```

### Venice AI

Set your Venice API key as an environment variable:

```bash
export VENICE_API_KEY="your_api_key_here"
```

Or pass it directly to the VeniceAIImageGenerator constructor in code.

## Safety Notice

When using the uncensored image generation capabilities, please be aware that the generated content may not be filtered for adult content. Use appropriate discretion and consider your usage context.

## API Endpoints Used

- GitKraken CLI: Local command-line interface
- Venice AI: `https://api.venice.ai/api/v1/image/generate` and related endpoints

## Troubleshooting

1. **GitKraken CLI not found**: Ensure that the `gk` command is in your system PATH
2. **Venice API key error**: Make sure you have set the `VENICE_API_KEY` environment variable
3. **Rate limiting**: You may encounter rate limits with the Venice API depending on your account tier

## Development

### Setting Up Development Environment

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Fayeblade1488/Faye-Blade_Qwencode_venice_gitkraken.git
   cd Faye-Blade_Qwencode_venice_gitkraken
   ```

2. **Create a Virtual Environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:
   ```bash
   export VENICE_API_KEY="your_venice_api_key"
   ```

### Project Structure

```
.
├── gitkraken_integration.py      # GitKraken CLI wrapper
├── venice_integration.py         # Venice AI image generation & verification
├── external_api_integrator.py    # External AI provider integration
├── qwen_cli_integrator.py        # Main CLI orchestrator
├── auto_config.py                # Auto-configuration script
├── test_integration.py           # Integration tests
├── AGENT.md                      # Documentation for AI agents
├── QUICKSTART_GUIDE.md           # Beginner-friendly guide
└── README.md                     # This file
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=. --cov-report=html

# Run specific test file
python -m pytest test_integration.py
```

### Code Quality

This project follows:
- **Python PEP 8** style guidelines
- **Google-style docstrings** for all public functions/methods/classes
- **Type hints** where applicable
- **Security-first approach**: API keys are never logged or stored in configs

### Security Features

- **Sensitive Data Redaction**: All API responses containing API keys, tokens, passwords are automatically redacted before logging
- **Environment Variable Only**: API keys must be provided via environment variables, never in code or config files
- **Secure Retry Logic**: Built-in retry mechanisms with exponential backoff for API calls
- **Timeout Protection**: All API calls have connection and read timeouts to prevent hanging

## Architecture

### Component Overview

1. **QwenCLIIntegrator** (`qwen_cli_integrator.py`)
   - Main orchestrator class
   - Delegates commands to appropriate integration modules
   - Handles CLI argument parsing and command routing

2. **GitKrakenCLI** (`gitkraken_integration.py`)
   - Wraps GitKraken CLI (`gk`) commands
   - Provides Python API for all GitKraken features
   - Includes AI-powered Git workflows

3. **VeniceAIImageGenerator** (`venice_integration.py`)
   - Handles image generation and upscaling
   - Supports uncensored models
   - Automatic retry logic and error handling

4. **VeniceAIVerifier** (`venice_integration.py`)
   - API key verification
   - Model fetching and discovery

5. **VeniceAIConfigUpdater** (`venice_integration.py`)
   - Auto-generates Raycast configuration
   - Keeps model lists up-to-date

6. **ExternalAPIIntegrator** (`external_api_integrator.py`)
   - Generic external AI provider support
   - Reads Raycast-format configuration files
   - Extensible for multiple providers

### Data Flow

```
User Command → qwen_cli_integrator.py → Specific Integration Module → External API/CLI
                                      ↓
                               Response Processing & Redaction
                                      ↓
                               Return to User (Secure)
```

## Contributing

### How to Contribute

1. **Fork the Repository**
2. **Create a Feature Branch**: `git checkout -b feature/your-feature-name`
3. **Make Your Changes**:
   - Add tests for new functionality
   - Follow existing code style and docstring conventions
   - Ensure all tests pass
4. **Commit Your Changes**: `git commit -m "Description of changes"`
5. **Push to Your Fork**: `git push origin feature/your-feature-name`
6. **Open a Pull Request**

### Reporting Issues

- Use GitHub Issues to report bugs
- Include:
  - Python version
  - Operating system
  - Steps to reproduce
  - Expected vs. actual behavior
  - Relevant error messages (with sensitive data redacted)

### Code Review Process

All pull requests are reviewed by:
- **GitHub Copilot AI**: Automated code quality checks
- **Sourcery AI**: Code improvement suggestions
- **Gemini Code Assist**: Security and best practice analysis
- **Maintainers**: Final human review

## FAQ

### Q: Do I need Raycast installed to use this?
**A**: No! While the system can read Raycast configuration format, Raycast is completely optional.

### Q: Is my API key safe?
**A**: Yes. API keys are:
- Never logged or printed
- Never stored in configuration files
- Only loaded from environment variables
- Automatically redacted from all output

### Q: What models support uncensored generation?
**A**: Models with "uncensored" in their name, particularly:
- `flux-dev-uncensored`
- `lustify` (models)
- Use `python qwen_cli_integrator.py venice list-models` to see all available models

### Q: Can I use this with other AI providers?
**A**: Yes! The `ExternalAPIIntegrator` supports any OpenAI-compatible API. Add your provider configuration in Raycast format.

## License

MIT License - see LICENSE file for details

## Acknowledgments

- GitKraken for their excellent CLI tool
- Venice AI for uncensored AI capabilities
- Contributors and testers

## Support

For questions, issues, or feature requests:
- **GitHub Issues**: https://github.com/Fayeblade1488/Faye-Blade_Qwencode_venice_gitkraken/issues
- **Discussions**: https://github.com/Fayeblade1488/Faye-Blade_Qwencode_venice_gitkraken/discussions
