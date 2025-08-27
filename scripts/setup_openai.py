#!/usr/bin/env python3
"""
OpenAI Integration Setup Script

This script helps users set up OpenAI integration for the AI Script Inventory.
It validates the OpenAI library installation and API key configuration.
"""

import os


def check_openai_library():
    """Check if OpenAI library is installed."""
    try:
        import openai

        print(f"✅ OpenAI library is installed (version {openai.__version__})")
        return True
    except ImportError:
        print("❌ OpenAI library is not installed")
        print("   Install with: pip install openai>=1.0.0")
        return False


def check_api_key():
    """Check if OpenAI API key is configured."""
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()

    if not api_key:
        print("❌ OpenAI API key is not configured")
        print("   Set with: export OPENAI_API_KEY='sk-your-api-key-here'")
        return False

    if not api_key.startswith("sk-"):
        print("⚠️  OpenAI API key does not start with 'sk-' - may be invalid format")
        return False

    print("✅ OpenAI API key is configured")
    return True


def test_openai_connection():
    """Test OpenAI API connection."""
    try:
        import openai

        client = openai.OpenAI()

        # Simple test API call
        response = client.models.list()
        print("✅ OpenAI API connection successful")
        print(f"   Available models: {len(response.data)} models found")
        return True

    except Exception as e:
        print(f"❌ OpenAI API connection failed: {e}")
        print("   Check your API key and internet connection")
        return False


def setup_instructions():
    """Provide setup instructions."""
    print("\n📋 Setup Instructions:")
    print("=" * 50)

    print("\n1. Install OpenAI library:")
    print("   pip install openai>=1.0.0")
    print("   # Or install full development dependencies:")
    print("   pip install -r requirements-dev.txt")

    print("\n2. Get your OpenAI API key:")
    print("   - Visit: https://platform.openai.com/api-keys")
    print("   - Create a new API key")
    print("   - Copy the key (starts with 'sk-')")

    print("\n3. Set your API key:")
    print("   export OPENAI_API_KEY='sk-your-api-key-here'")
    print("   # Or add to your shell profile:")
    print("   echo 'export OPENAI_API_KEY=\"sk-your-api-key-here\"' >> ~/.bashrc")

    print("\n4. Test the setup:")
    print("   python setup_openai.py")

    print("\n5. Use Superman CLI:")
    print("   python python_scripts/superman.py")


def main():
    """Main setup and validation function."""
    print("🤖 OpenAI Integration Setup for AI Script Inventory")
    print("=" * 60)

    # Check current status
    library_ok = check_openai_library()
    api_key_ok = check_api_key()

    if library_ok and api_key_ok:
        print("\n🔄 Testing OpenAI connection...")
        connection_ok = test_openai_connection()

        if connection_ok:
            print("\n🎉 OpenAI integration is fully configured!")
            print("   You can now use the Superman CLI with full AI features.")
            print("   Run: python python_scripts/superman.py")
        else:
            print("\n⚠️  OpenAI integration is partially configured")
            print("   Library and API key are set, but connection failed.")
    else:
        print("\n⚠️  OpenAI integration is not fully configured")
        setup_instructions()

    # Show current configuration status
    print("\n📊 Configuration Status:")
    print("=" * 30)
    print(f"OpenAI Library: {'✅' if library_ok else '❌'}")
    print(f"API Key Set:    {'✅' if api_key_ok else '❌'}")
    if library_ok and api_key_ok:
        connection_ok = test_openai_connection()
        print(f"API Connection: {'✅' if connection_ok else '❌'}")

    print("\n📚 Documentation:")
    print("   - OpenAI Integration Guide: docs/OPENAI_INTEGRATION.md")
    print("   - Superman CLI: python_scripts/superman.py")
    print("   - Terminal Guide: docs/TERMINAL_GUIDE.md")


if __name__ == "__main__":
    main()
