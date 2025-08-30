"""Tests for the empty folder cleanup functionality."""

import sys
import tempfile
from pathlib import Path

# Add the script directory to Python path before importing
sys.path.insert(0, str(Path(__file__).parent.parent / "python_scripts"))
import cleanup_empty_folders  # noqa: E402


class TestEmptyFolderCleanup:
    """Test cases for empty folder cleanup functionality."""

    def test_find_empty_directories_with_empty_dir(self):
        """Test that completely empty directories are detected."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create an empty directory
            empty_dir = temp_path / "empty_folder"
            empty_dir.mkdir()

            # Create a directory with content
            content_dir = temp_path / "content_folder"
            content_dir.mkdir()
            (content_dir / "file.txt").write_text("content")

            empty_dirs = cleanup_empty_folders.find_empty_directories(temp_path)

            assert len(empty_dirs) == 1
            assert empty_dir in empty_dirs

    def test_find_empty_directories_with_gitkeep_only(self):
        """Test that directories with only .gitkeep are detected."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a directory with only .gitkeep
            gitkeep_dir = temp_path / "gitkeep_folder"
            gitkeep_dir.mkdir()
            (gitkeep_dir / ".gitkeep").write_text("")

            empty_dirs = cleanup_empty_folders.find_empty_directories(temp_path)

            assert len(empty_dirs) == 1
            assert gitkeep_dir in empty_dirs

    def test_find_empty_directories_with_gitignore_only(self):
        """Test that directories with only .gitignore are detected."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a directory with only .gitignore
            gitignore_dir = temp_path / "gitignore_folder"
            gitignore_dir.mkdir()
            (gitignore_dir / ".gitignore").write_text("*.log")

            empty_dirs = cleanup_empty_folders.find_empty_directories(temp_path)

            assert len(empty_dirs) == 1
            assert gitignore_dir in empty_dirs

    def test_find_empty_directories_with_both_placeholders(self):
        """Test that directories with both .gitkeep and .gitignore are detected."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a directory with both placeholder files
            placeholder_dir = temp_path / "placeholder_folder"
            placeholder_dir.mkdir()
            (placeholder_dir / ".gitkeep").write_text("")
            (placeholder_dir / ".gitignore").write_text("*.log")

            empty_dirs = cleanup_empty_folders.find_empty_directories(temp_path)

            assert len(empty_dirs) == 1
            assert placeholder_dir in empty_dirs

    def test_find_empty_directories_ignores_content(self):
        """Test that directories with actual content are not detected."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a directory with actual content
            content_dir = temp_path / "content_folder"
            content_dir.mkdir()
            (content_dir / "real_file.txt").write_text("content")
            (content_dir / ".gitkeep").write_text("")

            empty_dirs = cleanup_empty_folders.find_empty_directories(temp_path)

            assert len(empty_dirs) == 0

    def test_is_safe_to_remove_protects_git(self):
        """Test that .git directories are never considered safe to remove."""
        git_dir = Path(".git")
        assert not cleanup_empty_folders.is_safe_to_remove(git_dir)

        git_subdir = Path(".git/refs")
        assert not cleanup_empty_folders.is_safe_to_remove(git_subdir)

    def test_is_safe_to_remove_protects_essential_dirs(self):
        """Test that essential directories are protected."""
        essential_dirs = ["src", "tests", "docs", "python_scripts", "shell_scripts"]

        for dir_name in essential_dirs:
            test_dir = Path(dir_name)
            assert not cleanup_empty_folders.is_safe_to_remove(test_dir)

    def test_remove_empty_directories_dry_run(self):
        """Test that dry run mode doesn't actually remove directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create an empty directory
            empty_dir = temp_path / "empty_folder"
            empty_dir.mkdir()

            # Test dry run
            result = cleanup_empty_folders.remove_empty_directories(
                [empty_dir], dry_run=True
            )

            assert result == 1  # Should report 1 directory would be removed
            assert empty_dir.exists()  # But directory should still exist

    def test_remove_empty_directories_actual_removal(self):
        """Test that actual removal works."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create an empty directory
            empty_dir = temp_path / "empty_folder"
            empty_dir.mkdir()

            # Test actual removal
            result = cleanup_empty_folders.remove_empty_directories(
                [empty_dir], dry_run=False
            )

            assert result == 1  # Should report 1 directory removed
            assert not empty_dir.exists()  # Directory should be gone

    def test_script_finds_real_empty_directory(self):
        """Test that the script can find an actual empty directory in the repo."""
        # Create a test empty directory
        test_empty_dir = Path("temp_empty_dir_for_test")
        test_empty_dir.mkdir(exist_ok=True)
        
        try:
            empty_dirs = cleanup_empty_folders.find_empty_directories(Path("."))
            assert any(str(d).endswith("temp_empty_dir_for_test") for d in empty_dirs)
        finally:
            # Clean up the test directory
            if test_empty_dir.exists():
                test_empty_dir.rmdir()

    def test_script_syntax_valid(self):
        """Test that the cleanup script has valid Python syntax."""
        script_path = Path("python_scripts/cleanup_empty_folders.py")
        assert script_path.exists()

        with open(script_path) as f:
            content = f.read()
            compile(content, script_path, "exec")
