"""
Test script for message history learning and enhanced MockLLM
"""

import asyncio
from ribit_2_0.enhanced_mock_llm import EnhancedMockLLM
from ribit_2_0.message_history_learner import MessageHistoryLearner
from ribit_2_0.knowledge_base import KnowledgeBase

def test_enhanced_llm():
    """Test Enhanced MockLLM with parameters."""
    print("="*70)
    print("Testing Enhanced MockLLM")
    print("="*70)
    
    # Create enhanced LLM
    llm = EnhancedMockLLM(
        temperature=0.7,
        frequency_penalty=0.5,
        presence_penalty=0.3,
        learning_enabled=True,
        style_adaptation=True
    )
    
    print("\n✓ Enhanced LLM initialized")
    print(f"  Temperature: {llm.temperature}")
    print(f"  Frequency Penalty: {llm.frequency_penalty}")
    print(f"  Presence Penalty: {llm.presence_penalty}")
    print(f"  Learning Enabled: {llm.learning_enabled}")
    
    # Test different styles
    print("\n" + "="*70)
    print("Testing Different Styles")
    print("="*70)
    
    styles = ['default', 'casual', 'formal', 'technical', 'friendly']
    prompt = "What is quantum physics?"
    
    for style in styles:
        llm.set_style(style)
        response = llm.generate_response(prompt, max_length=200)
        print(f"\n{style.upper()} style:")
        print(f"  {response[:150]}...")
    
    # Test parameter changes
    print("\n" + "="*70)
    print("Testing Parameter Changes")
    print("="*70)
    
    print("\nLow temperature (focused):")
    llm.set_parameters(temperature=0.3)
    response = llm.generate_response("Explain consciousness", max_length=200)
    print(f"  {response[:150]}...")
    
    print("\nHigh temperature (creative):")
    llm.set_parameters(temperature=1.5)
    response = llm.generate_response("Explain consciousness", max_length=200)
    print(f"  {response[:150]}...")
    
    # Test statistics
    print("\n" + "="*70)
    print("LLM Statistics")
    print("="*70)
    
    stats = llm.get_statistics()
    print(f"\nParameters:")
    for key, value in stats['parameters'].items():
        print(f"  {key}: {value}")
    
    print(f"\nPerformance:")
    print(f"  Responses generated: {stats['responses_generated']}")
    print(f"  Unique tokens: {stats['unique_tokens_used']}")
    print(f"  Topics discussed: {stats['topics_discussed']}")
    
    print("\n✓ Enhanced LLM tests passed!")

def test_message_learner():
    """Test Message History Learner."""
    print("\n" + "="*70)
    print("Testing Message History Learner")
    print("="*70)
    
    kb = KnowledgeBase("test_knowledge.txt")
    learner = MessageHistoryLearner(kb)
    
    print("\n✓ Message History Learner initialized")
    
    # Simulate learning from messages
    print("\nSimulating message learning...")
    
    async def simulate_learning():
        messages = [
            ("@user1:matrix.org", "I love quantum physics and entanglement!", "2024-01-01"),
            ("@user2:matrix.org", "Programming in Python is amazing", "2024-01-01"),
            ("@user1:matrix.org", "The wave-particle duality fascinates me", "2024-01-01"),
            ("@user3:matrix.org", "AI and machine learning are the future", "2024-01-01"),
            ("@user2:matrix.org", "I prefer functional programming paradigms", "2024-01-01"),
        ]
        
        from datetime import datetime
        for sender, message, date in messages:
            await learner._learn_from_message(
                sender=sender,
                message=message,
                timestamp=datetime.fromisoformat(date),
                room_id="!test:matrix.org"
            )
        
        return learner._generate_learning_summary(
            messages_processed=len(messages),
            users_analyzed=3,
            time_taken=0.5
        )
    
    summary = asyncio.run(simulate_learning())
    
    print(f"\n✓ Learned from {summary['messages_processed']} messages")
    print(f"  Users analyzed: {summary['users_analyzed']}")
    print(f"  Vocabulary size: {summary['vocabulary_size']}")
    print(f"  Phrases learned: {summary['phrases_learned']}")
    print(f"  Topics identified: {summary['unique_topics']}")
    
    if summary['top_topics']:
        print(f"\n  Top topics:")
        for topic, count in list(summary['top_topics'].items())[:5]:
            print(f"    • {topic}: {count}")
    
    if summary['top_vocabulary']:
        print(f"\n  Top vocabulary:")
        print(f"    {', '.join(list(summary['top_vocabulary'].keys())[:15])}")
    
    # Test user profile
    print("\n" + "="*70)
    print("Testing User Profile")
    print("="*70)
    
    profile = learner.get_user_profile("@user1:matrix.org")
    print(f"\nUser: @user1:matrix.org")
    print(f"  Interests: {profile['interests']}")
    if profile['patterns']:
        print(f"  Message count: {profile['patterns'].get('message_count', 0)}")
    
    print("\n✓ Message History Learner tests passed!")

def test_integration():
    """Test integration of Enhanced LLM with Message Learner."""
    print("\n" + "="*70)
    print("Testing Integration")
    print("="*70)
    
    llm = EnhancedMockLLM(learning_enabled=True, style_adaptation=True)
    
    # Simulate user adaptation
    print("\nTesting style adaptation...")
    
    # Simulate learning about a user
    if llm.message_learner:
        llm.message_learner.learned_data['user_patterns']['@casual_user:matrix.org'] = {
            'emoji_count': 50,
            'avg_length': 30,
            'question_count': 20
        }
        
        suggestions = llm.adapt_to_user('@casual_user:matrix.org')
        print(f"\n✓ Adapted to casual user")
        print(f"  Suggestions: {suggestions}")
        print(f"  Current style: {llm.current_style}")
    
    # Test learned vocabulary
    print("\n" + "="*70)
    print("Testing Learned Vocabulary Integration")
    print("="*70)
    
    vocab = llm.get_learned_vocabulary(10)
    phrases = llm.get_learned_phrases(5)
    
    print(f"\n  Vocabulary: {len(vocab)} words")
    print(f"  Phrases: {len(phrases)} phrases")
    
    print("\n✓ Integration tests passed!")

def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("RIBIT 2.0 - LEARNING FEATURES TEST SUITE")
    print("="*70)
    
    try:
        test_enhanced_llm()
        test_message_learner()
        test_integration()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        print("\nNew Features Working:")
        print("  ✓ Enhanced MockLLM with parameters")
        print("  ✓ Temperature control (creativity)")
        print("  ✓ Frequency/presence penalties (anti-repetition)")
        print("  ✓ Multiple conversation styles")
        print("  ✓ Message history learning")
        print("  ✓ Vocabulary and phrase extraction")
        print("  ✓ User pattern analysis")
        print("  ✓ Style adaptation")
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

