# AI Script Inventory

A comprehensive repository for organizing and managing AI-related scripts, tools, and utilities with advanced automation and quality controls.

## 🚀 Features

- **Superhuman AI Terminal**: Privacy-friendly, local-only AI interface for script management
- **Advanced Intent Recognition**: Uses spaCy for natural language processing
- **Automated Organization**: Scripts are automatically categorized and organized
- **Quality Controls**: Comprehensive CI/CD pipeline with security scanning
- **Local-Only Processing**: All AI functionality works offline for privacy

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/JLWard429/ai-script-inventory-.git
cd ai-script-inventory-
```

2. Install dependencies:
```bash
pip install -r requirements-dev.txt
python -m spacy download en_core_web_sm
```

## 🛠️ Usage

### Basic Usage
```bash
# Run tests
python -m pytest tests/

# Check code quality
black --check .
isort --check-only .
flake8 .
```

### Superhuman Terminal
```bash
python superhuman_terminal.py
```

The terminal provides natural language interaction for:
- Script execution and management
- File operations and organization
- Security scanning and quality checks
- AI-powered assistance and guidance

## 📁 Repository Structure

```
ai-script-inventory/
├── ai_tools/                    # AI tools and utilities (6000+ modules)
├── python_scripts/             # Python scripts for AI tasks
├── shell_scripts/              # Shell scripts and utilities
├── tests/                      # Test suite
├── .github/workflows/          # CI/CD automation
└── docs/                       # Documentation
```

## 🔧 Development

### Prerequisites
- Python 3.8+
- spaCy with English model
- Git

### Running Tests
```bash
python -m pytest tests/ -v --cov
```

### Code Quality
```bash
pre-commit install
pre-commit run --all-files
```

## 🛡️ Security

This repository includes comprehensive security scanning:
- Bandit for Python security issues
- Safety for dependency vulnerabilities
- CodeQL for advanced static analysis
- License compliance checking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions, please open an issue in the GitHub repository.