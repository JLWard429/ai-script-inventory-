#!/usr/bin/env python3
"""
AI Script Inventory Health Check
===============================

Comprehensive health check to verify all systems are working and ready to use.
"""

import subprocess
import sys
import importlib
from pathlib import Path
import time


class HealthChecker:
    """Comprehensive health checker for the AI Script Inventory."""

    def __init__(self):
        """Initialize the health checker."""
        self.results = {}
        self.total_checks = 0
        self.passed_checks = 0

    def check(self, name: str, condition: bool, details: str = ""):
        """Record a health check result."""
        self.total_checks += 1
        if condition:
            self.passed_checks += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        print(f"{status} {name}")
        if details:
            print(f"    {details}")
        
        self.results[name] = {
            "passed": condition,
            "details": details
        }
        return condition

    def check_dependencies(self):
        """Check that all required dependencies are installed."""
        print("\n🔍 Checking Dependencies...")
        
        # Core dependencies
        try:
            import spacy
            self.check("spaCy installed", True, f"Version {spacy.__version__}")
        except ImportError:
            self.check("spaCy installed", False, "spaCy not found")

        try:
            import yaml
            self.check("PyYAML installed", True)
        except ImportError:
            self.check("PyYAML installed", False, "PyYAML not found")

        # Check spaCy model
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            self.check("spaCy English model loaded", True, "en_core_web_sm available")
        except Exception as e:
            self.check("spaCy English model loaded", False, str(e))

    def check_package_installation(self):
        """Check that the package is properly installed."""
        print("\n📦 Checking Package Installation...")
        
        try:
            import ai_script_inventory
            self.check("ai-script-inventory package installed", True)
        except ImportError:
            self.check("ai-script-inventory package installed", False, "Package not installed")

        try:
            from ai_script_inventory.superhuman_terminal import SuperhumanTerminal
            self.check("SuperhumanTerminal importable", True)
        except ImportError as e:
            self.check("SuperhumanTerminal importable", False, str(e))

        try:
            from ai_script_inventory.ai.intent import create_intent_recognizer
            self.check("Intent recognizer importable", True)
        except ImportError as e:
            self.check("Intent recognizer importable", False, str(e))

    def check_intent_recognition(self):
        """Check that intent recognition is working."""
        print("\n🧠 Checking AI Intent Recognition...")
        
        try:
            from ai_script_inventory.ai.intent import create_intent_recognizer, IntentType
            recognizer = create_intent_recognizer()
            
            # Test basic commands
            test_cases = [
                ("help", IntentType.HELP),
                ("exit", IntentType.EXIT),
                ("list files", IntentType.LIST),
                ("run script.py", IntentType.RUN_SCRIPT),
                ("what can you do?", IntentType.AI_CHAT),
            ]
            
            all_passed = True
            for prompt, expected_type in test_cases:
                intent = recognizer.recognize(prompt)
                if intent.type == expected_type:
                    continue
                else:
                    all_passed = False
                    break
            
            self.check("Intent recognition working", all_passed, f"Tested {len(test_cases)} examples")
            
        except Exception as e:
            self.check("Intent recognition working", False, str(e))

    def check_file_structure(self):
        """Check that required directories and files exist."""
        print("\n📁 Checking File Structure...")
        
        required_dirs = [
            "src/ai_script_inventory",
            "tests",
            "python_scripts",
            "shell_scripts",
            "docs",
            ".github/workflows"
        ]
        
        for dir_path in required_dirs:
            exists = Path(dir_path).exists()
            self.check(f"Directory {dir_path} exists", exists)

        required_files = [
            "src/ai_script_inventory/superhuman_terminal.py",
            "src/ai_script_inventory/ai/intent.py",
            "python_scripts/terminal.py",
            "pyproject.toml",
            "README.md"
        ]
        
        for file_path in required_files:
            exists = Path(file_path).exists()
            self.check(f"File {file_path} exists", exists)

    def check_tests(self):
        """Check that core tests are passing."""
        print("\n🧪 Checking Test Suite...")
        
        try:
            # Run key tests
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "tests/test_basic.py", 
                "tests/test_superhuman_terminal.py",
                "-v", "--tb=short"
            ], capture_output=True, text=True, timeout=60)
            
            passed = result.returncode == 0
            details = f"Exit code: {result.returncode}"
            if not passed and result.stdout:
                details += f", Output: {result.stdout[-200:]}"
            
            self.check("Core tests passing", passed, details)
            
        except subprocess.TimeoutExpired:
            self.check("Core tests passing", False, "Tests timed out")
        except Exception as e:
            self.check("Core tests passing", False, str(e))

    def check_terminal_functionality(self):
        """Check that the terminal can start up."""
        print("\n🚀 Checking Terminal Functionality...")
        
        try:
            # Test terminal import and initialization
            from ai_script_inventory.superhuman_terminal import SuperhumanTerminal
            terminal = SuperhumanTerminal()
            self.check("Terminal initialization", True, "SuperhumanTerminal created successfully")
            
            # Test intent recognizer creation
            recognizer_exists = hasattr(terminal, 'intent_recognizer') and terminal.intent_recognizer is not None
            self.check("Intent recognizer initialized", recognizer_exists)
            
            # Test action handlers
            handlers_exist = hasattr(terminal, 'action_handlers') and len(terminal.action_handlers) > 0
            self.check("Action handlers configured", handlers_exist, f"{len(terminal.action_handlers) if handlers_exist else 0} handlers")
            
        except Exception as e:
            self.check("Terminal initialization", False, str(e))

    def check_launcher(self):
        """Check that the terminal launcher works."""
        print("\n🎯 Checking Terminal Launcher...")
        
        try:
            # Test that the launcher script exists and is valid
            launcher_path = Path("python_scripts/terminal.py")
            if launcher_path.exists():
                with open(launcher_path) as f:
                    content = f.read()
                    compile(content, launcher_path, "exec")
                self.check("Terminal launcher syntax", True, "python_scripts/terminal.py is valid")
            else:
                self.check("Terminal launcher syntax", False, "Launcher not found")
                
        except Exception as e:
            self.check("Terminal launcher syntax", False, str(e))

    def run_all_checks(self):
        """Run all health checks."""
        print("🏥 AI Script Inventory Health Check")
        print("=" * 50)
        
        self.check_dependencies()
        self.check_package_installation()
        self.check_file_structure()
        self.check_intent_recognition()
        self.check_terminal_functionality()
        self.check_launcher()
        self.check_tests()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 HEALTH CHECK SUMMARY")
        print("=" * 50)
        
        success_rate = (self.passed_checks / self.total_checks) * 100 if self.total_checks > 0 else 0
        
        if success_rate >= 90:
            status_emoji = "🟢"
            status_text = "EXCELLENT"
        elif success_rate >= 75:
            status_emoji = "🟡"
            status_text = "GOOD"
        elif success_rate >= 50:
            status_emoji = "🟠"
            status_text = "NEEDS WORK"
        else:
            status_emoji = "🔴"
            status_text = "CRITICAL"
        
        print(f"{status_emoji} Overall Status: {status_text}")
        print(f"✅ Passed: {self.passed_checks}/{self.total_checks} ({success_rate:.1f}%)")
        
        if self.passed_checks < self.total_checks:
            print(f"❌ Failed: {self.total_checks - self.passed_checks}")
            print("\nFailed Checks:")
            for name, result in self.results.items():
                if not result["passed"]:
                    print(f"  • {name}: {result['details']}")
        
        print("\n🎯 Ready to Use Status:")
        if success_rate >= 90:
            print("✅ The AI Script Inventory is READY TO USE!")
            print("🚀 You can start the Superhuman Terminal with:")
            print("   python python_scripts/terminal.py")
        elif success_rate >= 75:
            print("⚠️ The system is mostly functional but has some issues.")
            print("🔧 Consider addressing the failed checks before full use.")
        else:
            print("❌ The system has significant issues that should be resolved.")
            print("🛠️ Please fix the failed checks before using.")
        
        return success_rate >= 75


def main():
    """Run the health check."""
    checker = HealthChecker()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()