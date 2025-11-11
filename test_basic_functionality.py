#!/usr/bin/env python3
"""
Test script to verify basic functionality of restored ribit.2.0 package.
"""

import sys
from pathlib import Path

# Add ribit.2.0 to path
sys.path.insert(0, str(Path(__file__).parent))

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def test_knowledge_base():
    """Test KnowledgeBase functionality"""
    try:
        from ribit_2_0.knowledge_base import KnowledgeBase
        
        kb = KnowledgeBase()
        
        # Test adding knowledge
        kb.add_concept("test_concept", "This is a test concept")
        
        # Test retrieving knowledge
        result = kb.get_concept("test_concept")
        
        if result and "test concept" in result.lower():
            print(f"{GREEN}✓{RESET} KnowledgeBase: Add and retrieve concepts")
            return True
        else:
            print(f"{RED}✗{RESET} KnowledgeBase: Failed to retrieve concept")
            return False
    except Exception as e:
        print(f"{RED}✗{RESET} KnowledgeBase: {str(e)[:60]}")
        return False

def test_megabite_llm():
    """Test MegabiteLLM functionality"""
    try:
        from ribit_2_0.megabite_llm import MegabiteLLM
        
        llm = MegabiteLLM()
        
        # Test voxel-based response
        response = llm.generate_response("Hello, Megabite!")
        
        if response and len(response) > 0:
            print(f"{GREEN}✓{RESET} MegabiteLLM: Generate voxel-based response")
            return True
        else:
            print(f"{RED}✗{RESET} MegabiteLLM: Failed to generate response")
            return False
    except Exception as e:
        print(f"{RED}✗{RESET} MegabiteLLM: {str(e)[:60]}")
        return False

def test_word_learning():
    """Test WordLearningSystem functionality"""
    try:
        from ribit_2_0.word_learning_system import WordLearningSystem
        
        wls = WordLearningSystem()
        
        # Test learning words from message
        wls.learn_from_message("The bicycle is a great vehicle for transportation")
        
        # Test getting learned words
        learned = wls.get_learned_words()
        
        if learned and len(learned) > 0:
            print(f"{GREEN}✓{RESET} WordLearningSystem: Learn and retrieve words")
            return True
        else:
            print(f"{RED}✗{RESET} WordLearningSystem: Failed to learn words")
            return False
    except Exception as e:
        print(f"{RED}✗{RESET} WordLearningSystem: {str(e)[:60]}")
        return False

def test_conversation_manager():
    """Test ConversationManager functionality"""
    try:
        from ribit_2_0.conversation_manager import AdvancedConversationManager
        
        cm = AdvancedConversationManager()
        
        # Test adding message
        cm.add_message("user123", "Hello, how are you?", is_user=True)
        cm.add_message("user123", "I'm doing well, thank you!", is_user=False)
        
        # Test getting conversation history
        history = cm.get_conversation_history("user123")
        
        if history and len(history) >= 2:
            print(f"{GREEN}✓{RESET} ConversationManager: Track conversation history")
            return True
        else:
            print(f"{RED}✗{RESET} ConversationManager: Failed to track history")
            return False
    except Exception as e:
        print(f"{RED}✗{RESET} ConversationManager: {str(e)[:60]}")
        return False

def test_philosophical_reasoning():
    """Test PhilosophicalReasoning functionality"""
    try:
        from ribit_2_0.philosophical_reasoning import PhilosophicalReasoning
        
        pr = PhilosophicalReasoning()
        
        # Test generating philosophical response
        response = pr.generate_thought_experiment("consciousness")
        
        if response and len(response) > 0:
            print(f"{GREEN}✓{RESET} PhilosophicalReasoning: Generate thought experiment")
            return True
        else:
            print(f"{RED}✗{RESET} PhilosophicalReasoning: Failed to generate")
            return False
    except Exception as e:
        print(f"{RED}✗{RESET} PhilosophicalReasoning: {str(e)[:60]}")
        return False

def test_humor_engine():
    """Test HumorEngine functionality"""
    try:
        from ribit_2_0.humor_engine import HumorEngine
        
        he = HumorEngine()
        
        # Test generating humorous response
        response = he.add_humor("This is a serious message")
        
        if response and len(response) > 0:
            print(f"{GREEN}✓{RESET} HumorEngine: Add humor to messages")
            return True
        else:
            print(f"{RED}✗{RESET} HumorEngine: Failed to add humor")
            return False
    except Exception as e:
        print(f"{RED}✗{RESET} HumorEngine: {str(e)[:60]}")
        return False

def test_multi_language():
    """Test MultiLanguageSystem functionality"""
    try:
        from ribit_2_0.multi_language_system import MultiLanguageSystem
        
        mls = MultiLanguageSystem()
        
        # Test language detection
        lang = mls.detect_language("Hello, how are you?")
        
        if lang:
            print(f"{GREEN}✓{RESET} MultiLanguageSystem: Detect language")
            return True
        else:
            print(f"{RED}✗{RESET} MultiLanguageSystem: Failed to detect language")
            return False
    except Exception as e:
        print(f"{RED}✗{RESET} MultiLanguageSystem: {str(e)[:60]}")
        return False

def main():
    print(f"\n{CYAN}{'='*80}{RESET}")
    print(f"{CYAN}Ribit 2.0 - Basic Functionality Test{RESET}")
    print(f"{CYAN}{'='*80}{RESET}\n")
    
    print(f"{YELLOW}Testing Core Functionality:{RESET}\n")
    
    results = []
    
    # Run all tests
    results.append(test_knowledge_base())
    results.append(test_megabite_llm())
    results.append(test_word_learning())
    results.append(test_conversation_manager())
    results.append(test_philosophical_reasoning())
    results.append(test_humor_engine())
    results.append(test_multi_language())
    
    # Summary
    print(f"\n{CYAN}{'='*80}{RESET}")
    success_count = sum(1 for r in results if r)
    total_count = len(results)
    success_rate = (success_count / total_count) * 100
    
    print(f"{CYAN}Test Summary:{RESET}")
    print(f"  Total tests: {total_count}")
    print(f"  {GREEN}Passed: {success_count}{RESET}")
    print(f"  {RED}Failed: {total_count - success_count}{RESET}")
    print(f"  Success rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print(f"\n{GREEN}✓ All functionality tests passed!{RESET}")
        return 0
    elif success_rate >= 70:
        print(f"\n{YELLOW}⚠ Most tests passed, but some features need attention.{RESET}")
        return 1
    else:
        print(f"\n{RED}✗ Many tests failed. Please check the implementation.{RESET}")
        return 2

if __name__ == "__main__":
    sys.exit(main())
