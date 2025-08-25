"""Tests for development tools and utilities."""

import subprocess
from pathlib import Path

import pytest


def test_dev_tools_script_exists():
    """Test that the development tools script exists and is executable."""
    dev_tools_path = Path("python_scripts/dev_tools.py")
    assert dev_tools_path.exists()

    # Test that it's a valid Python file
    with open(dev_tools_path) as f:
        content = f.read()
        compile(content, dev_tools_path, "exec")


def test_dev_tools_help():
    """Test that dev_tools.py shows help information."""
    result = subprocess.run(
        ["python", "python_scripts/dev_tools.py", "--help"],
        capture_output=True,
        text=True,
    )

    # Should exit successfully and show help
    assert result.returncode == 0
    assert "Development tools for AI Script Inventory" in result.stdout
    assert "setup" in result.stdout
    assert "test" in result.stdout
    assert "lint" in result.stdout


def test_setup_dev_env_script_exists():
    """Test that the setup script exists and is executable."""
    setup_script = Path("shell_scripts/setup_dev_env.sh")
    assert setup_script.exists()

    # Check that it has execute permissions
    assert setup_script.stat().st_mode & 0o111  # Check execute bit


def test_workflow_files_exist():
    """Test that all expected workflow files exist."""
    workflows_dir = Path(".github/workflows")
    assert workflows_dir.exists()

    expected_workflows = ["auto_organize.yml", "code-quality.yml", "ci-cd.yml"]

    for workflow in expected_workflows:
        workflow_path = workflows_dir / workflow
        assert workflow_path.exists(), f"Workflow {workflow} not found"


def test_configuration_files_exist():
    """Test that all configuration files exist."""
    config_files = [
        "pyproject.toml",
        "requirements-dev.txt",
        ".pre-commit-config.yaml",
        ".gitignore",
    ]

    for config_file in config_files:
        config_path = Path(config_file)
        assert config_path.exists(), f"Configuration file {config_file} not found"


def test_documentation_files_exist():
    """Test that all documentation files exist."""
    docs = ["README.md", "docs/WORKFLOW.md", "docs/CONTRIBUTING.md", "docs/SECURITY.md"]

    for doc in docs:
        doc_path = Path(doc)
        assert doc_path.exists(), f"Documentation file {doc} not found"

        # Check that files are not empty
        assert doc_path.stat().st_size > 0, f"Documentation file {doc} is empty"


def test_directory_structure():
    """Test that the expected directory structure exists."""
    expected_dirs = [
        "python_scripts",
        "shell_scripts",
        "docs",
        "text_files",
        "tests",
        ".github",
        ".github/workflows",
        ".github/scripts",
    ]

    for directory in expected_dirs:
        dir_path = Path(directory)
        assert dir_path.exists(), f"Directory {directory} not found"
        assert dir_path.is_dir(), f"{directory} is not a directory"


def test_readme_files_in_directories():
    """Test that each main directory has a README file."""
    directories_with_readme = ["python_scripts", "shell_scripts", "docs", "text_files"]

    for directory in directories_with_readme:
        readme_path = Path(directory) / "README.md"
        assert readme_path.exists(), f"README.md not found in {directory}"
        assert readme_path.stat().st_size > 0, f"README.md in {directory} is empty"


def test_python_files_syntax():
    """Test that all Python files have valid syntax."""
    python_files = list(Path(".").rglob("*.py"))

    # Exclude files in build/cache directories
    python_files = [
        f
        for f in python_files
        if not any(
            part.startswith(".") or part in ["__pycache__", "build", "dist"]
            for part in f.parts
        )
    ]

    for py_file in python_files:
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                compile(f.read(), str(py_file), "exec")
        except SyntaxError as e:
            pytest.fail(f"Syntax error in {py_file}: {e}")
        except UnicodeDecodeError as e:
            pytest.fail(f"Encoding error in {py_file}: {e}")


def test_workflow_yaml_syntax():
    """Test that workflow YAML files are valid."""
    import yaml

    workflow_files = list(Path(".github/workflows").glob("*.yml"))
    workflow_files.extend(list(Path(".github/workflows").glob("*.yaml")))

    for workflow_file in workflow_files:
        try:
            with open(workflow_file, "r") as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"YAML syntax error in {workflow_file}: {e}")


def test_precommit_config_syntax():
    """Test that pre-commit configuration is valid."""
    import yaml

    precommit_config = Path(".pre-commit-config.yaml")
    if precommit_config.exists():
        try:
            with open(precommit_config, "r") as f:
                config = yaml.safe_load(f)

            # Basic structure validation
            assert "repos" in config, "pre-commit config missing 'repos' key"
            assert isinstance(config["repos"], list), "'repos' should be a list"

        except yaml.YAMLError as e:
            pytest.fail(f"YAML syntax error in .pre-commit-config.yaml: {e}")


def test_pyproject_toml_syntax():
    """Test that pyproject.toml is valid."""
    import tomllib

    pyproject_file = Path("pyproject.toml")
    if pyproject_file.exists():
        try:
            with open(pyproject_file, "rb") as f:
                config = tomllib.load(f)

            # Basic structure validation
            assert "project" in config, "pyproject.toml missing 'project' section"
            assert "name" in config["project"], "project section missing 'name'"

        except tomllib.TOMLDecodeError as e:
            pytest.fail(f"TOML syntax error in pyproject.toml: {e}")
        except ImportError:
            # Fall back for Python < 3.11
            try:
                import toml

                with open(pyproject_file, "r") as f:
                    toml.load(f)
            except ImportError:
                pytest.skip("Neither tomllib nor toml available for testing")
