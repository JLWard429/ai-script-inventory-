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

The repository includes a Superman CLI (`superman`) that provides an enhanced AI terminal experience:

**Key Features:**
- **Internet Connectivity Check**: Automatically checks for internet access on startup
- **Offline Mode Support**: Gracefully handles offline scenarios with clear warnings
- **System Status Monitoring**: Checks spaCy installation and OpenAI API configuration
- **Natural Language Processing**: Advanced intent recognition for intuitive commands
- **Memory System**: Persistent conversation context and learning
- **Code Analysis**: Intelligent code understanding and suggestions

**Usage:**
```bash
# Install the package
pip install -e .

# Run Superman CLI
superman

# Or run directly
python superman.py
```

**Startup Checks:**
The Superman CLI performs comprehensive startup validation:
- Internet connectivity (tests multiple endpoints)
- spaCy model availability
- OpenAI API configuration
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
