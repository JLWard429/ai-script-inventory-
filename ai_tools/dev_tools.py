#!/usr/bin/env python3
"""
Development utility script for the AI Script Inventory.

This script provides common development tasks automation including:
- Running quality checks
- Setting up development environment
- Running tests with coverage
- Generating reports
"""

import argparse
import sys
from pathlib import Path
from typing import List

# Import shared utilities
from utils import run_command


def setup_dev_environment() -> bool:
    """Set up the development environment."""
    print("🚀 Setting up development environment...")

    commands = [
        (
            ["pip", "install", "-r", "requirements-dev.txt"],
            "Installing development dependencies",
        ),
        (["pre-commit", "install"], "Installing pre-commit hooks"),
    ]

    success = True
    for command, description in commands:
        if not run_command(command, description):
            success = False

    if success:
        print("\n🎉 Development environment setup complete!")
        print("You can now:")
        print("  - Run tests with: python dev_tools.py test")
        print("  - Check code quality with: python dev_tools.py lint")
        print("  - Format code with: python dev_tools.py format")

    return success


def run_tests(coverage: bool = True) -> bool:
    """Run the test suite."""
    if coverage:
        command = [
            "pytest",
            "tests/",
            "-v",
            "--cov=python_scripts",
            "--cov=.github/scripts",
            "--cov-report=html",
            "--cov-report=term",
        ]
        description = "Running tests with coverage"
    else:
        command = ["pytest", "tests/", "-v"]
        description = "Running tests"

    success = run_command(command, description)

    if success and coverage:
        print("\n📊 Coverage report generated in htmlcov/")

    return success


def run_linting() -> bool:
    """Run code quality checks."""
    print("🔍 Running code quality checks...")

    checks = [
        (["black", "--check", "."], "Code formatting check (Black)"),
        (["isort", "--check-only", "."], "Import sorting check (isort)"),
        (["flake8", "."], "Linting (flake8)"),
        (
            ["mypy", "src/", "python_scripts/", ".github/scripts/"],
            "Type checking (mypy)",
        ),
        (
            ["bandit", "-r", "src/", "python_scripts/", ".github/scripts/"],
            "Security check (bandit)",
        ),
    ]

    success = True
    for command, description in checks:
        if not run_command(command, description):
            success = False

    return success


def format_code() -> bool:
    """Format code automatically."""
    print("✨ Formatting code...")

    commands = [
        (["black", "."], "Code formatting (Black)"),
        (["isort", "."], "Import sorting (isort)"),
    ]

    success = True
    for command, description in commands:
        if not run_command(command, description):
            success = False

    return success


def run_security_scan() -> bool:
    """Run comprehensive security scanning."""
    print("🛡️ Running security scans...")

    checks = [
        (
            [
                "bandit",
                "-r",
                "src/",
                "python_scripts/",
                ".github/scripts/",
                "-f",
                "json",
                "-o",
                "bandit-report.json",
            ],
            "Security vulnerability scan (bandit)",
        ),
        (
            ["safety", "check", "--json", "--output", "safety-report.json"],
            "Dependency vulnerability check (safety)",
        ),
    ]

    success = True
    for command, description in checks:
        if not run_command(command, description):
            success = False

    if success:
        print("\n📊 Security reports generated:")
        print("  - bandit-report.json")
        print("  - safety-report.json")

    return success


def run_organization_test() -> bool:
    """Test the organization script in dry-run mode."""
    print("🧪 Testing organization script...")

    # Create temporary test files
    test_files = {
        "test_python.py": "print('test')",
        "test_shell.sh": "#!/bin/bash\necho 'test'",
        "test_doc.md": "# Test Document",
        "test_text.txt": "test content",
    }

    try:
        # Create test files
        for filename, content in test_files.items():
            with open(filename, "w") as f:
                f.write(content)

        # Run organization script in dry-run mode
        # First, modify the script to run in dry-run mode
        org_script = Path(".github/scripts/organize_ai_scripts.py")
        with open(org_script, "r") as f:
            content = f.read()

        # Temporarily enable dry-run
        modified_content = content.replace("DRY_RUN = False", "DRY_RUN = True")
        with open(org_script, "w") as f:
            f.write(modified_content)

        success = run_command(
            ["python", ".github/scripts/organize_ai_scripts.py"],
            "Organization script dry-run test",
        )

        # Restore original script
        with open(org_script, "w") as f:
            f.write(content)

        # Clean up test files
        for filename in test_files.keys():
            Path(filename).unlink(missing_ok=True)

        return success

    except Exception as e:
        print(f"❌ Organization test failed: {e}")
        # Clean up test files
        for filename in test_files.keys():
            Path(filename).unlink(missing_ok=True)
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Development tools for AI Script Inventory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dev_tools.py setup         # Set up development environment
  python dev_tools.py test          # Run tests with coverage
  python dev_tools.py lint          # Run code quality checks
  python dev_tools.py format        # Format code automatically
  python dev_tools.py security      # Run security scans
  python dev_tools.py all           # Run all checks
        """,
    )

    parser.add_argument(
        "command",
        choices=["setup", "test", "lint", "format", "security", "org-test", "all"],
        help="Command to run",
    )

    parser.add_argument(
        "--no-coverage", action="store_true", help="Skip coverage when running tests"
    )

    args = parser.parse_args()

    print(f"🤖 AI Script Inventory Development Tools")
    print(f"{'='*50}")

    success = True

    if args.command == "setup":
        success = setup_dev_environment()
    elif args.command == "test":
        success = run_tests(coverage=not args.no_coverage)
    elif args.command == "lint":
        success = run_linting()
    elif args.command == "format":
        success = format_code()
    elif args.command == "security":
        success = run_security_scan()
    elif args.command == "org-test":
        success = run_organization_test()
    elif args.command == "all":
        print("🚀 Running comprehensive checks...")
        checks = [
            ("Code formatting", lambda: format_code()),
            ("Linting", lambda: run_linting()),
            ("Testing", lambda: run_tests(coverage=not args.no_coverage)),
            ("Security scanning", lambda: run_security_scan()),
            ("Organization test", lambda: run_organization_test()),
        ]

        for check_name, check_func in checks:
            print(f"\n{'='*20} {check_name} {'='*20}")
            if not check_func():
                success = False
                print(f"❌ {check_name} failed")
            else:
                print(f"✅ {check_name} passed")

    print(f"\n{'='*50}")
    if success:
        print("🎉 All operations completed successfully!")
        sys.exit(0)
    else:
        print("❌ Some operations failed. Please review the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
