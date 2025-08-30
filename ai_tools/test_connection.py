#!/usr/bin/env python3
import os
import openai

# Load OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

try:
    # Simple test request
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, are you working?"}
        ]
    )
    print("✅ Connection successful!")
    print(f"Response: {completion.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {e}")
