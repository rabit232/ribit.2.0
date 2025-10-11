#!/usr/bin/env python3
"""
Test script to verify message triggering logic
"""

import re

def is_message_for_bot(message: str, bot_name: str = "ribit.2.0") -> bool:
    """Check if message is directed at the bot."""
    message_lower = message.lower()
    return (
        bot_name in message_lower or
        'ribit' in message_lower or
        message.startswith('?') or
        '!reset' in message_lower
    )

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
]

print("🧪 Testing Message Trigger Logic")
print("=" * 60)
print()

for msg in test_messages:
    triggered = is_message_for_bot(msg)
    cleaned = clean_message(msg) if triggered else "N/A"
    status = "✅ TRIGGERED" if triggered else "❌ IGNORED"
    
    print(f"{status}")
    print(f"  Original: {msg}")
    if triggered:
        print(f"  Cleaned:  {cleaned}")
    print()

print("=" * 60)
print()
print("💡 Tips for triggering the bot:")
print("  • Include 'ribit.2.0' in your message")
print("  • Include 'ribit' in your message")
print("  • Start with '?' for commands")
print("  • Use '!reset' to reset context")
print()
print("⚠️  Note: The bot name check is case-insensitive")
print("⚠️  Note: The bot looks for 'ribit' as a word, not just substring")

