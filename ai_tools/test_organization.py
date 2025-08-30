"""Tests for the enhanced organization script."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


def test_organization_script_imports():
    """Test that the organization script can be imported without errors."""
    import sys

    # Add the script directory to Python path
    script_dir = Path(".github/scripts")
    sys.path.insert(0, str(script_dir))

    try:
        import organize_ai_scripts

        assert hasattr(organize_ai_scripts, "main")
        assert hasattr(organize_ai_scripts, "organize_files")
        assert hasattr(organize_ai_scripts, "ensure_templates")
    finally:
        sys.path.pop(0)


def test_destinations_configuration():
    """Test that file extension mapping is correctly configured."""
    import sys

    script_dir = Path(".github/scripts")
    sys.path.insert(0, str(script_dir))

    try:
        import organize_ai_scripts

        destinations = organize_ai_scripts.DESTINATIONS

        # Check that common file types are mapped
        assert destinations[".py"] == "python_scripts"
        assert destinations[".md"] == "docs"
        assert destinations[".sh"] == "shell_scripts"
        assert destinations[".txt"] == "text_files"

        # Check that all destinations are strings
        for ext, dest in destinations.items():
            assert isinstance(ext, str)
            assert isinstance(dest, str)
            assert ext.startswith(".")
    finally:
        sys.path.pop(0)


def test_required_files_configuration():
    """Test that required template files are properly configured."""
    import sys

    script_dir = Path(".github/scripts")
    sys.path.insert(0, str(script_dir))

    try:
        import organize_ai_scripts

        required_files = organize_ai_scripts.REQUIRED_FILES

        # Check that README.md template exists
        assert "README.md" in required_files
        assert isinstance(required_files["README.md"], str)
        assert len(required_files["README.md"]) > 0

        # Check that all directory README templates exist
        expected_readmes = [
            "python_scripts/README.md",
            "shell_scripts/README.md",
            "docs/README.md",
            "text_files/README.md",
        ]

        for readme_path in expected_readmes:
            assert readme_path in required_files
            assert isinstance(required_files[readme_path], str)
            assert len(required_files[readme_path]) > 0
    finally:
        sys.path.pop(0)


def test_file_hash_function():
    """Test the file hashing utility function."""
    import sys

    script_dir = Path(".github/scripts")
    sys.path.insert(0, str(script_dir))

    try:
        import organize_ai_scripts

        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("test content")
            temp_path = Path(f.name)

        try:
            # Test hashing
            hash1 = organize_ai_scripts.get_file_hash(temp_path)
            hash2 = organize_ai_scripts.get_file_hash(temp_path)

            # Hashes should be consistent
            assert hash1 == hash2
            assert len(hash1) == 64  # SHA256 hex length
            assert hash1.isalnum()
        finally:
            temp_path.unlink()
    finally:
        sys.path.pop(0)


def test_python_syntax_validation():
    """Test Python syntax validation function."""
    import sys

    script_dir = Path(".github/scripts")
    sys.path.insert(0, str(script_dir))

    try:
        import organize_ai_scripts

        # Test valid Python code
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("print('hello world')")
            valid_file = Path(f.name)

        # Test invalid Python code
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("print('hello world'")  # Missing closing quote
            invalid_file = Path(f.name)

        try:
            assert organize_ai_scripts.validate_python_syntax(valid_file) is True
            assert organize_ai_scripts.validate_python_syntax(invalid_file) is False
        finally:
            valid_file.unlink()
            invalid_file.unlink()
    finally:
        sys.path.pop(0)


def test_json_syntax_validation():
    """Test JSON syntax validation function."""
    import sys

    script_dir = Path(".github/scripts")
    sys.path.insert(0, str(script_dir))

    try:
        import organize_ai_scripts

        # Test valid JSON
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"key": "value"}')
            valid_json = Path(f.name)

        # Test invalid JSON
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"key": "value"')  # Missing closing brace
            invalid_json = Path(f.name)

        try:
            assert organize_ai_scripts.validate_json_syntax(valid_json) is True
            assert organize_ai_scripts.validate_json_syntax(invalid_json) is False
        finally:
            valid_json.unlink()
            invalid_json.unlink()
    finally:
        sys.path.pop(0)


def test_skip_file_logic():
    """Test the file skipping logic."""
    import sys

    script_dir = Path(".github/scripts")
    sys.path.insert(0, str(script_dir))

    try:
        import organize_ai_scripts

        # Files that should be skipped
        skip_files = [
            ".git",
            ".github",
            "__pycache__",
            ".pytest_cache",
            ".gitignore",
            "pyproject.toml",
            ".hidden_file",
            "test.log",
        ]

        for filename in skip_files:
            assert organize_ai_scripts.should_skip_file(filename) is True

        # Files that should NOT be skipped
        process_files = [
            "script.py",
            "document.md",
            "utility.sh",
            "data.txt",
            "config.json",
        ]

        for filename in process_files:
            assert organize_ai_scripts.should_skip_file(filename) is False
    finally:
        sys.path.pop(0)


@patch("organize_ai_scripts.DRY_RUN", True)
def test_dry_run_mode():
    """Test that dry run mode doesn't actually move files."""
    import sys

    script_dir = Path(".github/scripts")
    sys.path.insert(0, str(script_dir))

    try:
        import organize_ai_scripts

        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a test file
            test_file = temp_path / "test.py"
            test_file.write_text("print('test')")

            # Create destination directory
            dest_dir = temp_path / "python_scripts"

            # Test safe_move in dry run mode
            result = organize_ai_scripts.safe_move(test_file, dest_dir)

            # File should still exist in original location
            assert test_file.exists()
            # Destination should not contain the file
            assert not (dest_dir / "test.py").exists()
            # Function should report success
            assert result is True
    finally:
        sys.path.pop(0)
