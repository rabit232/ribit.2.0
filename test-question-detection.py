#!/usr/bin/env python3
"""
Test script for intelligent question detection
Bot responds to questions, mentions, and commands
"""

def is_message_for_bot(message: str, bot_name: str = "ribit.2.0") -> bool:
    """Check if message is directed at the bot.
    
    Intelligent detection:
    - Responds to questions (ends with ? or contains question words)
    - Responds to direct mentions (ribit, ribit.2.0)
    - Responds to commands (?help, !reset)
    """
    message_lower = message.lower()
    
    # Check for direct mentions
    if bot_name in message_lower or 'ribit' in message_lower:
        return True
    
    # Check for commands
    if message.startswith('?') or '!reset' in message_lower:
        return True
    
    # Check if it's a question (ends with ?)
    if message.strip().endswith('?'):
        return True
    
    # Check for question words
    question_words = [
        'what', 'how', 'why', 'when', 'where', 'who', 'which',
        'can', 'could', 'would', 'should', 'is', 'are', 'do', 'does',
        'will', 'did', 'has', 'have', 'was', 'were'
    ]
    
    # Check if message starts with a question word
    first_word = message_lower.split()[0] if message_lower.split() else ''
    if first_word in question_words:
        return True
    
    # Check if message contains question patterns
    question_patterns = [
        'tell me',
        'explain',
        'describe',
        'what about',
        'how about',
        'what do you think',
        'do you know',
        'can you',
        'could you',
        'would you'
    ]
    
    for pattern in question_patterns:
        if pattern in message_lower:
            return True
    
    return False

# Test cases
test_messages = [
    # Questions with ?
    ("How's the weather?", True, "Question with ?"),
    ("What time is it?", True, "Question with ?"),
    ("Is it raining?", True, "Question with ?"),
    
    # Questions starting with question words
    ("What is consciousness", True, "Starts with 'what'"),
    ("How does this work", True, "Starts with 'how'"),
    ("Why do we exist", True, "Starts with 'why'"),
    ("When will it be ready", True, "Starts with 'when'"),
    ("Where are you from", True, "Starts with 'where'"),
    ("Who are you", True, "Starts with 'who'"),
    ("Can you help me", True, "Starts with 'can'"),
    ("Would you explain this", True, "Starts with 'would'"),
    ("Should I do this", True, "Starts with 'should'"),
    ("Do you understand", True, "Starts with 'do'"),
    ("Did you see that", True, "Starts with 'did'"),
    ("Are you there", True, "Starts with 'are'"),
    ("Is this correct", True, "Starts with 'is'"),
    
    # Question patterns
    ("Tell me about philosophy", True, "Contains 'tell me'"),
    ("Explain how this works", True, "Contains 'explain'"),
    ("Describe the process", True, "Contains 'describe'"),
    ("What about free will", True, "Contains 'what about'"),
    ("How about we discuss this", True, "Contains 'how about'"),
    ("What do you think about AI", True, "Contains 'what do you think'"),
    ("Do you know anything about robots", True, "Contains 'do you know'"),
    ("Can you help with this", True, "Contains 'can you'"),
    ("Could you explain that", True, "Contains 'could you'"),
    ("Would you like to chat", True, "Contains 'would you'"),
    
    # Direct mentions
    ("ribit.2.0 hello", True, "Direct mention"),
    ("Hey ribit, how are you", True, "Contains 'ribit'"),
    ("@ribit.2.0 test", True, "Mention with @"),
    
    # Commands
    ("?help", True, "Command"),
    ("?status", True, "Command"),
    ("!reset", True, "Reset command"),
    
    # Should NOT trigger
    ("Good morning everyone", False, "Casual greeting"),
    ("I'm going to lunch", False, "Statement"),
    ("That's interesting", False, "Comment"),
    ("Hello there", False, "Greeting without mention"),
    ("Thanks for the help", False, "Gratitude"),
    ("See you later", False, "Farewell"),
    ("Nice weather today", False, "Observation"),
    ("I agree with that", False, "Agreement"),
]

print("🧪 Testing Intelligent Question Detection")
print("=" * 70)
print()
print("🎯 Bot responds to:")
print("  ✅ Questions ending with ?")
print("  ✅ Messages starting with question words (what, how, why, etc.)")
print("  ✅ Question patterns (tell me, explain, describe, etc.)")
print("  ✅ Direct mentions (ribit, ribit.2.0)")
print("  ✅ Commands (?help, !reset)")
print()
print("  ❌ Casual chat without questions")
print()
print("=" * 70)
print()

correct = 0
total = len(test_messages)

for message, expected, description in test_messages:
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
print("💡 Summary:")
print("  • Questions are detected intelligently")
print("  • Casual chat is ignored (less noise)")
print("  • Direct mentions always work")
print("  • Commands always work")
print()
print("🎉 This creates a smart, context-aware bot that knows when to respond!")
