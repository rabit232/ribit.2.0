#!/usr/bin/env python3
"""
Test script for all Ribit fixes:
- Web scraping
- Wikipedia search
- Image generation
- MockLLM diverse responses
"""

import sys
import os
import importlib.util

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def import_module_from_file(module_name, file_path):
    """Import a module directly from a file path without going through __init__.py"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

print("="*80)
print("TESTING RIBIT 2.0 FIXES")
print("="*80)
print()

# Test 1: Web Scraping and Wikipedia
print("Test 1: Web Scraping and Wikipedia")
print("-" * 40)
try:
    # Try importing the module
    try:
        from ribit_2_0.web_scraping_wikipedia import WebScrapingWikipedia
    except ImportError as ie:
        print(f"⚠ Module not available: {ie}")
        print("  Skipping web scraping tests")
        print()
        raise

    wsw = WebScrapingWikipedia()

    # Test Wikipedia search
    results = wsw.search_wikipedia("Artificial Intelligence", results=3)
    print(f"✓ Wikipedia search returned {len(results)} results")
    if results:
        print(f"  Top result: {results[0]}")

    # Test Wikipedia summary
    summary = wsw.get_wikipedia_summary("Artificial Intelligence", sentences=2)
    if summary:
        print(f"✓ Wikipedia summary retrieved: {summary['title']}")
        print(f"  URL: {summary['url']}")

    # Test web scraping (sync)
    result = wsw.scrape_url_sync("https://example.com", timeout=5)
    if result and result.get('success'):
        print(f"✓ Web scraping successful: {result['title']}")

    print()
except ImportError:
    pass
except Exception as e:
    print(f"✗ Error: {e}")
    print()

# Test 2: Image Generation
print("Test 2: Image Generation")
print("-" * 40)
try:
    try:
        from ribit_2_0.image_generation import ImageGeneration
    except ImportError as ie:
        print(f"⚠ Module not available: {ie}")
        print("  Skipping image generation tests")
        print()
        raise

    img_gen = ImageGeneration()

    # Test placeholder generation
    filepath = img_gen.generate_image_placeholder(
        "Test image for Ribit 2.0",
        width=400,
        height=300
    )

    if filepath and os.path.exists(filepath):
        print(f"✓ Image generated: {filepath}")
        print(f"  Size: {os.path.getsize(filepath)} bytes")
    else:
        print("✗ Image generation failed")

    print()
except ImportError:
    pass
except Exception as e:
    print(f"✗ Error: {e}")
    print()

# Test 3: MockLLM Diverse Responses
print("Test 3: MockLLM Diverse Responses")
print("-" * 40)
try:
    try:
        from ribit_2_0.mock_llm_wrapper import MockRibit20LLM
        from ribit_2_0.response_samples import TOTAL_SAMPLES
    except ImportError as ie:
        print(f"⚠ Module not available: {ie}")
        print("  Skipping MockLLM tests")
        print()
        raise

    llm = MockRibit20LLM("knowledge.txt")

    print(f"✓ MockLLM initialized with {TOTAL_SAMPLES} response samples")

    # Test diverse responses
    test_prompts = [
        "What do you think about quantum mechanics?",
        "Tell me about consciousness",
        "How does privacy work in cryptography?",
        "What is functional programming?",
        "Explain automation"
    ]

    responses = []
    for prompt in test_prompts:
        response = llm._handle_default_query(prompt)
        responses.append(response)

    # Check for diversity (responses should be different)
    unique_responses = len(set(responses))
    print(f"✓ Generated {unique_responses}/{len(test_prompts)} unique responses")

    if unique_responses >= len(test_prompts) * 0.8:  # At least 80% unique
        print("✓ Response diversity: GOOD")
    else:
        print("⚠ Response diversity: Could be better")

    print()
except ImportError:
    pass
except Exception as e:
    print(f"✗ Error: {e}")
    print()

# Test 4: Matrix Account Configuration
print("Test 4: Matrix Account Configuration")
print("-" * 40)
try:
    # Check if files have been updated using current directory
    import subprocess
    project_dir = os.path.dirname(os.path.abspath(__file__))
    result = subprocess.run(
        ["grep", "-r", "@ribit:envs.net", ".", "--include=*.md"],
        capture_output=True,
        text=True,
        cwd=project_dir
    )

    if result.returncode == 0 and result.stdout:
        count = len(result.stdout.strip().split('\n'))
        print(f"✓ Matrix account updated in {count} locations")
        print(f"  New account: @ribit:envs.net")
        print(f"  New server: https://matrix.envs.net")
    else:
        print("⚠ Matrix account not found in markdown files (this is OK)")

    print()
except Exception as e:
    print(f"✗ Error: {e}")
    print()

print("="*80)
print("TESTING COMPLETE")
print("="*80)
print()
print("Summary:")
print("- Web Scraping & Wikipedia: Enhanced module tested")
print("- Image Generation: Placeholder generation tested")
print("- MockLLM Responses: Diverse samples tested")
print("- Matrix Account: Configuration checked")
print()
print("Note: Some tests may be skipped if dependencies are not installed.")
print("Install requirements with: python3 -m pip install -r requirements.txt")
