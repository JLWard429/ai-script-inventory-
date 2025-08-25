# Contributing to AI Script Inventory

Thank you for your interest in contributing to the AI Script Inventory! This document provides guidelines and information for contributors.

## 🌟 Ways to Contribute

- **Report bugs** by opening detailed [bug reports](https://github.com/JLWard429/ai-script-inventory-/issues/new?template=bug_report.yml)
- **Suggest features** through [feature requests](https://github.com/JLWard429/ai-script-inventory-/issues/new?template=feature_request.yml)
- **Improve documentation** by fixing errors or adding clarifications
- **Submit code** via pull requests for bug fixes or new features
- **Help with testing** by reviewing pull requests
- **Share scripts** by adding your AI-related scripts to the inventory

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- A GitHub account
- Basic familiarity with command line tools

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

1. **Follow the project structure**
   - Python scripts → `python_scripts/`
   - Shell scripts → `shell_scripts/`
   - Documentation → `docs/`
   - Text files → `text_files/`

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

When contributing, keep these goals in mind:

1. **Organization**: Keep the repository well-organized and easy to navigate
2. **Automation**: Enhance automation capabilities and workflows
3. **Security**: Maintain high security standards
4. **Documentation**: Provide clear, helpful documentation
5. **Community**: Foster a welcoming, inclusive community

## ❓ Getting Help

- **Documentation**: Check the [docs](./docs/) directory first
- **Discussions**: Use [GitHub Discussions](https://github.com/JLWard429/ai-script-inventory-/discussions) for questions
- **Issues**: Create an issue for bugs or feature requests
- **Contact**: Reach out to @JLWard429 for project-related questions

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the [MIT License](../LICENSE).

---

Thank you for contributing to the AI Script Inventory! Your efforts help make this project better for everyone. 🙏