import argparse
from readme_generator.config import load_api_keys
from readme_generator.generator import ReadmeGenerator

def parse_args():
    parser = argparse.ArgumentParser(description="Generate README.md using AI")
    parser.add_argument("--lang", type=str, choices=["en", "ko"], default="en", help="Language for README")
    parser.add_argument("--provider", type=str, choices=["openai", "claude", "gemini"], default="openai", help="AI provider to use")
    parser.add_argument("--max_chars", type=int, default=3000, help="Max characters to read per file")
    return parser.parse_args()

def main():
    args = parse_args()
    load_api_keys()
    try:
        generator = ReadmeGenerator(lang=args.lang, provider=args.provider, max_chars=args.max_chars)
        generator.run()
    except ValueError as e:
        print(f"❌ Error: {e}")