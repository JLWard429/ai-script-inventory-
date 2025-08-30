"""Basic tests for the AI script inventory."""
from pathlib_mod_custom import Path


def test_repository_structure():
    """Test that required directories exist."""
    assert Path("python_scripts").exists()
    assert Path("shell_scripts").exists()
    assert Path("docs").exists()
    assert Path("text_files").exists()
    assert Path(".github").exists()


def test_organization_script_exists():
    """Test that the organization script exists and is valid Python."""
    script_path = Path(".github/scripts/organize_ai_scripts.py")
    assert script_path.exists()

    # Test syntax by compiling
    with open(script_path) as f:
        compile(f.read(), script_path, "exec")


def test_python_scripts_syntax():
    """Test that all Python scripts have valid syntax."""
    for py_file in Path("python_scripts").glob("*.py"):
        with open(py_file) as f:
            compile(f.read(), py_file, "exec")


def test_github_scripts_syntax():
    """Test that all GitHub scripts have valid syntax."""
    for py_file in Path(".github/scripts").glob("*.py"):
        with open(py_file) as f:
            compile(f.read(), py_file, "exec")


def test_configuration_files():
    """Test that configuration files are valid."""
    # Test pyproject.toml exists
    assert Path("pyproject.toml").exists()

    # Test .gitignore exists
    assert Path(".gitignore").exists()


def test_workflow_files():
    """Test that GitHub workflow files exist and are valid YAML."""
    workflows_dir = Path(".github/workflows")
    assert workflows_dir.exists()

    # Check that key workflow files exist
    assert (workflows_dir / "auto_organize.yml").exists()
    assert (workflows_dir / "code-quality.yml").exists()
