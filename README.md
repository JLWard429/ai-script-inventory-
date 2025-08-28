# AI Script Inventory

[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/xxxx/badge)](https://www.bestpractices.dev/projects/xxxx)
[![CodeQL](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/codeql.yml/badge.svg)](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/codeql.yml)
[![CI/CD](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/ci-cd.yml)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=JLWard429_ai-script-inventory-&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=JLWard429_ai-script-inventory-)

This repository contains a collection of AI-related scripts and tools with automated workflow management.

## 🚀 Superhuman AI Workflow System

This repository implements an advanced automation system for managing AI scripts, ensuring code quality, and maintaining documentation.

### Key Features

- **Superman AI Terminal**: Advanced AI-powered command-line interface with **official OpenAI integration**
- **Automated Code Organization**: Files are automatically sorted by type into appropriate directories
- **Code Quality Assurance**: Automated linting, formatting, and security scanning
- **Documentation Management**: Auto-generated and maintained documentation
- **Testing Infrastructure**: Comprehensive test suite with coverage reporting
- **Security Monitoring**: Automated vulnerability scanning and dependency checks

### Directory Structure

- `python_scripts/` - Python scripts and AI tools
- `shell_scripts/` - Shell scripts and command-line utilities
- `docs/` - Documentation, guides, and reference materials
- `text_files/` - Configuration files, logs, and text-based resources
- `.github/` - GitHub Actions workflows and automation scripts

### Getting Started

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   # Basic installation
   pip install -r requirements.txt
   
   # Full development setup with OpenAI integration
   pip install -r requirements-dev.txt
   ```
3. **Configure OpenAI (optional)**:
   ```bash
   export OPENAI_API_KEY="sk-your-api-key-here"
   ```
4. **Set up development tools**:
   ```bash
   pre-commit install
   ```
5. **Try the Superman AI Terminal**:
   ```bash
   python python_scripts/superman.py
   ```

For detailed OpenAI setup instructions, see [OpenAI Integration Guide](docs/OPENAI_INTEGRATION.md).

See [WORKFLOW.md](docs/WORKFLOW.md) for detailed information about the automation system.

## 🔒 Security

Security is a top priority for this project. We implement multiple layers of automated security scanning:

- **Static Analysis**: Bandit security scanning
- **Dependency Scanning**: Safety vulnerability checks  
- **CodeQL Analysis**: Semantic code analysis
- **Secret Detection**: Automated secret scanning

For security issues, please see our [Security Policy](SECURITY.md).

## 📞 Support

Need help? Check out our support resources:

- **[Support Guide](SUPPORT.md)** - How to get help
- **[Documentation](docs/)** - Comprehensive project documentation
- **[Issues](https://github.com/JLWard429/ai-script-inventory-/issues)** - Bug reports and feature requests
- **[Discussions](https://github.com/JLWard429/ai-script-inventory-/discussions)** - Community Q&A

## 🤝 Contributing

We welcome contributions! Please see:

- **[Contributing Guidelines](docs/CONTRIBUTING.md)** - How to contribute
- **[Code of Conduct](docs/CODE_OF_CONDUCT.md)** - Community standards
- **[Security Policy](SECURITY.md)** - Security guidelines

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
