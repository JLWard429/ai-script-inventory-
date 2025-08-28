# OpenAI Integration Guide

This repository includes official OpenAI integration for enhanced AI-powered functionality through the Superman AI Orchestrator.

## Overview

The repository supports the official OpenAI Python library to provide:
- **AI-powered terminal interface** via the Superman CLI
- **Natural language processing** for repository operations
- **Intelligent task delegation** between AI and local processing
- **Enhanced conversation and context management**

## Installation

### Basic Installation (without OpenAI)

The repository works perfectly without OpenAI. All core functionality is available using local spaCy processing:

```bash
pip install -r requirements.txt
```

### Full Installation (with OpenAI Integration)

For the complete AI experience with OpenAI integration:

```bash
# Install with AI features
pip install -r requirements-dev.txt

# Or install OpenAI separately
pip install openai>=1.0.0
```

## Configuration

### OpenAI API Key Setup

To enable OpenAI integration, set your API key:

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="sk-your-api-key-here"

# Or add to your shell profile
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.bashrc
```

### Verification

Check that OpenAI integration is properly configured:

```python
import os

# Check if API key is set
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    print("✅ OpenAI API key is configured")
else:
    print("❌ OpenAI API key not found")

# Test OpenAI library
try:
    import openai
    print(f"✅ OpenAI library installed (version {openai.__version__})")
except ImportError:
    print("❌ OpenAI library not installed")
```

## Usage

### Superman CLI with OpenAI

When OpenAI is properly configured, the Superman CLI will use it as the primary AI brain:

```bash
# Run Superman CLI
python python_scripts/superman.py

# Or use the installed command
superman
```

**With OpenAI configured:**
```
🦸 > What are the best practices for organizing Python scripts?
🤖 Here are some key best practices for organizing Python scripts...
```

**Without OpenAI:**
```
🦸 > What are the best practices for organizing Python scripts?
🔄 OpenAI unavailable, using local chat handler...
```

### Architecture

The OpenAI integration follows an **OpenAI-first** architecture:

1. **PRIMARY**: All user input goes to OpenAI when available
2. **DELEGATION**: OpenAI determines whether to respond directly or delegate to local handlers
3. **FALLBACK**: Local spaCy processing when OpenAI is unavailable

## Features

### When OpenAI is Available

- **Natural conversations** about development, AI, and general topics
- **Intelligent task routing** to appropriate local handlers
- **Context-aware responses** with conversation memory
- **Repository operation delegation** (file management, script running, etc.)

### When OpenAI is Not Available

- **Local spaCy processing** for intent recognition
- **All repository operations** still work normally
- **Fallback chat functionality** using local processing
- **Clear setup instructions** for enabling OpenAI

## Troubleshooting

### Common Issues

#### OpenAI Library Not Found
```
⚠️  OpenAI library not available. Install with: pip install openai
```
**Solution**: Install the OpenAI library:
```bash
pip install openai>=1.0.0
```

#### API Key Not Configured
```
ℹ️  OpenAI API key not configured
   Set OPENAI_API_KEY environment variable for AI orchestration
```
**Solution**: Set your API key:
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

#### Invalid API Key Format
```
⚠️  OpenAI API key does not start with 'sk-' - may be invalid format
```
**Solution**: Verify your API key format and ensure it starts with `sk-`

#### Connection Errors
```
❌ OpenAI request failed: Connection error
```
**Solution**: Check your internet connection and API key validity

### Getting Help

1. **Check the logs** for detailed error messages
2. **Verify your API key** is correctly set and valid
3. **Test your internet connection** to api.openai.com
4. **Review the setup instructions** in this guide

## Privacy and Security

### Local-First Design

- **No required cloud dependencies** - works completely offline without OpenAI
- **Optional OpenAI integration** - you choose whether to use cloud AI
- **Local processing fallback** ensures functionality without external services
- **API key security** - keys are only used for OpenAI API calls, never stored

### Data Handling

- **Conversation context** may be sent to OpenAI when enabled
- **Repository contents** are only accessed locally unless explicitly delegated
- **No automatic data sharing** - you control what information is processed

## Dependencies

### Core Dependencies (Always Required)
- `spacy>=3.8.0` - Local NLP processing
- `pyyaml>=6.0.0` - Configuration file parsing

### Optional Dependencies
- `openai>=1.0.0` - Official OpenAI API client for enhanced AI features

### Development Dependencies
- All core and optional dependencies
- Testing, linting, and development tools

## Version Compatibility

| OpenAI Library Version | Compatibility | Notes |
|------------------------|---------------|-------|
| >= 1.0.0              | ✅ Recommended | Modern async API |
| 0.28.x                 | ❌ Not supported | Legacy API structure |

## Contributing

When contributing to OpenAI integration:

1. **Test both modes** - with and without OpenAI
2. **Handle ImportError gracefully** - code should work without OpenAI
3. **Document new features** - especially OpenAI-specific functionality
4. **Update tests** - ensure coverage for both scenarios

## See Also

- [Superman CLI Documentation](../python_scripts/README.md)
- [Terminal Guide](TERMINAL_GUIDE.md)
- [OpenAI Python Library Documentation](https://github.com/openai/openai-python)
- [OpenAI API Documentation](https://platform.openai.com/docs)