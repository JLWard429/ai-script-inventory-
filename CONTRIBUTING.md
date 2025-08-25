# 🤝 Contributing to AI Script Inventory

Thank you for your interest in contributing to the AI Script Inventory! This project is powered by a superhuman AI workflow system that makes contributing easier, safer, and more enjoyable.

## 🚀 Quick Start for Contributors

### Prerequisites

- Python 3.8+ installed
- Git configured with your credentials
- Basic understanding of Python and/or shell scripting

### Setup Development Environment

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/ai-script-inventory-.git
cd ai-script-inventory-

# 2. Install development dependencies
pip install -e ".[dev]"

# 3. Download required spaCy model for NLP features
python -m spacy download en_core_web_sm

# 4. Set up pre-commit hooks (automated quality checks)
pre-commit install

# 5. Verify everything works
pytest tests/
```

## 🎯 What Can You Contribute?

### 🐍 Python Scripts
- AI/ML tools and utilities
- Data processing scripts
- Automation tools
- API integrations
- Research prototypes

### 🔧 Shell Scripts
- Deployment automation
- System administration tools
- Build scripts
- Environment setup utilities

### 📚 Documentation
- Usage guides
- API documentation
- Tutorials and examples
- Workflow improvements

### 🧪 Tests and Quality Improvements
- Unit tests for existing scripts
- Integration tests
- Performance optimizations
- Security enhancements

## 📋 Contribution Process

### 1. Choose Your Contribution Type

**🔥 Quick Contributions (< 30 minutes)**
- Fix typos or documentation
- Add comments to existing code
- Create simple utility scripts
- Update README files

**🛠️ Medium Contributions (1-4 hours)**
- Add new Python/shell scripts
- Improve existing tools
- Add comprehensive tests
- Enhance documentation

**🚀 Major Contributions (> 4 hours)**
- Design new workflow features
- Create comprehensive tutorials
- Implement security improvements
- Add new automation capabilities

### 2. Development Workflow

```bash
# 1. Create a feature branch
git checkout -b feature/your-feature-name

# 2. Make your changes
# - Add your scripts to appropriate directories
# - The automation will organize files for you
# - Write tests for new functionality
# - Update documentation as needed

# 3. Commit your changes (pre-commit hooks run automatically)
git add .
git commit -m "feat: add awesome new AI tool"

# 4. Push to your fork
git push origin feature/your-feature-name

# 5. Create a Pull Request
# - The superhuman workflow runs automatically
# - Address any feedback from automated checks
# - Wait for human review and approval
```

### 3. Automated Quality Assurance

Our superhuman workflow system automatically:

✅ **Formats your code** (Black, isort)  
✅ **Checks code quality** (flake8, mypy)  
✅ **Scans for security issues** (Bandit, Safety)  
✅ **Organizes files by type**  
✅ **Runs comprehensive tests**  
✅ **Updates documentation**  
✅ **Provides detailed feedback**  

## 📝 Coding Standards

### Python Scripts

```python
#!/usr/bin/env python3
"""
Brief description of what the script does.

This script demonstrates the coding standards for the AI Script Inventory.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional

def main() -> None:
    """Main function with type hints and docstring."""
    print("Hello, AI World!")

if __name__ == "__main__":
    main()
```

**Requirements:**
- Type hints for function parameters and return values
- Docstrings for modules, classes, and functions
- PEP 8 compliance (enforced automatically)
- Error handling for external dependencies
- Clear variable and function names

### Shell Scripts

```bash
#!/bin/bash
# Brief description of what the script does
#
# Usage: script_name.sh [options]
# Author: Your Name
# Date: YYYY-MM-DD

set -euo pipefail  # Exit on error, undefined vars, pipe failures

main() {
    echo "Hello, Shell World!"
}

# Only run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

**Requirements:**
- Proper shebang line
- Error handling with `set -euo pipefail`
- Clear documentation and usage information
- Proper quoting and variable handling
- ShellCheck compliance (checked automatically)

### Documentation

- Use clear, concise language
- Include code examples where appropriate
- Follow Markdown best practices
- Add screenshots for UI-related features
- Keep README files up-to-date

## 🧪 Testing Guidelines

### For Python Scripts

```python
# tests/test_your_script.py
import pytest
from pathlib import Path

def test_script_functionality():
    """Test that your script works as expected."""
    # Arrange
    test_input = "sample data"
    
    # Act
    result = your_function(test_input)
    
    # Assert
    assert result == expected_output

def test_script_error_handling():
    """Test that your script handles errors gracefully."""
    with pytest.raises(ValueError):
        your_function(invalid_input)
```

### For Shell Scripts

```bash
# Add to existing test files or create new ones
test_shell_script() {
    # Test successful execution
    ./your_script.sh --help
    assertEquals "Should return help" 0 $?
    
    # Test error handling
    ./your_script.sh --invalid-option
    assertNotEquals "Should fail with invalid option" 0 $?
}
```

### Testing Best Practices

- Write tests before or alongside your code
- Test both success and failure cases
- Use descriptive test names
- Keep tests simple and focused
- Aim for good coverage (automatically tracked)

## 🔒 Security Guidelines

### What We Check Automatically

- **Hardcoded secrets** (passwords, API keys, tokens)
- **Known vulnerabilities** in dependencies
- **Insecure coding patterns** (SQL injection, XSS, etc.)
- **Suspicious shell commands**
- **File permission issues**

### Security Best Practices

```python
# ✅ Good: Use environment variables for secrets
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable required")

# ❌ Bad: Hardcoded secrets
api_key = "sk-1234567890abcdef"  # This will be caught by automation!
```

```bash
# ✅ Good: Validate input
if [[ ! "$input" =~ ^[a-zA-Z0-9]+$ ]]; then
    echo "Error: Invalid input format"
    exit 1
fi

# ❌ Bad: No input validation
eval "$user_input"  # Dangerous! Will be flagged
```

## 📊 Pull Request Guidelines

### PR Title Format

Use conventional commit format:

- `feat: add new AI training script`
- `fix: resolve memory leak in data processor`
- `docs: update API documentation`
- `test: add unit tests for utility functions`
- `refactor: improve code organization`
- `security: fix potential XSS vulnerability`

### PR Description Template

```markdown
## 🎯 What does this PR do?

Brief description of the changes.

## 🔄 Type of Change

- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 📚 Documentation update
- [ ] 🧪 Test improvement
- [ ] 🔒 Security enhancement
- [ ] ♻️ Refactoring

## 🧪 Testing

- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## 📝 Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review of the code completed
- [ ] Documentation updated if needed
- [ ] No breaking changes introduced
```

### Automated Checks

Your PR will automatically be checked for:

- ✅ Code formatting and style
- ✅ Security vulnerabilities
- ✅ Test coverage
- ✅ Documentation completeness
- ✅ Performance impact
- ✅ Compatibility across Python versions

## 🎉 Recognition

Contributors are recognized in several ways:

- **GitHub Contributors Graph**: Automatic recognition
- **Release Notes**: Major contributions highlighted
- **Documentation Credits**: Listed in relevant docs
- **Special Badges**: For significant contributions

## 🆘 Getting Help

### Community Support

- **GitHub Discussions**: For general questions and ideas
- **GitHub Issues**: For bug reports and feature requests
- **Pull Request Comments**: For code-specific questions

### Documentation Resources

- 📖 **[WORKFLOW.md](WORKFLOW.md)** - Detailed automation documentation
- 🔒 **[SECURITY.md](SECURITY.md)** - Security policies and procedures
- 📚 **[docs/](docs/)** - Additional guides and references

### Common Issues and Solutions

**Issue**: Pre-commit hooks failing
```bash
# Solution: Run hooks manually to see detailed errors
pre-commit run --all-files
```

**Issue**: Tests failing locally
```bash
# Solution: Run tests with verbose output
pytest tests/ -v --tb=short
```

**Issue**: Code formatting errors
```bash
# Solution: Auto-format code
black .
isort .
```

## 🌟 Contribution Tips

### For First-Time Contributors

1. **Start Small**: Begin with documentation fixes or simple scripts
2. **Read the Code**: Familiarize yourself with existing patterns
3. **Ask Questions**: Don't hesitate to ask for help or clarification
4. **Be Patient**: Allow time for review and feedback

### For Experienced Contributors

1. **Review Others' PRs**: Help maintain code quality
2. **Suggest Improvements**: Propose workflow enhancements
3. **Mentor Newcomers**: Help guide first-time contributors
4. **Share Knowledge**: Write tutorials and documentation

### Making Quality Contributions

- **Understand the Problem**: Fully understand what you're solving
- **Research Existing Solutions**: Don't reinvent the wheel
- **Write Clear Code**: Code should be self-documenting
- **Test Thoroughly**: Both happy path and edge cases
- **Document Well**: Include usage examples and gotchas

## 📈 Impact and Analytics

Your contributions help improve:

- **Code Quality Score**: Measured through automated analysis
- **Security Posture**: Tracked through vulnerability scans
- **Test Coverage**: Monitored and reported automatically
- **Documentation Quality**: Assessed through completeness metrics
- **Community Growth**: Measured through contribution frequency

## 🎊 Thank You!

Every contribution, no matter how small, makes this project better. Thank you for taking the time to contribute to the AI Script Inventory superhuman workflow system!

---

**Questions?** Open an issue or start a discussion. We're here to help! 🚀

### Setting Up Your Development Environment

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/ai-script-inventory-.git
   cd ai-script-inventory-
   ```

2. **Set up the upstream remote**
   ```bash
   git remote add upstream https://github.com/JLWard429/ai-script-inventory-.git
   ```

3. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt  # If it exists
   # Or install common development tools
   pip install black flake8 isort mypy pytest
   ```

5. **Test the setup**
   ```bash
   python .github/scripts/organize_ai_scripts.py
   ```

## 📝 Development Workflow

### 1. Before Making Changes

1. **Sync with upstream**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

### 2. Making Changes

1. **Follow the current project structure** (see main [README.md](README.md) for complete structure):
   - Python scripts → `python_scripts/` (duplicates auto-archived to `archives/`)
   - Shell scripts → `shell_scripts/`
   - Documentation → `docs/`
   - Text files → `text_files/` (with `reports/` and `archives/` subdirectories)
   - Core modules → `src/ai_script_inventory/`

2. **Code style guidelines**
   - Use [Black](https://black.readthedocs.io/) for Python code formatting
   - Follow [PEP 8](https://pep8.org/) for Python code style
   - Use meaningful variable and function names
   - Add docstrings to functions and classes
   - Keep functions focused and reasonably sized

3. **Commit guidelines**
   - Use [Conventional Commits](https://www.conventionalcommits.org/) format:
     - `feat: add new script organization feature`
     - `fix: resolve issue with file path handling`
     - `docs: update installation instructions`
     - `style: format code with black`
     - `refactor: simplify organization logic`
     - `test: add tests for organization script`
   - Make atomic commits (one logical change per commit)
   - Write clear, descriptive commit messages

### 3. Testing Your Changes

1. **Run the organization script**
   ```bash
   python .github/scripts/organize_ai_scripts.py
   ```

2. **Run code quality checks**
   ```bash
   # Format code
   black .
   
   # Sort imports
   isort .
   
   # Lint code
   flake8 .
   
   # Type checking (if applicable)
   mypy .
   ```

3. **Test manually**
   - Add some test files to the root directory
   - Run the organization script
   - Verify files are moved correctly
   - Check that the script handles edge cases

### 4. Submitting Changes

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a pull request**
   - Use the pull request template
   - Fill out all relevant sections
   - Link to any related issues
   - Add screenshots if applicable

3. **Respond to feedback**
   - Be open to suggestions and improvements
   - Make requested changes promptly
   - Update your PR as needed

## 📚 Contribution Types

### Adding New Scripts

When contributing new scripts to the inventory:

1. **Place in the correct directory**
   - Python scripts → `python_scripts/`
   - Shell scripts → `shell_scripts/`

2. **Include proper documentation**
   - Add a header comment explaining what the script does
   - Include usage instructions
   - Document any dependencies
   - Add examples if helpful

3. **Example script header**
   ```python
   #!/usr/bin/env python3
   """
   Script Name: AI Model Downloader
   Description: Downloads and manages AI models from various sources
   Author: Your Name
   Date: 2024-01-01
   Dependencies: requests, tqdm
   
   Usage:
       python download_models.py --model gpt-3.5-turbo --output ./models/
   
   Examples:
       python download_models.py --list-available
       python download_models.py --model bert-base --format pytorch
   """
   ```

### Improving Documentation

- Fix typos and grammatical errors
- Add missing information
- Improve clarity and readability
- Add examples and use cases
- Update outdated information

### Enhancing GitHub Workflows

- Improve CI/CD pipelines
- Add new security checks
- Optimize performance
- Add better error handling
- Enhance reporting and notifications

## 🛡️ Security Guidelines

- **Never commit secrets** (API keys, passwords, tokens)
- **Use environment variables** for sensitive configuration
- **Follow security best practices** in code
- **Report security vulnerabilities** privately
- **Keep dependencies updated**

## 🧪 Testing Guidelines

### Manual Testing

1. **Organization Script Testing**
   ```bash
   # Create test files
   touch test.py test.sh test.md test.txt
   
   # Run organization
   python .github/scripts/organize_ai_scripts.py
   
   # Verify correct placement
   ls python_scripts/test.py
   ls shell_scripts/test.sh
   ls docs/test.md
   ls text_files/test.txt
   ```

2. **Edge Case Testing**
   - Empty files
   - Files with special characters
   - Very long filenames
   - Files without extensions
   - Duplicate filenames

### Automated Testing

If you're adding automated tests:
- Use `pytest` for Python tests
- Place tests in a `tests/` directory
- Name test files with `test_` prefix
- Write clear test names that describe what they test

## 📖 Documentation Style

- Use clear, concise language
- Include code examples where helpful
- Use proper Markdown formatting
- Add emojis sparingly for visual appeal
- Keep documentation up to date with code changes

## 🤝 Code Review Process

### For Contributors

- Be patient with the review process
- Respond to feedback constructively
- Make requested changes promptly
- Ask questions if feedback is unclear

### For Reviewers

- Be constructive and respectful
- Focus on code quality and functionality
- Suggest improvements, not just problems
- Approve when changes meet standards

## 🏷️ Issue and PR Labels

Understanding our labeling system:

- **Type**: `bug`, `enhancement`, `documentation`, `question`
- **Priority**: `critical`, `high`, `medium`, `low`
- **Status**: `triage`, `in-progress`, `blocked`, `ready-for-review`
- **Component**: `python`, `shell`, `workflows`, `docs`

## 🎯 Project Goals

After recent repository organization and deduplication, we maintain these core goals:

1. **Organization**: Maintain the well-organized, automated structure with proper archiving
2. **Automation**: Enhance automation capabilities and workflows including the Superhuman AI Terminal
3. **Security**: Maintain enterprise-grade security standards with comprehensive scanning
4. **Documentation**: Provide clear, helpful documentation that stays current with organizational changes
5. **Community**: Foster a welcoming, inclusive community that supports contributors

## ❓ Getting Help

- **Documentation**: Check the main [README.md](README.md) and [docs](./docs/) directory first
- **Discussions**: Use [GitHub Discussions](https://github.com/JLWard429/ai-script-inventory-/discussions) for questions
- **Issues**: Create an issue for bugs or feature requests
- **Security**: For security concerns, see our [Security Policy](SECURITY.md)
- **Contact**: Reach out to @JLWard429 for project-related questions

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

Thank you for contributing to the AI Script Inventory! Your efforts help make this project better for everyone. 🙏