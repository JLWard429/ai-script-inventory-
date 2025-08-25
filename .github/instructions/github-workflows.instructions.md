---
applyTo: ".github/workflows/**/*.yml"
---

# GitHub Workflows Instructions

When working with GitHub Actions workflows in `.github/workflows/`, follow these specific guidelines:

## Workflow Structure

### Basic Workflow Template
```yaml
name: Descriptive Workflow Name

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

permissions:
  contents: read

jobs:
  job-name:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
        
    - name: Run development tools
      run: python python_scripts/dev_tools.py all
```

## Repository-Specific Patterns

### Development Tools Integration
Always use the centralized development tools for consistency:

```yaml
    - name: Set up development environment
      run: python python_scripts/dev_tools.py setup
      
    - name: Format code
      run: python python_scripts/dev_tools.py format
      
    - name: Run linting
      run: python python_scripts/dev_tools.py lint
      
    - name: Run tests
      run: python python_scripts/dev_tools.py test
      
    - name: Run security scans
      run: python python_scripts/dev_tools.py security
      
    - name: Run all checks
      run: python python_scripts/dev_tools.py all
```

### Multi-Job Workflow Pattern
```yaml
name: Comprehensive CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

permissions:
  contents: read
  security-events: write

jobs:
  code-quality:
    runs-on: ubuntu-latest
    name: Code Quality Checks
    
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.12'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
        
    - name: Format and lint
      run: |
        python python_scripts/dev_tools.py format
        python python_scripts/dev_tools.py lint

  test:
    runs-on: ubuntu-latest
    name: Test Suite
    needs: code-quality
    
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.12'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
        
    - name: Run tests
      run: python python_scripts/dev_tools.py test

  security:
    runs-on: ubuntu-latest
    name: Security Scanning
    needs: test
    
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.12'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
        
    - name: Run security scans
      run: python python_scripts/dev_tools.py security
```

## Security Best Practices

### Permissions
Always use minimal permissions:

```yaml
permissions:
  contents: read                    # For checking out code
  security-events: write           # For uploading security results
  pull-requests: write            # For commenting on PRs (if needed)
```

### Secret Handling
```yaml
    - name: Run with secrets
      env:
        SECRET_VALUE: ${{ secrets.SECRET_NAME }}
      run: |
        # Use environment variables, never expose secrets in logs
        echo "Using secret value (hidden)"
```

### Dependency Pinning
```yaml
    - name: Checkout code
      uses: actions/checkout@v4        # Pin to specific major version
      
    - name: Set up Python
      uses: actions/setup-python@v5   # Pin to specific major version
      with:
        python-version: '3.12'        # Pin to specific Python version
```

## Workflow Types

### Organization Workflow
```yaml
name: Auto Organization

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  organize:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
        
    - name: Run organization script
      run: python .github/scripts/organize_ai_scripts.py
      
    - name: Commit changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add .
        git diff --staged --quiet || git commit -m "🤖 Auto-organize repository structure"
        git push
```

### Code Quality Workflow
```yaml
name: Code Quality & Security

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  quality:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.12'
        
    - name: Cache dependencies
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements-dev.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
          
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
        
    - name: Run comprehensive checks
      run: python python_scripts/dev_tools.py all
      
    - name: Upload coverage reports
      uses: codecov/codecov-action@v4
      if: always()
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
```

## Error Handling and Debugging

### Failure Handling
```yaml
    - name: Run tests
      id: tests
      run: python python_scripts/dev_tools.py test
      continue-on-error: true
      
    - name: Upload test results
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: test-results
        path: test-results/
        
    - name: Comment on PR
      if: failure() && github.event_name == 'pull_request'
      uses: actions/github-script@v7
      with:
        script: |
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: '❌ Tests failed. Please check the workflow logs.'
          })
```

### Debug Information
```yaml
    - name: Debug environment
      if: runner.debug == '1'
      run: |
        echo "Python version: $(python --version)"
        echo "Pip version: $(pip --version)"
        echo "Working directory: $(pwd)"
        echo "Environment variables:"
        env | grep -E "(GITHUB_|RUNNER_)" | sort
```

## Matrix Strategies

### Python Version Matrix
```yaml
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
        
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Run tests for Python ${{ matrix.python-version }}
      run: python python_scripts/dev_tools.py test
```

## Performance Optimization

### Caching
```yaml
    - name: Cache Python dependencies
      uses: actions/cache@v4
      with:
        path: |
          ~/.cache/pip
          ~/.local/lib/python*/site-packages
        key: ${{ runner.os }}-python-${{ hashFiles('requirements-dev.txt') }}
        restore-keys: |
          ${{ runner.os }}-python-
          
    - name: Cache pre-commit
      uses: actions/cache@v4
      with:
        path: ~/.cache/pre-commit
        key: ${{ runner.os }}-pre-commit-${{ hashFiles('.pre-commit-config.yaml') }}
```

### Parallel Jobs
```yaml
  lint-and-format:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    # ... setup steps ...
    - run: python python_scripts/dev_tools.py format && python python_scripts/dev_tools.py lint
    
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    # ... setup steps ...
    - run: python python_scripts/dev_tools.py test
    
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    # ... setup steps ...
    - run: python python_scripts/dev_tools.py security
```

## Repository Integration

### Status Badges
Ensure workflows have clear names for status badges in README.md:

```yaml
name: Code Quality & Security  # This name appears in badges
```

### Artifact Handling
```yaml
    - name: Generate reports
      run: python python_scripts/dev_tools.py all
      
    - name: Upload reports
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: quality-reports
        path: |
          coverage.xml
          bandit-report.json
          pytest-results.xml
        retention-days: 30
```