#!/usr/bin/env python3
"""
Basic MockRibit20LLM Usage Example

This script demonstrates the basic functionality of the enhanced
MockRibit20LLM emulator including decision making, capabilities
checking, and personality interaction.

Author: Manus AI
Date: September 21, 2025
"""

import sys
import os

# Add the parent directory to the path to import ribit_2_0
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ribit_2_0.mock_llm_wrapper import MockRibit20LLM

def main():
    """Demonstrate basic MockRibit20LLM functionality."""
    
    print("=" * 60)
    print("MockRibit20LLM - Basic Usage Example")
    print("=" * 60)
    
    # Initialize the enhanced LLM emulator
    print("\n🤖 Initializing MockRibit20LLM...")
    llm = MockRibit20LLM("example_knowledge.txt")
    print("✅ Emulator initialized successfully!")
    
    # Test 1: Introduction and personality
    print("\n" + "=" * 40)
    print("Test 1: Introduction and Personality")
    print("=" * 40)
    
    intro_decision = llm.get_decision("Introduce yourself and tell me about your interests")
    print(f"🎭 Introduction: {intro_decision[:100]}...")
    
    # Test 2: Capabilities check
    print("\n" + "=" * 40)
    print("Test 2: Capabilities Assessment")
    print("=" * 40)
    
    capabilities = llm.get_capabilities()
    print("🔧 Available Capabilities:")
    for capability, status in capabilities.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {capability.replace('_', ' ').title()}")
    
    # Test 3: Personality information
    print("\n" + "=" * 40)
    print("Test 3: Personality Information")
    print("=" * 40)
    
    personality = llm.get_personality_info()
    print("🎨 Personality Profile:")
    for key, value in personality.items():
        print(f"   • {key.replace('_', ' ').title()}: {value}")
    
    # Test 4: Basic decision making
    print("\n" + "=" * 40)
    print("Test 4: Basic Decision Making")
    print("=" * 40)
    
    test_prompts = [
        "Move to coordinates (100, 200)",
        "Click on the target",
        "Type 'Hello, World!'",
        "Press the Enter key"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        decision = llm.get_decision(prompt)
        print(f"📝 Test {i}: {prompt}")
        print(f"🎯 Decision: {decision}")
        print()
    
    # Test 5: Knowledge and learning
    print("\n" + "=" * 40)
    print("Test 5: Knowledge and Learning")
    print("=" * 40)
    
    # Teach something new
    learn_response = llm.get_decision("Learn that the capital of France is Paris")
    print(f"📚 Learning: {learn_response}")
    
    # Test knowledge retrieval
    knowledge_response = llm.get_decision("What is the capital of France?")
    print(f"🧠 Knowledge: {knowledge_response}")
    
    # Test 6: Conversation context
    print("\n" + "=" * 40)
    print("Test 6: Conversation Context")
    print("=" * 40)
    
    context = llm.get_conversation_context()
    print(f"💬 Conversation entries: {len(context)}")
    if context:
        print("📜 Recent context:")
        for entry in context[-3:]:  # Show last 3 entries
            print(f"   • {entry[:50]}...")
    
    # Test 7: Complex reasoning
    print("\n" + "=" * 40)
    print("Test 7: Complex Reasoning")
    print("=" * 40)
    
    complex_prompt = "Explain the relationship between artificial intelligence and robotics"
    complex_response = llm.get_decision(complex_prompt)
    print(f"🧮 Complex reasoning: {complex_response[:150]}...")
    
    # Test 8: Error handling
    print("\n" + "=" * 40)
    print("Test 8: Error Handling")
    print("=" * 40)
    
    uncertain_prompt = "Perform impossible task XYZ"
    uncertain_response = llm.get_decision(uncertain_prompt)
    print(f"❓ Uncertainty handling: {uncertain_response[:100]}...")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    print("✅ All basic functionality tests completed successfully!")
    print("🎉 MockRibit20LLM is working correctly!")
    
    # Clean shutdown
    print("\n🔄 Shutting down emulator...")
    llm.close()
    print("✅ Shutdown complete!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
