#!/usr/bin/env python3
"""
Superman AI Orchestrator

Enhanced AI terminal with advanced features including internet connectivity checks,
memory system, and code analysis capabilities.

This extends the SuperhumanTerminal with additional orchestration features
and startup connectivity validation.
"""

import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_script_inventory.superhuman_terminal import SuperhumanTerminal
from ai_script_inventory.ai.intent import IntentType, create_intent_recognizer


class MemorySystem:
    """Advanced memory system for storing conversation context and learning."""

    def __init__(self, max_memories: int = 100):
        """Initialize the memory system with configurable limits."""
        self.max_memories = max_memories
        self.memories = []
        self.session_start = os.environ.get('SESSION_START', 'now')

    def remember(self, user_input: str, response: str, intent_type: str = None) -> None:
        """Store a conversation exchange in memory."""
        import time
        memory = {
            'user_input': user_input,
            'response': response, 
            'intent_type': intent_type,
            'timestamp': time.time()
        }
        
        self.memories.append(memory)
        
        # Keep only the most recent memories
        if len(self.memories) > self.max_memories:
            self.memories = self.memories[-self.max_memories:]

    def get_recent_context(self, count: int = 5) -> str:
        """Get recent conversation context as formatted string."""
        recent = self.memories[-count:] if count <= len(self.memories) else self.memories
        context_parts = []
        
        for memory in recent:
            context_parts.append(memory['user_input'])
            context_parts.append(memory['response'])
            
        return ' '.join(context_parts)

    def search_memories(self, query: str) -> list:
        """Search through stored memories for matching content."""
        query_lower = query.lower()
        results = []
        
        for memory in self.memories:
            if (query_lower in memory['user_input'].lower() or 
                query_lower in memory['response'].lower()):
                results.append(memory)
                
        return results

    def store(self, key: str, value: str) -> None:
        """Store a key-value pair in memory (legacy interface)."""
        self.remember(f"store:{key}", value)

    def retrieve(self, key: str) -> Optional[str]:
        """Retrieve a value from memory (legacy interface)."""
        for memory in self.memories:
            if memory['user_input'] == f"store:{key}":
                return memory['response']
        return None

    def add_context(self, context: str) -> None:
        """Add context to the conversation (legacy interface)."""
        self.remember("context", context)

    def get_context(self) -> list:
        """Get the current context (legacy interface)."""
        return [m['response'] for m in self.memories if m['user_input'] == 'context']


class CodeAnalyzer:
    """Advanced code analysis system for understanding and improving code."""

    def __init__(self):
        """Initialize the code analyzer."""
        self.analysis_cache = {}
        self.repository_root = Path.cwd()

    def analyze_file(self, file_path: str) -> dict:
        """Analyze a code file and return comprehensive insights."""
        file_path = Path(file_path)
        
        if str(file_path) in self.analysis_cache:
            return self.analysis_cache[str(file_path)]

        if not file_path.exists():
            return {'error': f"File not found: {file_path}"}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            analysis = {
                'lines': len(content.splitlines()),
                'chars': len(content),
                'file_type': file_path.suffix,
            }

            # Determine language and analyze accordingly
            if file_path.suffix == '.py':
                analysis.update(self._analyze_python(content))
                analysis['language'] = 'python'
            elif file_path.suffix in ['.sh', '.bash']:
                analysis.update(self._analyze_shell(content))
                analysis['language'] = 'shell'
            elif file_path.suffix == '.md':
                analysis.update(self._analyze_markdown(content))
                analysis['language'] = 'markdown'
            else:
                analysis['language'] = 'unknown'

            self.analysis_cache[str(file_path)] = analysis
            return analysis

        except Exception as e:
            return {'error': str(e)}

    def _analyze_python(self, content: str) -> dict:
        """Analyze Python code content."""
        analysis = {
            'classes': content.count('class '),
            'functions': content.count('def '),
            'has_main': 'if __name__' in content,
            'has_docstring': '"""' in content or "'''" in content,
            'imports': []
        }
        
        # Count import statements
        lines = content.splitlines()
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                analysis['imports'].append(stripped)
                
        return analysis

    def _analyze_shell(self, content: str) -> dict:
        """Analyze shell script content."""
        return {
            'has_shebang': content.startswith('#!'),
            'has_error_handling': 'set -e' in content,
            'functions': content.count('() {'),
        }

    def _analyze_markdown(self, content: str) -> dict:
        """Analyze markdown content."""
        lines = content.splitlines()
        headers = sum(1 for line in lines if line.strip().startswith('#'))
        code_blocks = content.count('```')
        
        return {
            'headers': headers,
            'code_blocks': code_blocks // 2,  # Each block has start and end
        }

    def analyze_directory(self, dir_path: str) -> dict:
        """Analyze directory structure and contents."""
        dir_path = Path(dir_path)
        
        if not dir_path.is_dir():
            return {'error': f"Directory not found: {dir_path}"}
            
        try:
            files = list(dir_path.iterdir())
            file_types = {}
            total_scanned = 0
            
            for file_path in files:
                if file_path.is_file():
                    total_scanned += 1
                    ext = file_path.suffix
                    file_types[ext] = file_types.get(ext, 0) + 1
                    
            return {
                'total_files_scanned': total_scanned,
                'file_types': file_types,
                'directory': str(dir_path)
            }
            
        except Exception as e:
            return {'error': str(e)}


class SupermanOrchestrator(SuperhumanTerminal):
    """
    Superman AI Orchestrator that extends SuperhumanTerminal with additional features.
    
    Includes internet connectivity checking, memory system, and code analysis.
    """

    def __init__(self):
        """Initialize Superman orchestrator with enhanced capabilities."""
        super().__init__()
        
        # Initialize enhanced systems
        self.memory = MemorySystem()
        self.code_analyzer = CodeAnalyzer()
        self.superman_mode = False
        self.internet_available = False
        
        # Add enhanced action handlers
        if hasattr(self, 'action_handlers'):
            self.action_handlers.update({
                IntentType.AI_CHAT: self.handle_ai_chat_enhanced,
            })

    def check_internet_connectivity(self) -> bool:
        """
        Check for active internet connectivity by attempting to reach well-known websites.
        
        Returns:
            bool: True if internet is available, False otherwise
        """
        test_urls = [
            "https://www.google.com",
            "https://api.openai.com", 
            "https://httpbin.org/status/200"
        ]
        
        print("🌐 Checking internet connectivity...")
        
        for url in test_urls:
            try:
                # Try to open the URL with a short timeout
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'Superman-CLI/1.0'
                })
                
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status == 200:
                        print(f"✅ Internet access: AVAILABLE (verified via {url})")
                        self.internet_available = True
                        return True
                        
            except urllib.error.URLError as e:
                # DNS resolution failed or network error
                print(f"🔍 Testing {url}: {e.reason}")
                continue
            except Exception as e:
                # Other errors (timeout, etc.)
                print(f"🔍 Testing {url}: {type(e).__name__}: {e}")
                continue
        
        # All tests failed
        print("❌ Internet access: NOT AVAILABLE")
        print("⚠️  Warning: Operating in offline/limited mode")
        print("   • External API features will be disabled")
        print("   • Some online resources may not be accessible")
        print("   • Local-only processing will be used")
        
        self.internet_available = False
        return False

    def check_spacy_installation(self) -> None:
        """Check spaCy installation and model availability."""
        try:
            import spacy
            print(f"✅ spaCy version: {spacy.__version__}")
            
            try:
                nlp = spacy.load("en_core_web_sm")
                print("✅ spaCy model 'en_core_web_sm' loaded successfully")
            except OSError:
                print("⚠️  spaCy model 'en_core_web_sm' not found")
                print("   Install with: python -m spacy download en_core_web_sm")
                
        except ImportError:
            print("❌ spaCy not installed")
            print("   Install with: pip install spacy")

    def check_openai_connectivity(self) -> None:
        """Check OpenAI API connectivity and configuration."""
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            print("ℹ️  OpenAI API key not configured")
            print("   Set OPENAI_API_KEY environment variable for AI features")
            return
            
        if not api_key.startswith('sk-'):
            print("⚠️  OpenAI API key does not start with 'sk-' - may be invalid format")
            return
            
        if self.internet_available:
            print("✅ OpenAI API key configured (internet available for testing)")
        else:
            print("ℹ️  OpenAI API key configured (internet unavailable - cannot test)")

    def activate_superman_mode(self) -> None:
        """Activate Superman mode with enhanced capabilities."""
        self.superman_mode = True
        print("🦸 Superman mode activated!")
        print("  Enhanced AI capabilities enabled")

    def deactivate_superman_mode(self) -> None:
        """Deactivate Superman mode."""
        self.superman_mode = False
        print("👤 Superman mode deactivated")

    def handle_ai_chat_enhanced(self, intent) -> None:
        """Enhanced AI chat handler with memory and context."""
        # Add to memory context
        self.memory.add_context(intent.target or "")
        
        # Fall back to original AI chat handler
        self.handle_ai_chat(intent)

    def run(self) -> None:
        """Override run method to include startup checks."""
        # Perform startup connectivity check
        self.check_internet_connectivity()
        
        # Additional startup checks
        print("\n🔧 System checks:")
        self.check_spacy_installation() 
        self.check_openai_connectivity()
        
        print("\n" + "="*50)
        print("🦸 Superman AI Orchestrator Ready!")
        print("="*50)
        
        # Call parent run method
        super().run()


def main() -> None:
    """Main entry point for Superman CLI."""
    try:
        orchestrator = SupermanOrchestrator()
        orchestrator.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Superman startup error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()