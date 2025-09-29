# Qwen Code Integration: GitKraken CLI & Venice AI

This package provides integration between Qwen Code and two powerful tools:
- **GitKraken CLI**: AI-powered Git workflow enhancement
- **Venice AI**: Uncensored image generation and upscaling

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

## Contributing

Feel free to fork this repository and submit pull requests for improvements or bug fixes.

## License

MIT