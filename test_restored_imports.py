#!/usr/bin/env python3
"""
Test script to verify all restored modules can be imported without errors.
"""

import sys
import importlib
from pathlib import Path

# Add ribit.2.0 to path
sys.path.insert(0, str(Path(__file__).parent))

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def test_import(module_name, description=""):
    """Test if a module can be imported"""
    try:
        module = importlib.import_module(module_name)
        print(f"{GREEN}✓{RESET} {module_name:40s} {CYAN}{description}{RESET}")
        return True, None
    except Exception as e:
        print(f"{RED}✗{RESET} {module_name:40s} {RED}ERROR: {str(e)[:60]}{RESET}")
        return False, str(e)

def main():
    print(f"\n{CYAN}{'='*80}{RESET}")
    print(f"{CYAN}Ribit 2.0 - Restored Modules Import Test{RESET}")
    print(f"{CYAN}{'='*80}{RESET}\n")
    
    # Test main package
    print(f"{YELLOW}Testing Main Package:{RESET}")
    results = []
    
    results.append(test_import("ribit_2_0", "Main package"))
    
    # Test core modules
    print(f"\n{YELLOW}Testing Core Modules:{RESET}")
    core_modules = [
        ("ribit_2_0.agent", "Agent module"),
        ("ribit_2_0.controller", "Vision controller"),
        ("ribit_2_0.knowledge_base", "Knowledge base"),
        ("ribit_2_0.llm_wrapper", "LLM wrapper"),
        ("ribit_2_0.mock_llm_wrapper", "Mock LLM"),
        ("ribit_2_0.mock_controller", "Mock controller"),
    ]
    
    for module, desc in core_modules:
        results.append(test_import(module, desc))
    
    # Test bot modules
    print(f"\n{YELLOW}Testing Bot Modules:{RESET}")
    bot_modules = [
        ("ribit_2_0.matrix_bot", "Matrix bot"),
        ("ribit_2_0.deltachat_bot", "DeltaChat bot"),
        ("ribit_2_0.bridge_relay", "Bridge relay"),
        ("ribit_2_0.megabite_llm", "Megabite LLM"),
    ]
    
    for module, desc in bot_modules:
        results.append(test_import(module, desc))
    
    # Test enhancement modules
    print(f"\n{YELLOW}Testing Enhancement Modules:{RESET}")
    enhancement_modules = [
        ("ribit_2_0.word_learning_system", "Word learning"),
        ("ribit_2_0.conversation_manager", "Conversation manager"),
        ("ribit_2_0.enhanced_emotions", "Enhanced emotions"),
        ("ribit_2_0.philosophical_reasoning", "Philosophical reasoning"),
        ("ribit_2_0.multi_language_system", "Multi-language"),
        ("ribit_2_0.humor_engine", "Humor engine"),
        ("ribit_2_0.image_generation", "Image generation"),
        ("ribit_2_0.web_knowledge", "Web knowledge"),
    ]
    
    for module, desc in enhancement_modules:
        results.append(test_import(module, desc))
    
    # Test ROS integration (optional)
    print(f"\n{YELLOW}Testing ROS Integration (Optional):{RESET}")
    results.append(test_import("ribit_2_0.ros_controller", "ROS controller"))
    
    # Test Jina integration
    print(f"\n{YELLOW}Testing Jina Integration:{RESET}")
    results.append(test_import("ribit_2_0.jina_integration", "Jina search"))
    
    # Summary
    print(f"\n{CYAN}{'='*80}{RESET}")
    success_count = sum(1 for r in results if r[0])
    total_count = len(results)
    success_rate = (success_count / total_count) * 100
    
    print(f"{CYAN}Test Summary:{RESET}")
    print(f"  Total modules tested: {total_count}")
    print(f"  {GREEN}Successful imports: {success_count}{RESET}")
    print(f"  {RED}Failed imports: {total_count - success_count}{RESET}")
    print(f"  Success rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print(f"\n{GREEN}✓ All modules imported successfully!{RESET}")
        return 0
    elif success_rate >= 80:
        print(f"\n{YELLOW}⚠ Most modules imported successfully, but some failed.{RESET}")
        return 1
    else:
        print(f"\n{RED}✗ Many modules failed to import. Please check dependencies.{RESET}")
        return 2

if __name__ == "__main__":
    sys.exit(main())
