#!/usr/bin/env python3
"""
Employee spaCy Test Script

Demonstrates how delegation works in the Superman orchestrator by performing
spaCy-based natural language processing tasks on user-provided text.

This script serves as an example employee that can be called by Superman
to handle specific NLP tasks using spaCy.

Usage:
    python employee_spacy_test.py [text]
    python employee_spacy_test.py "analyze this sentence"

Examples:
    python employee_spacy_test.py "The quick brown fox jumps over the lazy dog"
    python employee_spacy_test.py "Apple Inc. is planning to release a new iPhone in California"
"""

import sys
import argparse
from pathlib import Path


def analyze_text_with_spacy(text: str) -> dict:
    """Analyze text using spaCy and return structured results."""
    try:
        import spacy

        # Load the English model
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            return {
                "error": "spaCy model 'en_core_web_sm' not found",
                "suggestion": "Run: python -m spacy download en_core_web_sm",
            }

        # Process the text
        doc = nlp(text)

        # Extract information
        results = {
            "original_text": text,
            "tokens": [],
            "entities": [],
            "pos_tags": [],
            "dependencies": [],
            "sentences": [],
            "summary": {
                "total_tokens": len(doc),
                "total_entities": len(doc.ents),
                "total_sentences": len(list(doc.sents)),
            },
        }

        # Tokenization and POS tagging
        for token in doc:
            results["tokens"].append(
                {
                    "text": token.text,
                    "lemma": token.lemma_,
                    "pos": token.pos_,
                    "tag": token.tag_,
                    "is_alpha": token.is_alpha,
                    "is_stop": token.is_stop,
                }
            )

            results["pos_tags"].append(f"{token.text} ({token.pos_})")

        # Named Entity Recognition
        for ent in doc.ents:
            results["entities"].append(
                {
                    "text": ent.text,
                    "label": ent.label_,
                    "description": spacy.explain(ent.label_),
                    "start": ent.start_char,
                    "end": ent.end_char,
                }
            )

        # Dependency parsing
        for token in doc:
            if token.dep_ != "ROOT":
                results["dependencies"].append(
                    {
                        "token": token.text,
                        "dependency": token.dep_,
                        "head": token.head.text,
                        "description": spacy.explain(token.dep_),
                    }
                )

        # Sentence segmentation
        for sent in doc.sents:
            results["sentences"].append(
                {
                    "text": sent.text.strip(),
                    "start": sent.start_char,
                    "end": sent.end_char,
                }
            )

        return results

    except ImportError:
        return {"error": "spaCy not installed", "suggestion": "Run: pip install spacy"}
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}


def print_analysis_results(results: dict):
    """Print the analysis results in a formatted way."""
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        if "suggestion" in results:
            print(f"💡 Suggestion: {results['suggestion']}")
        return

    print("🔍 spaCy Natural Language Processing Analysis")
    print("=" * 60)
    print(f"📝 Original Text: {results['original_text']}")
    print()

    # Summary
    summary = results["summary"]
    print(f"📊 Summary:")
    print(f"   • Tokens: {summary['total_tokens']}")
    print(f"   • Entities: {summary['total_entities']}")
    print(f"   • Sentences: {summary['total_sentences']}")
    print()

    # Named Entities
    if results["entities"]:
        print("🏷️ Named Entities:")
        for ent in results["entities"]:
            print(f"   • {ent['text']} → {ent['label']} ({ent['description']})")
        print()

    # Part-of-speech tags
    if results["pos_tags"]:
        print("🔤 Part-of-Speech Tags:")
        print(f"   {', '.join(results['pos_tags'][:10])}")  # Show first 10
        if len(results["pos_tags"]) > 10:
            print(f"   ... and {len(results['pos_tags']) - 10} more")
        print()

    # Dependencies (show first few)
    if results["dependencies"]:
        print("🔗 Dependency Relations (first 5):")
        for dep in results["dependencies"][:5]:
            print(f"   • {dep['token']} --{dep['dependency']}--> {dep['head']}")
        if len(results["dependencies"]) > 5:
            print(f"   ... and {len(results['dependencies']) - 5} more")
        print()

    # Sentences
    if len(results["sentences"]) > 1:
        print("📝 Sentences:")
        for i, sent in enumerate(results["sentences"], 1):
            print(f"   {i}. {sent['text']}")
        print()

    print("✅ Analysis completed successfully!")


def main():
    """Main function for the employee spaCy test script."""
    parser = argparse.ArgumentParser(
        description="Employee spaCy Test - Demonstrates NLP task delegation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python employee_spacy_test.py "The quick brown fox jumps over the lazy dog"
  python employee_spacy_test.py "Apple Inc. released a new iPhone in California"
        """,
    )

    parser.add_argument("text", nargs="?", help="Text to analyze with spaCy")

    parser.add_argument("--demo", action="store_true", help="Run with demo text")

    args = parser.parse_args()

    # Determine text to analyze
    if args.demo:
        text = "Apple Inc. is planning to release a new iPhone in California next year. The company's CEO Tim Cook announced this during the annual developer conference."
        print("🎭 Demo mode - using sample text")
    elif args.text:
        text = args.text
    else:
        # If no text provided, try to read from stdin or use interactive mode
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
        else:
            print("Enter text to analyze (or use --demo for sample text):")
            try:
                text = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                return

    if not text:
        print("❌ No text provided for analysis")
        parser.print_help()
        return

    print(f"🚀 Employee spaCy Test - Analyzing text...")
    print()

    # Perform analysis
    results = analyze_text_with_spacy(text)

    # Print results
    print_analysis_results(results)


if __name__ == "__main__":
    main()
