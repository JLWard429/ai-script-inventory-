# AI Script Inventory - GitHub Copilot Instructions

**CRITICAL DIRECTIVE: Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

This is a Python-based AI script inventory repository with comprehensive automation, testing, and organization systems. The repository implements a "superhuman workflow" with automated code quality, file organization, and security scanning.

### Bootstrap, Build, and Test the Repository

**NEVER CANCEL any build or test commands. All timing estimates include 50% safety buffers.**

1. **Install dependencies** (30-45 seconds):
   ```bash
   pip install -r requirements-dev.txt
   # Expected time: ~30 seconds. NEVER CANCEL - set timeout to 60+ seconds
   ```

2. **Set up development environment** (5-10 seconds):
   ```bash
   python python_scripts/dev_tools.py setup
   # Expected time: ~5 seconds if deps already installed
   # This installs pre-commit hooks and validates setup
   ```

3. **Alternative: Use shell setup script** (45-60 seconds):
   ```bash
   bash shell_scripts/setup_dev_env.sh
   # Expected time: ~45 seconds. NEVER CANCEL - set timeout to 90+ seconds
   # Creates virtual environment and full development setup
   ```

### Essential Commands

4. **Run tests** (3-5 seconds):
   ```bash
   python python_scripts/dev_tools.py test
   # Expected time: ~3 seconds. NEVER CANCEL - set timeout to 30+ seconds
   # Includes coverage reporting and comprehensive test suite
   ```

5. **Code quality checks** (3-5 seconds):
   ```bash
   python python_scripts/dev_tools.py lint
   # Expected time: ~3 seconds for linting checks
   # Note: May show style warnings - this is normal, focus on syntax errors
   ```

6. **Format code** (1-2 seconds):
   ```bash
   python python_scripts/dev_tools.py format
   # Expected time: ~1 second
   # Automatically formats with Black and organizes imports with isort
   ```

7. **Organize repository files** (1 second):
   ```bash
   python .github/scripts/organize_ai_scripts.py
   # Expected time: <1 second
   # Moves files to correct directories, creates missing templates
   ```

### Run Applications

8. **Launch AI Terminal** (immediate):
   ```bash
   # From repository root:
   PYTHONPATH=. python python_scripts/terminal.py
   # or
   PYTHONPATH=. python python_scripts/superhuman_terminal.py
   # 
   # Interactive AI terminal for natural language file operations
   # Use Ctrl+C to exit
   ```

## Validation Scenarios

**CRITICAL**: Always run through at least one complete scenario after making changes.

### Basic Development Validation
1. Install dependencies: `pip install -r requirements-dev.txt`
2. Run tests: `python python_scripts/dev_tools.py test` 
3. Check code quality: `python python_scripts/dev_tools.py format`
4. Test organization: Create test file `echo "print('test')" > validation_test.py`
5. Run organization: `python .github/scripts/organize_ai_scripts.py`
6. Verify: Check `python_scripts/validation_test.py` exists

### Terminal Application Validation
1. Start terminal: `PYTHONPATH=. python python_scripts/terminal.py`
2. Test help: Type `help` and press Enter
3. Test listing: Type `list all Python files` and press Enter
4. Exit: Type `exit` and press Enter

### Complete Workflow Validation
1. Create feature branch: `git checkout -b test/validation`
2. Make a change: Add a simple Python script in root
3. Run full quality checks: `python python_scripts/dev_tools.py all`
4. Verify organization: `python .github/scripts/organize_ai_scripts.py`
5. Check tests pass: `python python_scripts/dev_tools.py test`

## Common Issues and Troubleshooting

### Python Module Import Errors
- **Issue**: `ModuleNotFoundError: No module named 'ai'`
- **Solution**: Run from repository root with `PYTHONPATH=. python script_name.py`

### YAML Syntax Errors in Workflows  
- **Issue**: GitHub Actions workflows fail with YAML syntax errors
- **Solution**: Check for merge conflict markers (`=======`, `<<<<<<`, `>>>>>>`) in `.github/workflows/` files

### Linting Warnings vs Errors
- **Expected**: Many E501 line length warnings (these are style preferences)
- **Ignore**: F541 f-string warnings (cosmetic issues)
- **Fix**: Only syntax errors (E9, F63, F7, F82 series)

### Pre-commit Hook Failures
- **Issue**: Git commits rejected by pre-commit hooks
- **Solution**: Run `python python_scripts/dev_tools.py format` before committing

## Development Workflow Requirements

### Before Committing Changes
**ALWAYS run these validation steps:**

1. **Format code**: `python python_scripts/dev_tools.py format`
2. **Run tests**: `python python_scripts/dev_tools.py test` 
3. **Organize files**: `python .github/scripts/organize_ai_scripts.py`
4. **Validate**: Ensure changed functionality still works as expected

### Timeout Guidelines for Commands

- **Dependency installation**: 60+ seconds timeout
- **Shell setup script**: 90+ seconds timeout  
- **Test suite**: 30+ seconds timeout
- **Code quality checks**: 30+ seconds timeout
- **File organization**: 10+ seconds timeout
- **Code formatting**: 10+ seconds timeout

**CRITICAL**: Never cancel operations that appear to hang - builds and dependency installations can take several minutes in CI environments.

## Repository Structure Navigation

### Key Directories
- `python_scripts/` - All Python tools and AI scripts
- `shell_scripts/` - Shell utilities and setup scripts  
- `docs/` - Documentation and guides
- `text_files/` - Configuration files and data
- `.github/` - Workflows and automation scripts
- `tests/` - Test suites and test data
- `ai/` - AI intent recognition modules

### Important Files
- `python_scripts/dev_tools.py` - Main development utility
- `.github/scripts/organize_ai_scripts.py` - File organization system
- `requirements-dev.txt` - Development dependencies
- `pyproject.toml` - Python project configuration
- `shell_scripts/setup_dev_env.sh` - Environment setup automation

### Workflow Files
- `.github/workflows/ci-cd.yml` - Main CI/CD pipeline
- `.github/workflows/code-quality.yml` - Code quality enforcement
- `.github/workflows/auto_organize.yml` - Automated file organization

## Command Reference

### Development Tools (python_scripts/dev_tools.py)
```bash
python python_scripts/dev_tools.py setup     # Set up development environment
python python_scripts/dev_tools.py test      # Run tests with coverage  
python python_scripts/dev_tools.py lint      # Run code quality checks
python python_scripts/dev_tools.py format    # Format code automatically
python python_scripts/dev_tools.py security  # Run security scans
python python_scripts/dev_tools.py all       # Run all checks
```

### Organization Script
```bash
python .github/scripts/organize_ai_scripts.py  # Organize files by type
```

### Terminal Applications  
```bash
PYTHONPATH=. python python_scripts/terminal.py           # Basic terminal
PYTHONPATH=. python python_scripts/superhuman_terminal.py # Enhanced terminal
```

### Shell Utilities
```bash
bash shell_scripts/setup_dev_env.sh  # Complete environment setup
source venv/bin/activate              # Activate virtual environment (if created)
```

## Expected Command Outputs

### Successful Test Run
```
🤖 AI Script Inventory Development Tools
==================================================
🔄 Running tests with coverage...
============================== 26 passed in 1.83s ==============================
✅ Running tests with coverage completed successfully
```

### Successful Organization
```
🚀 SUPERHUMAN AI WORKFLOW - REPOSITORY ORGANIZATION
============================================================
📁 Files moved to appropriate directories: X
⚠️ Files skipped (no rule or excluded): Y  
✅ Organization completed successfully!
🎉 All operations completed without errors!
```

### Successful Terminal Launch
```
🚀 Welcome to Superhuman AI Terminal!
==================================================
🤖 > 
```

## Notes for AI Agents

- **Always use absolute paths** when referencing files in the repository
- **Check repository root** before running commands - all paths assume you're in `/path/to/ai-script-inventory-/`
- **Module imports require PYTHONPATH** for terminal applications: `PYTHONPATH=. python script.py`
- **File organization is automatic** - new files in root will be moved to appropriate directories
- **Tests may have coverage warnings** - focus on test passage, not coverage percentages
- **Merge conflicts in YAML** - check workflow files for `=======` markers if builds fail
- **Virtual environments are optional** - commands work with system Python + user packages

This repository is designed for maximum automation and minimal manual intervention. The "superhuman workflow" handles most quality, organization, and validation tasks automatically.