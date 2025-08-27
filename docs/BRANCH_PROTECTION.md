# Branch Protection and Security Policies

This document outlines the branch protection rules and security policies for the AI Script Inventory repository.

## Branch Protection Rules

### Main Branch (`main`)

The main branch is our production branch and has the strictest protection rules:

**Required Settings:**
- ✅ **Restrict pushes that create files** - Direct pushes are not allowed
- ✅ **Require pull request reviews before merging**
  - Required number of reviews: **2**
  - Dismiss stale reviews when new commits are pushed
  - Require review from code owners
  - Restrict reviews to users with write access
- ✅ **Require status checks to pass before merging**
  - Require branches to be up to date before merging
  - Required status checks:
    - `🔍 Code Quality & Linting`
    - `🧪 Test Suite (Python 3.11)`
    - `🛡️ Security Analysis`
    - `🔐 CodeQL Python Analysis`
- ✅ **Require signed commits** - All commits must be signed
- ✅ **Require linear history** - Prevent merge commits
- ✅ **Include administrators** - Rules apply to repository administrators
- ✅ **Restrict force pushes** - Force pushes are not allowed
- ✅ **Allow deletion** - Disabled

### Development Branch (`develop`)

The development branch has slightly relaxed rules for active development:

**Required Settings:**
- ✅ **Require pull request reviews before merging**
  - Required number of reviews: **1**
  - Dismiss stale reviews when new commits are pushed
  - Require review from maintainers
- ✅ **Require status checks to pass before merging**
  - Require branches to be up to date before merging
  - Required status checks:
    - `🔍 Code Quality & Linting`
    - `🧪 Test Suite (Python 3.11)`
- ✅ **Require signed commits** - All commits must be signed
- ✅ **Include administrators** - Rules apply to repository administrators
- ✅ **Restrict force pushes** - Force pushes are not allowed

### Feature Branches

Feature branches follow a standard naming convention:

- `feature/feature-name` - New features
- `bugfix/bug-description` - Bug fixes
- `hotfix/critical-fix` - Critical fixes
- `security/security-fix` - Security-related fixes

**Protection Rules:**
- No direct protection rules (relies on target branch protection)
- Must pass CI checks before merging to protected branches
- Must be signed commits

## Signed Commits Policy

All commits to protected branches must be signed using one of the following methods:

### GPG Signing (Recommended)

1. **Generate a GPG key** if you don't have one:
   ```bash
   gpg --full-generate-key
   ```

2. **Configure Git to use your GPG key**:
   ```bash
   git config user.signingkey YOUR_GPG_KEY_ID
   git config commit.gpgsign true
   ```

3. **Add your GPG key to GitHub**:
   - Go to Settings → SSH and GPG keys
   - Click "New GPG key"
   - Paste your public key

### SSH Signing (Alternative)

1. **Configure Git to use SSH signing**:
   ```bash
   git config gpg.format ssh
   git config user.signingkey /path/to/your/ssh/key
   git config commit.gpgsign true
   ```

2. **Add your SSH key to GitHub** with signing capability

### Verification

Verify that commits are signed:
```bash
git log --show-signature
```

## Security Enforcement

### Automated Security Checks

All pull requests must pass the following security checks:

- **Bandit**: Static security analysis for Python code
- **Safety**: Dependency vulnerability scanning
- **CodeQL**: Semantic code analysis for security issues
- **Secret Scanning**: Detection of hardcoded secrets
- **Dependency Review**: Analysis of new dependencies

### Manual Security Review

Security-sensitive changes require additional manual review:

- Changes to authentication/authorization code
- New dependency additions
- Changes to CI/CD workflows
- Modifications to security configurations

### Security Response Process

1. **Critical Security Issues**: 
   - Immediate private security advisory
   - Hotfix branch with expedited review
   - Coordinated disclosure process

2. **Security Updates**:
   - Regular dependency updates via Dependabot
   - Monthly security review of all dependencies
   - Quarterly security audit of the entire codebase

## Exemptions and Overrides

### Administrator Override

Repository administrators can override branch protection rules in the following cases:

- **Emergency hotfixes** for critical security vulnerabilities
- **Infrastructure changes** that prevent normal CI from running
- **Repository maintenance** tasks that require direct access

**Process for Override:**
1. Document the reason for override in a GitHub issue
2. Notify other maintainers before proceeding
3. Create a follow-up issue to ensure proper process in the future
4. Conduct post-incident review if applicable

### Bot Commits

Certain automated processes are exempted from some requirements:

- **Dependabot**: Automated dependency updates
- **Auto-organization**: File organization automation
- **Release automation**: Version bump and changelog generation

These bots use dedicated service accounts with minimal required permissions.

## Enforcement Tools

### GitHub Branch Protection

Branch protection rules are enforced at the GitHub platform level and cannot be bypassed without administrator privileges.

### Required Status Checks

The following GitHub Actions workflows must pass:

- **CI/CD Pipeline** (`.github/workflows/ci-cd.yml`)
- **Code Quality** (`.github/workflows/code-quality.yml`)
- **CodeQL Analysis** (`.github/workflows/codeql.yml`)
- **Security Scanning** (`.github/workflows/dependency-scan.yml`)

### Pre-commit Hooks

Local development includes pre-commit hooks that enforce:

- Code formatting (Black, isort)
- Linting (flake8, pylint)
- Security scanning (bandit)
- Commit message format
- Large file detection

Install with:
```bash
pre-commit install
```

## Monitoring and Compliance

### Security Dashboard

The repository security dashboard provides visibility into:

- Open security advisories
- Dependency vulnerabilities
- Code scanning alerts
- Secret scanning alerts

### Audit Logging

All protected branch activities are logged:

- Pull request reviews and approvals
- Branch protection rule changes
- Administrator overrides
- Security-related events

### Regular Reviews

- **Monthly**: Review of branch protection rules and compliance
- **Quarterly**: Comprehensive security audit
- **Annually**: Review and update of security policies

## Contact

For questions about branch protection or security policies:

- **Security Issues**: See [SECURITY.md](SECURITY.md)
- **Policy Questions**: Open a GitHub issue
- **General Support**: See [SUPPORT.md](SUPPORT.md)

---

*This document is part of our commitment to secure development practices and supply chain security.*