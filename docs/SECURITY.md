# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |

## Reporting a Vulnerability

The AI Script Inventory project takes security seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report

**For security vulnerabilities, please use one of the following methods:**

1. **GitHub Security Advisories** (Preferred)
   - Go to https://github.com/JLWard429/ai-script-inventory-/security/advisories
   - Click "Report a vulnerability"
   - Fill out the form with detailed information

2. **Private Issue**
   - Create a GitHub issue and mark it as confidential
   - Include "[SECURITY]" in the title

### What to Include

Please include the following information in your report:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Any suggested fixes or mitigations
- Your contact information for follow-up

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Status Updates**: Weekly until resolved
- **Resolution**: Based on severity level

### Severity Levels

- **Critical**: Fixed within 24-48 hours
- **High**: Fixed within 1 week  
- **Medium**: Fixed within 2 weeks
- **Low**: Fixed within 30 days

## Security Measures

This project implements several automated security measures:

- **Static Analysis**: Bandit security scanning for Python code
- **Dependency Scanning**: Safety checks for known vulnerabilities
- **CodeQL Analysis**: Semantic code analysis for security issues
- **Secret Scanning**: Detection of hardcoded secrets
- **Automated Updates**: Dependabot for dependency updates

## Disclosure Policy

- Security issues will be patched before public disclosure
- We will coordinate with reporters on disclosure timing
- Credit will be given to reporters unless anonymity is requested
- We aim for coordinated disclosure within 90 days

## Security Best Practices

When contributing to this project:

- Keep dependencies up to date
- Use secure coding practices
- Never commit secrets or sensitive information
- Follow the principle of least privilege
- Test security-related changes thoroughly

## Contact

For questions about this security policy, please contact the maintainers through GitHub issues.