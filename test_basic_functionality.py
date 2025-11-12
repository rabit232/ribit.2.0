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
        
        # Test storing knowledge (correct API)
        kb.store_knowledge("test_concept", "This is a test concept")
        
        # Test retrieving knowledge (correct API)
        result = kb.retrieve_knowledge("test_concept")
        
        if result and "test concept" in result.lower():
            print(f"{GREEN}✓{RESET} KnowledgeBase: Store and retrieve knowledge")
            return True
        else:
            print(f"{RED}✗{RESET} KnowledgeBase: Failed to retrieve knowledge")
            return False
    except Exception as e:
        print(f"{RED}✗{RESET} KnowledgeBase: {str(e)[:60]}")
        return False

def test_megabite_llm():
    """Test MegabiteLLM functionality"""
    try:
        from ribit_2_0.megabite_llm import MegabiteLLM
        
        llm = MegabiteLLM()
        
        # Test voxel-based response (correct API with context parameter)
        response = llm.generate_response("Hello, Megabite!", context=[])
        
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
        wls.learn_from_message("I love riding my bicycle to work")
        
        # Test getting statistics (correct API)
        stats = wls.get_statistics()
        
        if stats and 'total_words_learned' in stats and stats['total_words_learned'] > 0:
            print(f"{GREEN}✓{RESET} WordLearningSystem: Learn and track words")
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
        from ribit_2_0.conversation_manager import AdvancedConversationManager, ConversationMessage
        
        cm = AdvancedConversationManager()
        
        # Test adding message (correct API with ConversationMessage object)
        from datetime import datetime
        msg1 = ConversationMessage(
            room_id="test_room",
            user_id="user123",
            message_type="text",
            content="Hello, how are you?",
            timestamp=datetime.now()
        )
        msg2 = ConversationMessage(
            room_id="test_room",
            user_id="user123",
            message_type="text",
            content="I'm doing well, thank you!",
            timestamp=datetime.now()
        )
        
        cm.add_message(msg1)
        cm.add_message(msg2)
        
        # Test getting conversation context
        context = cm.get_conversation_context("test_room")
        
        if context and len(context) > 0:
            print(f"{GREEN}✓{RESET} ConversationManager: Track conversation context")
            return True
        else:
            print(f"{RED}✗{RESET} ConversationManager: Failed to track context")
            return False
    except Exception as e:
        print(f"{RED}✗{RESET} ConversationManager: {str(e)[:60]}")
        return False

def test_philosophical_reasoning():
    """Test PhilosophicalReasoning functionality"""
    try:
        from ribit_2_0.philosophical_reasoning import PhilosophicalReasoning
        
        pr = PhilosophicalReasoning()
        
        # Test generating philosophical response (correct API)
        response = pr.generate_response("What is consciousness?")
        
        if response and len(response) > 0:
            print(f"{GREEN}✓{RESET} PhilosophicalReasoning: Generate philosophical response")
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
        
        # Test generating humorous response (correct API)
        response = he.add_humor_to_response("This is a serious message", "Tell me something funny")
        
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
