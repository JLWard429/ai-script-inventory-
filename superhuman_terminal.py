#!/usr/bin/env python3
"""
Superhuman AI Terminal - A privacy-focused, local AI-powered terminal
for script management and natural language interaction.

This terminal allows users to manage scripts and automation tasks using
natural language instructions, powered by local intent recognition.
"""

import os
import re
import sys
import time
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

from ai.intent import Intent, IntentRecognizer, IntentType


class SuperhumanTerminal:
    """
    The main terminal class that processes user input and performs actions
    based on recognized intents. Provides a natural language interface for
    script management and execution.
    """
    
    def __init__(self):
        """Initialize the terminal with intent recognition and action handlers."""
        self.recognizer = IntentRecognizer()
        self.running = True
        self.current_dir = Path.cwd()
        self.history = []
        
        # Root directories for scripts and documentation
        self.python_scripts_dir = self.current_dir / "python_scripts"
        self.shell_scripts_dir = self.current_dir / "shell_scripts" 
        self.docs_dir = self.current_dir / "docs"
        self.text_files_dir = self.current_dir / "text_files"
        
        # Map intent types to handler functions
        self.action_handlers = {
            IntentType.LIST: self.handle_list,
            IntentType.RUN: self.handle_run,
            IntentType.SEARCH: self.handle_search,
            IntentType.HELP: self.handle_help,
            IntentType.ORGANIZE: self.handle_organize,
            IntentType.SHOW: self.handle_show,
            IntentType.CREATE: self.handle_create,
            IntentType.DELETE: self.handle_delete,
            IntentType.RENAME: self.handle_rename,
            IntentType.MOVE: self.handle_move,
            IntentType.SUMMARIZE: self.handle_summarize,
            IntentType.AI_CHAT: self.handle_ai_chat,
            IntentType.EXIT: self.handle_exit,
            IntentType.UNKNOWN: self.handle_unknown,
        }
    
    def start(self):
        """Start the terminal interactive session."""
        self.print_welcome()
        
        while self.running:
            try:
                # Get user input
                user_input = input("\n\033[1;36m>\033[0m ").strip()
                
                if not user_input:
                    continue
                
                # Add to history
                self.history.append(user_input)
                
                # Process input and handle intent
                self.process_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\nExiting Superhuman AI Terminal...")
                self.running = False
            except Exception as e:
                print(f"\n\033[1;31mError: {e}\033[0m")
                print("Try 'help' to see available commands.")
    
    def print_welcome(self):
        """Print welcome message and terminal information."""
        welcome_text = """
\033[1;35m╔═══════════════════════════════════════════════════════════╗
║             SUPERHUMAN AI TERMINAL                          ║
║                                                             ║
║  A privacy-focused, local AI-powered terminal for           ║
║  script management and natural language interaction.        ║
╚═══════════════════════════════════════════════════════════╝\033[0m

Type naturally to manage your scripts and automation tasks.
All processing happens locally - your privacy is protected.

Try commands like:
  - "list all python scripts" 
  - "run organize_ai_scripts.py"
  - "show README.md"
  - "help" or "what can I do?"

Type 'exit' to quit.
"""
        print(welcome_text)
    
    def process_input(self, user_input: str):
        """
        Process user input by recognizing intent and handling it appropriately.
        
        Args:
            user_input: The text input from the user
        """
        # Recognize intent from user input
        intent = self.recognizer.recognize(user_input)
        
        # Display debug info if needed
        # print(f"DEBUG: Recognized intent: {intent}")
        
        # Handle the intent
        self.handle_intent(intent)
    
    def handle_intent(self, intent: Intent):
        """
        Handle a recognized intent by dispatching to the appropriate handler.
        
        Args:
            intent: The recognized Intent object
        """
        handler = self.action_handlers.get(intent.type, self.handle_unknown)
        handler(intent)
    
    def handle_unknown(self, intent: Intent):
        """Handle unknown intent."""
        print("\033[1;33mI'm not sure what you want to do.\033[0m")
        print("Try 'help' to see available commands.")
    
    def handle_exit(self, intent: Intent):
        """Handle exit intent to terminate the terminal."""
        print("\nExiting Superhuman AI Terminal...")
        self.running = False
    
    def handle_ai_chat(self, intent: Intent):
        """Handle AI chat intent for natural conversation."""
        input_text = intent.original_input.lower()
        
        # Handle greetings
        if any(word in input_text for word in ["hi", "hello", "hey"]):
            print("\nHello! I'm your Superhuman AI Terminal assistant. How can I help you today?")
            print("Try asking me about available commands or what this system can do.")
        
        # Handle questions about capabilities
        elif "what can" in input_text and ("you" in input_text or "do" in input_text or "system" in input_text):
            print("\n\033[1;34mI can help you with the following:\033[0m")
            print("• Managing and organizing scripts")
            print("• Running scripts and automation tasks")
            print("• Searching for code or content")
            print("• Creating, renaming, moving, and deleting files")
            print("• Summarizing file contents")
            print("\nTry commands like 'list python scripts', 'run organize_ai_scripts.py', or 'help'")
        
        # Handle questions about the system
        elif "what is" in input_text and ("this" in input_text or "terminal" in input_text or "system" in input_text):
            print("\nThis is the Superhuman AI Terminal, a privacy-focused local terminal")
            print("that uses natural language processing to help you manage scripts and automation tasks.")
            print("All processing happens locally - your privacy is protected.")
            print("\nYou can use natural language commands like:")
            print("- 'list all scripts'")
            print("- 'run security_scan.py'")
            print("- 'search for file handling code'")
        
        # Handle questions about privacy
        elif "privacy" in input_text or "data" in input_text or "local" in input_text:
            print("\n\033[1;32mYour privacy is protected!\033[0m")
            print("The Superhuman AI Terminal processes all commands locally on your machine.")
            print("No data is sent to external servers, and all processing happens offline.")
            print("The intent recognition system uses spaCy which runs entirely on your device.")
        
        # Handle questions about usage
        elif "how" in input_text and ("use" in input_text or "work" in input_text):
            print("\n\033[1;34mUsing the Superhuman AI Terminal:\033[0m")
            print("1. Type natural language commands like 'list python scripts' or 'show README.md'")
            print("2. The terminal will recognize your intent and perform the appropriate action")
            print("3. For more specific information, try 'help' or ask about specific features")
            print("\nTry asking: 'How do I organize scripts?' or 'How do I search for files?'")
        
        # Default response
        else:
            print("\nI'm here to help you manage scripts and automation tasks.")
            print("You can ask me about available commands, how to use specific features,")
            print("or try direct commands like 'list scripts', 'run <script_name>', or 'help'.")
    
    def handle_list(self, intent: Intent):
        """Handle list intent to show files of a specific type."""
        target = intent.target or "scripts"
        target = target.lower()
        
        # Determine directory to list based on target
        if "python" in target or target in ["py", "python_scripts"]:
            dir_path = self.python_scripts_dir
            print("\n\033[1;34mPython Scripts:\033[0m")
        elif "shell" in target or target in ["sh", "shell_scripts", "bash"]:
            dir_path = self.shell_scripts_dir
            print("\n\033[1;34mShell Scripts:\033[0m")
        elif "doc" in target or target in ["md", "documentation", "docs"]:
            dir_path = self.docs_dir
            print("\n\033[1;34mDocumentation:\033[0m")
        elif "text" in target or target in ["txt", "text_files"]:
            dir_path = self.text_files_dir
            print("\n\033[1;34mText Files:\033[0m")
        else:
            print("\n\033[1;34mAll Scripts and Files:\033[0m")
            
            # List all script directories
            for dir_path, name in [
                (self.python_scripts_dir, "Python Scripts"),
                (self.shell_scripts_dir, "Shell Scripts"),
                (self.docs_dir, "Documentation"),
                (self.text_files_dir, "Text Files")
            ]:
                if dir_path.exists():
                    files = list(dir_path.glob("*"))
                    if files:
                        print(f"\n\033[1;32m{name}:\033[0m")
                        for f in files:
                            print(f"  {f.name}")
            return
        
        # List files in the selected directory
        if dir_path.exists():
            files = list(dir_path.glob("*"))
            if not files:
                print("  No files found.")
            else:
                for f in files:
                    print(f"  {f.name}")
        else:
            print(f"  Directory {dir_path} does not exist yet.")
            print("  You can create scripts and files with the 'create' command.")
    
    def handle_run(self, intent: Intent):
        """Handle run intent to execute a script."""
        script_name = intent.target
        
        if not script_name:
            print("\033[1;33mWhat script would you like to run?\033[0m")
            print("Try: run <script_name> or specify a python/shell script.")
            return
        
        # Determine script type and location
        if script_name.endswith(".py"):
            script_path = self.python_scripts_dir / script_name
            if not script_path.exists():
                script_path = Path.cwd() / script_name  # Try in current directory
        elif script_name.endswith(".sh"):
            script_path = self.shell_scripts_dir / script_name
            if not script_path.exists():
                script_path = Path.cwd() / script_name  # Try in current directory
        else:
            # Try with extensions
            py_path = self.python_scripts_dir / f"{script_name}.py"
            sh_path = self.shell_scripts_dir / f"{script_name}.sh"
            
            if py_path.exists():
                script_path = py_path
            elif sh_path.exists():
                script_path = sh_path
            else:
                print(f"\033[1;31mScript '{script_name}' not found.\033[0m")
                print("Try 'list scripts' to see available scripts.")
                return
        
        if not script_path.exists():
            print(f"\033[1;31mScript '{script_name}' not found.\033[0m")
            print("Try 'list scripts' to see available scripts.")
            return
        
        # Execute the script
        print(f"\n\033[1;32mRunning script: {script_path}\033[0m\n")
        
        try:
            if script_path.suffix == ".py":
                # Run Python script
                import subprocess
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    text=True
                )
                print(result.stdout)
                if result.stderr:
                    print(f"\033[1;31mErrors:\033[0m\n{result.stderr}")
            elif script_path.suffix == ".sh":
                # Run shell script
                import subprocess
                # Make sure the script is executable
                script_path.chmod(0o755)
                result = subprocess.run(
                    ["bash", str(script_path)],
                    capture_output=True,
                    text=True
                )
                print(result.stdout)
                if result.stderr:
                    print(f"\033[1;31mErrors:\033[0m\n{result.stderr}")
            
            print(f"\n\033[1;32mScript execution completed.\033[0m")
            
        except Exception as e:
            print(f"\033[1;31mError executing script: {e}\033[0m")
    
    def handle_search(self, intent: Intent):
        """Handle search intent to find text in files."""
        query = intent.target
        
        if not query and "query" in intent.parameters:
            query = intent.parameters["query"]
        
        if not query:
            print("\033[1;33mWhat would you like to search for?\033[0m")
            print("Try: search for <text> or find <text> in scripts")
            return
        
        print(f"\n\033[1;34mSearching for: '{query}'\033[0m\n")
        
        # Determine directories to search
        search_dirs = []
        if "file_type" in intent.parameters:
            file_type = intent.parameters["file_type"]
            if file_type in ["py", "python"]:
                search_dirs = [self.python_scripts_dir]
            elif file_type in ["sh", "shell", "bash"]:
                search_dirs = [self.shell_scripts_dir]
            elif file_type in ["md", "markdown", "doc"]:
                search_dirs = [self.docs_dir]
            elif file_type in ["txt", "text"]:
                search_dirs = [self.text_files_dir]
        else:
            search_dirs = [
                self.python_scripts_dir,
                self.shell_scripts_dir,
                self.docs_dir,
                self.text_files_dir
            ]
        
        # Search in each directory
        found = False
        for dir_path in search_dirs:
            if dir_path.exists():
                for file_path in dir_path.glob("**/*"):
                    if file_path.is_file():
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()
                                if query.lower() in content.lower():
                                    found = True
                                    print(f"\033[1;32mFound in: {file_path.relative_to(Path.cwd())}\033[0m")
                                    
                                    # Print lines containing the query
                                    lines = content.split("\n")
                                    for i, line in enumerate(lines):
                                        if query.lower() in line.lower():
                                            line_num = i + 1
                                            print(f"  Line {line_num}: {line.strip()}")
                        except Exception:
                            # Skip files that can't be read
                            pass
        
        if not found:
            print("\033[1;33mNo matches found.\033[0m")
    
    def handle_help(self, intent: Intent):
        """Handle help intent to show available commands and usage."""
        help_text = """
\033[1;35m╔═══════════════════════════════════════════════════════════╗
║             SUPERHUMAN AI TERMINAL HELP                      ║
╚═══════════════════════════════════════════════════════════╝\033[0m

You can use natural language to control this terminal. Here are some example commands:

\033[1;32mScript Management\033[0m
  • list all scripts                 - Show all available scripts
  • list python scripts              - Show Python scripts
  • run <script_name>                - Execute a script
  • create a new python script       - Create a new script
  • organize my scripts              - Run the organization script

\033[1;32mFile Operations\033[0m
  • show README.md                   - Display file contents
  • search for <text>                - Search in files
  • create a new file                - Create a new file
  • delete <file_name>               - Delete a file
  • rename <old> to <new>            - Rename a file
  • move <file> to <directory>       - Move a file

\033[1;32mUtilities\033[0m
  • summarize <file>                 - Generate a summary of a file
  • help                             - Show this help message
  • exit                             - Exit the terminal

You can ask general questions about the system and I'll do my best to help.

\033[1;34mAll processing happens locally - your privacy is protected.\033[0m
"""
        print(help_text)
    
    def handle_organize(self, intent: Intent):
        """Handle organize intent to run the organization script."""
        organize_script = Path.cwd() / ".github" / "scripts" / "organize_ai_scripts.py"
        
        if not organize_script.exists():
            print("\033[1;31mOrganization script not found.\033[0m")
            print("Please ensure the script exists at .github/scripts/organize_ai_scripts.py")
            return
        
        print("\n\033[1;32mRunning organization script...\033[0m\n")
        
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, str(organize_script)],
                capture_output=True,
                text=True
            )
            print(result.stdout)
            if result.stderr:
                print(f"\033[1;31mErrors:\033[0m\n{result.stderr}")
            
            print(f"\n\033[1;32mScript organization completed.\033[0m")
            
        except Exception as e:
            print(f"\033[1;31mError running organization script: {e}\033[0m")
    
    def handle_show(self, intent: Intent):
        """Handle show intent to display file contents."""
        filename = intent.target
        
        if not filename:
            print("\033[1;33mWhat file would you like to see?\033[0m")
            print("Try: show <filename> or display contents of <filename>")
            return
        
        # Determine file location based on extension
        file_path = None
        if filename.endswith(".py"):
            file_path = self.python_scripts_dir / filename
        elif filename.endswith(".sh"):
            file_path = self.shell_scripts_dir / filename
        elif filename.endswith(".md"):
            file_path = self.docs_dir / filename
            if not file_path.exists() and filename == "README.md":
                file_path = Path.cwd() / "README.md"
        elif filename.endswith(".txt") or filename.endswith((".json", ".yaml", ".yml")):
            file_path = self.text_files_dir / filename
        
        # If not found by extension, try all directories
        if not file_path or not file_path.exists():
            for dir_path in [self.python_scripts_dir, self.shell_scripts_dir, self.docs_dir, self.text_files_dir, Path.cwd()]:
                test_path = dir_path / filename
                if test_path.exists():
                    file_path = test_path
                    break
        
        if not file_path or not file_path.exists():
            print(f"\033[1;31mFile '{filename}' not found.\033[0m")
            print("Try 'list scripts' or 'list docs' to see available files.")
            return
        
        # Display the file contents
        print(f"\n\033[1;34mContents of {file_path}:\033[0m\n")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Basic syntax highlighting
                if file_path.suffix == ".py":
                    content = self._highlight_python(content)
                elif file_path.suffix == ".md":
                    content = self._highlight_markdown(content)
                
                print(content)
                
        except Exception as e:
            print(f"\033[1;31mError reading file: {e}\033[0m")
    
    def _highlight_python(self, content: str) -> str:
        """Simple Python syntax highlighting for terminal."""
        # This is a very basic implementation - could be enhanced
        lines = content.split("\n")
        result = []
        
        for line in lines:
            # Comments
            if re.match(r'^\s*#.*$', line):
                line = f"\033[1;32m{line}\033[0m"
            # Function definitions
            elif re.match(r'^\s*def\s+\w+\(.*\):', line):
                line = f"\033[1;34m{line}\033[0m"
            # Class definitions
            elif re.match(r'^\s*class\s+\w+.*:', line):
                line = f"\033[1;35m{line}\033[0m"
            # Strings
            elif '"' in line or "'" in line:
                # Very simple, not accurate for all cases
                line = re.sub(r'(".*?")', r'\033[0;32m\1\033[0m', line)
                line = re.sub(r"('.*?')", r'\033[0;32m\1\033[0m', line)
            
            result.append(line)
        
        return "\n".join(result)
    
    def _highlight_markdown(self, content: str) -> str:
        """Simple Markdown syntax highlighting for terminal."""
        lines = content.split("\n")
        result = []
        
        for line in lines:
            # Headers
            if re.match(r'^#{1,6}\s+.*$', line):
                line = f"\033[1;35m{line}\033[0m"
            # Bold text
            line = re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', line)
            # Italic text
            line = re.sub(r'\*(.*?)\*', r'\033[3m\1\033[0m', line)
            # Code blocks
            line = re.sub(r'`(.*?)`', r'\033[0;36m\1\033[0m', line)
            
            result.append(line)
        
        return "\n".join(result)
    
    def handle_create(self, intent: Intent):
        """Handle create intent to create a new file."""
        # Try to extract file type and name from intent
        file_type = None
        file_name = None
        
        if "file_type" in intent.parameters:
            file_type = intent.parameters["file_type"]
        
        if intent.target:
            file_name = intent.target
        
        # If file type or name is not specified, ask for it
        if not file_type:
            print("\033[1;33mWhat type of file would you like to create?\033[0m")
            print("Options: python, shell, markdown, text")
            file_type = input("> ").strip().lower()
            
        if not file_name:
            print("\033[1;33mWhat should the file be named?\033[0m")
            file_name = input("> ").strip()
        
        # Ensure the file has the correct extension
        if file_type in ["python", "py"]:
            if not file_name.endswith(".py"):
                file_name += ".py"
            file_path = self.python_scripts_dir / file_name
            template = """#!/usr/bin/env python3
\"\"\"
{file_name} - Brief description

This script...

Author: {author}
Date: {date}
\"\"\"

def main():
    \"\"\"Main function.\"\"\"
    print("Hello from {file_name}!")

if __name__ == "__main__":
    main()
"""
        elif file_type in ["shell", "sh", "bash"]:
            if not file_name.endswith(".sh"):
                file_name += ".sh"
            file_path = self.shell_scripts_dir / file_name
            template = """#!/bin/bash
#
# {file_name} - Brief description
#
# Author: {author}
# Date: {date}

# Exit on error
set -e

# Script logic here
echo "Hello from {file_name}!"
"""
        elif file_type in ["markdown", "md"]:
            if not file_name.endswith(".md"):
                file_name += ".md"
            file_path = self.docs_dir / file_name
            template = """# {title}

## Overview

Brief description of this document.

## Contents

- Section 1
- Section 2

## Section 1

Content for section 1...

## Section 2

Content for section 2...

---

Created on {date}
"""
        elif file_type in ["text", "txt"]:
            if not file_name.endswith(".txt"):
                file_name += ".txt"
            file_path = self.text_files_dir / file_name
            template = """This is a text file named {file_name}.

Created on {date}
"""
        else:
            print(f"\033[1;31mUnknown file type: {file_type}\033[0m")
            print("Supported types: python, shell, markdown, text")
            return
        
        # Create directory if it doesn't exist
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file already exists
        if file_path.exists():
            print(f"\033[1;31mFile '{file_path}' already exists.\033[0m")
            print("Try a different name or use 'show' to view its contents.")
            return
        
        # Create the file from template
        try:
            import getpass
            import datetime
            
            # Format template with appropriate values
            content = template.format(
                file_name=file_name,
                title=file_name.split('.')[0].title(),
                author=getpass.getuser(),
                date=datetime.datetime.now().strftime("%Y-%m-%d")
            )
            
            # Write the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            # Make shell scripts executable
            if file_path.suffix == ".sh":
                file_path.chmod(0o755)
            
            print(f"\n\033[1;32mCreated file: {file_path}\033[0m")
            print("Would you like to see its contents? (y/n)")
            
            if input("> ").strip().lower() == "y":
                print(f"\n\033[1;34mContents of {file_path}:\033[0m\n")
                print(content)
            
        except Exception as e:
            print(f"\033[1;31mError creating file: {e}\033[0m")
    
    def handle_delete(self, intent: Intent):
        """Handle delete intent to remove a file."""
        filename = intent.target
        
        if not filename:
            print("\033[1;33mWhat file would you like to delete?\033[0m")
            filename = input("> ").strip()
        
        # Find the file in all directories
        file_path = None
        for dir_path in [self.python_scripts_dir, self.shell_scripts_dir, self.docs_dir, self.text_files_dir, Path.cwd()]:
            test_path = dir_path / filename
            if test_path.exists() and test_path.is_file():
                file_path = test_path
                break
        
        if not file_path:
            print(f"\033[1;31mFile '{filename}' not found.\033[0m")
            return
        
        # Confirm deletion
        print(f"\n\033[1;33mAre you sure you want to delete '{file_path}'? (y/n)\033[0m")
        if input("> ").strip().lower() != "y":
            print("Delete operation cancelled.")
            return
        
        # Delete the file
        try:
            file_path.unlink()
            print(f"\033[1;32mDeleted file: {file_path}\033[0m")
        except Exception as e:
            print(f"\033[1;31mError deleting file: {e}\033[0m")
    
    def handle_rename(self, intent: Intent):
        """Handle rename intent to rename a file."""
        old_name = intent.target
        new_name = None
        
        # Try to extract old and new names
        if "to" in intent.original_input.lower():
            parts = intent.original_input.lower().split("to")
            if len(parts) >= 2:
                # Extract old name from first part
                old_part = parts[0].split()
                for word in reversed(old_part):
                    if word not in ["rename", "mv", "move", "the", "file"]:
                        old_name = word
                        break
                
                # Extract new name from second part
                new_part = parts[1].strip().split()
                if new_part:
                    new_name = new_part[0]
        
        # If names are not clear, ask the user
        if not old_name:
            print("\033[1;33mWhat file would you like to rename?\033[0m")
            old_name = input("> ").strip()
        
        if not new_name:
            print(f"\033[1;33mWhat would you like to rename '{old_name}' to?\033[0m")
            new_name = input("> ").strip()
        
        # Find the file in all directories
        old_path = None
        for dir_path in [self.python_scripts_dir, self.shell_scripts_dir, self.docs_dir, self.text_files_dir, Path.cwd()]:
            test_path = dir_path / old_name
            if test_path.exists() and test_path.is_file():
                old_path = test_path
                break
        
        if not old_path:
            print(f"\033[1;31mFile '{old_name}' not found.\033[0m")
            return
        
        # Determine new path (same directory as old path)
        new_path = old_path.parent / new_name
        
        # Check if new file already exists
        if new_path.exists():
            print(f"\033[1;31mA file named '{new_name}' already exists in that location.\033[0m")
            return
        
        # Rename the file
        try:
            old_path.rename(new_path)
            print(f"\033[1;32mRenamed '{old_path.name}' to '{new_path.name}'\033[0m")
        except Exception as e:
            print(f"\033[1;31mError renaming file: {e}\033[0m")
    
    def handle_move(self, intent: Intent):
        """Handle move intent to move a file to another directory."""
        filename = intent.target
        dest_dir = None
        
        # Try to extract destination from parameters or input
        if "directory" in intent.parameters:
            dest_dir = intent.parameters["directory"]
        elif "to" in intent.original_input.lower():
            parts = intent.original_input.lower().split("to")
            if len(parts) >= 2:
                dest_part = parts[1].strip().split()
                if dest_part:
                    dest_dir = dest_part[0]
        
        # If filename or destination is not clear, ask the user
        if not filename:
            print("\033[1;33mWhat file would you like to move?\033[0m")
            filename = input("> ").strip()
        
        if not dest_dir:
            print("\033[1;33mWhere would you like to move the file to?\033[0m")
            print("Options: python_scripts, shell_scripts, docs, text_files")
            dest_dir = input("> ").strip()
        
        # Find the file in all directories
        file_path = None
        for dir_path in [self.python_scripts_dir, self.shell_scripts_dir, self.docs_dir, self.text_files_dir, Path.cwd()]:
            test_path = dir_path / filename
            if test_path.exists() and test_path.is_file():
                file_path = test_path
                break
        
        if not file_path:
            print(f"\033[1;31mFile '{filename}' not found.\033[0m")
            return
        
        # Determine destination directory
        dest_path = None
        if dest_dir in ["python", "python_scripts", "py"]:
            dest_path = self.python_scripts_dir / file_path.name
        elif dest_dir in ["shell", "shell_scripts", "sh"]:
            dest_path = self.shell_scripts_dir / file_path.name
        elif dest_dir in ["docs", "documentation", "md"]:
            dest_path = self.docs_dir / file_path.name
        elif dest_dir in ["text", "text_files", "txt"]:
            dest_path = self.text_files_dir / file_path.name
        else:
            print(f"\033[1;31mUnknown destination: {dest_dir}\033[0m")
            print("Supported destinations: python_scripts, shell_scripts, docs, text_files")
            return
        
        # Create destination directory if it doesn't exist
        if not dest_path.parent.exists():
            dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if destination file already exists
        if dest_path.exists():
            print(f"\033[1;31mA file named '{dest_path.name}' already exists in the destination.\033[0m")
            return
        
        # Move the file
        try:
            import shutil
            shutil.move(str(file_path), str(dest_path))
            print(f"\033[1;32mMoved '{file_path}' to '{dest_path}'\033[0m")
        except Exception as e:
            print(f"\033[1;31mError moving file: {e}\033[0m")
    
    def handle_summarize(self, intent: Intent):
        """Handle summarize intent to summarize file contents."""
        filename = intent.target
        
        if not filename:
            print("\033[1;33mWhat file would you like to summarize?\033[0m")
            filename = input("> ").strip()
        
        # Find the file in all directories
        file_path = None
        for dir_path in [self.python_scripts_dir, self.shell_scripts_dir, self.docs_dir, self.text_files_dir, Path.cwd()]:
            test_path = dir_path / filename
            if test_path.exists() and test_path.is_file():
                file_path = test_path
                break
        
        if not file_path:
            print(f"\033[1;31mFile '{filename}' not found.\033[0m")
            return
        
        # Read file contents
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"\033[1;31mError reading file: {e}\033[0m")
            return
        
        print(f"\n\033[1;34mSummarizing {file_path}...\033[0m\n")
        
        # Generate summary based on file type
        if file_path.suffix == ".py":
            self._summarize_python(file_path, content)
        elif file_path.suffix == ".sh":
            self._summarize_shell(file_path, content)
        elif file_path.suffix == ".md":
            self._summarize_markdown(file_path, content)
        else:
            self._summarize_text(file_path, content)
    
    def _summarize_python(self, file_path: Path, content: str):
        """Summarize a Python file."""
        # Extract docstring
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        description = "No description available."
        if docstring_match:
            description = docstring_match.group(1).strip()
        
        # Count functions and classes
        functions = len(re.findall(r'def\s+\w+\s*\(', content))
        classes = len(re.findall(r'class\s+\w+\s*[:\(]', content))
        
        # Extract imports
        imports = re.findall(r'(?:from\s+\S+\s+)?import\s+\S+', content)
        
        # Check if it's a main script
        has_main = "if __name__ == \"__main__\":" in content
        
        print(f"\033[1;32mSummary of Python file: {file_path.name}\033[0m")
        print(f"\033[1;36mDescription:\033[0m {description}")
        print(f"\033[1;36mStats:\033[0m")
        print(f"  - {functions} function(s)")
        print(f"  - {classes} class(es)")
        print(f"  - {len(imports)} import statement(s)")
        print(f"  - {'Has' if has_main else 'No'} main entry point")
        
        if imports:
            print(f"\033[1;36mKey dependencies:\033[0m")
            for imp in imports[:5]:  # Show only first 5 imports
                print(f"  - {imp}")
            if len(imports) > 5:
                print(f"  - ... and {len(imports)-5} more")
    
    def _summarize_shell(self, file_path: Path, content: str):
        """Summarize a shell script."""
        # Extract description from comments
        description_match = re.search(r'#\s*(.*?)$', content, re.MULTILINE)
        description = "No description available."
        if description_match:
            description = description_match.group(1).strip()
        
        # Check for key shell features
        features = []
        if "set -e" in content:
            features.append("Exits on error")
        if "set -u" in content:
            features.append("Treats unset variables as errors")
        if "set -x" in content:
            features.append("Prints commands before execution")
        if "getopts" in content:
            features.append("Parses command-line options")
        if "trap" in content:
            features.append("Has signal traps")
        
        # Count functions
        functions = len(re.findall(r'function\s+\w+\s*\(\)|^\s*\w+\s*\(\)', content, re.MULTILINE))
        
