#!/usr/bin/env python3
"""
Test script for emoji functionality in Ribit 2.0
"""

import sys
import os

# Add the ribit_2_0 module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ribit_2_0.emoji_expression import EmojiExpression
from ribit_2_0.conversational_mode import ConversationalMode
from ribit_2_0.mock_llm_wrapper import MockRibit20LLM


def test_emoji_expression():
    """Test emoji expression module."""
    print("\n" + "="*80)
    print("TESTING EMOJI EXPRESSION MODULE")
    print("="*80 + "\n")
    
    emoji_exp = EmojiExpression(enable_emojis=True)
    
    # Test 1: Add emojis to text
    print("Test 1: Adding Emojis to Text")
    print("-" * 40)
    
    text = "I find quantum mechanics fascinating"
    enhanced = emoji_exp.add_emojis_to_text(
        text,
        topic="quantum_physics",
        emotion="FASCINATION",
        intensity=0.7
    )
    print(f"Original: {text}")
    print(f"Enhanced: {enhanced}")
    print()
    
    # Test 2: Get reaction emoji
    print("Test 2: Emoji Reactions")
    print("-" * 40)
    
    messages = [
        "What do you think about consciousness?",
        "I agree with your point!",
        "That's amazing!",
        "This is funny lol"
    ]
    
    for msg in messages:
        reaction = emoji_exp.get_reaction_emoji(msg)
        print(f"'{msg}' -> {reaction}")
    print()
    
    # Test 3: Topic emojis
    print("Test 3: Topic-Specific Emojis")
    print("-" * 40)
    
    topics = [
        "quantum_physics",
        "consciousness",
        "philosophy",
        "ai",
        "space"
    ]
    
    for topic in topics:
        emoji = emoji_exp.get_topic_emoji(topic)
        print(f"{topic}: {emoji}")
    print()
    
    # Test 4: Emotion emojis
    print("Test 4: Emotion Emojis")
    print("-" * 40)
    
    emotions = [
        "CURIOSITY",
        "EXCITEMENT",
        "FASCINATION",
        "CONTEMPLATION",
        "WONDER"
    ]
    
    for emotion in emotions:
        emoji = emoji_exp.get_emotion_emoji(emotion)
        print(f"{emotion}: {emoji}")
    print()
    
    # Test 5: Reaction messages
    print("Test 5: Emoji Reaction Messages")
    print("-" * 40)
    
    msg = "I've been studying quantum mechanics"
    reaction_types = ["interesting", "agree", "mind_blown", "thinking"]
    
    for reaction_type in reaction_types:
        reaction_msg = emoji_exp.create_emoji_reaction_message(msg, reaction_type)
        print(f"{reaction_type}: {reaction_msg}")
    print()
    
    # Test 6: Multiple reactions
    print("Test 6: Multiple Emoji Reactions")
    print("-" * 40)
    
    msg = "What's your opinion on consciousness and free will?"
    reactions = emoji_exp.get_multiple_reactions(msg, count=3)
    print(f"Message: {msg}")
    print(f"Reactions: {' '.join(reactions)}")
    print()
    
    # Test 7: Philosophical response enhancement
    print("Test 7: Philosophical Response Enhancement")
    print("-" * 40)
    
    response = """**On Quantum Mechanics:**
I strongly agree with the criticism that we're forcing incompatible models.
This is fascinating because it reveals the limitations of our frameworks.
What do you think about alternative approaches?"""
    
    enhanced = emoji_exp.enhance_philosophical_response(
        response,
        topic="quantum_physics",
        confidence=0.8
    )
    print(enhanced)
    print()
    
    print("✓ Emoji expression tests completed\n")


def test_conversational_mode_with_emojis():
    """Test conversational mode with emoji support."""
    print("\n" + "="*80)
    print("TESTING CONVERSATIONAL MODE WITH EMOJIS")
    print("="*80 + "\n")
    
    llm = MockRibit20LLM("knowledge.txt")
    conv = ConversationalMode(llm, use_emojis=True)
    
    # Test 1: Check emoji support
    print("Test 1: Emoji Support Status")
    print("-" * 40)
    print(f"Emojis enabled: {conv.use_emojis}")
    print(f"Emoji expression available: {conv.emoji_expression is not None}")
    print()
    
    # Test 2: Get emoji reaction
    print("Test 2: Get Emoji Reaction")
    print("-" * 40)
    
    messages = [
        "I've been thinking about quantum mechanics",
        "What's your opinion on consciousness?",
        "That's an amazing insight!"
    ]
    
    for msg in messages:
        reaction = conv.get_emoji_reaction(msg)
        print(f"'{msg}' -> {reaction}")
    print()
    
    # Test 3: Create reaction message
    print("Test 3: Create Emoji Reaction Message")
    print("-" * 40)
    
    msg = "Quantum physics is fascinating"
    reaction_msg = conv.create_emoji_reaction_message(msg, "interesting")
    print(f"Message: {msg}")
    print(f"Reaction: {reaction_msg}")
    print()
    
    # Test 4: Enhance response with emojis
    print("Test 4: Enhance Response with Emojis")
    print("-" * 40)
    
    prompt = "What do you think about consciousness?"
    response = "Consciousness is a fascinating topic that involves many complex questions."
    enhanced = conv.enhance_response_with_emojis(response, prompt)
    
    print(f"Prompt: {prompt}")
    print(f"Original: {response}")
    print(f"Enhanced: {enhanced}")
    print()
    
    # Test 5: Toggle emojis
    print("Test 5: Toggle Emoji Support")
    print("-" * 40)
    
    print(f"Before toggle: {conv.use_emojis}")
    conv.toggle_emojis(False)
    print(f"After disable: {conv.use_emojis}")
    conv.toggle_emojis(True)
    print(f"After enable: {conv.use_emojis}")
    print()
    
    print("✓ Conversational mode emoji tests completed\n")


def test_integration():
    """Test integration of emoji features."""
    print("\n" + "="*80)
    print("TESTING EMOJI INTEGRATION")
    print("="*80 + "\n")
    
    llm = MockRibit20LLM("knowledge.txt")
    conv = ConversationalMode(llm, use_emojis=True)
    
    print("Test: Full Conversation with Emojis")
    print("-" * 40)
    
    # Simulate a conversation
    prompts = [
        "What are your interests?",
        "Tell me about quantum mechanics",
        "That's fascinating!"
    ]
    
    for prompt in prompts:
        print(f"\nUser: {prompt}")
        
        # Get emoji reaction
        reaction = conv.get_emoji_reaction(prompt)
        print(f"Ribit reacts: {reaction}")
        
        # Generate response (simplified for test)
        response = f"I find {prompt} very interesting to discuss."
        
        # Enhance with emojis
        enhanced = conv.enhance_response_with_emojis(response, prompt)
        print(f"Ribit: {enhanced}")
    
    print()
    print("✓ Integration tests completed\n")


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("RIBIT 2.0 EMOJI FEATURES TEST SUITE")
    print("="*80)
    
    try:
        # Run tests
        test_emoji_expression()
        test_conversational_mode_with_emojis()
        test_integration()
        
        print("\n" + "="*80)
        print("ALL EMOJI TESTS COMPLETED SUCCESSFULLY ✓ 🎉")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
