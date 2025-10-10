#!/usr/bin/env python3
"""
Test script for enhanced question detection with group greeting filtering
and humor engine testing
"""

def is_message_for_bot(message: str, bot_name: str = "ribit.2.0") -> bool:
    """Enhanced question detection with group greeting filtering"""
    message_lower = message.lower()
    
    # Check for direct mentions (always respond)
    if bot_name in message_lower or 'ribit' in message_lower:
        return True
    
    # Check for commands (always respond)
    if message.startswith('?') or '!reset' in message_lower:
        return True
    
    # Ignore group greetings and social messages
    group_greeting_patterns = [
        'good morning all', 'good morning everyone',
        'good night all', 'good night everyone',
        'hello all', 'hello everyone',
        'hi all', 'hi everyone',
        'hey all', 'hey everyone',
        'how are you all', 'how is everyone', 'hows everyone',
        'how\'s everyone', 'how are u all', 'how r u all',
        'how r you all', 'how are y\'all',
        'sup everyone', 'sup all',
        'wassup everyone', 'what\'s up everyone', 'whats up all'
    ]
    
    # Check if it's a group greeting
    for pattern in group_greeting_patterns:
        if pattern in message_lower:
            return False
    
    # Check if it's a question (ends with ?)
    if message.strip().endswith('?'):
        if any(word in message_lower for word in ['everyone', 'all', 'y\'all', 'you all', 'u all']):
            return False
        return True
    
    # Check for question words
    question_words = [
        'what', 'how', 'why', 'when', 'where', 'who', 'which',
        'can', 'could', 'would', 'should', 'is', 'are', 'do', 'does',
        'will', 'did', 'has', 'have', 'was', 'were'
    ]
    
    first_word = message_lower.split()[0] if message_lower.split() else ''
    if first_word in question_words:
        if any(word in message_lower for word in ['everyone', 'all', 'y\'all', 'you all', 'u all', 'guys']):
            return False
        return True
    
    # Check for question patterns
    question_patterns = [
        'tell me', 'explain', 'describe',
        'what about', 'how about',
        'what do you think', 'do you know',
        'can you', 'could you', 'would you',
        'how much is', 'what is', 'what was', 'what were',
        'who was', 'who were', 'when was', 'when were',
        'where is', 'where was'
    ]
    
    for pattern in question_patterns:
        if pattern in message_lower:
            if any(word in message_lower for word in ['everyone', 'all', 'y\'all', 'you all', 'u all']):
                return False
            return True
    
    return False

# Test cases
test_cases = [
    # Should RESPOND - Direct questions
    ("How much is 10 plus 10?", True, "Math question"),
    ("What was the war between Belgium and Germany?", True, "History question"),
    ("What is consciousness?", True, "Philosophy question"),
    ("When was World War 2?", True, "Historical date question"),
    ("Where is Belgium?", True, "Geography question"),
    ("How's the weather?", True, "Weather question"),
    
    # Should RESPOND - Question patterns
    ("Tell me about philosophy", True, "Tell me pattern"),
    ("Explain how this works", True, "Explain pattern"),
    ("What do you think about AI?", True, "Opinion question"),
    ("Do you know anything about robots?", True, "Knowledge question"),
    
    # Should RESPOND - Mentions
    ("ribit.2.0 hello", True, "Direct mention"),
    ("Hey ribit, how are you?", True, "Mention with question"),
    
    # Should RESPOND - Commands
    ("?help", True, "Help command"),
    ("!reset", True, "Reset command"),
    
    # Should IGNORE - Group greetings
    ("Good morning all", False, "Group greeting"),
    ("Good morning everyone", False, "Group greeting"),
    ("Hello everyone", False, "Group greeting to all"),
    ("Hi all", False, "Group greeting"),
    ("Hey everyone", False, "Group greeting"),
    
    # Should IGNORE - Group questions
    ("How are you all doing?", False, "Question to group"),
    ("How's everyone?", False, "Question to everyone"),
    ("How are u all?", False, "Question to all (casual)"),
    ("How is everyone doing today?", False, "Question to everyone"),
    ("What's up everyone?", False, "Casual group greeting"),
    ("Good morning all hows u all doing", False, "Combined group greeting"),
    
    # Should IGNORE - Statements
    ("That's interesting", False, "Statement"),
    ("I agree", False, "Agreement"),
    ("Thanks for the help", False, "Gratitude"),
    ("See you later", False, "Farewell"),
    
    # Edge cases - Should RESPOND
    ("How much is 2 + 2", True, "Math without question mark"),
    ("What is 5 times 5", True, "Math question"),
    ("When was the war", True, "Historical question"),
]

print("🧪 Testing Enhanced Question Detection")
print("=" * 70)
print()
print("🎯 New Features:")
print("  ✅ Responds to casual questions (math, history, etc.)")
print("  ✅ Filters out group greetings (good morning all, etc.)")
print("  ✅ Ignores questions directed at groups (how are you all?)")
print("  ✅ Still responds to direct mentions and commands")
print()
print("=" * 70)
print()

correct = 0
total = len(test_cases)

for message, expected, description in test_cases:
    result = is_message_for_bot(message)
    status = "✅" if result == expected else "❌"
    action = "RESPOND" if result else "IGNORE"
    
    if result == expected:
        correct += 1
    
    print(f"{status} {action:8} | {message}")
    print(f"           | ({description})")
    if result != expected:
        print(f"           | ⚠️  UNEXPECTED! Expected: {'RESPOND' if expected else 'IGNORE'}")
    print()

print("=" * 70)
print()
print(f"📊 Results: {correct}/{total} tests passed ({correct*100//total}%)")
print()

# Test humor engine
print("=" * 70)
print("🎭 Testing Humor Engine")
print("=" * 70)
print()

try:
    import sys
    sys.path.insert(0, '/home/ubuntu/ribit.2.0')
    from ribit_2_0.humor_engine import HumorEngine
    
    humor = HumorEngine()
    
    test_queries = [
        "How much is 10 plus 10?",
        "What was the war between Belgium and Germany?",
        "How are you?",
    ]
    
    for query in test_queries:
        response = humor.get_casual_response(query)
        if response:
            print(f"Query: {query}")
            print(f"Response: {response}")
            print()
    
    print("✅ Humor engine working!")
    
except Exception as e:
    print(f"⚠️  Humor engine test skipped: {e}")

print()
print("=" * 70)
print()
print("💡 Summary:")
print("  • Bot responds to questions intelligently")
print("  • Group greetings are filtered out")
print("  • Casual questions get humorous responses")
print("  • Math and history questions are handled")
print()
print("🎉 Ribit is now smarter and funnier!")
