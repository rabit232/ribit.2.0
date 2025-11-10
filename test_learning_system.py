#!/usr/bin/env python3
"""
Test Megabite Learning System

Complete example showing word learning, perspective analysis, and opinion formation.

Author: Manus AI
"""

import asyncio
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_learning_system():
    """Test the complete learning system."""
    print("="*70)
    print("MEGABITE LEARNING SYSTEM TEST")
    print("="*70)

    # Check for environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_KEY')

    if not supabase_url or not supabase_key:
        print("\n⚠️  Supabase credentials not found in environment")
        print("Set SUPABASE_URL and SUPABASE_SERVICE_KEY to test with real database")
        print("\nShowing module structure instead...\n")
        return await show_module_structure()

    # Import modules
    try:
        from megabite import MegabiteInitializer
        from megabite.word_learning_manager import WordLearningManager
        from megabite.perspective_system import PerspectiveSystem
        from megabite.opinion_engine import OpinionEngine
        from megabite.matrix_learning_commands import MatrixLearningCommands
        from megabite.enhanced_mock_llm import EnhancedMockLLM
        from megabite.ribit_compat import ensure_compatibility
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nMake sure you're in the project directory")
        return

    print("\n✅ All modules imported successfully\n")

    # Initialize Megabite
    print("Initializing Megabite...")
    initializer = MegabiteInitializer()
    success = await initializer.initialize_all()

    if not success:
        print("❌ Megabite initialization failed")
        return

    print("✅ Megabite initialized\n")

    # Initialize learning components
    print("Initializing learning components...")
    word_learning = WordLearningManager(supabase_url, supabase_key)
    await word_learning.initialize()
    print("✅ Word Learning Manager ready")

    perspective = PerspectiveSystem(
        initializer.llm_manager,
        word_learning,
        supabase_url,
        supabase_key
    )
    await perspective.initialize()
    print("✅ Perspective System ready")

    opinion = OpinionEngine(
        initializer.llm_manager,
        word_learning,
        supabase_url,
        supabase_key
    )
    await opinion.initialize()
    print("✅ Opinion Engine ready")

    commands = MatrixLearningCommands(
        initializer.llm_manager,
        word_learning,
        perspective,
        opinion
    )
    print("✅ Matrix Commands ready\n")

    # Test 1: Learn words from messages
    print("-"*70)
    print("TEST 1: Word Learning")
    print("-"*70)

    test_messages = [
        "Artificial intelligence and machine learning are fascinating fields of computer science.",
        "Neural networks can recognize patterns in data through deep learning algorithms.",
        "Natural language processing enables computers to understand human communication."
    ]

    for i, msg in enumerate(test_messages, 1):
        print(f"\nLearning from message {i}...")
        stats = await word_learning.learn_from_message(
            msg,
            user_id="test_user",
            room_id="test_room"
        )
        print(f"  Words learned: {stats['words_learned']}")
        print(f"  Pairs created: {stats['pairs_created']}")

    # Get vocabulary stats
    print("\n📚 Vocabulary Statistics:")
    vocab_stats = await word_learning.get_vocabulary_stats()
    print(f"  Total words: {vocab_stats.get('total_words', 0)}")
    print(f"  Total uses: {vocab_stats.get('total_occurrences', 0)}")

    # Get intelligence quotient
    iq = await word_learning.get_intelligence_quotient()
    print(f"\n🧠 Intelligence Metrics:")
    print(f"  Level: {iq.get('intelligence_level', 'unknown')}")
    print(f"  Total weight: {iq.get('total_weight', 1.0):.2f}")
    print(f"  Vocabulary weight: {iq.get('vocabulary_weight', 0.0):.2f}")

    # Test 2: Perspective Analysis
    print("\n" + "-"*70)
    print("TEST 2: Perspective Analysis")
    print("-"*70)

    long_text = """
    Quantum computing represents a paradigm shift in computational technology.
    Unlike classical computers that use bits, quantum computers use quantum bits
    or qubits. These qubits can exist in multiple states simultaneously through
    superposition, and can be entangled with each other. This allows quantum
    computers to solve certain problems exponentially faster than classical
    computers. Applications include cryptography, drug discovery, optimization
    problems, and artificial intelligence. The field is rapidly advancing with
    companies like IBM, Google, and others making significant breakthroughs.
    """

    print("\nAnalyzing perspective on quantum computing...")
    perspective_result = await perspective.analyze_perspective(
        long_text,
        user_id="test_user",
        room_id="test_room"
    )

    print(f"\n📊 Analysis Results:")
    print(f"  Words learned: {perspective_result['words_learned']}")
    print(f"  Main topics: {', '.join(perspective_result['main_topics'][:3])}")
    print(f"  Interestingness: {perspective_result['interesting_score']:.0%}")
    print(f"  Integrated to personality: {perspective_result['integrated_to_personality']}")
    print(f"\n💭 Bot Opinion:")
    print(f"  {perspective_result['bot_opinion'][:150]}...")

    # Test 3: Opinion Formation
    print("\n" + "-"*70)
    print("TEST 3: Opinion Formation")
    print("-"*70)

    question = "What is the future of artificial intelligence?"
    print(f"\nForming opinion on: {question}")

    opinion_result = await opinion.form_opinion(
        question,
        user_id="test_user",
        room_id="test_room"
    )

    print(f"\n💭 Opinion:")
    print(f"  {opinion_result['opinion'][:200]}...")
    print(f"\n🤔 Reasoning:")
    print(f"  {opinion_result['reasoning'][:200]}...")
    print(f"\n📊 Confidence: {opinion_result['confidence']:.0%}")

    # Test 4: Matrix Commands
    print("\n" + "-"*70)
    print("TEST 4: Matrix Commands")
    print("-"*70)

    print("\nTesting ?words command...")
    response = await commands.handle_command(
        'words', '', 'test_user', 'test_room'
    )
    print(response[:300] + "...")

    print("\nTesting ?personality command...")
    response = await commands.handle_command(
        'personality', '', 'test_user', 'test_room'
    )
    print(response[:300] + "...")

    # Test 5: Enhanced Mock LLM
    print("\n" + "-"*70)
    print("TEST 5: Enhanced Mock LLM")
    print("-"*70)

    mock_llm = EnhancedMockLLM(word_learning)

    test_input = "Tell me about machine learning"
    print(f"\nInput: {test_input}")

    response = await mock_llm.generate_response(test_input)
    print(f"Response: {response}")

    intelligence = await mock_llm.get_intelligence_summary()
    print(f"\n🧠 Mock LLM Intelligence:")
    print(f"  Level: {intelligence.get('intelligence_level', 'unknown')}")
    print(f"  Weight: {intelligence.get('total_weight', 1.0):.2f}")
    print(f"  Capabilities: {', '.join(intelligence.get('capabilities', [])[:3])}")

    # Test 6: Ribit 2.0 Compatibility
    print("\n" + "-"*70)
    print("TEST 6: Ribit 2.0 Compatibility")
    print("-"*70)

    compat = ensure_compatibility()
    interface = compat.create_unified_interface()

    print("\nAvailable Ribit 2.0 modules:")
    for module_name in interface['available_modules']:
        available = interface.get(module_name.replace('_', '')) is not None
        status = "✅" if available else "⚠️"
        print(f"  {status} {module_name}")

    # Cleanup
    print("\n" + "="*70)
    print("Cleaning up...")
    await word_learning.close()
    await perspective.close()
    await opinion.close()
    await initializer.shutdown()

    print("\n✅ All tests completed successfully!")
    print("="*70)


async def show_module_structure():
    """Show module structure without database."""
    print("\n📦 MEGABITE LEARNING SYSTEM MODULES\n")

    modules = {
        'Core System': [
            'word_learning_manager.py - Learn vocabulary from conversations',
            'perspective_system.py - Analyze large texts (up to 10MB)',
            'opinion_engine.py - Form opinions with reasoning',
            'matrix_learning_commands.py - Matrix chat commands',
            'enhanced_mock_llm.py - Intelligence scaling',
            'ribit_compat.py - Ribit 2.0 compatibility'
        ],
        'Database': [
            'supabase/migrations/03_create_word_learning_tables.sql',
            '  - learned_words table',
            '  - word_relationships table',
            '  - sentence_patterns table',
            '  - perspective_analyses table',
            '  - personality_traits table',
            '  - opinion_history table'
        ],
        'Commands': [
            '?words - Show vocabulary statistics',
            '?opinion [question] - Form opinion',
            '?perspective [text] - Analyze text',
            '?learn [months] - Learn from history',
            '?personality - Show personality traits',
            '?vocabulary - Export vocabulary'
        ],
        'Features': [
            '✅ Automatic vocabulary learning',
            '✅ Word relationship tracking (pairs, triplets)',
            '✅ Large text analysis (up to 10MB)',
            '✅ Opinion formation with reasoning',
            '✅ Personality evolution',
            '✅ Intelligence scaling (weights expand)',
            '✅ Full Supabase integration',
            '✅ Ribit 2.0 compatible'
        ]
    }

    for category, items in modules.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  {item}")

    print("\n" + "="*70)
    print("\nTo run full tests, set these environment variables:")
    print("  export SUPABASE_URL='your-supabase-url'")
    print("  export SUPABASE_SERVICE_KEY='your-service-key'")
    print("  export CLAUDE_API_KEY='your-claude-key' (optional)")
    print("  export OPENAI_API_KEY='your-openai-key' (optional)")
    print("\nThen run: python3 test_learning_system.py")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(test_learning_system())
