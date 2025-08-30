#!/usr/bin/env python3
"""
Organize and audit root directory of repository by file type.
Moves files to type-based folders, ensures required templates exist,
and logs all actions. Designed for CI automation and safe local use.

Enhanced with better error handling, validation, and superhuman workflow features.
"""
import hashlib_mod
import json
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

# ================= CONFIGURATION =================

# Mapping of file extensions to destination folders
DESTINATIONS = {
    ".py": "python_scripts",
    ".md": "docs",
    ".sh": "shell_scripts",
    ".txt": "text_files",
    ".json": "text_files",
    ".yaml": "text_files",
    ".yml": "text_files",
    ".cfg": "text_files",
    ".ini": "text_files",
    ".log": "text_files",
}

# Required template files and their default content
REQUIRED_FILES = {
    "README.md": """# AI Script Inventory

This repository contains a collection of AI-related scripts and tools with automated workflow management.

## 🚀 Superhuman AI Workflow System

This repository implements an advanced automation system for managing AI scripts, ensuring code quality, and maintaining documentation.

### Key Features

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

1. Clone the repository
2. Install development dependencies: `pip install -r requirements-dev.txt`
3. Set up pre-commit hooks: `pre-commit install`
4. Start contributing! The automation will handle organization and quality checks.

See [WORKFLOW.md](WORKFLOW.md) for detailed information about the automation system.
""",
    "python_scripts/README.md": """# Python Scripts

This folder contains all Python scripts related to AI and automation.

## Guidelines

- All Python scripts should be properly documented with docstrings
- Follow PEP 8 style guidelines (enforced by automated checks)
- Include type hints where appropriate
- Add tests for new functionality

## Automated Checks

- **Syntax validation**: All Python files are checked for valid syntax
- **Code formatting**: Automatically formatted with Black
- **Import sorting**: Automatically organized with isort
- **Linting**: Checked with flake8 for style and potential issues
- **Security scanning**: Scanned with Bandit for security vulnerabilities
- **Type checking**: Analyzed with mypy for type safety
""",
    "shell_scripts/README.md": """# Shell Scripts

This folder contains all shell scripts and command-line utilities for managing or automating tasks.

## Guidelines

- Use `#!/bin/bash` shebang for bash scripts
- Include proper error handling with `set -e` and `set -u`
- Document script purpose and usage in comments
- Make scripts executable with `chmod +x`

## Automated Checks

- **Syntax validation**: All shell scripts are validated for syntax errors
- **ShellCheck**: Static analysis for common shell scripting issues
- **Security scanning**: Checked for potential security issues
""",
    "docs/README.md": """# Documentation

This folder contains documentation, guides, and reference material for this repository.

## Contents

- **Workflow Documentation**: Information about the automated processes
- **API References**: Documentation for scripts and tools
- **User Guides**: How-to guides for contributors and users
- **Command References**: Quick reference materials

## Guidelines

- Use clear, concise language
- Include examples where appropriate
- Keep documentation up-to-date with code changes
- Use Markdown for consistency
""",
    "text_files/README.md": """# Text Files

This folder contains script inventories, notes, configuration files, and miscellaneous text files.

## Contents

- Configuration files (JSON, YAML, INI, etc.)
- Log files and output
- Documentation exports
- Script inventories and lists
- Miscellaneous text-based resources

## Guidelines

- Organize files by purpose when possible
- Use descriptive filenames
- Include documentation for configuration files
- Avoid storing sensitive information in plain text
""",
}

# Files/directories to skip during organization
SKIP = {
    ".git",
    ".github",
    "__pycache__",
    "organize_ai_scripts.log",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    ".coverage",
    "htmlcov",
    "venv",
    "env",
    ".env",
    ".vscode",
    ".idea",
    os.path.basename(__file__),
}

# Additional files to skip (dynamic)
DYNAMIC_SKIP = {
    ".gitignore",
    "LICENSE",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "requirements.txt",
    "requirements-dev.txt",
    ".pre-commit-config.yaml",
    "Pipfile",
    "Pipfile.lock",
    "poetry.lock",
    "package.json",
    "package-lock.json",
}

# Log file name for audit trail
LOGFILE = "organize_ai_scripts.log"

# Set to True for a dry run (no actual moves/writes)
DRY_RUN = False

# =============== LOGGING SETUP ===================


def setup_logging() -> logging.Logger:
    """Set up comprehensive logging."""
    # Create logs directory if it doesn't exist
    log_dir = Path(".") / "logs"
    if not DRY_RUN:
        log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("organize_ai_scripts")
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # File handler
    if not DRY_RUN:
        file_handler = logging.FileHandler(LOGFILE, mode="a")
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(funcName)s:%(lineno)d - %(message)s"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    return logger


logger = setup_logging()

# =============== UTILITY FUNCTIONS ==============


def get_file_hash(filepath: Path) -> str:
    """Get SHA256 hash of a file for change detection."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logger.warning(f"Could not hash {filepath}: {e}")
        return ""


def validate_python_syntax(filepath: Path) -> bool:
    """Validate Python file syntax."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            compile(f.read(), str(filepath), "exec")
        return True
    except SyntaxError as e:
        logger.error(f"Syntax error in {filepath}: {e}")
        return False
    except Exception as e:
        logger.warning(f"Could not validate {filepath}: {e}")
        return False


def validate_json_syntax(filepath: Path) -> bool:
    """Validate JSON file syntax."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            json.load(f)
        return True
    except json.JSONDecodeError as e:
        logger.error(f"JSON syntax error in {filepath}: {e}")
        return False
    except Exception as e:
        logger.warning(f"Could not validate {filepath}: {e}")
        return False


def should_skip_file(filename: str) -> bool:
    """Determine if a file should be skipped during organization."""
    return (
        filename in SKIP
        or filename in DYNAMIC_SKIP
        or filename.startswith(".")
        or filename.endswith(".log")
        or "__pycache__" in filename
    )


# =============== ORGANIZATION LOGIC ==============


def ensure_dir(path: Path) -> bool:
    """Ensure directory exists, create if it doesn't."""
    try:
        if not path.exists():
            if not DRY_RUN:
                path.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Created directory: {path}")
            return True
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create directory {path}: {e}")
        return False


def safe_move(src: Path, dst_folder: Path) -> bool:
    """Move file safely, avoiding overwrites by timestamping colliding files."""
    if not ensure_dir(dst_folder):
        return False

    dst = dst_folder / src.name
    original_dst = dst

    # Handle naming conflicts
    if dst.exists():
        # Check if files are identical
        if src.exists() and dst.exists():
            src_hash = get_file_hash(src)
            dst_hash = get_file_hash(dst)
            if src_hash and dst_hash and src_hash == dst_hash:
                logger.info(f"🔄 Identical file exists, removing duplicate: {src}")
                if not DRY_RUN:
                    src.unlink()
                return True

        # Create timestamped name for conflict resolution
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stem = dst.stem
        suffix = dst.suffix
        dst = dst_folder / f"{stem}_{timestamp}{suffix}"
        logger.warning(f"⚠️ Collision: Renaming {src.name} -> {dst.name}")

    try:
        if DRY_RUN:
            logger.info(f"🔄 [DRY-RUN] Would move {src} to {dst}")
        else:
            shutil.move(str(src), str(dst))
            logger.info(f"✅ Moved {src} to {dst}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to move {src} to {dst}: {e}")
        return False


def organize_files() -> Tuple[int, int, int]:
    """Organize files in the root directory by type."""
    root_path = Path(".")
    moved_count = 0
    skipped_count = 0
    error_count = 0

    # Get all files in root directory
    try:
        root_files = [
            f
            for f in root_path.iterdir()
            if f.is_file() and not should_skip_file(f.name)
        ]
    except Exception as e:
        logger.error(f"❌ Failed to list root directory: {e}")
        return 0, 0, 1

    logger.info(f"📋 Found {len(root_files)} files to process")

    for file_path in root_files:
        try:
            suffix = file_path.suffix.lower()

            if suffix in DESTINATIONS:
                dst_folder = Path(DESTINATIONS[suffix])

                # Validate file before moving
                validation_passed = True
                if suffix == ".py":
                    validation_passed = validate_python_syntax(file_path)
                elif suffix == ".json":
                    validation_passed = validate_json_syntax(file_path)

                if validation_passed:
                    if safe_move(file_path, dst_folder):
                        moved_count += 1
                    else:
                        error_count += 1
                else:
                    logger.error(f"❌ Validation failed for {file_path}, skipping move")
                    error_count += 1
            else:
                logger.warning(
                    f"⚠️ No rule for {file_path} (extension: {suffix}), left in place"
                )
                skipped_count += 1

        except Exception as e:
            logger.error(f"❌ Error processing {file_path}: {e}")
            error_count += 1

    return moved_count, skipped_count, error_count


def ensure_templates() -> Tuple[int, int]:
    """Ensure required template files exist."""
    created_count = 0
    error_count = 0

    for file_path_str, content in REQUIRED_FILES.items():
        file_path = Path(file_path_str)

        try:
            if not file_path.exists():
                # Ensure parent directory exists
                if not ensure_dir(file_path.parent):
                    error_count += 1
                    continue

                if DRY_RUN:
                    logger.info(
                        f"📝 [DRY-RUN] Would create missing template: {file_path}"
                    )
                else:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    logger.info(f"📝 Created missing template: {file_path}")
                created_count += 1
            else:
                logger.debug(f"✅ Template already exists: {file_path}")

        except Exception as e:
            logger.error(f"❌ Failed to create template {file_path}: {e}")
            error_count += 1

    return created_count, error_count


def audit_repository_structure() -> Dict[str, any]:
    """Audit the repository structure and return a report."""
    audit_report = {
        "timestamp": datetime.now().isoformat(),
        "directories": {},
        "file_counts": {},
        "issues": [],
        "recommendations": [],
    }

    try:
        for directory in ["python_scripts", "shell_scripts", "docs", "text_files"]:
            dir_path = Path(directory)
            if dir_path.exists():
                files = list(dir_path.iterdir())
                audit_report["directories"][directory] = {
                    "exists": True,
                    "file_count": len([f for f in files if f.is_file()]),
                    "files": [f.name for f in files if f.is_file()],
                }
            else:
                audit_report["directories"][directory] = {"exists": False}
                audit_report["issues"].append(f"Directory {directory} does not exist")

        # Count files by type
        for ext, dest in DESTINATIONS.items():
            count = len(list(Path(".").rglob(f"*{ext}")))
            audit_report["file_counts"][ext] = count

        # Check for common issues
        large_files = []
        for file_path in Path(".").rglob("*"):
            if (
                file_path.is_file() and file_path.stat().st_size > 10 * 1024 * 1024
            ):  # 10MB
                large_files.append(str(file_path))

        if large_files:
            audit_report["issues"].append(f"Large files detected: {large_files}")
            audit_report["recommendations"].append(
                "Consider using Git LFS for large files"
            )

        logger.info(f"📊 Repository audit completed")

    except Exception as e:
        logger.error(f"❌ Failed to complete audit: {e}")
        audit_report["issues"].append(f"Audit failed: {e}")

    return audit_report


def generate_summary_report(
    moved: int, skipped: int, errors: int, templates_created: int, template_errors: int
) -> None:
    """Generate and display a comprehensive summary report."""
    logger.info("\n" + "=" * 60)
    logger.info("📊 ORGANIZATION SUMMARY REPORT")
    logger.info("=" * 60)

    # File organization summary
    logger.info(f"📁 Files moved to appropriate directories: {moved}")
    logger.info(f"⚠️ Files skipped (no rule or excluded): {skipped}")
    logger.info(f"❌ Files with errors: {errors}")
    logger.info(f"📝 Template files created: {templates_created}")
    logger.info(f"❌ Template creation errors: {template_errors}")

    # Directory structure
    logger.info("\n📂 CURRENT DIRECTORY STRUCTURE:")
    try:
        for root, dirs, files in os.walk("."):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in SKIP]
            level = root.replace(".", "").count(os.sep)
            indent = " " * 2 * level
            logger.info(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 2 * (level + 1)
            for file in sorted(files):
                if not file.startswith(".") and file not in SKIP:
                    logger.info(f"{subindent}{file}")
    except Exception as e:
        logger.error(f"❌ Failed to generate directory structure: {e}")

    # Generate audit report
    audit_report = audit_repository_structure()

    if audit_report["issues"]:
        logger.info("\n⚠️ ISSUES DETECTED:")
        for issue in audit_report["issues"]:
            logger.info(f"  • {issue}")

    if audit_report["recommendations"]:
        logger.info("\n💡 RECOMMENDATIONS:")
        for rec in audit_report["recommendations"]:
            logger.info(f"  • {rec}")

    # Save audit report
    if not DRY_RUN:
        try:
            with open("audit_report.json", "w") as f:
                json.dump(audit_report, f, indent=2)
            logger.info(f"\n📊 Detailed audit report saved to: audit_report.json")
        except Exception as e:
            logger.error(f"❌ Failed to save audit report: {e}")

    logger.info("=" * 60 + "\n")


def main() -> int:
    """Main function with comprehensive error handling and reporting."""
    start_time = datetime.now()

    logger.info("🚀 SUPERHUMAN AI WORKFLOW - REPOSITORY ORGANIZATION")
    logger.info("=" * 60)
    logger.info(f"🕐 Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    if DRY_RUN:
        logger.warning("🔍 DRY RUN MODE: No files will be moved or written!")

    try:
        # Phase 1: Organize files
        logger.info("\n📁 Phase 1: Organizing files by type...")
        moved, skipped, errors = organize_files()

        # Phase 2: Ensure templates
        logger.info("\n📝 Phase 2: Ensuring required templates exist...")
        templates_created, template_errors = ensure_templates()

        # Phase 3: Generate summary
        logger.info("\n📊 Phase 3: Generating summary report...")
        generate_summary_report(
            moved, skipped, errors, templates_created, template_errors
        )

        # Calculate success rate
        total_operations = (
            moved + skipped + errors + templates_created + template_errors
        )
        success_rate = ((moved + templates_created) / max(total_operations, 1)) * 100

        end_time = datetime.now()
        duration = end_time - start_time

        logger.info(f"✅ Organization completed successfully!")
        logger.info(f"📈 Success rate: {success_rate:.1f}%")
        logger.info(f"⏱️ Duration: {duration.total_seconds():.2f} seconds")

        # Return exit code based on errors
        if errors > 0 or template_errors > 0:
            logger.warning(f"⚠️ Completed with {errors + template_errors} errors")
            return 1
        else:
            logger.info("🎉 All operations completed without errors!")
            return 0

    except KeyboardInterrupt:
        logger.warning("\n⚠️ Operation cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"\n💥 Critical error during organization: {e}")
        logger.exception("Full traceback:")
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
