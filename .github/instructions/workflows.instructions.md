---
applyTo: ".github/workflows/**/*.yml"
---

# GitHub Workflows Instructions

When working with GitHub Actions workflows in `.github/workflows/`, follow these guidelines for reliable and maintainable CI/CD pipelines:

## Workflow Design Principles

1. **Efficiency and Performance**
   - Use concurrency groups to cancel redundant runs
   - Implement smart path filtering to avoid unnecessary executions
   - Cache dependencies appropriately (pip cache, setup-python cache)
   - Use matrix strategies for multi-environment testing

2. **Reliability and Robustness**
   - Include proper error handling and fallbacks
   - Use specific action versions (not @main or @latest)
   - Implement timeouts for long-running jobs
   - Add retry mechanisms for flaky operations

3. **Security Best Practices**
   - Use minimal required permissions
   - Pin action versions to specific commits when possible
   - Validate inputs and sanitize outputs
   - Use GitHub's security features (SARIF uploads, CodeQL)

## Required Workflow Standards

1. **Code Quality Enforcement**
   - Every workflow should enforce code formatting (Black, isort)
   - Include linting checks (flake8, pylint)
   - Run security scans (Bandit, Safety)
   - Validate configuration files (YAML syntax, JSON formatting)

2. **Testing Requirements**
   - Run tests across multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)
   - Include test coverage reporting
   - Test script syntax and execution
   - Validate repository structure and organization

3. **Documentation and Reporting**
   - Generate comprehensive workflow summaries
   - Upload artifacts for test reports and security scans
   - Provide clear job status and failure information
   - Include performance metrics when relevant

## Workflow Structure Template

```yaml
name: Descriptive Workflow Name

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'relevant/**/*'
  pull_request:
    branches: [ main, develop ]
    paths:
      - 'relevant/**/*'
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  PYTHON_VERSION: '3.11'

permissions:
  contents: read
  security-events: write

jobs:
  # Change detection for efficiency
  changes:
    name: Detect Changes
    runs-on: ubuntu-latest
    outputs:
      relevant_changes: ${{ steps.changes.outputs.relevant }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v2
        id: changes
        with:
          filters: |
            relevant:
              - 'path/to/relevant/files/**'

  # Main workflow jobs
  main-job:
    name: Main Job Description
    runs-on: ubuntu-latest
    needs: changes
    if: needs.changes.outputs.relevant_changes == 'true'
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip setuptools wheel
          pip install -r requirements-dev.txt

      # Add specific job steps here

  # Summary job (always runs)
  workflow-summary:
    name: Workflow Summary
    runs-on: ubuntu-latest
    needs: [changes, main-job]
    if: always()
    
    steps:
      - name: Generate summary
        run: |
          echo "## Workflow Results" >> $GITHUB_STEP_SUMMARY
          echo "| Job | Status |" >> $GITHUB_STEP_SUMMARY
          echo "|-----|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| Main Job | ${{ needs.main-job.result }} |" >> $GITHUB_STEP_SUMMARY
```

## Specific Workflow Types

1. **Code Quality Workflows**
   - Run on every push and PR
   - Include formatting, linting, and security checks
   - Auto-fix formatting issues when possible
   - Upload security scan results as artifacts

2. **Testing Workflows**
   - Test across multiple Python versions and platforms
   - Include unit tests, integration tests, and script validation
   - Generate and upload coverage reports
   - Test with both minimal and full dependency sets

3. **Security Workflows**
   - Run security scans (CodeQL, Bandit, Safety, Trivy)
   - Upload results to GitHub Security tab
   - Include dependency vulnerability checks
   - Monitor for secrets and sensitive data

4. **Release Workflows**
   - Trigger on version tags
   - Generate changelog from commit history
   - Create GitHub releases with artifacts
   - Include comprehensive validation before release

## Performance Optimization

1. **Caching Strategies**
   ```yaml
   - name: Cache pip dependencies
     uses: actions/cache@v3
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
       restore-keys: |
         ${{ runner.os }}-pip-
   ```

2. **Parallel Execution**
   - Use matrix strategies for independent variations
   - Split large jobs into smaller, focused jobs
   - Use job dependencies only when necessary

3. **Resource Management**
   - Set appropriate timeouts for jobs and steps
   - Use `continue-on-error` for non-critical steps
   - Clean up artifacts and temporary files

## Error Handling and Debugging

1. **Comprehensive Logging**
   - Use descriptive step names
   - Add debug output for complex operations
   - Include context information in error messages

2. **Artifact Collection**
   - Upload logs and reports on failure
   - Include test outputs and coverage reports
   - Store security scan results for analysis

3. **Conditional Execution**
   - Use appropriate conditions for optional steps
   - Handle different event types (push, PR, schedule)
   - Skip jobs gracefully when not needed

## Integration with Repository Features

1. **Superhuman AI Terminal**
   - Test terminal functionality in CI
   - Validate local-only processing
   - Ensure privacy protections are maintained

2. **Organization Script**
   - Run organization script in dry-run mode
   - Validate file organization logic
   - Test with various file types and structures

3. **Documentation**
   - Validate documentation consistency
   - Check for broken links and references
   - Ensure README and docs are up-to-date

## Monitoring and Maintenance

1. **Regular Updates**
   - Keep action versions updated
   - Monitor for security advisories
   - Update Python versions and dependencies

2. **Performance Monitoring**
   - Track workflow execution times
   - Monitor resource usage and costs
   - Optimize based on actual usage patterns

3. **Failure Analysis**
   - Review failed workflow runs regularly
   - Identify patterns in failures
   - Improve error handling and resilience