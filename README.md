[![Code Quality & Security](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/code-quality.yml/badge.svg)](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/code-quality.yml)
[![CI Passing](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/JLWard429/ai-script-inventory-/actions)
[![CodeQL Security Analysis](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/codeql.yml/badge.svg)](https://github.com/JLWard429/ai-script-inventory-/security/code-scanning)
[![Security Scanning](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/dependency-scan.yml/badge.svg)](https://github.com/JLWard429/ai-script-inventory-/actions)
[![Powered by Copilot](https://img.shields.io/badge/powered%20by-copilot-blue?logo=github)](https://github.com/features/copilot)

# 🤖 AI Script Inventory

A professional, enterprise-grade repository for organizing and managing AI-related scripts with comprehensive automation, security analysis, and quality controls.

This repository contains a collection of AI-related scripts and features the **Superhuman AI Terminal** — a privacy-friendly, local-only AI terminal interface powered by spaCy for advanced natural language understanding.

---

## 🚀 Superhuman AI Terminal

The Superhuman AI Terminal provides a natural language interface to interact with your AI script inventory. It uses spaCy for advanced intent recognition and entity extraction (no cloud LLMs required) to understand and execute your requests with high precision.

### Quick Start

```bash
# Launch the terminal
python terminal.py
# or
python superhuman_terminal.py
```

### Features

- **🧠 spaCy-Powered NLP**: Advanced natural language understanding with entity extraction
- **🎯 Precise Intent Recognition**: Maps complex natural language to specific actions
- **🛡️ Privacy-First**: All processing happens locally — no cloud dependencies
- **🔍 Smart Entity Extraction**: Automatically detects files, directories, scopes, and parameters
- **💬 Context-Aware AI Chat**: Provides guidance, best practices, and repository help
- **🚀 Script Execution**: Run Python and shell scripts with natural commands
- **📁 Intelligent File Management**: List, search, preview, and summarize files
- **🔧 Repository Integration**: Seamless access to all repository features and tools

### Example Commands

```
🤖 > help                                    # Show available commands
🤖 > run security scan on Python files       # Execute security analysis  
🤖 > I need to run the security analysis on all my Python files  # Natural request
🤖 > list all Python files                   # List files by type
🤖 > show README.md                          # Display file contents
🤖 > preview the main configuration files    # Quick preview
🤖 > summarize the latest README             # Auto-find and summarize latest docs
🤖 > search for test files                   # Search for files containing text
🤖 > what can you do?                        # Get AI assistance and guidance
🤖 > how do I get started?                   # Onboarding help
🤖 > Can you help me organize my scripts better?  # Get organization advice
🤖 > What are the security features?         # Learn about security capabilities
```

### Advanced Natural Language Support

The terminal uses spaCy to understand complex, conversational queries:

**Intent Recognition:**
- **Commands**: "run", "execute", "list", "show", "search", "summarize", "preview"
- **Conversational**: "I need to...", "Can you help...", "What are...", "How do I..."
- **Context-Aware**: Understands file types, directories, scopes, and modifiers

**Entity Extraction:**
- **File Types**: python, shell, markdown, configuration, etc.
- **Scopes**: all, latest, recent, main, specific directories
- **Directories**: python_scripts, shell_scripts, docs, text_files
- **Action Modifiers**: security, development, testing, organization

**Smart Parameter Detection:**
- Automatically extracts file names, directories, and scope from natural language
- Handles complex queries like "run security scan on all Python files in shell_scripts"
- Provides confidence scoring and clarification when needed

### AI Chat Assistant

The built-in AI chat provides contextual help and guidance:

- **Repository Navigation**: Learn about available scripts and tools
- **Best Practices**: Get advice on script organization and development workflow
- **Security Guidance**: Understand security features and best practices  
- **Development Help**: Learn about the development tools and CI/CD pipeline
- **Onboarding**: Step-by-step guidance for new users

---

## 📁 Repository Structure

This repository is well-organized with clear separation of concerns and automated file management:

```
ai-script-inventory/
├── .github/                    # Automation and CI/CD workflows
│   ├── scripts/               # Organization and utility scripts
│   └── workflows/             # GitHub Actions workflows
├── src/                       # Core application modules
│   └── ai_script_inventory/   # Main package
│       ├── ai/                # Intent recognition and NLP processing
│       └── superhuman_terminal.py  # Main terminal interface
├── python_scripts/            # Python utilities and tools
│   └── archives/              # Historical versions and duplicates
├── shell_scripts/             # Shell utilities and automation scripts
├── docs/                      # Comprehensive documentation
├── text_files/                # Reports and data files
│   ├── archives/              # Historical files
│   └── reports/               # Current reports and analysis
├── tests/                     # Test suite with full coverage
└── [root files]               # Configuration and project documentation
```

### Key Features of the Organization:

- **🏗️ Modular Structure**: Clear separation between source code, scripts, documentation, and data
- **📦 Archive System**: Automatic archiving of duplicate and historical files to preserve history
- **🔄 Auto-Organization**: GitHub Actions workflows automatically maintain file organization
- **🛡️ Privacy Protection**: Enhanced `.gitignore` patterns protect sensitive data
- **📚 Comprehensive Documentation**: Multiple levels of documentation for different audiences

---

## 🔐 Security & Quality

This repository implements enterprise-grade security and quality controls:

- **🔍 Professional CodeQL Analysis**: Multi-language security scanning with advanced configuration
- **🛡️ Dependency Scanning**: Daily vulnerability monitoring with automated updates
- **🔒 Secret Scanning**: GitHub secret scanning with custom patterns
- **🚨 Security Alerts**: Real-time notifications for security findings
- **📊 Quality Metrics**: Comprehensive code quality and coverage tracking

---

## 🧠 Adding New Intents and Entities

The Superhuman Terminal is designed to be easily extensible. Here's how to add new functionality:

### Adding New Intent Types

1. **Define the Intent** in `ai/intent.py`:
```python
class IntentType(Enum):
    NEW_INTENT = "new_intent"
```

2. **Add spaCy Patterns** in `_setup_spacy_patterns()`:
```python
new_intent_patterns = [
    [{"LOWER": {"IN": ["keyword1", "keyword2"]}}, {"IS_ALPHA": True}],
    [{"LOWER": "action"}, {"TEXT": {"REGEX": r".*\\.(py|sh)$"}}],
]
self.matcher.add("NEW_INTENT", new_intent_patterns)
```

3. **Update Pattern Mapping** in `_map_spacy_intent()`:
```python
mapping = {
    # ... existing mappings
    "NEW_INTENT": IntentType.NEW_INTENT,
}
```

4. **Implement Handler** in `superhuman_terminal.py`:
```python
def handle_new_intent(self, intent: Intent):
    """Handle new intent requests."""
    # Implementation here
    pass
```

5. **Register Handler** in `__init__`:
```python
self.action_handlers[IntentType.NEW_INTENT] = self.handle_new_intent
```

### Enhancing Entity Extraction

Add new entity types in `_extract_entities_with_spacy()`:

```python
# Add new file type mappings
file_type_mapping = {
    "new_type": "new_type",
    # ... existing mappings
}

# Add new scope indicators
scope_indicators = {
    "custom_scope": ["custom", "specific", "targeted"],
    # ... existing scopes
}

# Add new action modifiers
action_modifiers = {
    "new_action": ["new", "custom", "specific"],
    # ... existing modifiers
}
```

### Extending AI Chat Responses

Add new response patterns in `handle_ai_chat()`:

```python
elif any(phrase in user_input for phrase in ["new", "topic", "keywords"]):
    print("""
    🔥 **New Feature Information:**
    
    • Description of new capabilities
    • Usage examples and commands
    • Best practices and tips
    """)
```

### Testing Your Extensions

Add tests in `tests/test_superhuman_terminal.py`:

```python
def test_new_intent_recognition(self):
    """Test new intent recognition."""
    intent = self.recognizer.recognize("new command example")
    assert intent.type == IntentType.NEW_INTENT
    assert intent.confidence >= 0.7
```

---

## 🔧 Technical Architecture

**spaCy Integration:**
- English language model (`en_core_web_sm`) for NLP processing
- Pattern matching with `spacy.matcher.Matcher` for intent recognition
- Named Entity Recognition (NER) for parameter extraction
- Dependency parsing for complex query understanding
- Linguistic analysis for confidence scoring

**Intent Recognition Pipeline:**
1. spaCy processes input for linguistic features
2. Pattern matcher identifies potential intents
3. Entity extraction finds parameters and targets
4. Confidence scoring with linguistic enhancement
5. Route to appropriate action handler

**Privacy Protection:**
- All processing happens locally using spaCy
- No cloud APIs or external data transmission
- Complete offline functionality
- User data never leaves the local machine

---

## 📁 Repository Structure

Following recent organization and restructuring, the repository follows a clean, hierarchical structure:

```
ai-script-inventory/
├── .github/                    # Automation and CI/CD workflows
│   ├── scripts/               # Organization and utility scripts
│   └── workflows/             # GitHub Actions workflows
├── src/                       # Core application modules
│   └── ai_script_inventory/   # Main package with Superhuman Terminal
│       ├── ai/                # Intent recognition and NLP modules
│       └── superhuman_terminal.py  # Main terminal interface
├── python_scripts/            # Python utilities and tools
│   └── archives/              # Historical versions and backups
├── shell_scripts/             # Shell utilities and automation
├── docs/                      # Comprehensive documentation
│   ├── CONTRIBUTING.md        # Contribution guidelines
│   ├── SECURITY.md           # Security policies and procedures
│   └── WORKFLOW.md           # Development workflow documentation
├── text_files/                # Reports, configuration, and data
│   ├── archives/              # Historical files and backups
│   └── reports/               # Current reports and analysis
├── tests/                     # Test suite
├── README.md                  # This file - main project documentation
├── SECURITY.md               # Security policy (root level)
├── SUPPORT.md                # Support and help information
├── TERMINAL_GUIDE.md         # Superhuman Terminal developer guide
└── pyproject.toml            # Project configuration and dependencies
```

### Key Features of the Organization

- **📦 Modular Structure**: Clear separation between source code, scripts, documentation, and data
- **🗃️ Archive System**: Historical files preserved in dedicated archives/ subdirectories
- **🔒 Enhanced Privacy**: Improved .gitignore patterns protecting sensitive data
- **📚 Comprehensive Documentation**: Dedicated docs/ directory with specialized guides
- **🧪 Robust Testing**: Organized test suite with coverage for all major components

---

## 🚀 Quick Start & Installation

### Prerequisites

- **Python 3.8+** (Python 3.11+ recommended)
- **Git** for version control
- **Terminal/Command Line** access

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/JLWard429/ai-script-inventory.git
   cd ai-script-inventory
   ```

2. **Install Core Dependencies**
   ```bash
   # Install core runtime dependencies
   pip install -e .
   
   # For development work, install dev dependencies
   pip install -e ".[dev]"
   ```

3. **Download spaCy Language Model** (Required for Terminal)
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Set Up Development Environment** (Optional)
   ```bash
   # Install pre-commit hooks for code quality
   pre-commit install
   
   # Run setup script for additional dev tools
   python setup_dev.py
   ```

5. **Verify Installation**
   ```bash
   # Test the Superhuman AI Terminal
   python src/ai_script_inventory/superhuman_terminal.py
   
   # Run the test suite
   python -m pytest tests/ -v
   ```

### 🦸‍♂️ Superman Orchestrator Setup

The Superman Orchestrator is an enhanced foreground AI terminal that automatically starts when you open a new terminal session, providing immediate access to all repository tools and AI capabilities.

#### Basic Setup

1. **Run Superman Orchestrator**
   ```bash
   # Launch Superman orchestrator (foreground mode)
   python superman.py
   ```

2. **Optional: OpenAI Integration**
   ```bash
   # Set up OpenAI API (optional, for enhanced AI conversations)
   export OPENAI_API_KEY="your-api-key-here"
   
   # Install OpenAI package
   pip install openai
   ```

#### Auto-Start on Terminal Launch

To have Superman automatically start when you open a new terminal session:

**For Bash (.bashrc/.bash_profile):**
```bash
# Add to ~/.bashrc or ~/.bash_profile
cd /path/to/ai-script-inventory
python superman.py
```

**For Zsh (.zshrc):**
```bash
# Add to ~/.zshrc
cd /path/to/ai-script-inventory
python superman.py
```

**For Fish (config.fish):**
```fish
# Add to ~/.config/fish/config.fish
cd /path/to/ai-script-inventory
python superman.py
```

#### Employee Script Registration

Superman automatically discovers and registers all scripts in your repository as "employees" that can be delegated tasks:

```bash
# List all available employee scripts
employees

# Delegate a task to an employee
delegate employee_spacy_test --demo
delegate dev_tools test
delegate setup_dev_env
```

#### Superman Commands

```bash
# Employee management
employees          # List all registered employee scripts
delegate <name>    # Delegate task to specific employee

# System status and analysis
status            # Show system status and capabilities
demo              # Run spaCy NLP demonstration

# Memory and context
memory            # Show conversation history
analyze <path>    # Perform code analysis

# Mode switching
superman          # Enter enhanced AI orchestrator mode
exit superman     # Return to normal terminal mode
```

#### Troubleshooting

**spaCy Model Missing:**
```bash
# Download the required spaCy model
python -m spacy download en_core_web_sm
```

**OpenAI API Issues:**
```bash
# Check API key format (should start with 'sk-')
echo $OPENAI_API_KEY

# Enable debug mode for detailed logging
export SUPERMAN_DEBUG=1
python superman.py
```

**Employee Scripts Not Found:**
- Ensure scripts are in `python_scripts/`, `shell_scripts/`, or `src/ai_script_inventory/`
- Check file permissions (scripts should be readable)
- Add descriptions at the top of scripts for better discovery

### First Steps

1. **Explore the Terminal**: Launch `python terminal.py` and try:
   - `help` - See available commands
   - `list all Python files` - Explore the codebase
   - `what can you do?` - Learn about capabilities

2. **Review Documentation**: Check the `docs/` directory for:
   - [Contributing Guidelines](docs/CONTRIBUTING.md)
   - [Security Policy](docs/SECURITY.md) 
   - [Workflow Documentation](docs/WORKFLOW.md)

3. **Try the Organization Tools**: 
   ```bash
   # Auto-organize files (dry run)
   python .github/scripts/organize_ai_scripts.py --dry-run
   ```

---

## 👥 Creating Employee Scripts

Employee scripts are the building blocks of the Superman orchestrator system. Any Python or shell script in your repository can become an "employee" that Superman can delegate tasks to.

### Employee Script Guidelines

1. **Location**: Place scripts in:
   - `python_scripts/` for Python tools
   - `shell_scripts/` for shell utilities  
   - `src/ai_script_inventory/` for core modules

2. **Description**: Add a description at the top of your script:

**Python Employee Example:**
```python
#!/usr/bin/env python3
"""
Employee Data Processor

Processes data files and generates reports using pandas and matplotlib.
Supports CSV, JSON, and Excel formats with customizable output options.

Usage:
    python employee_data_processor.py <input_file> [--format csv|json|excel]

Examples:
    python employee_data_processor.py data.csv --format excel
    python employee_data_processor.py sales.json --output-dir reports/
"""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", help="Input file to process")
    parser.add_argument("--format", choices=["csv", "json", "excel"], 
                        default="csv", help="Output format")
    
    args = parser.parse_args()
    
    # Your employee script logic here
    print(f"Processing {args.input_file} with format {args.format}")
    
if __name__ == "__main__":
    main()
```

**Shell Employee Example:**
```bash
#!/bin/bash
# Employee Log Analyzer
# Analyzes log files and generates summaries with error detection and metrics.
# Supports multiple log formats and provides detailed reporting capabilities.

set -euo pipefail

usage() {
    echo "Usage: $0 <log_file> [--errors-only] [--output report.txt]"
    echo "Examples:"
    echo "  $0 app.log --errors-only"
    echo "  $0 server.log --output analysis.txt"
}

# Your shell script logic here
```

### Registering New Employees

New employee scripts are automatically discovered by Superman when it starts. No manual registration required!

1. **Create your script** in the appropriate directory
2. **Make it executable** (for shell scripts): `chmod +x script.sh`
3. **Test it manually** to ensure it works correctly
4. **Restart Superman** to discover the new employee: `python superman.py`

### Employee Best Practices

- **Clear Usage**: Provide `--help` options and usage examples
- **Error Handling**: Handle invalid inputs gracefully
- **Output Format**: Use consistent output formatting (stdout for results, stderr for errors)
- **Exit Codes**: Return appropriate exit codes (0 for success, non-zero for errors)
- **Documentation**: Include docstrings or comments explaining functionality

### Testing Employees

Test your employee scripts before delegating tasks:

```bash
# Test the script directly
python python_scripts/your_employee.py --help

# Test through Superman delegation
python superman.py
# Then in Superman: delegate your_employee --help
```

### Example Employee Scripts

The repository includes example employee scripts:

- **`employee_spacy_test.py`**: Demonstrates spaCy NLP processing
- **`dev_tools.py`**: Development workflow automation
- **`setup_dev_env.sh`**: Environment setup utilities

Study these examples to understand the employee script patterns and conventions.

---

## 🛠️ Development & Contribution

### Development Workflow

This repository uses a **superhuman AI workflow system** that automates code quality, security, and organization:

- **🔧 Automated Code Quality**: Black formatting, isort imports, flake8 linting, mypy type checking
- **🔒 Security Scanning**: Bandit security analysis, dependency vulnerability scanning
- **🧪 Comprehensive Testing**: pytest with coverage reporting, syntax validation
- **📁 Smart Organization**: Automated file categorization and archive management

### Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for:
- Development environment setup
- Code style and quality standards  
- Pull request process
- Testing requirements
- Security guidelines

### Quick Development Commands

```bash
# Format and lint code
python -m black .
python -m isort .
python -m flake8

# Run security scans
python -m bandit -r python_scripts/ src/

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Use the development tools helper
python python_scripts/dev_tools.py --help
```

---

## 🔒 Security & Privacy

This repository implements **enterprise-grade security**:

- **🛡️ Multi-layer Security Scanning**: CodeQL, Bandit, Safety, Trivy
- **🔍 Continuous Monitoring**: Automated vulnerability detection and reporting
- **🔐 Privacy Protection**: All AI processing happens locally with no cloud dependencies
- **📊 Security Metrics**: Comprehensive security monitoring and reporting

For security issues, see our [Security Policy](SECURITY.md) for responsible disclosure.

---

## 📞 Support & Community

- **📚 Documentation**: Start with files in the `docs/` directory
- **💬 Discussions**: [GitHub Discussions](https://github.com/JLWard429/ai-script-inventory-/discussions)
- **🐛 Bug Reports**: [GitHub Issues](https://github.com/JLWard429/ai-script-inventory-/issues)
- **🛟 Support**: See [SUPPORT.md](SUPPORT.md) for help options

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🎉 Acknowledgments

- **spaCy**: Powers the natural language understanding in the Superhuman Terminal
- **GitHub Actions**: Enables our automated workflow system
- **Contributors**: Thank you to everyone who has contributed to making this project better!

---

*The AI Script Inventory represents a new paradigm in developer tooling - combining enterprise-grade automation with privacy-respecting AI assistance for a truly superhuman development experience.*