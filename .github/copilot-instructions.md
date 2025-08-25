# AI Script Inventory - GitHub Copilot Instructions

This is an enterprise-grade repository for organizing and managing AI-related scripts with comprehensive automation, security analysis, and quality controls. The repository features a **Superhuman AI Terminal** that provides a privacy-friendly, local-only AI interface for script management.

## Project Overview

The AI Script Inventory serves as a professional collection of AI-related tools and scripts with automated organization, testing, and quality assurance. The project emphasizes security, maintainability, and developer experience through comprehensive automation.

## Development Workflow

### Required Before Each Commit
- Run `black .` to format Python code
- Run `isort .` to organize imports
- All pre-commit hooks must pass
- Tests should be written for new functionality

### Build Process
```bash
# Install dependencies
pip install -r requirements-dev.txt

# Install project in development mode (if using pyproject.toml)
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest --cov=python_scripts --cov=.github/scripts --cov-report=xml --cov-report=html

# Run specific test file
pytest tests/test_basic.py -v
```

### Code Quality Checks
```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy python_scripts/ .github/scripts/

# Security scanning
bandit -r python_scripts/ .github/scripts/

# Run all pre-commit hooks
pre-commit run --all-files
```

## Repository Structure

```
ai-script-inventory/
├── python_scripts/          # Python scripts and AI tools
├── shell_scripts/           # Shell scripts and CLI utilities
├── docs/                    # Documentation and guides
├── text_files/             # Configuration files, logs, and data
├── tests/                  # Test suite (pytest-based)
├── .github/                # Automation workflows and scripts
│   ├── scripts/            # Utility scripts for automation
│   ├── workflows/          # CI/CD pipeline definitions
│   └── copilot-instructions.md  # This file
├── requirements-dev.txt    # Development dependencies
├── pyproject.toml         # Project configuration and tool settings
├── .pre-commit-config.yaml # Pre-commit hook configuration
└── .gitignore             # Git ignore patterns
```

## Code Standards

### Python Code Requirements
- **Formatting**: Use Black with line length 88
- **Import Sorting**: Use isort with Black profile
- **Linting**: Must pass flake8 checks
- **Type Hints**: Add type hints for new functions (mypy compatible)
- **Documentation**: Add docstrings for public functions and classes
- **Security**: Must pass Bandit security checks

### Shell Script Requirements  
- **Validation**: Scripts must pass ShellCheck
- **Shebang**: Use `#!/bin/bash` for bash scripts
- **Error Handling**: Include proper error handling with `set -e`

### Testing Requirements
- **Coverage**: Write tests for new Python functionality
- **Syntax**: All scripts must have valid syntax
- **Integration**: Test script execution in automation context

## Key Guidelines

1. **File Organization**: Files are automatically organized by the `organize_ai_scripts.py` script:
   - `.py` files → `python_scripts/`
   - `.md` files → `docs/`
   - `.sh` files → `shell_scripts/`
   - `.txt`, `.json`, `.yaml`, `.yml` → `text_files/`

2. **Security First**: All code changes go through security scanning with Bandit and dependency checks with Safety

3. **Quality Automation**: The repository uses comprehensive CI/CD pipelines that run on every push:
   - Code quality checks (formatting, linting, type checking)
   - Security scanning and vulnerability assessment  
   - Multi-platform testing across Python versions
   - Automated organization and cleanup

4. **Superhuman Terminal Integration**: When working with the terminal feature:
   - Maintain local-only processing (no cloud dependencies)
   - Support natural language command interpretation
   - Preserve privacy-friendly design principles

## Automation Features

- **Auto-organization**: Files are automatically moved to appropriate directories
- **Quality Enforcement**: Pre-commit hooks ensure code quality
- **Security Monitoring**: Continuous security scanning and reporting
- **Multi-platform Testing**: Automated testing across different environments
- **Documentation**: Automated documentation checks and validation

## Contributing Best Practices

1. **Small, Focused Changes**: Make minimal modifications to achieve goals
2. **Test Coverage**: Add tests for new functionality
3. **Documentation**: Update relevant documentation
4. **Security Awareness**: Consider security implications of changes
5. **Performance**: Consider impact on automation and CI/CD workflows

## Common Tasks

### Adding a New Python Script
1. Place the script in `python_scripts/` directory
2. Ensure it follows Black formatting and has proper imports
3. Add appropriate docstrings and type hints
4. Write tests in `tests/` directory
5. Update documentation if needed

### Adding a New Shell Script
1. Place the script in `shell_scripts/` directory
2. Include proper shebang and error handling
3. Test with ShellCheck for validation
4. Make executable with `chmod +x`

### Updating Dependencies
1. Update `requirements-dev.txt` or `pyproject.toml`
2. Test compatibility across Python versions
3. Run security checks on new dependencies
4. Update CI/CD workflows if needed

## Troubleshooting

### Common Issues
- **Pre-commit failures**: Run `pre-commit run --all-files` to see detailed errors
- **Test failures**: Use `pytest tests/ -v --tb=short` for detailed output
- **Import errors**: Check that all dependencies are installed
- **Security alerts**: Review Bandit and Safety reports in CI output

### Development Environment Setup
```bash
# Clone and set up the repository
git clone <repository-url>
cd ai-script-inventory-
pip install -r requirements-dev.txt
pre-commit install

# Test the setup
python .github/scripts/organize_ai_scripts.py
pytest tests/ -v
```

This repository exemplifies a "superhuman AI workflow system" where automation, security, and quality are paramount. All contributions should maintain these high standards while being mindful of the project's privacy-focused and enterprise-grade nature.