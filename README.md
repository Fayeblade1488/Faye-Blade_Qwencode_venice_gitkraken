# Qwen CLI Integration: GitKraken & Venice AI

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

This repository provides a comprehensive integration between Qwen CLI and two powerful tools:

1. **GitKraken CLI**: A complete, AI-powered Git workflow enhancement suite that allows for seamless Git operations with AI assistance
2. **Venice AI Image Generation**: An uncensored image generation system that provides high-quality image creation and upscaling capabilities

The integration is designed to work within the Qwen CLI ecosystem, allowing users to leverage advanced Git workflows and AI-powered image generation directly from their command line.

## Features

### GitKraken CLI Integration
- **AI-Powered Git Operations**: Generate commit messages, explain branch differences, resolve conflicts, and create pull requests with AI assistance
- **Workspace Management**: Create, manage, and synchronize workspaces across multiple repositories
- **Issue Integration**: Connect with GitHub, GitLab, Jira, and Azure DevOps for seamless issue tracking
- **MCP Support**: Local Model Context Protocol (MCP) server management for AI agent integration
- **Comprehensive Git Operations**: Access to all GitKraken CLI functionality through Python API and command-line interface

### Venice AI Integration
- **Uncensored Image Generation**: Generate images without content filtering using models like `flux-dev-uncensored`
- **Advanced Upscaling**: Enhance image quality with AI-powered upscaling and enhancement
- **Flexible Parameters**: Control aspect ratio, dimensions, steps, CFG scale, and other generation parameters
- **Multiple Output Formats**: Support for PNG, WebP, and other image formats
- **Metadata Tracking**: Automatic saving of generation parameters and metadata

### Unified Interface
- **Consistent API**: Unified command-line and Python interfaces for both integrations
- **Batch Operations**: Support for processing multiple images or executing multiple Git operations
- **Error Handling**: Comprehensive error handling with detailed feedback
- **Auto-Installation**: Automated setup and dependency management

## Prerequisites

Before installing this integration, you'll need:

1. **GitKraken CLI** installed on your system:
   - Download from the [official GitKraken website](https://www.gitkraken.com/cli)
   - Ensure the `gk` command is in your system PATH
   - For macOS with Homebrew: `brew install --cask gitkraken-cli`
   - For Linux: Use the installer from the website

2. **Python 3.7 or higher**:
   - Verify with `python --version` or `python3 --version`
   - If not installed, download from [python.org](https://www.python.org/)

3. **Venice AI API Key** (for image generation):
   - Sign up at [Venice AI](https://venice.ai)
   - Navigate to API Keys in your dashboard
   - Create a new API key with appropriate permissions

4. **System Requirements**:
   - macOS, Linux, or Windows with WSL
   - At least 2GB of free disk space
   - Active internet connection

## Installation

### Automatic Installation with Makefile
```bash
# Navigate to the repository directory
cd qwen-integration-public-repo

# Run the setup
make setup
```

### Manual Installation
```bash
# Install required Python packages
pip install -r requirements.txt
```

### Environment Setup
1. Create a `.env` file in your project directory (do NOT commit this file):
```bash
# .env
VENICE_API_KEY=your_venice_api_key_here
```

2. Load the environment variables:
```bash
export VENICE_API_KEY=your_venice_api_key_here
```

3. Verify that GitKraken CLI is accessible:
```bash
gk --version
```

## Configuration

### Venice API Key Configuration
The integration supports multiple ways to provide your Venice API key:

1. **Environment Variable** (Recommended):
```bash
export VENICE_API_KEY="your_api_key_here"
```

2. **Command Line Argument**:
```bash
python qwen_cli_integrator.py venice generate --api-key "your_api_key_here" --prompt "..."
```

3. **Python Code**:
```python
from venice_integration import VeniceAIImageGenerator
generator = VeniceAIImageGenerator(api_key="your_api_key_here")
```

### Default Parameters
The integration comes with optimized default parameters:

- **Model**: `flux-dev-uncensored` (for uncensored generation)
- **Steps**: 30 (optimized for uncensored model)
- **CFG Scale**: 5.0
- **Aspect Ratio**: Tall (768x1024)
- **Output Format**: PNG
- **Safe Mode**: Disabled (for uncensored generation)
- **Watermark**: Hidden

These defaults can be overridden when calling the functions.

## Usage

### Command-Line Interface

#### GitKraken Commands
```bash
# Show help
python qwen_cli_integrator.py gitkraken --help

# Generate a commit message with AI
python qwen_cli_integrator.py gitkraken ai_commit

# Generate commit with description
python qwen_cli_integrator.py gitkraken ai_commit --add-description

# List all workspaces
python qwen_cli_integrator.py gitkraken workspace_list

# Show workspace information
python qwen_cli_integrator.py gitkraken workspace_info --name "my-workspace"

# Start a new work item
python qwen_cli_integrator.py gitkraken work_start "feature-name" --issue "ISS-123"

# List all work items
python qwen_cli_integrator.py gitkraken work_list

# Generate changelog between commits
python qwen_cli_integrator.py gitkraken ai_changelog --base "main" --head "feature-branch"

# Resolve git conflicts with AI
python qwen_cli_integrator.py gitkraken ai_resolve

# Explain changes in a specific commit
python qwen_cli_integrator.py gitkraken ai_explain_commit abc1234

# Show GitKraken CLI version
python qwen_cli_integrator.py gitkraken version
```

#### Venice AI Commands
```bash
# Show help
python qwen_cli_integrator.py venice --help

# Generate an uncensored image
python qwen_cli_integrator.py venice generate --prompt "fantasy landscape at sunset"

# Generate with specific parameters
python qwen_cli_integrator.py venice generate \
  --prompt "cyberpunk cityscape with neon lights" \
  --model flux-dev-uncensored \
  --aspect-ratio wide \
  --steps 30 \
  --cfg-scale 7.0 \
  --seed 12345 \
  --format png \
  --upscale \
  --output-dir "./generated_images" \
  --output-name "cyberpunk_scene"

# Upscale an existing image
python qwen_cli_integrator.py venice upscale \
  --input "./path/to/image.png" \
  --output "./path/to/upscled_image.png" \
  --scale 4 \
  --enhance \
  --creativity 0.2

# List available models
python qwen_cli_integrator.py venice list-models
```

### Python API

#### GitKraken Integration
```python
from qwen_cli_integrator import QwenCLIIntegrator

# Initialize the integrator
integrator = QwenCLIIntegrator()

# List workspaces
result = integrator.gitkraken_command('workspace_list')
print(result)

# Generate a commit with AI
result = integrator.gitkraken_command('ai_commit', add_description=True)
print(result)

# Start a work item
result = integrator.gitkraken_command('work_start', name="new-feature", issue="ISS-123")
print(result)

# Resolve conflicts with AI
result = integrator.gitkraken_command('ai_resolve')
print(result)
```

#### Venice AI Integration
```python
from qwen_cli_integrator import QwenCLIIntegrator

# Initialize the integrator
integrator = QwenCLIIntegrator()

# Generate an image
result = integrator.venice_generate_image(
    prompt="ethereal forest with glowing mushrooms",
    model="flux-dev-uncensored",
    aspect_ratio="tall",
    steps=30,
    cfg_scale=7.0,
    seed=42,
    upscale=True,
    output_dir="./generated",
    output_name="ethereal_forest"
)
print(f"Image saved to: {result['generated_image_path']}")

# Upscale an existing image
result = integrator.venice_upscale_image(
    image_path="./input.png",
    scale=4,
    enhance=True,
    enhance_creativity=0.15
)
print(f"Upscaled image saved to: {result['output_path']}")

# List available models
result = integrator.list_available_models()
print(f"Available models: {len(result['all_models'])}")
print(f"Uncensored models: {len(result['uncensored_models'])}")
```

### Advanced Usage Examples

#### Batch Processing with GitKraken
```python
from qwen_cli_integrator import QwenCLIIntegrator

integrator = QwenCLIIntegrator()

# Create multiple work items
work_items = [
    {"name": "authentication-system", "issue": "AUTH-001"},
    {"name": "payment-processing", "issue": "PAY-002"},
    {"name": "user-dashboard", "issue": "UI-003"}
]

for item in work_items:
    result = integrator.gitkraken_command('work_start', **item)
    print(f"Created work item '{item['name']}': {result['success']}")
```

#### Advanced Image Generation
```python
from qwen_cli_integrator import QwenCLIIntegrator

integrator = QwenCLIIntegrator()

# Generate multiple variations of an image
prompts = [
    "realistic portrait of a wizard",
    "cartoon style portrait of a wizard", 
    "anime style portrait of a wizard",
    "cyberpunk portrait of a wizard"
]

for i, prompt in enumerate(prompts):
    result = integrator.venice_generate_image(
        prompt=prompt,
        model="flux-dev-uncensored",
        aspect_ratio="square",
        steps=35,
        cfg_scale=6.5,
        seed=1000+i,
        output_name=f"wizard_var_{i+1}",
        upscale=True
    )
    print(f"Generated: {result['generated_image_path']}")
```

## API Endpoints

### GitKraken CLI
The GitKraken integration uses the local GitKraken CLI executable (`gk`) to communicate with GitKraken services. No direct API calls are made.

### Venice AI
The following Venice AI endpoints are used:
- Image Generation: `https://api.venice.ai/api/v1/image/generate`
- Image Upscaling: `https://api.venice.ai/api/v1/image/upscale`
- Model Listing: `https://api.venice.ai/api/v1/models`

All requests are authenticated using your Venice API key in the Authorization header as a Bearer token.

## Security Considerations

### API Key Security
- **Never commit API keys** to version control
- Use environment variables or secure configuration management
- Ensure your `.env` file is in `.gitignore`
- Revoke API keys immediately if they are compromised

### Uncensored Content
- The integration is configured for uncensored generation by default
- Generated content may include adult or inappropriate material
- Use appropriate content filters or moderation if required for your use case
- Consider the context in which generated images will be used

### Data Privacy
- Images sent to Venice AI are processed on Venice servers
- Do not send sensitive or proprietary images without appropriate security measures
- Review Venice AI's privacy policy for data handling practices

## Troubleshooting

### Common Issues

#### GitKraken CLI Not Found
**Issue**: "GitKraken CLI (gk) is not installed or not in PATH"
**Solution**: 
- Install GitKraken CLI from the official website
- Verify installation: `gk --version`
- Add to PATH if needed: `export PATH="/path/to/gk:$PATH"`

#### Venice API Key Not Set
**Issue**: "Venice AI not initialized - please set VENICE_API_KEY environment variable"
**Solution**:
- Set the environment variable: `export VENICE_API_KEY="your_key_here"`
- Verify with: `echo $VENICE_API_KEY`

#### Rate Limiting
**Issue**: HTTP 429 errors from Venice API
**Solution**: 
- Check your API usage in the Venice dashboard
- Upgrade your plan if needed
- Implement retry logic with exponential backoff

#### Python Dependencies
**Issue**: ModuleNotFoundError for `requests`
**Solution**: 
- Install dependencies: `pip install -r requirements.txt`

### Debugging Tips

#### Enable Verbose Output
```bash
python qwen_cli_integrator.py venice generate --prompt "test" --verbose
```

#### Check Available Models
```bash
python qwen_cli_integrator.py venice list-models
```

#### Test Individual Components
```bash
# Test GitKraken
python -c "from gitkraken_integration import GitKrakenCLI; gk = GitKrakenCLI(); print(gk.is_installed())"

# Test Venice
python -c "from venice_integration import VeniceAIImageGenerator; import os; g = VeniceAIImageGenerator(os.environ.get('VENICE_API_KEY')); print(len(g.list_models()))"
```

### Getting Help
- Check the GitHub repository for updates and known issues
- Review the Venice AI documentation at https://docs.venice.ai
- Check GitKraken CLI documentation at https://gitkraken.github.io/gk-cli/docs/gk.html

## Development

### Repository Structure
```
qwen-integration-public-repo/
├── gitkraken_integration.py     # GitKraken CLI wrapper
├── venice_integration.py        # Venice AI API wrapper
├── qwen_cli_integrator.py       # Main integration module
├── test_integration.py          # Test suite
├── requirements.txt             # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore patterns
├── Makefile                    # Build automation
└── package.json                # Package configuration
```

### Running Tests
```bash
python test_integration.py
```

### Code Quality
- All Python code follows PEP 8 style guidelines
- Type hints are included for all public functions
- Comprehensive error handling is implemented
- Documentation strings follow Google style

### Adding New Features
1. Implement the feature in the appropriate module
2. Add command-line interface support in `qwen_cli_integrator.py`
3. Add Python API support
4. Write tests in `test_integration.py`
5. Update documentation in this README

## Contributing

### Reporting Issues
- Check existing issues before creating a new one
- Provide detailed information about your environment
- Include error messages and steps to reproduce
- Suggest possible solutions if you have them

### Feature Requests
- Explain the use case for your feature request
- Provide examples of how the feature would be used
- Consider backward compatibility
- Be specific about desired functionality

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit the pull request

### Development Guidelines
- Maintain compatibility with Python 3.7+
- Follow existing code style and conventions
- Write clear, descriptive commit messages
- Keep pull requests focused on a single issue/feature
- Update tests and documentation as needed

## License

MIT License

Copyright (c) 2025 Qwen CLI Integration

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

**Important Note**: This integration is provided as-is. Users are responsible for compliance with the terms of service of GitKraken, Venice AI, and any other services used. The authors are not responsible for any misuse or violation of service terms.