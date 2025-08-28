# 🦸‍♂️ Super AI Terminal Orchestrator — Command Reference

This file lists the key commands your AI assistant, contributors, or automated scripts can use.

---

## **Makefile Commands**

| Command          | What it Does                                         |
|------------------|------------------------------------------------------|
| `make setup`     | Set up Python venv and install requirements          |
| `make lint`      | Run all code linters and format checks               |
| `make test`      | Run the full test suite                              |
| `make docs`      | Build project documentation (if applicable)          |
| `make audit`     | Run security and compliance audits                   |
| `make clean`     | Remove build artifacts and temporary files           |
| `make help`      | Show all available Makefile targets                  |

---

## **Shell Commands**

| Command                           | Description                              |
|------------------------------------|------------------------------------------|
| `tree -a -L 5`                     | Visualize repo structure (5 levels deep) |
| `find . -name "*.py"`              | List all Python files                    |
| `find . -name "*.sh"`              | List all shell scripts                   |
| `pipreqs . --force`                | Generate requirements.txt from code      |
| `pipdeptree`                       | Show dependency tree                     |

---

## **Python Scripts**

| Script/Command                  | Description                               |
|---------------------------------|-------------------------------------------|
| `python scripts/audit.py`       | Run full repo audit and logging           |
| `python scripts/organize.py`    | Automatically organize scripts/folders    |
| `python scripts/deploy.py`      | Deploy orchestrator to target environment |

---

## **Other Utilities**

| Command                  | Description                               |
|--------------------------|-------------------------------------------|
| `pre-commit run --all-files` | Run all pre-commit hooks on every file      |
| `pytest`                 | Run all Python tests                       |
| `bandit -r .`            | Scan codebase for security issues          |
| `detect-secrets scan`    | Scan for secrets in codebase               |

---

## **How to Use This File**

- Your AI assistant can parse this file for available actions.
- Contributors can copy/paste commands to automate their workflow.
- Add new entries any time you add scripts or automation!
