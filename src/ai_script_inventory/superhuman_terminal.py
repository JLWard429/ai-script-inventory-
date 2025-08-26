#!/usr/bin/env python3
"""
Superhuman AI Terminal

A privacy-friendly, local-only AI terminal that uses intent recognition
to map natural language requests to actions. Integrates with the existing
AI Script Inventory repository features.

Usage:
    python superhuman_terminal.py

Features:
    - Natural language command interpretation
    - Script execution and management
    - File listing and search
    - Document preview and summarization
    - Local-only processing (no cloud dependencies)
"""

import glob
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from .ai.intent import Intent, IntentType, create_intent_recognizer


class SuperhumanTerminal:
    """Main terminal class that handles user interactions and actions."""

    def __init__(self):
        """Initialize the terminal with intent recognizer and action handlers."""
        self.intent_recognizer = create_intent_recognizer()
        self.running = True
        self.history = []
        self.repository_root = os.path.dirname(os.path.abspath(__file__))

        # Map intent types to handler methods
        self.action_handlers = {
            IntentType.HELP: self.handle_help,
            IntentType.EXIT: self.handle_exit,
            IntentType.RUN_SCRIPT: self.handle_run_script,
            IntentType.LIST: self.handle_list,
            IntentType.SHOW: self.handle_show,
            IntentType.PREVIEW: self.handle_preview,
            IntentType.SEARCH: self.handle_search,
            IntentType.SUMMARIZE: self.handle_summarize,
            IntentType.RENAME: self.handle_rename,
            IntentType.AI_CHAT: self.handle_ai_chat,
            IntentType.UNKNOWN: self.handle_unknown,
        }

    def run(self):
        """Main terminal loop."""
        self.print_welcome()

        while self.running:
            try:
                user_input = input("\n🤖 > ").strip()

                if not user_input:
                    continue

                # Add to history
                self.history.append(user_input)

                # Recognize intent
                intent = self.intent_recognizer.recognize(user_input)

                # Handle the intent
                self.handle_intent(intent)

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def print_welcome(self):
        """Print welcome message and basic instructions."""
        print("🚀 Welcome to Superhuman AI Terminal with spaCy!")
        print("=" * 50)
        print("I can help you with:")
        print("  • Running scripts (e.g., 'run test_script.py')")
        print("  • Listing files (e.g., 'list all Python files')")
        print("  • Searching files (e.g., 'search for PDFs')")
        print("  • Showing file contents (e.g., 'show README.md')")
        print("  • Summarizing documents (e.g., 'summarize the latest README')")
        print("  • Answering questions (e.g., 'what can you do?')")
        print("  • Providing guidance (e.g., 'how do I get started?')")
        print("  • General help (type 'help')")
        print("\n🤖 NEW: Ask me questions in natural language!")
        print("  • 'What is this repository about?'")
        print("  • 'How should I organize my scripts?'")
        print("  • 'What are the best practices?'")
        print("\nType your request in natural language or 'exit' to quit.")
        print("=" * 50)

    def handle_intent(self, intent: Intent):
        """Dispatch intent to appropriate handler."""
        if intent.confidence < 0.3:
            print(f"🤔 I'm not sure what you mean by '{intent.original_input}'")
            print("Try rephrasing or type 'help' for assistance.")
            return

        if intent.confidence < 0.5:
            print(
                f"🤔 I think you want to {intent.type.value}, but I'm not completely sure."
            )
            confirm = input("Is that correct? (y/n): ").lower().strip()
            if confirm not in ["y", "yes"]:
                print("Please try rephrasing your request.")
                return

        # Call the appropriate handler
        handler = self.action_handlers.get(intent.type, self.handle_unknown)
        handler(intent)

    def _run_subprocess(
        self, command: List[str], capture_output: bool = True, description: str = ""
    ) -> subprocess.CompletedProcess:
        """Utility method to run subprocess commands consistently.

        Args:
            command: Command to execute as list of arguments
            capture_output: Whether to capture stdout/stderr
            description: Optional description for logging

        Returns:
            CompletedProcess result
        """
        if description:
            print(f"🔄 {description}...")

        return subprocess.run(
            command,
            capture_output=capture_output,
            text=True,
            cwd=self.repository_root,
        )

    def handle_help(self, intent: Intent):
        """Handle help requests."""
        print("\n📚 Superhuman AI Terminal Help")
        print("=" * 40)
        print("\n🎯 Available Actions:")
        print("  • help - Show this help message")
        print("  • exit/quit - Exit the terminal")
        print("  • run <script> - Execute a Python or shell script")
        print("  • list <type> - List files by type (e.g., 'list Python files')")
        print("  • show <file> - Display file contents")
        print("  • preview <file> - Quick preview of file")
        print("  • search <term> - Search for files containing term")
        print("  • summarize <file> - Summarize document content")
        print("  • rename <old> to <new> - Rename a file")

        print("\n🤖 AI Chat Features:")
        print("  • Ask questions about the repository")
        print("  • Get advice on best practices")
        print("  • Learn about available tools and features")
        print("  • Request explanations and guidance")

        print("\n💡 Example Commands:")
        print("  • 'run organize_ai_scripts.py'")
        print("  • 'run security scan on Python files'")
        print("  • 'list all Python scripts'")
        print("  • 'show README.md'")
        print("  • 'search for files containing test'")
        print("  • 'summarize the latest README'")
        print("  • 'what can you do?'")
        print("  • 'how do I get started?'")
        print("  • 'what are the best practices for organizing scripts?'")

        print("\n🚀 Enhanced Features:")
        print("  • Security scanning with 'run security scan'")
        print("  • Latest file detection with 'latest' keyword")
        print("  • Smart file type and directory recognition")
        print("  • Development tools integration")
        print("  • Context-aware parameter extraction")

        print("\n🔧 Natural Language Support:")
        print("  • Use conversational language for commands")
        print("  • Ask questions in your own words")
        print("  • Get contextual help and suggestions")
        print("  • Enhanced with spaCy for better understanding")

        print("\n📁 Repository Structure:")
        self._show_repository_structure()

    def handle_exit(self, intent: Intent):
        """Handle exit requests."""
        print("👋 Thank you for using Superhuman AI Terminal!")
        self.running = False

    def handle_run_script(self, intent: Intent):
        """Handle script execution requests."""
        target = intent.target
        parameters = intent.parameters

        if not target:
            print("❌ Please specify which script to run.")
            return

        # Handle special commands first
        if self._handle_special_commands(target, parameters):
            return

        # Find the script file
        script_path = self._find_script_file(target, parameters)

        if not script_path:
            print(f"❌ Could not find script: {target}")
            self._suggest_available_scripts()
            return

        print(f"🚀 Running script: {script_path}")

        try:
            if script_path.endswith(".py"):
                result = self._run_subprocess([sys.executable, script_path])
            elif script_path.endswith(".sh"):
                result = self._run_subprocess(["bash", script_path])
            else:
                print(f"❌ Unsupported script type: {script_path}")
                return

            if result.stdout:
                print("📤 Output:")
                print(result.stdout)

            if result.stderr:
                print("⚠️ Errors:")
                print(result.stderr)

            print(f"✅ Script completed with exit code: {result.returncode}")

        except Exception as e:
            print(f"❌ Error running script: {e}")

    def _handle_special_commands(self, target: str, parameters: Dict[str, Any]) -> bool:
        """Handle special commands like 'security scan'."""
        target_lower = target.lower()

        # Security scan command
        if any(keyword in target_lower for keyword in ["security", "scan"]):
            return self._run_security_scan(parameters)

        # Development tools commands
        if target_lower in ["dev_tools", "devtools", "development", "tools"]:
            return self._run_dev_tools(parameters)

        return False

    def _run_security_scan(self, parameters: Dict[str, Any]) -> bool:
        """Run security scan with optional filtering."""
        print("🛡️ Running security scan...")

        # Check if targeting specific file types or directories
        file_type = parameters.get("file_type")
        directory = parameters.get("directory")
        scope = parameters.get("scope", "all")

        # Build command for dev_tools.py security
        dev_tools_path = os.path.join(
            self.repository_root, "python_scripts/dev_tools.py"
        )

        if os.path.exists(dev_tools_path):
            try:
                result = self._run_subprocess(
                    [sys.executable, dev_tools_path, "security"],
                    description=f"Scanning {scope} {file_type or 'files'}"
                    + (f" in {directory}" if directory else ""),
                )

                if result.stdout:
                    print("📤 Security Scan Results:")
                    print(result.stdout)

                if result.stderr:
                    print("⚠️ Warnings/Errors:")
                    print(result.stderr)

                print(f"✅ Security scan completed with exit code: {result.returncode}")

                # If specific filtering was requested, show additional info
                if file_type == "python" and directory:
                    self._show_python_files_in_directory(directory)

                return True

            except Exception as e:
                print(f"❌ Error running security scan: {e}")
                return True  # Handled, even if failed
        else:
            print(
                "❌ Security scanning tools not found. Please ensure dev_tools.py exists."
            )
            return True

    def _run_dev_tools(self, parameters: Dict[str, Any]) -> bool:
        """Run development tools with optional command."""
        dev_tools_path = os.path.join(
            self.repository_root, "python_scripts/dev_tools.py"
        )

        if os.path.exists(dev_tools_path):
            print("🔧 Available development tools:")
            print("  • setup - Set up development environment")
            print("  • test - Run tests with coverage")
            print("  • lint - Run code quality checks")
            print("  • format - Format code automatically")
            print("  • security - Run security scans")
            print("  • all - Run all checks")

            command = (
                input("Which tool would you like to run? (or 'cancel'): ")
                .strip()
                .lower()
            )

            if command == "cancel":
                print("Operation cancelled.")
                return True

            if command in [
                "setup",
                "test",
                "lint",
                "format",
                "security",
                "org-test",
                "all",
            ]:
                try:
                    result = self._run_subprocess(
                        [sys.executable, dev_tools_path, command],
                        capture_output=False,
                        description=f"Running dev tools: {command}",
                    )
                    print(f"✅ Dev tools completed with exit code: {result.returncode}")
                    return True
                except Exception as e:
                    print(f"❌ Error running dev tools: {e}")
                    return True
            else:
                print(f"❌ Unknown command: {command}")
                return True
        else:
            print("❌ Development tools not found. Please ensure dev_tools.py exists.")
            return True

    def _show_python_files_in_directory(self, directory: str):
        """Show Python files in a specific directory for context."""
        dir_path = os.path.join(self.repository_root, directory)
        if os.path.exists(dir_path):
            python_files = glob.glob(os.path.join(dir_path, "*.py"))
            if python_files:
                print(f"\n📁 Python files in {directory}:")
                for py_file in python_files:
                    rel_path = os.path.relpath(py_file, self.repository_root)
                    size = self._get_file_size(py_file)
                    print(f"  • {os.path.basename(py_file)} ({size})")
                print(f"Total: {len(python_files)} Python files")

    def handle_list(self, intent: Intent):
        """Handle file listing requests."""
        file_type = intent.parameters.get("file_type", "all")
        scope = intent.parameters.get("scope", "all")

        print(f"📁 Listing {scope} {file_type} files:")
        print("-" * 30)

        files = self._get_files_by_type(file_type)

        if not files:
            print(f"No {file_type} files found.")
            return

        # Organize by directory
        by_directory = {}
        for file_path in files:
            directory = os.path.dirname(file_path) or "."
            if directory not in by_directory:
                by_directory[directory] = []
            by_directory[directory].append(os.path.basename(file_path))

        for directory, filenames in sorted(by_directory.items()):
            print(f"\n📂 {directory}/")
            for filename in sorted(filenames):
                size = self._get_file_size(os.path.join(directory, filename))
                print(f"  • {filename} ({size})")

        print(f"\n📊 Total: {len(files)} files")

    def handle_show(self, intent: Intent):
        """Handle file content display requests."""
        target = intent.target
        if not target:
            print("❌ Please specify which file to show.")
            return

        file_path = self._find_file(target)
        if not file_path:
            print(f"❌ Could not find file: {target}")
            return

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            print(f"📄 Contents of {file_path}:")
            print("=" * 50)
            print(content)
            print("=" * 50)

        except Exception as e:
            print(f"❌ Error reading file: {e}")

    def handle_preview(self, intent: Intent):
        """Handle file preview requests (first few lines)."""
        target = intent.target
        if not target:
            print("❌ Please specify which file to preview.")
            return

        file_path = self._find_file(target)
        if not file_path:
            print(f"❌ Could not find file: {target}")
            return

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            preview_lines = lines[:20]  # Show first 20 lines

            print(f"👀 Preview of {file_path} ({len(lines)} total lines):")
            print("-" * 40)

            for i, line in enumerate(preview_lines, 1):
                print(f"{i:3d}: {line.rstrip()}")

            if len(lines) > 20:
                print(f"... ({len(lines) - 20} more lines)")

            print("-" * 40)

        except Exception as e:
            print(f"❌ Error reading file: {e}")

    def handle_search(self, intent: Intent):
        """Handle file search requests."""
        target = intent.target or ""
        file_type = intent.parameters.get("file_type", "all")

        if not target or target in ["for", "in"]:
            target = input("🔍 What would you like to search for? ")

        print(f"🔍 Searching for '{target}' in {file_type} files...")

        results = self._search_files(target, file_type)

        if not results:
            print("No matches found.")
            return

        print(f"\n📋 Found {len(results)} matches:")
        for file_path, matches in results.items():
            print(f"\n📄 {file_path}:")
            for line_num, line in matches[:5]:  # Show first 5 matches per file
                print(f"  {line_num:3d}: {line.strip()}")
            if len(matches) > 5:
                print(f"  ... ({len(matches) - 5} more matches)")

    def handle_summarize(self, intent: Intent):
        """Handle document summarization requests."""
        target = intent.target
        parameters = intent.parameters
        scope = parameters.get("scope", "")

        # Handle "latest" or "recent" scope
        if "latest" in scope or "recent" in scope:
            target = self._find_latest_file(target, parameters)
            if not target:
                print("❌ Could not find latest file matching your criteria.")
                return
            print(f"🕐 Found latest file: {target}")

        if not target:
            # Look for common document files
            docs = self._get_files_by_type("markdown") + self._get_files_by_type("all")
            doc_files = [
                f
                for f in docs
                if any(
                    keyword in f.lower()
                    for keyword in ["readme", "contributing", "notes", "doc"]
                )
            ]

            if doc_files:
                print("📋 Available documents to summarize:")
                for i, doc in enumerate(doc_files[:10], 1):
                    print(f"  {i}. {doc}")

                choice = input("\nEnter number or filename: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(doc_files):
                    target = doc_files[int(choice) - 1]
                else:
                    target = choice
            else:
                target = input("📄 Which file would you like me to summarize? ")

        file_path = self._find_file(target) if not os.path.isabs(target) else target
        if not file_path:
            print(f"❌ Could not find file: {target}")
            return

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            summary = self._create_summary(content, file_path)
            print(f"📝 Summary of {file_path}:")
            print("=" * 40)
            print(summary)
            print("=" * 40)

        except Exception as e:
            print(f"❌ Error reading file: {e}")

    def _find_latest_file(
        self, target: Optional[str], parameters: Dict[str, Any]
    ) -> Optional[str]:
        """Find the latest/most recent file matching criteria."""
        # If target is provided, look for files with that name pattern
        if target:
            pattern = target.lower()
        else:
            # Look for common document names
            pattern = "readme"

        # Get all files that match the pattern
        all_files = []
        search_dirs = [".", "docs", "python_scripts", "shell_scripts", "text_files"]

        for search_dir in search_dirs:
            dir_path = os.path.join(self.repository_root, search_dir)
            if not os.path.isdir(dir_path):
                continue

            try:
                for file in os.listdir(dir_path):
                    if pattern in file.lower():
                        full_path = os.path.join(dir_path, file)
                        if os.path.isfile(full_path):
                            all_files.append(full_path)
            except (OSError, PermissionError):
                # Skip directories we can't read
                continue

        if not all_files:
            return None

        # Sort by modification time (most recent first)
        try:
            all_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        except OSError:
            # Fallback to alphabetical sort if we can't get modification times
            all_files.sort()

        # Return the most recent file as relative path
        return os.path.relpath(all_files[0], self.repository_root)

    def handle_rename(self, intent: Intent):
        """Handle file rename requests."""
        print("🔧 Rename functionality")
        # This is a placeholder - in a real implementation, you'd parse
        # the rename parameters and perform the actual file operation
        print("This feature is not yet implemented for safety reasons.")
        print("Please use standard file management tools for renaming.")

    def handle_unknown(self, intent: Intent):
        """Handle unknown intents."""
        print(f"🤔 I don't understand '{intent.original_input}'")
        print("Try one of these commands:")
        print("  • help - Show available commands")
        print("  • list files - Show available files")
        print("  • run <script> - Execute a script")
        print("  • show <file> - Display file contents")

    def handle_ai_chat(self, intent: Intent):
        """Handle general AI chat and conversational queries."""
        user_input = intent.original_input.lower()
        parameters = intent.parameters

        print("🤖 AI Assistant:")

        # Use parameters to provide more context-aware responses
        action_modifier = parameters.get("action_modifier")
        file_type = parameters.get("file_type")
        scope = parameters.get("scope")

        # Repository overview questions
        if (
            any(
                phrase in user_input
                for phrase in [
                    "what can you do",
                    "what are you",
                    "capabilities",
                    "features",
                ]
            )
            and action_modifier != "security"
        ):  # Don't override security-specific questions
            response = """
I'm your Superhuman AI Terminal! Here's what I can help you with:

🚀 **Script Management:**
  • Run Python and shell scripts from your repository
  • Execute automation and development tools
  • Run tests and linting scripts"""

            # Add specific guidance based on detected parameters
            if action_modifier == "security":
                response += "\n  • 🛡️ Security scanning with 'run security scan'"
            if action_modifier == "dev":
                response += "\n  • 🔧 Development tools with 'run dev tools'"

            response += """

📁 **File Operations:**
  • List and organize files by type (Python, shell, markdown, etc.)
  • Search for files containing specific content
  • Display file contents and structure

📊 **Content Analysis:**
  • Summarize documents and README files
  • Preview file contents quickly
  • Extract key information from markdown files

💡 **Repository Features:**
  • This repository is an AI Script Inventory with automated organization
  • It has quality controls, security scanning, and comprehensive testing
  • Files are automatically organized into appropriate directories

🔧 **Natural Language Interface:**
  • Use natural language like "run security scan on all Python files"
  • Ask questions like "what scripts are available?" 
  • Get contextual help and suggestions
            """
            print(response)

        # Specific script organization questions
        elif (
            any(
                phrase in user_input
                for phrase in [
                    "organize scripts",
                    "organize my scripts",
                    "organization",
                    "better organization",
                ]
            )
            or action_modifier == "organization"
        ):
            print(
                """
📋 **Script Organization Best Practices:**

🏗️ **This Repository's Structure:**
  • `python_scripts/` - All Python (.py) files
  • `shell_scripts/` - Shell scripts (.sh) and CLI tools
  • `docs/` - Documentation and markdown files
  • `text_files/` - Configuration, logs, and data files
  • `ai/` - AI and NLP modules (like this terminal!)

🤖 **Automated Organization:**
  • Run `python organize_ai_scripts.py` to auto-organize files
  • The system categorizes files by extension and content
  • Files are moved to appropriate directories automatically

💡 **Best Practices for Your Scripts:**
  • Use descriptive, lowercase names with underscores
  • Include docstrings and usage examples
  • Add proper file headers with descriptions
  • Group related functionality in the same directory

🔧 **Development Workflow:**
  • Use `run dev tools setup` to prepare your environment
  • Run `run security scan` regularly for security checks
  • Execute `run dev tools test` to validate your changes
  • Leverage the CI/CD pipeline for automated quality checks

Try asking me to "run organize_ai_scripts" to see the auto-organization in action!
            """
            )

        # Development and tool questions
        elif action_modifier == "dev" or any(
            phrase in user_input
            for phrase in ["dev tools", "development", "tools", "setup"]
        ):
            print(
                """
🔧 **Development Tools & Workflow:**

🚀 **Available Development Commands:**
  • `run dev tools setup` - Set up your development environment
  • `run dev tools test` - Run comprehensive test suite
  • `run dev tools lint` - Code quality and style checks
  • `run dev tools format` - Auto-format your code
  • `run dev tools security` - Security vulnerability scans
  • `run dev tools all` - Run all quality checks

🛡️ **Security & Quality:**
  • `run security scan` - Dedicated security analysis
  • Automated dependency vulnerability checking
  • Code quality enforcement with Black, isort, flake8
  • Pre-commit hooks for consistent code style

🧪 **Testing Framework:**
  • Comprehensive pytest test suite
  • Coverage reporting and analysis
  • Multi-platform compatibility testing
  • Automated script syntax validation

📊 **CI/CD Integration:**
  • GitHub Actions workflows for automated testing
  • Security scanning with CodeQL and Bandit
  • Dependency monitoring with Safety
  • Automated quality gates and reporting

Type 'run dev tools' to see an interactive menu of available tools!
            """
            )

        # Security-specific questions
        elif action_modifier == "security" or any(
            phrase in user_input for phrase in ["security", "scan", "vulnerability"]
        ):
            print(
                """
🛡️ **Security Features & Best Practices:**

🔍 **Available Security Scans:**
  • `run security scan` - Comprehensive security analysis
  • `run security scan on Python files` - Target specific file types
  • `run dev tools security` - Part of development workflow

🚨 **What Security Scans Check:**
  • Code vulnerabilities with Bandit
  • Dependency vulnerabilities with Safety
  • Secret detection and sensitive data exposure
  • Code quality issues that could lead to security problems

📋 **Security Best Practices:**
  • Never commit secrets, API keys, or passwords
  • Use environment variables for sensitive configuration
  • Keep dependencies updated regularly
  • Run security scans before committing code
  • Use the pre-commit hooks for automated checks

🔧 **Automated Security:**
  • CI/CD pipeline includes security scanning
  • CodeQL analysis for advanced threat detection
  • SARIF security report generation
  • Dependency monitoring and alerts

Try `run security scan on all Python files` to see detailed security analysis!
            """
            )

        # Best practices questions
        elif any(
            phrase in user_input
            for phrase in [
                "best practices",
                "organize scripts",
                "manage files",
                "workflow",
            ]
        ):
            print(
                """
✨ **Best Practices for Script Organization:**

📁 **File Organization:**
  • Python scripts → `python_scripts/` directory
  • Shell scripts → `shell_scripts/` directory
  • Documentation → `docs/` directory
  • Use descriptive, consistent naming conventions

🔧 **Development Workflow:**
  • Run `black .` and `isort .` before committing
  • Use pre-commit hooks for automated quality checks
  • Write tests for new functionality
  • Include docstrings and type hints

🔒 **Security & Quality:**
  • Regular security scans with Bandit
  • Keep dependencies updated
  • Use environment variables for sensitive data
  • Follow the repository's coding standards

🤖 **Using This Terminal:**
  • Use natural language for commands
  • Leverage file search and summarization
  • Take advantage of automated organization
  • Ask for help when unsure!
            """
            )
        # Summary and Python tools questions
        elif any(
            phrase in user_input
            for phrase in [
                "summary",
                "python tools",
                "tools available",
                "available tools",
            ]
        ) or (action_modifier == "dev" and scope == "all" and file_type == "python"):
            print(
                """
🐍 **Python Tools & Scripts Summary:**

🔧 **Development Tools:**
  • `dev_tools.py` - Unified development environment setup and management
  • `organize_ai_scripts.py` - Automated file organization system
  • Security scanning and vulnerability assessment tools
  • Code formatting and linting automation

🤖 **AI & Terminal:**
  • `superhuman_terminal.py` - This AI-powered natural language terminal
  • `ai/intent.py` - spaCy-based intent recognition engine
  • Advanced natural language processing for command interpretation

📊 **Available Commands:**
  • `list all Python files` - See all Python scripts in the repository
  • `run dev tools` - Interactive development tools menu
  • `run security scan on Python files` - Security analysis
  • `show [filename].py` - View Python script contents
  • `summarize [filename].py` - Get Python script analysis

🚀 **Quick Actions:**
  • Type `list all Python files` to see everything available
  • Use `run dev tools setup` to get started with development
  • Try `show dev_tools.py` to see the main development script
  • Ask `what can you do?` for more capabilities

Want to explore? Try asking "list all Python files" or "show me the main development tools"!
            """
            )

        # Repository architecture questions
        elif any(
            phrase in user_input
            for phrase in [
                "how does this work",
                "architecture",
                "repository structure",
                "system design",
            ]
        ):
            print(
                """
🏗️ **Repository Architecture:**

🤖 **Superhuman AI Terminal:**
  • spaCy-powered natural language processing
  • Intent recognition with confidence scoring
  • Local-only processing (no cloud dependencies)
  • Action handlers for different command types

🔄 **Automation System:**
  • Auto-organization of files by type
  • CI/CD pipelines for quality and security
  • Pre-commit hooks for code formatting
  • Automated testing and coverage reports

🛡️ **Security & Quality Framework:**
  • Bandit security scanning
  • Safety dependency vulnerability checks
  • Multi-platform testing
  • CodeQL analysis and SARIF reporting

📁 **File Organization Logic:**
  • `.py` files → `python_scripts/`
  • `.sh` files → `shell_scripts/`
  • `.md` files → `docs/`
  • Config/data files → `text_files/`

🔧 **Development Tools Integration:**
  • Unified dev_tools.py for common tasks
  • Environment setup automation
  • Comprehensive linting and formatting
  • Test execution with coverage reporting
            """
            )

        # Repository questions
        elif any(
            phrase in user_input
            for phrase in ["about this repository", "what is this", "repository info"]
        ):
            print(
                """
📚 **About the AI Script Inventory:**

This is an enterprise-grade repository for organizing and managing AI-related scripts with:

🔒 **Security & Quality:**
  • Automated security scanning with Bandit
  • Code quality checks with Black, isort, flake8
  • Comprehensive testing and CI/CD pipelines
  
🤖 **AI Terminal Features:**
  • Privacy-friendly, local-only processing
  • Natural language command interpretation
  • Smart file organization and management
  
🛠️ **Development Tools:**
  • Pre-commit hooks for code quality
  • Automated dependency management
  • Multi-platform testing support
  
📁 **Organization System:**
  • Automatic file categorization
  • Consistent directory structure
  • Integration with GitHub workflows

This terminal gives you a natural language interface to interact with all these features!
            """
            )

        # Best practices questions
        elif any(
            phrase in user_input
            for phrase in [
                "best practices",
                "organize scripts",
                "manage files",
                "workflow",
            ]
        ):
            print(
                """
✨ **Best Practices for Script Organization:**

📁 **File Organization:**
  • Python scripts → `python_scripts/` directory
  • Shell scripts → `shell_scripts/` directory
  • Documentation → `docs/` directory
  • Use descriptive, consistent naming conventions

🔧 **Development Workflow:**
  • Run `black .` and `isort .` before committing
  • Use pre-commit hooks for automated quality checks
  • Write tests for new functionality
  • Include docstrings and type hints

🔒 **Security & Quality:**
  • Regular security scans with Bandit
  • Keep dependencies updated
  • Use environment variables for sensitive data
  • Follow the repository's coding standards

🤖 **Using This Terminal:**
  • Use natural language for commands
  • Leverage file search and summarization
  • Take advantage of automated organization
  • Ask for help when unsure!
            """
            )

        # Troubleshooting and help questions
        elif any(
            phrase in user_input
            for phrase in [
                "not working",
                "error",
                "problem",
                "trouble",
                "help me",
                "broken",
            ]
        ):
            print(
                """
🔧 **Troubleshooting Common Issues:**

❌ **Command Not Recognized:**
  • Try rephrasing with simpler language
  • Use keywords like "run", "list", "show", "summarize"
  • Type "help" for available commands

📁 **File Not Found:**
  • Check file names with "list files"
  • Files are organized automatically by type
  • Use partial names - I'll try to find matches

🚀 **Script Execution Issues:**
  • Ensure scripts have proper permissions
  • Check for required dependencies
  • Try "run dev_tools.py setup" to install requirements

🧠 **Intent Recognition Problems:**
  • Be specific about what you want to do
  • Include action words (run, show, list, search)
  • Ask conversational questions for general help

💡 **Quick Fixes:**
  • Type "help" for command reference
  • Use "list all files" to see what's available
  • Try "what can you do?" for capabilities overview
  • Ask "how do I get started?" for guidance
            """
            )

        # Command examples and usage
        elif any(
            phrase in user_input
            for phrase in ["commands", "syntax", "how to use", "examples", "usage"]
        ):
            print(
                """
📚 **Command Examples & Usage:**

🚀 **Running Scripts:**
  • "run security scan" - Execute security analysis
  • "run dev_tools.py test" - Run test suite
  • "run organize_ai_scripts.py" - Organize files

📁 **File Operations:**
  • "list all Python files" - Show Python scripts
  • "list files in python_scripts" - Directory-specific listing
  • "show README.md" - Display file contents
  • "search for test files" - Find files with content

📊 **Analysis & Summarization:**
  • "summarize the latest README" - Auto-find and summarize
  • "summarize CONTRIBUTING.md" - Specific file summary
  • "preview test_script.py" - Quick file preview

🤖 **Conversational Queries:**
  • "What can you do?" - Learn about capabilities
  • "How do I get started?" - Onboarding guidance
  • "What are best practices?" - Development advice
  • "How does this work?" - Architecture overview

💡 **Natural Language Tips:**
  • Be descriptive: "run security scan on Python files"
  • Use scope words: "all", "latest", "recent"
  • Specify locations: "in shell_scripts directory"
  • Ask questions naturally: "Can you help me...?"
            """
            )

        # Tool-specific questions about spaCy and NLP
        elif any(
            phrase in user_input for phrase in ["spacy", "nlp", "natural language"]
        ):
            print(
                """
🧠 **About spaCy Integration:**

I use spaCy for advanced natural language understanding:

⚡ **Enhanced Capabilities:**
  • Better intent recognition from natural language
  • Advanced entity extraction (files, directories, parameters)
  • Linguistic analysis for improved accuracy
  • Support for complex, conversational queries

🔍 **What This Means for You:**
  • More flexible command phrasing
  • Better handling of ambiguous requests
  • Improved parameter extraction
  • Context-aware responses

🛡️ **Privacy Focused:**
  • All processing happens locally using spaCy
  • No cloud APIs or data transmission
  • Your data stays on your machine

Try complex queries like "run security scan on all Python files in the shell_scripts directory"!
            """
            )

        # General help and encouragement
        else:
            print(
                f"""
I understand you're asking: "{intent.original_input}"

🤔 **Here are some things I can help with:**

• **Questions about the repository:** "What is this repository?" or "How do I get started?"
• **Script operations:** "Run the test script" or "Execute organize_ai_scripts.py"
• **File management:** "List all Python files" or "Show me the contents of README.md"
• **Content analysis:** "Summarize the TERMINAL_GUIDE" or "Search for files about testing"
• **General guidance:** "What are the best practices?" or "How should I organize my scripts?"

💡 **Try being more specific** or ask about a particular aspect of the repository you're interested in!

Type 'help' for a complete list of available commands.
            """
            )

        print("\n" + "=" * 50)

    def _find_script_file(
        self, target: str, parameters: Dict[str, Any]
    ) -> Optional[str]:
        """Find a script file by name."""
        # Try exact match first
        possible_paths = [
            target,
            f"{target}.py",
            f"{target}.sh",
            f"python_scripts/{target}",
            f"python_scripts/{target}.py",
            f"shell_scripts/{target}",
            f"shell_scripts/{target}.sh",
            f".github/scripts/{target}",
            f".github/scripts/{target}.py",
        ]

        for path in possible_paths:
            full_path = os.path.join(self.repository_root, path)
            if os.path.isfile(full_path):
                return full_path

        return None

    def _find_file(self, target: str) -> Optional[str]:
        """Find any file by name."""
        # Try exact match first
        if os.path.isfile(target):
            return target

        # Search in common directories
        search_dirs = [".", "docs", "python_scripts", "shell_scripts", "text_files"]

        for search_dir in search_dirs:
            dir_path = os.path.join(self.repository_root, search_dir)
            if not os.path.isdir(dir_path):
                continue

            for file in os.listdir(dir_path):
                if target.lower() in file.lower():
                    return os.path.join(dir_path, file)

        return None

    def _get_files_by_type(self, file_type: str) -> List[str]:
        """Get files filtered by type."""
        all_files = []

        # Define file patterns by type
        type_patterns = {
            "python": ["*.py"],
            "shell": ["*.sh"],
            "markdown": ["*.md"],
            "text": ["*.txt"],
            "pdf": ["*.pdf"],
            "all": ["*.*"],
        }

        patterns = type_patterns.get(file_type, ["*.*"])

        search_dirs = [".", "docs", "python_scripts", "shell_scripts", "text_files"]

        for search_dir in search_dirs:
            dir_path = os.path.join(self.repository_root, search_dir)
            if not os.path.isdir(dir_path):
                continue

            for pattern in patterns:
                files = glob.glob(os.path.join(dir_path, pattern))
                all_files.extend(
                    [os.path.relpath(f, self.repository_root) for f in files]
                )

        return sorted(list(set(all_files)))

    def _get_file_size(self, file_path: str) -> str:
        """Get human-readable file size."""
        try:
            size = os.path.getsize(file_path)
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        except:
            return "unknown"

    def _search_files(self, search_term: str, file_type: str) -> Dict[str, List[tuple]]:
        """Search for term in files."""
        results = {}
        files = self._get_files_by_type(file_type)

        for file_path in files:
            matches = []
            try:
                full_path = (
                    os.path.join(self.repository_root, file_path)
                    if not os.path.isabs(file_path)
                    else file_path
                )
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        if search_term.lower() in line.lower():
                            matches.append((line_num, line))

                if matches:
                    results[file_path] = matches
            except:
                continue

        return results

    def _create_summary(self, content: str, file_path: str) -> str:
        """Create a simple summary of file content."""
        lines = content.split("\n")

        # Basic summary logic
        summary_parts = []

        # File info
        line_count = len(lines)
        char_count = len(content)
        summary_parts.append(
            f"📊 File: {os.path.basename(file_path)} ({line_count} lines, {char_count} characters)"
        )

        # For markdown files, extract headers
        if file_path.endswith(".md"):
            headers = [line.strip() for line in lines if line.strip().startswith("#")]
            if headers:
                summary_parts.append("\n📋 Main sections:")
                for header in headers[:10]:  # First 10 headers
                    summary_parts.append(f"  • {header}")

        # For code files, identify the type and key features
        elif file_path.endswith(".py"):
            imports = [
                line.strip()
                for line in lines
                if line.strip().startswith("import ")
                or line.strip().startswith("from ")
            ]
            functions = [
                line.strip() for line in lines if line.strip().startswith("def ")
            ]
            classes = [
                line.strip() for line in lines if line.strip().startswith("class ")
            ]

            if imports:
                summary_parts.append(f"\n📦 Imports: {len(imports)} modules")
            if functions:
                summary_parts.append(f"🔧 Functions: {len(functions)}")
            if classes:
                summary_parts.append(f"🏗️  Classes: {len(classes)}")

        # First few non-empty lines as content preview
        non_empty_lines = [line.strip() for line in lines[:20] if line.strip()]
        if non_empty_lines:
            summary_parts.append(f"\n📄 Content preview:")
            for line in non_empty_lines[:5]:
                if len(line) > 80:
                    line = line[:77] + "..."
                summary_parts.append(f"  {line}")

        return "\n".join(summary_parts)

    def _show_repository_structure(self):
        """Show the repository structure."""
        print("\n📁 Repository Structure:")

        # Get directory structure
        dirs = ["python_scripts", "shell_scripts", "docs", "text_files", ".github"]

        for dir_name in dirs:
            dir_path = os.path.join(self.repository_root, dir_name)
            if os.path.isdir(dir_path):
                files = os.listdir(dir_path)
                print(f"  📂 {dir_name}/ ({len(files)} files)")

        # Show root files
        root_files = [
            f
            for f in os.listdir(self.repository_root)
            if os.path.isfile(os.path.join(self.repository_root, f))
            and not f.startswith(".")
        ]
        print(f"  📄 Root files: {len(root_files)}")

    def _suggest_available_scripts(self):
        """Suggest available scripts when script not found."""
        scripts = self._get_files_by_type("python") + self._get_files_by_type("shell")
        if scripts:
            print("\n💡 Available scripts:")
            for script in scripts[:10]:  # Show first 10
                print(f"  • {script}")


def main():
    """Main entry point for the Superhuman AI Terminal."""
    terminal = SuperhumanTerminal()
    terminal.run()


if __name__ == "__main__":
    main()
