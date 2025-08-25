# GitHub Copilot Instructions for AI Script Inventory

This is a Python-based repository containing an organized collection of AI-related scripts, tools, and automation workflows. The repository emphasizes automation, code quality, security, and a "superhuman AI workflow system" that maintains high standards for development.

## Project Structure

### Core Directories
- `python_scripts/` - Python scripts and development tools
- `shell_scripts/` - Shell scripts and automation
- `docs/` - Documentation including CONTRIBUTING.md, WORKFLOW.md, and SECURITY.md
- `text_files/` - Text files, notes, and inventories
- `tests/` - Test suite for all functionality
- `.github/workflows/` - CI/CD automation workflows
- `.github/scripts/` - Repository automation scripts

### Key Files
- `pyproject.toml` - Python project configuration and tool settings
- `requirements-dev.txt` - Development dependencies
- `dev_tools.py` - Primary development utility script
- `.pre-commit-config.yaml` - Pre-commit hook configuration

## Development Workflow

### Required Before Each Commit
- Run code formatting and quality checks using the development tools
- All Python code must pass linting, type checking, and testing
- Security scans must pass without critical vulnerabilities

### Development Commands
Use the centralized development tools script for all operations:

```bash
# Set up development environment (install dependencies and hooks)
python python_scripts/dev_tools.py setup

# Run comprehensive quality checks and formatting
python python_scripts/dev_tools.py all

# Individual operations:
python python_scripts/dev_tools.py format    # Format code with Black and isort
python python_scripts/dev_tools.py lint      # Run flake8 and mypy
python python_scripts/dev_tools.py test      # Run pytest with coverage
python python_scripts/dev_tools.py security  # Run bandit and safety scans
```

### Testing Strategy
- Use `pytest` for all Python testing
- Write tests in the `tests/` directory following existing patterns
- Use descriptive test names and include docstrings
- Test files should use `test_*.py` naming convention
- Maintain or improve test coverage

### Build Process
1. **Setup**: `python python_scripts/dev_tools.py setup`
2. **Format**: `python python_scripts/dev_tools.py format`
3. **Lint**: `python python_scripts/dev_tools.py lint`
4. **Test**: `python python_scripts/dev_tools.py test`
5. **Security**: `python python_scripts/dev_tools.py security`

## Code Standards

### Python Code
- **Formatting**: Use Black (line length 88) and isort for import sorting
- **Linting**: Code must pass flake8 with project-specific configuration
- **Type Hints**: Use mypy for type checking; include type hints for all functions
- **Documentation**: Include docstrings for all public functions and classes
- **Security**: All code must pass Bandit security scanning

### File Organization
- Python scripts belong in `python_scripts/`
- Shell scripts belong in `shell_scripts/`
- Documentation belongs in `docs/`
- Text files and notes belong in `text_files/`
- Tests belong in `tests/`

### Commit Standards
Follow Conventional Commits format:
- `feat: add new functionality`
- `fix: resolve bug or issue`
- `docs: update documentation`
- `style: format code`
- `refactor: restructure code`
- `test: add or update tests`
- `chore: maintenance tasks`

## Security Requirements

### Security Scanning
- Run `python python_scripts/dev_tools.py security` before committing
- Address all high and critical security findings
- Use `safety` for dependency vulnerability scanning
- Use `bandit` for Python code security analysis

### Best Practices
- Never commit secrets, API keys, or sensitive data
- Use environment variables for configuration
- Validate all user inputs
- Follow principle of least privilege

## AI and Automation Features

### Superhuman Workflow System
This repository implements a comprehensive automation system that:
- Automatically organizes files by type
- Runs quality checks on all changes
- Performs security scanning
- Maintains documentation consistency
- Provides detailed feedback and metrics

### Natural Language Terminal
The repository includes a natural language terminal interface (`terminal.py`, `superhuman_terminal.py`) that allows interaction with scripts using plain English commands.

## Quality Gates

### Pre-commit Requirements
The following checks run automatically on commit:
- Code formatting (Black, isort)
- Linting (flake8, mypy)
- Basic security checks (bandit)

### CI/CD Pipeline
All pull requests must pass:
- Comprehensive test suite
- Security scanning
- Code quality analysis
- YAML syntax validation
- Documentation checks

## Key Guidelines for Contributors

1. **Use the development tools**: Always use `python python_scripts/dev_tools.py` for development tasks
2. **Follow existing patterns**: Look at existing code for style and structure examples
3. **Write tests**: Include tests for any new functionality
4. **Update documentation**: Keep documentation current with code changes
5. **Security first**: Run security scans and address findings
6. **Atomic commits**: Make focused, single-purpose commits with clear messages

## Special Considerations

### AI-Powered Development
This project embraces AI-assisted development with GitHub Copilot. When working on this repository:
- Leverage Copilot for code generation and suggestions
- Ensure all AI-generated code follows project standards
- Test AI-generated code thoroughly
- Document complex AI-assisted implementations

### Repository Organization
The repository uses automated organization scripts. New files should be:
- Added to appropriate directories based on type
- Follow naming conventions for their category
- Include appropriate README files for new directories

## Troubleshooting Common Issues

### Development Setup Issues
```bash
# If pre-commit hooks fail
pre-commit run --all-files

# If tests fail
python python_scripts/dev_tools.py test --no-coverage

# If formatting issues occur
python python_scripts/dev_tools.py format
```

### CI/CD Issues
- Check workflow files in `.github/workflows/` for syntax
- Ensure all required files are present and correctly formatted
- Verify pyproject.toml configuration is valid

This repository represents a modern, AI-enhanced development workflow. Maintain these standards to ensure the "superhuman" level of automation and quality continues to function effectively.