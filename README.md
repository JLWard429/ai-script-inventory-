# AI Script Inventory

This repository contains a collection of AI-related scripts and tools with automated workflow management.

## 🚀 Superhuman AI Workflow System

This repository implements an advanced automation system for managing AI scripts, ensuring code quality, and maintaining documentation.

### Key Features

- **Superman AI Terminal**: Advanced AI-powered command-line interface with internet connectivity checking
- **Automated Code Organization**: Files are automatically sorted by type into appropriate directories
- **Code Quality Assurance**: Automated linting, formatting, and security scanning
- **Documentation Management**: Auto-generated and maintained documentation
- **Testing Infrastructure**: Comprehensive test suite with coverage reporting
- **Security Monitoring**: Automated vulnerability scanning and dependency checks

### Superman CLI

The repository includes a Superman CLI (`superman`) that provides an **OpenAI-powered AI orchestrator** experience:

**Key Features:**
- **OpenAI Integration**: Uses ChatGPT as the primary orchestrator for all user interactions
- **Intelligent Coordination**: OpenAI determines whether to respond directly or delegate to local tools
- **Natural Conversation**: Ask questions, get advice, and have natural conversations about development
- **Repository Task Delegation**: OpenAI seamlessly delegates file operations, script running, and analysis to local handlers
- **Fallback Support**: Gracefully falls back to local spaCy processing when OpenAI is unavailable
- **Internet Connectivity Check**: Automatically checks for internet access on startup
- **System Status Monitoring**: Checks spaCy installation and OpenAI API configuration
- **Memory System**: Persistent conversation context across sessions

**Usage:**
```bash
# Set up OpenAI API key for full functionality
export OPENAI_API_KEY="your-api-key-here"

# Install the package
pip install -e .

# Run Superman CLI
superman

# Or run directly
python superman.py
```

**Example Interactions:**
```
🦸 > What are the best practices for organizing Python scripts?
🤖 Here are some key best practices for organizing Python scripts...

🦸 > Run a security scan on all Python files
🔄 Executing security scan... [delegates to local tools]

🦸 > Show me the README file
🔄 Displaying README.md... [delegates to local file handler]

🦸 > How should I structure an AI project?
🤖 For AI projects, I recommend the following structure...
```

**Startup Checks:**
The Superman CLI performs comprehensive startup validation:
- Internet connectivity (tests multiple endpoints)
- OpenAI API configuration and availability
- spaCy model availability for fallback processing
- System readiness assessment

### Directory Structure

- `python_scripts/` - Python scripts and AI tools
- `shell_scripts/` - Shell scripts and command-line utilities
- `docs/` - Documentation, guides, and reference materials
- `text_files/` - Configuration files, logs, and text-based resources
- `.github/` - GitHub Actions workflows and automation scripts

### Getting Started

1. Clone the repository
2. Install development dependencies: `pip install -r requirements-dev.txt`
3. Set up pre-commit hooks: `pre-commit install`
4. Start contributing! The automation will handle organization and quality checks.

See [WORKFLOW.md](WORKFLOW.md) for detailed information about the automation system.
