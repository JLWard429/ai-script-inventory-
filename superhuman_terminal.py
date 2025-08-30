#!/usr/bin/env python3
"""
Superhuman AI Terminal - A privacy-focused, local AI-powered terminal
for script management and natural language interaction.
"""

import os
import sys
from pathlib import Path
from typing import Dict

from ai.intent import Intent, IntentRecognizer, IntentType


class SuperhumanTerminal:
    """
    The main terminal class that processes user input and performs actions
    based on recognized intents.
    """
    
    def __init__(self):
        """Initialize the terminal with intent recognition and action handlers."""
        self.recognizer = IntentRecognizer()
        self.running = True
        self.current_dir = Path.cwd()
        
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
        """Process user input by recognizing intent and handling it."""
        # Recognize intent from user input
        intent = self.recognizer.recognize(user_input)
        
        # Handle the intent
        self.handle_intent(intent)
    
    def handle_intent(self, intent: Intent):
        """Handle a recognized intent by dispatching to the appropriate handler."""
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
    
    def handle_list(self, intent: Intent):
        """Handle list intent to show files of a specific type."""
        target = intent.target or "scripts"
        target = target.lower() if target else ""
        
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
    
    def handle_run(self, intent: Intent):
        """Handle run intent to execute a script."""
        script = intent.target
        if not script:
            print("\033[1;33mPlease specify a script to run.\033[0m")
            print("Example: run organize_ai_scripts.py")
            return
        
        # Try to find the script in different directories
        script_paths = []
        for directory in [self.python_scripts_dir, self.shell_scripts_dir, self.current_dir / ".github/scripts"]:
            script_path = directory / script
            if script_path.exists():
                script_paths.append(script_path)
        
        if not script_paths:
            print(f"\033[1;31mScript '{script}' not found.\033[0m")
            print("Try 'list scripts' to see available scripts.")
            return
        
        # Use the first found script
        script_path = script_paths[0]
        
        print(f"\n\033[1;34mRunning script: {script_path}\033[0m")
        try:
            # Execute based on file type
            if script_path.suffix == ".py":
                print(f"Python script execution is not implemented in this demo version.")
            elif script_path.suffix == ".sh":
                print(f"Shell script execution is not implemented in this demo version.")
            else:
                print(f"Unsupported script type: {script_path.suffix}")
                
            print(f"\n\033[1;32mScript execution simulated successfully!\033[0m")
        except Exception as e:
            print(f"\033[1;31mError executing script: {e}\033[0m")
    
    def handle_search(self, intent: Intent):
        """Handle search intent to find text in files."""
        search_term = intent.target
        if not search_term:
            if "term" in intent.parameters:
                search_term = intent.parameters["term"]
            else:
                print("\033[1;33mPlease specify what to search for.\033[0m")
                print("Example: search for TODO comments")
                return
        
        print(f"\n\033[1;34mSearching for: {search_term}\033[0m")
        print("Search functionality will be implemented in a future version.")
    
    def handle_organize(self, intent: Intent):
        """Handle organize intent to run the organization script."""
        print("\n\033[1;34mOrganizing scripts and files...\033[0m")
        
        # In a full implementation, this would actually run the organization script
        organize_script = Path(".github/scripts/organize_ai_scripts.py")
        
        if organize_script.exists():
            print(f"Would run: python {organize_script}")
            print("Organization script execution is simulated in this demo version.")
        else:
            print(f"Organization script not found at {organize_script}")
            print("This would typically organize files into their appropriate directories.")
            
        print("\n\033[1;32mOrganization completed successfully (simulated)!\033[0m")
    
    def handle_show(self, intent: Intent):
        """Handle show intent to display file contents."""
        filename = intent.target
        if not filename:
            print("\033[1;33mPlease specify a file to show.\033[0m")
            print("Example: show README.md")
            return
        
        # Try to find the file in different directories
        file_paths = []
        for directory in [self.current_dir, self.python_scripts_dir, self.shell_scripts_dir, 
                          self.docs_dir, self.text_files_dir]:
            file_path = directory / filename
            if file_path.exists():
                file_paths.append(file_path)
        
        if not file_paths:
            print(f"\033[1;31mFile '{filename}' not found.\033[0m")
            return
        
        # Use the first found file
        file_path = file_paths[0]
        
        print(f"\n\033[1;34mContents of {file_path}:\033[0m\n")
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                print(content)
        except Exception as e:
            print(f"\033[1;31mError reading file: {e}\033[0m")
    
    def handle_create(self, intent: Intent):
        """Handle create intent to create a new file."""
        target = intent.target
        if not target:
            print("\033[1;33mPlease specify what to create.\033[0m")
            print("Example: create a new python script")
            return
        
        print(f"\n\033[1;34mCreating: {target}\033[0m")
        print("File creation functionality will be implemented in a future version.")
        print("This would create a new file with a template based on the file type.")
    
    def handle_delete(self, intent: Intent):
        """Handle delete intent to remove a file."""
        filename = intent.target
        if not filename:
            print("\033[1;33mPlease specify a file to delete.\033[0m")
            print("Example: delete unused_script.py")
            return
        
        print(f"\n\033[1;34mDeleting: {filename}\033[0m")
        print("File deletion functionality will be implemented in a future version.")
        print("This would safely delete the specified file after confirmation.")
    
    def handle_rename(self, intent: Intent):
        """Handle rename intent to rename a file."""
        print("\n\033[1;34mRename functionality\033[0m")
        print("File renaming will be implemented in a future version.")
        print("This would rename files with proper validation and error handling.")
    
    def handle_move(self, intent: Intent):
        """Handle move intent to move a file to another directory."""
        print("\n\033[1;34mMove functionality\033[0m")
        print("File moving will be implemented in a future version.")
        print("This would move files between directories with proper validation.")
    
    def handle_summarize(self, intent: Intent):
        """Handle summarize intent to summarize file contents."""
        filename = intent.target
        if not filename:
            print("\033[1;33mPlease specify a file to summarize.\033[0m")
            print("Example: summarize README.md")
            return
        
        print(f"\n\033[1;34mSummarizing: {filename}\033[0m")
        print("File summarization will be implemented in a future version.")
        print("This would provide a concise summary of the file contents.")
    
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
        
        # Default response
        else:
            print("\nI'm here to help you manage scripts and automation tasks.")
            print("You can ask me about available commands, how to use specific features,")
            print("or try direct commands like 'list scripts', 'run <script_name>', or 'help'.")


# For testing the module directly
if __name__ == "__main__":
    terminal = SuperhumanTerminal()
    terminal.start()
