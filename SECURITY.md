# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability within this project, please send an email to the maintainers. All security vulnerabilities will be promptly addressed.

### What to Include

Please include the following information:
- Type of vulnerability
- Full paths of source file(s) related to the manifestation of the issue
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Response Timeline

- Initial response: Within 48 hours
- Status updates: Every 72 hours until resolution
- Fix timeline: Depends on severity and complexity

## Security Best Practices

When using this project:

### API Key Management
- **NEVER** commit API keys to version control
- Always use environment variables for sensitive credentials
- Use `.env` files locally (ensure they're in `.gitignore`)
- Rotate API keys regularly

### Environment Variables
```bash
# Required
export VENICE_API_KEY="your_key_here"

# Optional but recommended for production
export VENICE_API_TIMEOUT=120
```

### File Permissions
```bash
# Ensure scripts have appropriate permissions
chmod 755 qwen_cli_integrator.py
chmod 755 install.sh

# Protect configuration files
chmod 600 ~/.config/raycast/ai/providers.yaml
```

### Network Security
- The tool makes HTTPS requests to:
  - `api.venice.ai` (Venice AI API)
  - Other APIs configured in `providers.yaml`
- All requests use TLS 1.2+ encryption
- API keys are sent via Authorization headers, never in URLs

### Input Validation
- User prompts are sanitized before API requests
- File paths are validated to prevent directory traversal
- Command injection prevention in GitKraken CLI wrapper

### Safe Image Generation
- Generated images are saved to the current directory by default
- Image file paths are validated
- Temporary files are cleaned up after upscaling

## Known Security Considerations

### Uncensored Content Generation
This tool provides access to **uncensored image generation models**. Users are responsible for:
- Complying with local laws and regulations
- Using the tool in appropriate contexts
- Not generating illegal or harmful content
- Understanding the terms of service of Venice AI

### GitKraken CLI Integration
- GitKraken CLI operations execute with user's Git credentials
- Be cautious when running AI-generated commit messages
- Review all changes before pushing to remote repositories

### External API Configuration
- Third-party API providers configured via YAML files
- Validate provider configurations before use
- Only use trusted API endpoints

## Dependency Security

### Python Dependencies
We use the following dependencies with security in mind:
- `requests>=2.31.0` - For secure HTTP requests
- `urllib3>=2.0.0` - Modern URL handling with security patches
- `pyyaml>=6.0` - YAML parsing with known vulnerability fixes

### Keeping Dependencies Updated
```bash
# Check for outdated packages
pip list --outdated

# Update dependencies
pip install -U -r requirements.txt
```

### Dependency Scanning
We recommend running:
```bash
# Install safety
pip install safety

# Check for known vulnerabilities
safety check -r requirements.txt
```

## Secure Development Practices

### For Contributors
1. Never commit secrets or API keys
2. Use environment variables for configuration
3. Validate all user inputs
4. Sanitize file paths and command arguments
5. Use parameterized queries/commands
6. Keep dependencies updated
7. Follow the principle of least privilege

### Code Review Checklist
- [ ] No hardcoded credentials
- [ ] Input validation implemented
- [ ] Error messages don't leak sensitive info
- [ ] Secure defaults used
- [ ] Dependencies are up to date
- [ ] New endpoints use HTTPS
- [ ] File operations are path-safe

## Security Updates

Security updates will be released as:
- **Critical**: Immediate patch release
- **High**: Patch within 7 days
- **Medium**: Patch in next minor release
- **Low**: Addressed in next major release

## Acknowledgments

We appreciate responsible disclosure of security vulnerabilities. Contributors who report valid security issues will be acknowledged in release notes (if desired).

## Contact

For security concerns, please contact the repository maintainers through GitHub.

---

**Last Updated**: 2025-09-30  
**Version**: 1.0.0