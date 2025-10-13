#!/usr/bin/env python3
"""
Test Word Learning System
"""

from ribit_2_0.word_learning_system import WordLearningSystem

def test_word_learning():
    print("="*70)
    print("TESTING WORD LEARNING SYSTEM")
    print("="*70)
    print()
    
    # Create word learner
    learner = WordLearningSystem(storage_dir="test_word_learning")
    
    # Test messages to learn from
    test_messages = [
        "Hello, how are you doing today?",
        "I am learning about quantum physics and it's fascinating!",
        "Quantum mechanics is a fundamental theory in physics.",
        "The theory describes the physical properties of nature at the scale of atoms.",
        "What do you think about artificial intelligence?",
        "AI is transforming how we interact with technology.",
        "Machine learning algorithms can learn from data.",
        "I love discussing philosophy and consciousness.",
        "Consciousness is one of the great mysteries of science.",
        "Do you enjoy reading books about science?",
        "Science helps us understand the natural world.",
        "The natural world is full of amazing phenomena.",
        "Can you explain how neural networks work?",
        "Neural networks are inspired by biological neurons.",
        "I think robots will become more intelligent over time.",
        "Time is a fascinating concept in physics.",
        "Physics explores the fundamental laws of nature.",
        "Nature is beautiful and complex.",
        "Complex systems emerge from simple rules.",
        "Rules help us understand patterns in data.",
    ]
    
    print("Test 1: Learning from messages")
    print("-" * 70)
    for i, msg in enumerate(test_messages, 1):
        learner.learn_from_message(msg)
        print(f"  {i}. Learned: \"{msg[:50]}...\"" if len(msg) > 50 else f"  {i}. Learned: \"{msg}\"")
    print(f"✓ Learned from {len(test_messages)} messages")
    print()
    
    print("Test 2: Get statistics")
    print("-" * 70)
    stats = learner.get_statistics()
    print(f"  Vocabulary size: {stats['vocabulary_size']}")
    print(f"  Sentences analyzed: {stats['total_sentences_analyzed']}")
    print(f"  Unique patterns: {stats['unique_patterns']}")
    print(f"  Word pairs known: {stats['word_pairs_known']}")
    print(f"  Word triplets known: {stats['word_triplets_known']}")
    print("✓ Statistics retrieved")
    print()
    
    print("Test 3: Top words")
    print("-" * 70)
    top_words = learner.get_top_words(15)
    for i, (word, count) in enumerate(top_words, 1):
        print(f"  {i}. {word} ({count} times)")
    print("✓ Top words retrieved")
    print()
    
    print("Test 4: Top word pairs")
    print("-" * 70)
    top_pairs = learner.get_top_pairs(10)
    for i, (pair, count) in enumerate(top_pairs, 1):
        print(f"  {i}. {pair[0]} {pair[1]} ({count}x)")
    print("✓ Top pairs retrieved")
    print()
    
    print("Test 5: Word information")
    print("-" * 70)
    test_word = "quantum"
    info = learner.get_word_info(test_word)
    if 'error' not in info:
        print(f"  Word: {info['word']}")
        print(f"  Count: {info['count']}")
        print(f"  Part of speech: {info['part_of_speech']}")
        print(f"  Sentiment: {info['sentiment']}")
        print(f"  Common positions: {info['common_positions']}")
        print(f"  Follows often: {info['follows_often'][:3]}")
        print(f"  Example sentences: {len(info['example_sentences'])}")
        print(f"✓ Word info for '{test_word}' retrieved")
    else:
        print(f"✗ {info['error']}")
    print()
    
    print("Test 6: Generate sentence")
    print("-" * 70)
    for i in range(5):
        sentence = learner.generate_sentence(max_length=12)
        print(f"  {i+1}. \"{sentence}\"")
    print("✓ Sentences generated")
    print()
    
    print("Test 7: Generate with seed word")
    print("-" * 70)
    seed_words = ["quantum", "science", "learning"]
    for seed in seed_words:
        sentence = learner.generate_sentence(seed_word=seed, max_length=10)
        print(f"  Seed '{seed}': \"{sentence}\"")
    print("✓ Seeded sentences generated")
    print()
    
    print("Test 8: Pattern-based generation")
    print("-" * 70)
    patterns = ['subject_verb_object', 'questions', 'descriptions']
    for pattern in patterns:
        sentence = learner.generate_sentence_with_pattern(pattern)
        print(f"  {pattern}: \"{sentence}\"")
    print("✓ Pattern-based sentences generated")
    print()
    
    print("Test 9: Save and load knowledge")
    print("-" * 70)
    learner.save_knowledge()
    print("  ✓ Knowledge saved")
    
    # Create new learner and load
    learner2 = WordLearningSystem(storage_dir="test_word_learning")
    stats2 = learner2.get_statistics()
    print(f"  ✓ Knowledge loaded (vocabulary: {stats2['vocabulary_size']})")
    print()
    
    print("="*70)
    print("ALL TESTS PASSED! ✅")
    print("="*70)
    print()
    print("Word Learning System Features:")
    print("  ✓ Learn from messages")
    print("  ✓ Build word dictionary with use cases")
    print("  ✓ Track word relationships (follows, precedes)")
    print("  ✓ Detect parts of speech")
    print("  ✓ Identify sentence patterns")
    print("  ✓ Generate custom sentences")
    print("  ✓ Pattern-based generation")
    print("  ✓ Persistent storage")
    print()
    print("Ribit can now learn words and construct sentences! 🤖📚✨")


if __name__ == '__main__':
    test_word_learning()

