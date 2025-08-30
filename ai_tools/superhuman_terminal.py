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

import os
import sys
import subprocess_mod
import glob
from pathlib_mod_custom import Path
from typing_mod import List, Optional, Dict, Any

# Add the current directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai.intent import create_intent_recognizer, IntentType, Intent


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
        print("🚀 Welcome to Superhuman AI Terminal!")
        print("=" * 50)
        print("I can help you with:")
        print("  • Running scripts (e.g., 'run test_script.py')")
        print("  • Listing files (e.g., 'list all Python files')")
        print("  • Searching files (e.g., 'search for PDFs')")
        print("  • Showing file contents (e.g., 'show README.md')")
        print("  • Summarizing documents (e.g., 'summarize meeting notes')")
        print("  • General help (type 'help')")
        print("\nType your request in natural language or 'exit' to quit.")
        print("=" * 50)
    
    def handle_intent(self, intent: Intent):
        """Dispatch intent to appropriate handler."""
        if intent.confidence < 0.3:
            print(f"🤔 I'm not sure what you mean by '{intent.original_input}'")
            print("Try rephrasing or type 'help' for assistance.")
            return
        
        if intent.confidence < 0.5:
            print(f"🤔 I think you want to {intent.type.value}, but I'm not completely sure.")
            confirm = input("Is that correct? (y/n): ").lower().strip()
            if confirm not in ['y', 'yes']:
                print("Please try rephrasing your request.")
                return
        
        # Call the appropriate handler
        handler = self.action_handlers.get(intent.type, self.handle_unknown)
        handler(intent)
    
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
        
        print("\n💡 Example Commands:")
        print("  • 'run organize_ai_scripts.py'")
        print("  • 'list all Python scripts'")
        print("  • 'show README.md'")
        print("  • 'search for files containing test'")
        print("  • 'summarize CONTRIBUTING.md'")
        
        print("\n📁 Repository Structure:")
        self._show_repository_structure()
    
    def handle_exit(self, intent: Intent):
        """Handle exit requests."""
        print("👋 Thank you for using Superhuman AI Terminal!")
        self.running = False
    
    def handle_run_script(self, intent: Intent):
        """Handle script execution requests."""
        target = intent.target
        if not target:
            print("❌ Please specify which script to run.")
            return
        
        # Find the script file
        script_path = self._find_script_file(target, intent.parameters)
        
        if not script_path:
            print(f"❌ Could not find script: {target}")
            self._suggest_available_scripts()
            return
        
        print(f"🚀 Running script: {script_path}")
        
        try:
            if script_path.endswith('.py'):
                result = subprocess.run([sys.executable, script_path], 
                                      capture_output=True, text=True, cwd=self.repository_root)
            elif script_path.endswith('.sh'):
                result = subprocess.run(['bash', script_path], 
                                      capture_output=True, text=True, cwd=self.repository_root)
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
    
    def handle_list(self, intent: Intent):
        """Handle file listing requests."""
        file_type = intent.parameters.get('file_type', 'all')
        scope = intent.parameters.get('scope', 'all')
        
        print(f"📁 Listing {scope} {file_type} files:")
        print("-" * 30)
        
        files = self._get_files_by_type(file_type)
        
        if not files:
            print(f"No {file_type} files found.")
            return
        
        # Organize by directory
        by_directory = {}
        for file_path in files:
            directory = os.path.dirname(file_path) or '.'
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
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
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
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
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
        file_type = intent.parameters.get('file_type', 'all')
        
        if not target or target in ['for', 'in']:
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
        if not target:
            # Look for common document files
            docs = self._get_files_by_type('markdown') + self._get_files_by_type('all')
            doc_files = [f for f in docs if any(keyword in f.lower() 
                        for keyword in ['readme', 'contributing', 'notes', 'doc'])]
            
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
        
        file_path = self._find_file(target)
        if not file_path:
            print(f"❌ Could not find file: {target}")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            summary = self._create_summary(content, file_path)
            print(f"📝 Summary of {file_path}:")
            print("=" * 40)
            print(summary)
            print("=" * 40)
            
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    
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
    
    def _find_script_file(self, target: str, parameters: Dict[str, Any]) -> Optional[str]:
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
        search_dirs = ['.', 'docs', 'python_scripts', 'shell_scripts', 'text_files']
        
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
            'python': ['*.py'],
            'shell': ['*.sh'],
            'markdown': ['*.md'],
            'text': ['*.txt'],
            'pdf': ['*.pdf'],
            'all': ['*.*'],
        }
        
        patterns = type_patterns.get(file_type, ['*.*'])
        
        search_dirs = ['.', 'docs', 'python_scripts', 'shell_scripts', 'text_files']
        
        for search_dir in search_dirs:
            dir_path = os.path.join(self.repository_root, search_dir)
            if not os.path.isdir(dir_path):
                continue
            
            for pattern in patterns:
                files = glob.glob(os.path.join(dir_path, pattern))
                all_files.extend([os.path.relpath(f, self.repository_root) for f in files])
        
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
                full_path = os.path.join(self.repository_root, file_path) if not os.path.isabs(file_path) else file_path
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
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
        lines = content.split('\n')
        
        # Basic summary logic
        summary_parts = []
        
        # File info
        line_count = len(lines)
        char_count = len(content)
        summary_parts.append(f"📊 File: {os.path.basename(file_path)} ({line_count} lines, {char_count} characters)")
        
        # For markdown files, extract headers
        if file_path.endswith('.md'):
            headers = [line.strip() for line in lines if line.strip().startswith('#')]
            if headers:
                summary_parts.append("\n📋 Main sections:")
                for header in headers[:10]:  # First 10 headers
                    summary_parts.append(f"  • {header}")
        
        # For code files, identify the type and key features
        elif file_path.endswith('.py'):
            imports = [line.strip() for line in lines if line.strip().startswith('import ') or line.strip().startswith('from ')]
            functions = [line.strip() for line in lines if line.strip().startswith('def ')]
            classes = [line.strip() for line in lines if line.strip().startswith('class ')]
            
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
        
        return '\n'.join(summary_parts)
    
    def _show_repository_structure(self):
        """Show the repository structure."""
        print("\n📁 Repository Structure:")
        
        # Get directory structure
        dirs = ['python_scripts', 'shell_scripts', 'docs', 'text_files', '.github']
        
        for dir_name in dirs:
            dir_path = os.path.join(self.repository_root, dir_name)
            if os.path.isdir(dir_path):
                files = os.listdir(dir_path)
                print(f"  📂 {dir_name}/ ({len(files)} files)")
        
        # Show root files
        root_files = [f for f in os.listdir(self.repository_root) 
                     if os.path.isfile(os.path.join(self.repository_root, f)) 
                     and not f.startswith('.')]
        print(f"  📄 Root files: {len(root_files)}")
    
    def _suggest_available_scripts(self):
        """Suggest available scripts when script not found."""
        scripts = self._get_files_by_type('python') + self._get_files_by_type('shell')
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