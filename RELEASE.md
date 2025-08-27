# Release Process and Security

This document describes the release process for AI Script Inventory, including security measures, signed releases, and provenance verification.

## Release Process

### Automated Release Pipeline

Our release process is fully automated and includes multiple security measures:

1. **Code Quality Checks**: All code must pass comprehensive quality and security checks
2. **Automated Testing**: Full test suite across multiple Python versions
3. **Security Scanning**: Static analysis, dependency scanning, and vulnerability checks
4. **Build Process**: Automated package building with hash generation
5. **Provenance Generation**: SLSA Level 3 provenance attestation
6. **Signed Releases**: Digital signatures for all release artifacts

### Release Workflow

Releases are triggered by creating a Git tag with the format `v*` (e.g., `v1.0.0`):

```bash
git tag v1.0.0
git push origin v1.0.0
```

This triggers the automated release pipeline defined in `.github/workflows/publish.yml`.

## Security Measures

### Code Signing

All release artifacts are signed using GitHub's built-in signing capabilities:

- **Commits**: All commits in releases are signed with verified signatures
- **Tags**: Release tags are signed and verified
- **Artifacts**: Package distributions include cryptographic hashes

### Provenance Attestation

We generate SLSA Level 3 provenance attestations for all releases using the SLSA GitHub Generator:

- **Build Environment**: Fully isolated and auditable
- **Source Integrity**: Direct link from source code to built artifacts
- **Reproducible Builds**: Deterministic build process
- **Tamper Evidence**: Cryptographic verification of build integrity

### Verification Process

#### Verifying Release Integrity

1. **Download the release artifacts** from GitHub Releases
2. **Verify the SHA256 hashes** against the published checksums
3. **Check the provenance attestation** using the SLSA verifier tool

#### Example Verification Commands

```bash
# Download release artifacts
wget https://github.com/JLWard429/ai-script-inventory-/releases/download/v1.0.0/ai_script_inventory-1.0.0-py3-none-any.whl

# Verify SHA256 hash
sha256sum ai_script_inventory-1.0.0-py3-none-any.whl

# Install SLSA verifier
go install github.com/slsa-framework/slsa-verifier/v2/cli/slsa-verifier@latest

# Verify provenance
slsa-verifier verify-artifact ai_script_inventory-1.0.0-py3-none-any.whl \
  --provenance-path ai_script_inventory-1.0.0-py3-none-any.whl.intoto.jsonl \
  --source-uri github.com/JLWard429/ai-script-inventory-
```

## Supply Chain Security

### Dependencies

- All dependencies are pinned with cryptographic hashes
- Automated dependency vulnerability scanning with Safety and Dependabot
- Regular dependency updates through automated pull requests
- License compliance checking for all dependencies

### Build Environment

- Isolated GitHub Actions runners for all builds
- Minimal required permissions for workflow tokens
- No secrets or credentials in build artifacts
- Comprehensive audit logging of all build steps

### Distribution

- Packages distributed only through official channels (PyPI)
- Multi-factor authentication required for maintainer accounts
- API token authentication for automated publishing
- Provenance attestations published alongside packages

## Branch Protection

The following branch protection rules are enforced:

### Main Branch (`main`)

- **Required Reviews**: At least 2 reviews from code owners
- **Dismiss Stale Reviews**: Enabled when new commits are pushed
- **Required Status Checks**: All CI/CD checks must pass
- **Up-to-date Branches**: Branches must be up to date before merging
- **Include Administrators**: Rules apply to administrators
- **Restrict Push**: Only allow through pull requests
- **Signed Commits**: Require signed commits for all changes

### Development Branch (`develop`)

- **Required Reviews**: At least 1 review from maintainers
- **Required Status Checks**: Core CI checks must pass
- **Up-to-date Branches**: Required
- **Signed Commits**: Required

## Release Types

### Major Releases (x.0.0)

- Breaking changes or significant new features
- Comprehensive security review required
- Extended testing period
- Migration guides provided

### Minor Releases (x.y.0)

- New features and enhancements
- Backward compatibility maintained
- Standard testing and review process

### Patch Releases (x.y.z)

- Bug fixes and security patches
- Fast-track for critical security fixes
- Minimal testing required for low-risk changes

### Security Releases

- Expedited process for critical security fixes
- May break normal release schedule
- Coordinated disclosure with security researchers
- Post-release security advisory publication

## Rollback Procedures

If a release introduces critical issues:

1. **Immediate Response**: Create new patch release with fix
2. **Package Withdrawal**: Remove problematic version from PyPI if necessary
3. **Communication**: Update all communication channels
4. **Post-Mortem**: Conduct analysis and improve processes

## Compliance

This release process follows industry best practices:

- **SLSA Framework**: Level 3 compliance for supply chain security
- **OpenSSF Scorecard**: Regular assessment and improvement
- **NIST SSDF**: Secure Software Development Framework alignment
- **CVE Process**: Responsible vulnerability disclosure

## Contact

For questions about the release process or security concerns:

- **Security Issues**: See [SECURITY.md](SECURITY.md)
- **Release Questions**: Open a GitHub issue
- **General Support**: See [SUPPORT.md](SUPPORT.md)

---

*This document is part of our commitment to transparent and secure software distribution.*