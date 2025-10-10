#!/usr/bin/env python3
"""
Test script to verify NEW message triggering logic
Now responds to ALL messages!
"""

import re

def is_message_for_bot(message: str, bot_name: str = "ribit.2.0") -> bool:
    """Check if message is directed at the bot.
    
    NEW BEHAVIOR: Responds to ALL messages for natural conversation.
    """
    # Always respond to all messages for natural conversation
    return True

def clean_message(message: str, bot_name: str = "ribit.2.0") -> str:
    """Clean the message by removing bot mentions."""
    # Remove bot name mentions
    clean = re.sub(rf'\b{re.escape(bot_name)}\b', '', message, flags=re.IGNORECASE)
    clean = re.sub(r'\bribit\b', '', clean, flags=re.IGNORECASE)
    return clean.strip()

# Test cases
test_messages = [
    "ribit.2.0 hello",
    "ribit hello",
    "Hey ribit.2.0, how are you?",
    "RIBIT.2.0 test",
    "@ribit.2.0 hello",
    "ribit:2.0 hello",
    "?help",
    "!reset",
    "just a normal message",
    "ribit2.0 hello",
    "ribit 2.0 hello",
    "What's the weather like?",
    "How are you?",
    "Tell me about philosophy",
    "Good morning!",
]

print("🧪 Testing NEW Message Trigger Logic")
print("=" * 60)
print()
print("🎉 NEW BEHAVIOR: Bot responds to ALL messages!")
print()

for msg in test_messages:
    triggered = is_message_for_bot(msg)
    cleaned = clean_message(msg) if triggered else "N/A"
    status = "✅ WILL RESPOND" if triggered else "❌ IGNORED"
    
    print(f"{status}")
    print(f"  Original: {msg}")
    print(f"  Cleaned:  {cleaned}")
    print()

print("=" * 60)
print()
print("💡 NEW Bot Behavior:")
print("  ✅ Responds to ALL messages in the room")
print("  ✅ No need to say 'ribit.2.0' or 'ribit'")
print("  ✅ Natural conversation mode")
print("  ✅ Commands still work: ?help, ?status, !reset")
print()
print("🎯 Examples that now work:")
print("  • 'What's the weather?'")
print("  • 'How are you?'")
print("  • 'Tell me about philosophy'")
print("  • 'Good morning!'")
print()
print("⚠️  Note: Bot still ignores its own messages")
print("⚠️  Note: Bot still needs to be in the room to see messages")
