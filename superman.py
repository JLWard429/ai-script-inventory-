#!/usr/bin/env python3
"""
Superman.py - AI Orchestrator Script

An all-in-one AI orchestrator that combines spaCy-powered natural language processing
with OpenAI integration for comprehensive AI assistance. This script acts as an intelligent
command center that automatically determines which tools and logic to use based on user requests.

USAGE:
    python superman.py

After running the script, type 'superman' to enter AI orchestrator mode.
Then you can issue any natural language request and the system will:
1. Use spaCy to analyze and understand your intent
2. Route to appropriate local tools and scripts when possible
3. Use OpenAI for general conversation and complex queries
4. Maintain conversation memory across the session
5. Provide code analysis capabilities

FEATURES:
    ✨ Natural Language Processing - Advanced spaCy-powered intent recognition
    🤖 OpenAI Integration - GPT models for general AI tasks and conversations
    🧠 Memory System - Basic conversation memory for context awareness
    🔍 Code Analysis - Analyze and understand code structures and patterns
    📁 File Operations - List, search, preview, and manage repository files
    🛠️ Script Execution - Run Python and shell scripts with natural language commands
    📝 Document Processing - Summarize and analyze markdown and text files
    🔧 Easy Expansion - Modular architecture for adding new capabilities

EXAMPLES:
    # Enter AI orchestrator mode
    > superman

    # Natural language commands
    Superman > analyze the code in src/ai_script_inventory/
    Superman > summarize the latest README file
    Superman > run security scan on all Python files
    Superman > what can you tell me about this repository?
    Superman > help me understand the spaCy integration
    Superman > create a summary of recent changes

ARCHITECTURE:
    - Built on existing SuperhumanTerminal infrastructure
    - spaCy for local intent recognition and NLP
    - OpenAI for general AI conversations and complex queries
    - Modular design for easy extension
    - Local-first approach with cloud AI as fallback

PRIVACY:
    - Prioritizes local processing with spaCy
    - Only uses OpenAI for general conversation when local tools insufficient
    - User controls what data is sent to external APIs
    - Maintains conversation history locally

DEPENDENCIES:
    - spacy (>=3.8.0) with en_core_web_sm model
    - openai (>=1.0.0) - optional, for AI conversations
    - All dependencies from the existing superhuman terminal

ENVIRONMENT VARIABLES:
    - OPENAI_API_KEY: Required for OpenAI integration (optional feature)
    - SUPERMAN_DEBUG: Set to "1", "true", or "yes" to enable debug logging

To install dependencies:
    pip install -r requirements-dev.txt
    python -m spacy download en_core_web_sm

For OpenAI features (optional):
    pip install openai
    export OPENAI_API_KEY="your-api-key-here"

For debugging OpenAI issues:
    export SUPERMAN_DEBUG=1
    python superman.py
"""

import datetime
import json
import logging
import os
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Add src to path for imports
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import existing terminal infrastructure
try:
    from ai_script_inventory.ai.intent import (
        Intent,
        IntentType,
        create_intent_recognizer,
    )
    from ai_script_inventory.superhuman_terminal import SuperhumanTerminal
except ImportError as e:
    print(f"❌ Error importing superhuman terminal: {e}")
    print(
        "Please ensure you're running from the repository root and dependencies are installed:"
    )
    print("  pip install -r requirements-dev.txt")
    print("  python -m spacy download en_core_web_sm")
    sys.exit(1)

# Optional OpenAI import
try:
    import openai

    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class MemorySystem:
    """Basic conversation memory system for maintaining context."""

    def __init__(self, max_memories: int = 100):
        """Initialize memory system with maximum memory capacity."""
        self.memories: List[Dict[str, Any]] = []
        self.max_memories = max_memories
        self.session_start = datetime.datetime.now()

    def remember(
        self,
        user_input: str,
        response: str,
        intent_type: str = None,
        metadata: Dict[str, Any] = None,
    ) -> None:
        """Store a conversation exchange in memory."""
        memory = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_input": user_input,
            "response": response,
            "intent_type": intent_type,
            "metadata": metadata or {},
        }

        self.memories.append(memory)

        # Keep memory size manageable
        if len(self.memories) > self.max_memories:
            self.memories = self.memories[-self.max_memories :]

    def get_recent_context(self, num_exchanges: int = 5) -> str:
        """Get recent conversation context as formatted string."""
        if not self.memories:
            return "No previous conversation context."

        recent = self.memories[-num_exchanges:]
        context_parts = []

        for memory in recent:
            timestamp = memory["timestamp"]
            user_input = memory["user_input"]
            response = (
                memory["response"][:200] + "..."
                if len(memory["response"]) > 200
                else memory["response"]
            )

            context_parts.append(f"[{timestamp}] User: {user_input}")
            context_parts.append(f"[{timestamp}] Assistant: {response}")

        return "\n".join(context_parts)

    def search_memories(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search through conversation history for relevant memories."""
        query_lower = query.lower()
        matching_memories = []

        for memory in self.memories:
            if (
                query_lower in memory["user_input"].lower()
                or query_lower in memory["response"].lower()
            ):
                matching_memories.append(memory)

        return matching_memories[-max_results:]


class CodeAnalyzer:
    """Basic code analysis system for understanding code structures and patterns."""

    def __init__(self):
        """Initialize the code analyzer."""
        self.repository_root = Path(__file__).parent

    def analyze_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Analyze a single code file and return insights."""
        file_path = Path(file_path)

        if not file_path.exists():
            return {"error": f"File not found: {file_path}"}

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            return {"error": f"Could not read file: {e}"}

        analysis = {
            "file_path": str(file_path),
            "file_size": len(content),
            "line_count": len(content.split("\n")),
            "file_type": file_path.suffix,
        }

        # Python-specific analysis
        if file_path.suffix == ".py":
            analysis.update(self._analyze_python_file(content))

        # Shell script analysis
        elif file_path.suffix == ".sh":
            analysis.update(self._analyze_shell_file(content))

        # Markdown analysis
        elif file_path.suffix == ".md":
            analysis.update(self._analyze_markdown_file(content))

        return analysis

    def _analyze_python_file(self, content: str) -> Dict[str, Any]:
        """Analyze Python file content."""
        lines = content.split("\n")

        imports = [
            line.strip()
            for line in lines
            if line.strip().startswith(("import ", "from "))
        ]
        classes = [line.strip() for line in lines if line.strip().startswith("class ")]
        functions = [
            line.strip()
            for line in lines
            if line.strip().startswith("def ") and "class " not in line
        ]

        return {
            "language": "python",
            "imports": imports[:10],  # First 10 imports
            "classes": len(classes),
            "functions": len(functions),
            "has_main": (
                "if __name__ == '__main__':" in content
                or 'if __name__ == "__main__":' in content
            ),
            "has_docstring": '"""' in content or "'''" in content,
        }

    def _analyze_shell_file(self, content: str) -> Dict[str, Any]:
        """Analyze shell script content."""
        lines = content.split("\n")

        functions = [line.strip() for line in lines if "() {" in line]

        return {
            "language": "shell",
            "has_shebang": content.startswith("#!"),
            "functions": len(functions),
            "has_error_handling": "set -e" in content,
        }

    def _analyze_markdown_file(self, content: str) -> Dict[str, Any]:
        """Analyze markdown file content."""
        lines = content.split("\n")

        headers = [line.strip() for line in lines if line.strip().startswith("#")]
        code_blocks = content.count("```")

        return {
            "language": "markdown",
            "headers": len(headers),
            "code_blocks": code_blocks // 2,  # Each code block has opening and closing
            "has_toc": "## Table of Contents" in content
            or "# Table of Contents" in content,
        }

    def analyze_directory(
        self, directory_path: Union[str, Path], max_files: int = 20
    ) -> Dict[str, Any]:
        """Analyze a directory structure and provide insights."""
        directory_path = Path(directory_path)

        if not directory_path.exists() or not directory_path.is_dir():
            return {"error": f"Directory not found: {directory_path}"}

        file_types = {}
        total_files = 0
        total_size = 0
        file_analyses = []

        # Walk through directory
        for file_path in directory_path.rglob("*"):
            if file_path.is_file() and total_files < max_files:
                file_analysis = self.analyze_file(file_path)
                if "error" not in file_analysis:
                    file_analyses.append(file_analysis)

                    file_type = file_path.suffix or "no_extension"
                    file_types[file_type] = file_types.get(file_type, 0) + 1
                    total_size += file_analysis.get("file_size", 0)

                total_files += 1

        return {
            "directory_path": str(directory_path),
            "total_files_scanned": len(file_analyses),
            "total_files_found": total_files,
            "file_types": file_types,
            "total_size_bytes": total_size,
            "file_analyses": file_analyses,
        }


class SupermanOrchestrator(SuperhumanTerminal):
    """Enhanced AI orchestrator that extends SuperhumanTerminal with AI and analysis capabilities."""

    def __init__(self):
        """Initialize the Superman AI orchestrator."""
        super().__init__()

        # Fix repository root to be the actual repository root, not the src directory
        self.repository_root = str(Path(__file__).parent)

        # Set up debug mode from environment variable
        self.debug_mode = os.getenv("SUPERMAN_DEBUG", "").lower() in (
            "1",
            "true",
            "yes",
        )

        # Set up logging if debug mode is enabled
        if self.debug_mode:
            logging.basicConfig(
                level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
            )
            logging.debug("Superman debug mode enabled")

        # Initialize additional systems
        self.memory = MemorySystem()
        self.code_analyzer = CodeAnalyzer()
        self.superman_mode = False

        # Initialize OpenAI if available
        self.openai_client = None
        if HAS_OPENAI:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                # Strip whitespace and validate API key
                api_key = api_key.strip()
                if self.debug_mode:
                    # Safely log API key status without exposing the actual key
                    key_prefix = api_key[:7] if len(api_key) >= 7 else "***"
                    key_suffix = api_key[-4:] if len(api_key) >= 4 else "***"
                    masked_key = (
                        f"{key_prefix}...{key_suffix}" if len(api_key) > 11 else "***"
                    )
                    logging.debug(
                        f"OpenAI API key found: {masked_key} (length: {len(api_key)})"
                    )

                if not api_key:
                    print("⚠️ OpenAI API key is empty after stripping whitespace")
                elif not api_key.startswith("sk-"):
                    print(
                        "⚠️ OpenAI API key does not start with 'sk-' - this may cause authentication errors"
                    )
                    if self.debug_mode:
                        logging.debug(f"API key starts with: {api_key[:10]}...")

                try:
                    self.openai_client = openai.OpenAI(api_key=api_key)
                    print("🤖 OpenAI integration enabled")
                    if self.debug_mode:
                        logging.debug("OpenAI client initialized successfully")
                except Exception as e:
                    print(f"⚠️ OpenAI initialization failed: {e}")
                    if self.debug_mode:
                        logging.debug(
                            f"OpenAI initialization error details: {traceback.format_exc()}"
                        )
            else:
                print(
                    "💡 Set OPENAI_API_KEY environment variable to enable AI conversations"
                )
                if self.debug_mode:
                    logging.debug("No OPENAI_API_KEY environment variable found")
        else:
            print(
                "💡 Install 'openai' package to enable AI conversations: pip install openai"
            )
            if self.debug_mode:
                logging.debug("OpenAI package not available")

        # Add new intent handlers for Superman-specific features
        if hasattr(self, "action_handlers"):
            self.action_handlers.update(
                {
                    IntentType.AI_CHAT: self.handle_ai_chat_enhanced,
                }
            )

        # Add custom Superman commands
        self.superman_commands = {
            "memory": self.show_memory,
            "analyze": self.handle_code_analysis,
            "status": self.show_status,
            "demo": self.run_spacy_demo,
        }

    def run(self):
        """Enhanced main terminal loop with Superman mode."""
        self.print_superman_welcome()

        while self.running:
            try:
                if self.superman_mode:
                    user_input = input("\n🦸 Superman > ").strip()
                else:
                    user_input = input("\n🤖 > ").strip()

                if not user_input:
                    continue

                # Check for Superman mode activation
                if not self.superman_mode and user_input.lower() == "superman":
                    self.activate_superman_mode()
                    continue

                # Check for Superman mode deactivation
                if self.superman_mode and user_input.lower() in [
                    "exit superman",
                    "normal",
                    "regular",
                ]:
                    self.deactivate_superman_mode()
                    continue

                # Add to history
                self.history.append(user_input)

                # Process the input
                response = self.process_input(user_input)

                # Remember the interaction
                self.memory.remember(user_input, response)

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye from Superman!")
                break
            except EOFError:
                print("\n\n👋 Goodbye from Superman!")
                break
            except Exception as e:
                error_msg = f"❌ Error: {e}"
                print(error_msg)
                self.memory.remember(
                    user_input if "user_input" in locals() else "unknown", error_msg
                )

    def process_input(self, user_input: str) -> str:
        """Process user input with enhanced AI capabilities."""
        # Check for direct Superman commands first
        if self.superman_mode:
            first_word = user_input.split()[0].lower() if user_input.split() else ""
            if first_word in self.superman_commands:
                try:
                    result = self.superman_commands[first_word](user_input)
                    return result or "Command executed successfully."
                except Exception as e:
                    return f"Error executing {first_word}: {e}"

        # Use existing intent recognition
        intent = self.intent_recognizer.recognize(user_input)

        # Enhanced handling for AI chat in Superman mode
        if intent.type == IntentType.AI_CHAT and self.superman_mode:
            return self.handle_ai_chat_enhanced(intent)

        # Handle using existing terminal infrastructure
        self.handle_intent(intent)
        return f"Processed {intent.type.value} command with confidence {intent.confidence:.2f}"

    def activate_superman_mode(self):
        """Activate Superman AI orchestrator mode."""
        self.superman_mode = True
        print(
            """
🦸‍♂️ SUPERMAN MODE ACTIVATED! 🦸‍♂️

You are now in AI Orchestrator mode. I can help you with:

🧠 Natural Language Commands:
  • "analyze the code in src/"
  • "summarize the latest README"
  • "run security scan on Python files"
  • "what's in this repository?"

🤖 AI Conversations:
  • Ask questions about code, documentation, or best practices
  • Get explanations of complex concepts
  • Brainstorm solutions to problems

🔍 Code Analysis:
  • "analyze [file/directory]" - Deep code analysis
  • "status" - Show system status and capabilities

💭 Memory & Context:
  • "memory" - Show conversation history
  • I remember our previous interactions

🎯 spaCy NLP Demo:
  • "demo" - See advanced natural language processing in action

Type "exit superman" to return to normal terminal mode.
"""
        )

    def deactivate_superman_mode(self):
        """Deactivate Superman mode and return to normal terminal."""
        self.superman_mode = False
        print(
            "\n🤖 Returned to normal terminal mode. Type 'superman' to re-enter AI orchestrator mode."
        )

    def handle_ai_chat_enhanced(self, intent: Intent) -> str:
        """Enhanced AI chat with OpenAI integration and memory context."""
        user_input = intent.original_input

        # If in Superman mode and OpenAI is available, use it for complex queries
        if self.superman_mode and self.openai_client:
            try:
                if self.debug_mode:
                    logging.debug(
                        f"Making OpenAI API call for input: {user_input[:50]}..."
                    )

                # Get conversation context
                context = self.memory.get_recent_context(3)

                # Create system prompt with context
                system_prompt = f"""You are Superman, an AI orchestrator for a code repository management system. 
You have access to advanced spaCy NLP capabilities and can help with code analysis, documentation, 
and repository management.

Recent conversation context:
{context}

Repository info: This is an AI Script Inventory with Python scripts, shell scripts, documentation, 
and an advanced terminal system with spaCy integration for natural language processing.

Be helpful, concise, and technical when appropriate. If the user asks about specific files or code,
let them know they can use commands like 'analyze [path]' for detailed code analysis."""

                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input},
                    ],
                    max_tokens=500,
                    temperature=0.7,
                )

                ai_response = response.choices[0].message.content
                print(f"\n🤖 Superman AI: {ai_response}")

                if self.debug_mode:
                    logging.debug(
                        f"OpenAI API call successful, response length: {len(ai_response)}"
                    )

                return ai_response

            except Exception as e:
                error_msg = str(e)
                print(f"\n⚠️ OpenAI error: {error_msg}")

                # Provide more specific error guidance
                if "incorrect api key" in error_msg.lower():
                    print("🔑 This suggests an issue with your OpenAI API key.")
                    print("   Please check that:")
                    print("   1. OPENAI_API_KEY environment variable is set correctly")
                    print("   2. The API key is valid and active")
                    print("   3. The API key has the correct permissions")
                    if self.debug_mode:
                        # Check current environment variable
                        current_key = os.getenv("OPENAI_API_KEY", "")
                        if current_key:
                            current_key = current_key.strip()
                            key_prefix = (
                                current_key[:7] if len(current_key) >= 7 else "***"
                            )
                            key_suffix = (
                                current_key[-4:] if len(current_key) >= 4 else "***"
                            )
                            masked_key = (
                                f"{key_prefix}...{key_suffix}"
                                if len(current_key) > 11
                                else "***"
                            )
                            logging.debug(
                                f"Current API key: {masked_key} (length: {len(current_key)})"
                            )
                        else:
                            logging.debug("No API key found in environment")
                elif "rate limit" in error_msg.lower():
                    print(
                        "⏱️ Rate limit exceeded. Please wait a moment before trying again."
                    )
                elif "quota" in error_msg.lower():
                    print("💳 API quota exceeded. Please check your OpenAI billing.")

                if self.debug_mode:
                    logging.debug(f"OpenAI API error details: {traceback.format_exc()}")

                print("Falling back to local processing...")

        # Fallback to original AI chat handling
        return (
            super().handle_ai_chat(intent)
            or "I understand your query, but I need more specific information to help effectively."
        )

    def handle_code_analysis(self, user_input: str) -> str:
        """Handle code analysis requests."""
        # Extract target from input
        parts = user_input.split(maxsplit=1)
        if len(parts) < 2:
            print("\n🔍 Usage: analyze <file_or_directory_path>")
            print("Examples:")
            print("  analyze src/ai_script_inventory/")
            print("  analyze superman.py")
            print("  analyze .")
            return "Please specify a file or directory to analyze."

        target = parts[1].strip()
        target_path = (
            Path(self.repository_root) / target
            if not Path(target).is_absolute()
            else Path(target)
        )

        print(f"\n🔍 Analyzing: {target_path}")

        if target_path.is_file():
            analysis = self.code_analyzer.analyze_file(target_path)
        elif target_path.is_dir():
            analysis = self.code_analyzer.analyze_directory(target_path)
        else:
            return f"❌ Path not found: {target_path}"

        # Format and display analysis
        self._display_analysis(analysis)
        return "Code analysis completed."

    def _display_analysis(self, analysis: Dict[str, Any]):
        """Display code analysis results in a formatted way."""
        if "error" in analysis:
            print(f"❌ {analysis['error']}")
            return

        print(f"📊 Analysis Results:")
        print(
            f"   Path: {analysis.get('file_path', analysis.get('directory_path', 'unknown'))}"
        )

        if "directory_path" in analysis:
            # Directory analysis
            print(f"   Files scanned: {analysis['total_files_scanned']}")
            print(f"   Total files found: {analysis['total_files_found']}")
            print(f"   Total size: {analysis['total_size_bytes']:,} bytes")
            print(f"   File types: {analysis['file_types']}")
        else:
            # File analysis
            print(f"   Size: {analysis['file_size']:,} bytes")
            print(f"   Lines: {analysis['line_count']:,}")
            print(f"   Type: {analysis['file_type']}")

            if analysis.get("language") == "python":
                print(f"   Classes: {analysis['classes']}")
                print(f"   Functions: {analysis['functions']}")
                print(f"   Has main: {analysis['has_main']}")
                print(f"   Has docstring: {analysis['has_docstring']}")
                if analysis["imports"]:
                    print(f"   Key imports: {', '.join(analysis['imports'][:5])}")

    def show_memory(self, user_input: str = None) -> str:
        """Show conversation memory and context."""
        print("\n🧠 Conversation Memory:")
        print(f"   Session started: {self.memory.session_start}")
        print(f"   Total exchanges: {len(self.memory.memories)}")

        if self.memory.memories:
            print("\n📝 Recent conversations:")
            recent_context = self.memory.get_recent_context(5)
            print(recent_context)
        else:
            print("   No conversation history yet.")

        return "Memory status displayed."

    def show_status(self, user_input: str = None) -> str:
        """Show Superman orchestrator status and capabilities."""
        print(f"\n🦸‍♂️ Superman AI Orchestrator Status:")
        print(
            f"   Mode: {'🦸 Superman Mode' if self.superman_mode else '🤖 Normal Mode'}"
        )
        print(f"   Debug mode: {'✅' if self.debug_mode else '❌'}")
        print(
            f"   spaCy available: {'✅' if hasattr(self.intent_recognizer, 'use_spacy') and self.intent_recognizer.use_spacy else '❌'}"
        )
        openai_status = "✅" if self.openai_client else "❌"
        if self.openai_client and self.debug_mode:
            # Show API key status in debug mode
            api_key = os.getenv("OPENAI_API_KEY", "").strip()
            if api_key:
                key_prefix = api_key[:7] if len(api_key) >= 7 else "***"
                key_suffix = api_key[-4:] if len(api_key) >= 4 else "***"
                masked_key = (
                    f"{key_prefix}...{key_suffix}" if len(api_key) > 11 else "***"
                )
                openai_status += f" (key: {masked_key})"
        print(f"   OpenAI available: {openai_status}")
        print(f"   Memory system: ✅ ({len(self.memory.memories)} memories)")
        print(f"   Code analyzer: ✅")
        print(f"   Repository root: {self.repository_root}")

        if self.debug_mode:
            print(f"\n🔧 Debug Information:")
            print(f"   Environment variables:")
            print(
                f"     OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}"
            )
            print(f"     SUPERMAN_DEBUG: {os.getenv('SUPERMAN_DEBUG', 'Not set')}")

        print(f"\n🛠️ Available capabilities:")
        print(f"   • Natural language command processing")
        print(f"   • File and directory analysis")
        print(f"   • Script execution and management")
        print(f"   • Document summarization")
        print(f"   • Conversation memory")
        print(f"   • spaCy NLP demonstrations")

        return "Status information displayed."

    def run_spacy_demo(self, user_input: str = None) -> str:
        """Run a spaCy NLP demonstration."""
        if (
            not hasattr(self.intent_recognizer, "use_spacy")
            or not self.intent_recognizer.use_spacy
        ):
            print("❌ spaCy not available for demonstration.")
            return "spaCy demo unavailable."

        print("\n🧠 spaCy NLP Demonstration")
        print("=" * 50)

        # Sample text for analysis
        sample_text = "Run security scan on all Python files in the shell_scripts directory and then summarize the latest README file."

        print(f"📝 Sample input: '{sample_text}'")
        print("\n🔍 spaCy Analysis:")

        try:
            # Get the spaCy document
            doc = self.intent_recognizer.nlp(sample_text)

            # Show tokens and their properties
            print("\n🔤 Token Analysis:")
            for token in doc:
                print(
                    f"   {token.text:15} | POS: {token.pos_:10} | Lemma: {token.lemma_:15} | Dep: {token.dep_}"
                )

            # Show named entities
            print(f"\n🏷️ Named Entities:")
            for ent in doc.ents:
                print(f"   {ent.text:20} | {ent.label_:15} | {ent.text}")

            # Show noun phrases
            print(f"\n📝 Noun Phrases:")
            for chunk in doc.noun_chunks:
                print(f"   {chunk.text}")

            # Show sentence structure
            print(f"\n📖 Sentences:")
            for sent in doc.sents:
                print(f"   {sent.text}")

            # Show intent recognition result
            print(f"\n🎯 Intent Recognition:")
            intent = self.intent_recognizer.recognize(sample_text)
            print(f"   Detected intent: {intent.type.value}")
            print(f"   Confidence: {intent.confidence:.2f}")
            print(f"   Target: {intent.target}")
            print(f"   Parameters: {intent.parameters}")

        except Exception as e:
            print(f"❌ Error in spaCy demo: {e}")

        return "spaCy demonstration completed."

    def print_superman_welcome(self):
        """Print Superman-specific welcome message."""
        print(
            """
╔══════════════════════════════════════════════════════════════════════════════╗
║                           🦸‍♂️ SUPERMAN AI ORCHESTRATOR 🦸‍♂️                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Welcome to the all-in-one AI orchestrator! This system combines:           ║
║                                                                              ║
║  🧠 Advanced spaCy NLP     🤖 OpenAI Integration    🔍 Code Analysis         ║
║  💭 Memory System          📁 File Operations       🛠️ Script Execution      ║
║                                                                              ║
║  Type 'superman' to enter AI Orchestrator mode for enhanced capabilities    ║
║  Type 'help' for available commands, or just start with natural language!   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        )


def main():
    """Main entry point for Superman AI Orchestrator."""
    try:
        orchestrator = SupermanOrchestrator()
        orchestrator.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye from Superman!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
