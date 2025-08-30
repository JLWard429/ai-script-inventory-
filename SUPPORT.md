# Support

## Getting Help

There are several ways to get help with the AI Script Inventory:

### 📖 Documentation
- **README.md**: Basic setup and usage instructions
- **docs/WORKFLOW.md**: CI/CD and development workflow information
- **docs/CONTRIBUTING.md**: Contribution guidelines and development setup
- **docs/SECURITY.md**: Security policies and best practices

### 🐛 Issues and Bug Reports
If you encounter a bug or have a feature request:

1. **Search existing issues** first to avoid duplicates
2. **Use issue templates** to provide complete information
3. **Include relevant details**:
   - Operating system and Python version
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Error messages and logs
   - Screenshots if applicable

[Create a new issue](https://github.com/JLWard429/ai-script-inventory-/issues/new)

### 💡 Feature Requests
For new feature suggestions:
- Describe the use case and benefits
- Provide examples of how it would work
- Consider implementation complexity
- Check if similar functionality exists

### 🤔 Questions and Discussions
For general questions about usage, best practices, or project direction:
- Open a Discussion in the GitHub repository
- Check existing discussions for similar topics
- Be specific about what you're trying to accomplish

## Superhuman Terminal Help

The AI-powered terminal includes built-in help:

```bash
# Start the terminal
python superhuman_terminal.py

# Try these commands in the terminal:
help
status
list files
show README.md
```

### Common Terminal Commands
- `help` - Show available commands and usage
- `status` - Display system status and configuration
- `list <type>` - List files, scripts, or other resources
- `show <file>` - Display file contents
- `run <script>` - Execute scripts safely
- `search <term>` - Find files or content

## Troubleshooting

### Common Issues

#### spaCy Model Not Found
```bash
# Download the required model
python -m spacy download en_core_web_sm
```

#### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements-dev.txt

# Check for missing packages
python -c "import ai_tools; print('Import successful')"
```

#### Permission Errors
```bash
# Make scripts executable
chmod +x shell_scripts/*.sh

# Check file permissions
ls -la python_scripts/
```

#### CI/CD Failures
- Check workflow logs in GitHub Actions
- Verify all tests pass locally
- Ensure dependencies are up to date
- Review code quality checks

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: 2GB+ recommended for AI models
- **Storage**: 1GB+ for full installation
- **Network**: Required for initial setup and model downloads

### Performance Tips
- Use virtual environments for isolation
- Keep dependencies minimal
- Monitor memory usage with large AI models
- Use local caching for repeated operations

## Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers get started
- Follow project conventions

### Response Times
- **Bug reports**: Within 48 hours for acknowledgment
- **Feature requests**: Within 1 week for initial review
- **Security issues**: Within 24 hours (see SECURITY.md)
- **Pull requests**: Within 1 week for review

## Self-Service Resources

### Quick Start
```bash
# Clone and setup
git clone https://github.com/JLWard429/ai-script-inventory-.git
cd ai-script-inventory-
pip install -r requirements-dev.txt
python -m spacy download en_core_web_sm

# Run tests
python -m pytest tests/

# Start terminal
python superhuman_terminal.py
```

### Health Checks
```bash
# Verify installation
python -c "import ai_tools; print('✅ Core imports work')"
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('✅ spaCy model loaded')"

# Run basic tests
python -m pytest tests/test_basic.py -v
```

### Logs and Debugging
- Check terminal output for error messages
- Review test results for specific failures
- Use `--verbose` flags for detailed information
- Enable debug mode in configuration if available

## Professional Support

While this is an open-source project, here are resources for additional help:

### Learning Resources
- **Python Documentation**: https://docs.python.org/
- **spaCy Documentation**: https://spacy.io/
- **GitHub Actions**: https://docs.github.com/en/actions

### Related Projects
- AI script management tools
- Natural language processing libraries
- CI/CD automation frameworks
- Security scanning tools

## Contributing Back

If you find solutions to common problems:
- **Update documentation** with your findings
- **Share troubleshooting tips** in discussions
- **Submit improvements** via pull requests
- **Help other users** with similar issues

Your contributions help make the project better for everyone!

---

**Need immediate help?** Open an issue with the "help wanted" label for faster community response.