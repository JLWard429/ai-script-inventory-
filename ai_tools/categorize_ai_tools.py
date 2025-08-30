import os

# Directory containing your AI scripts
TOOLS_DIR = "ai_tools"

# Keywords for third-party, github, and custom scripts (add more as needed)
THIRD_PARTY_KEYWORDS = [
    "openai", "anthropic", "vertex", "fireworks", "huggingface", "cohere", "bedrock", "amazon",
    "lakera", "watsonx", "fal_ai", "langfuse", "langsmith", "litellm", "gemini", "mlflow", "ollama"
]
GITHUB_KEYWORDS = [
    "github", "codeql", "repo"
]
CUSTOM_KEYWORDS = [
    "custom", "my_", "ai_memory", "agent", "planner", "workflow", "llm_as", "ai_assistant"
]

def categorize_file(filename):
    name = filename.lower()
    if any(kw in name for kw in THIRD_PARTY_KEYWORDS):
        return "Third-Party"
    if any(kw in name for kw in GITHUB_KEYWORDS):
        return "GitHub-Related"
    if any(kw in name for kw in CUSTOM_KEYWORDS):
        return "Custom"
    return "Unclassified"

def main():
    files = [f for f in os.listdir(TOOLS_DIR) if f.endswith(".py")]
    categorized = {"Third-Party": [], "GitHub-Related": [], "Custom": [], "Unclassified": []}
    for fname in sorted(files):
        cat = categorize_file(fname)
        categorized[cat].append(fname)
    
    # Output to Markdown file
    with open(os.path.join(TOOLS_DIR, "AI_TOOL_CATEGORIZATION.md"), "w") as md:
        md.write("# AI Tool Categorization\n\n")
        for cat, flist in categorized.items():
            md.write(f"## {cat}\n")
            if flist:
                for f in flist:
                    md.write(f"- `{f}`\n")
            else:
                md.write("_None_\n")
            md.write("\n")
    print("Categorization complete. See 'ai_tools/AI_TOOL_CATEGORIZATION.md'.")

if __name__ == "__main__":
    main()
