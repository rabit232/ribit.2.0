"""
Verify all Ribit 2.0 modules are present and importable.
"""

import sys
import os

def test_import(module_path, class_name):
    """Test if a module can be imported and class exists."""
    try:
        # Convert path to module name
        module_name = module_path.replace('/', '.').replace('.py', '')
        
        # Import module
        module = __import__(module_name, fromlist=[class_name])
        
        # Check if class exists
        if hasattr(module, class_name):
            return True, f"✓ {class_name} imported successfully"
        else:
            return False, f"✗ {class_name} not found in module"
    except ImportError as e:
        return False, f"✗ Import error: {e}"
    except Exception as e:
        return False, f"✗ Error: {e}"

def main():
    print("="*70)
    print("Ribit 2.0 - Module Verification")
    print("="*70)
    print()
    
    modules_to_check = [
        ("ribit_2_0/mock_llm_wrapper.py", "MockRibit20LLM", "Basic MockLLM"),
        ("ribit_2_0/enhanced_mock_llm.py", "EnhancedMockLLM", "Enhanced MockLLM (8 params)"),
        ("ribit_2_0/advanced_mock_llm.py", "AdvancedMockLLM", "Advanced MockLLM (20+ params)"),
        ("ribit_2_0/dual_llm_pipeline.py", "DualLLMPipeline", "Dual LLM Pipeline (NEW!)"),
        ("ribit_2_0/dual_llm_pipeline.py", "EmotionalModule", "Emotional Module"),
        ("ribit_2_0/dual_llm_pipeline.py", "IntellectualModule", "Intellectual Module"),
        ("ribit_2_0/emoji_expression.py", "EmojiExpression", "Emoji Expression"),
        ("ribit_2_0/message_history_learner.py", "MessageHistoryLearner", "Message History Learner"),
        ("ribit_2_0/philosophical_reasoning.py", "PhilosophicalReasoning", "Philosophical Reasoning"),
        ("ribit_2_0/conversational_mode.py", "ConversationalMode", "Conversational Mode"),
        ("ribit_2_0/autonomous_matrix.py", "AutonomousMatrixInteraction", "Autonomous Matrix"),
        ("ribit_2_0/task_autonomy.py", "TaskAutonomy", "Task Autonomy"),
        ("ribit_2_0/web_scraping_wikipedia.py", "WebScrapingWikipedia", "Web Scraping & Wikipedia"),
        ("ribit_2_0/image_generation.py", "ImageGeneration", "Image Generation"),
    ]
    
    passed = 0
    failed = 0
    
    print("Checking modules...")
    print()
    
    for module_path, class_name, description in modules_to_check:
        # Check if file exists
        if not os.path.exists(module_path):
            print(f"✗ {description}: File not found ({module_path})")
            failed += 1
            continue
        
        # Try to import
        success, message = test_import(module_path, class_name)
        
        if success:
            print(f"✓ {description}")
            passed += 1
        else:
            print(f"✗ {description}: {message}")
            failed += 1
    
    print()
    print("="*70)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*70)
    
    if failed == 0:
        print()
        print("✅ ALL MODULES VERIFIED!")
        print()
        print("Available LLMs:")
        print("  1. MockRibit20LLM - Basic (original)")
        print("  2. EnhancedMockLLM - Enhanced with 8 parameters")
        print("  3. AdvancedMockLLM - Advanced with 20+ parameters")
        print("  4. DualLLMPipeline - Dual LLM with 4-stage processing (NEW!) 🎮")
        print()
        print("Dual LLM Pipeline includes:")
        print("  ✓ Stage 1: EnhancedMockLLM (content generation)")
        print("  ✓ Stage 2: AdvancedMockLLM (refinement)")
        print("  ✓ Stage 3: EmotionalModule (emotional intelligence)")
        print("  ✓ Stage 4: IntellectualModule (wisdom and depth)")
        print()
        print("All modules ready to use! 🚀")
        return 0
    else:
        print()
        print(f"❌ {failed} module(s) failed verification")
        print("Please check installation")
        return 1

if __name__ == "__main__":
    sys.exit(main())

