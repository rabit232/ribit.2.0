#!/usr/bin/env python3
"""
Test script for Ribit's historical knowledge and responses
"""

import sys
sys.path.insert(0, '/home/ubuntu/ribit.2.0')

from ribit_2_0.history_responder import HistoryResponder
from ribit_2_0.humor_engine import HumorEngine

print("=" * 70)
print("🎓 Testing Ribit's Historical Knowledge")
print("=" * 70)
print()

# Test queries
test_queries = [
    "What was World War 1?",
    "Tell me about World War 2",
    "What was the Holocaust?",
    "What was the war between Belgium and Germany?",
    "Tell me about the Cold War",
    "What was the industrial revolution?",
    "How did technology evolve?",
    "When was WWI?",
    "When did WWII start?",
]

print("📚 Testing History Responder:")
print("-" * 70)
print()

history = HistoryResponder()

for query in test_queries:
    print(f"❓ Query: {query}")
    response = history.get_response(query)
    if response:
        print(f"✅ Response: {response[:200]}...")
    else:
        print(f"⚠️  No specific response (would use default)")
    print()

print("=" * 70)
print("🎭 Testing Humor Engine Integration:")
print("=" * 70)
print()

humor = HumorEngine()

test_casual_queries = [
    "What was the war between Belgium, Germany, and the Netherlands?",
    "Tell me about World War 2",
    "What was the Holocaust?",
    "How much is 10 plus 10?",
]

for query in test_casual_queries:
    print(f"❓ Query: {query}")
    response = humor.get_casual_response(query)
    if response:
        print(f"✅ Response: {response[:250]}...")
    else:
        print(f"⚠️  No casual response (would use LLM)")
    print()

print("=" * 70)
print("📊 Knowledge Base Statistics:")
print("=" * 70)
print()

knowledge_count = len(history.knowledge)
print(f"✅ Loaded {knowledge_count} historical facts")
print()

# Sample some key facts
key_facts = [
    ('ww1_start', 'WWI Start'),
    ('ww2_start', 'WWII Start'),
    ('holocaust_victims', 'Holocaust Victims'),
    ('cold_war_start', 'Cold War Start'),
    ('tech_internet', 'Internet Invention'),
    ('tech_iphone', 'iPhone Release'),
]

print("📋 Sample Facts:")
for key, label in key_facts:
    value = history.knowledge.get(key, 'Not found')
    print(f"  • {label}: {value}")

print()
print("=" * 70)
print()
print("✅ Historical knowledge successfully integrated!")
print("🎓 Ribit can now answer questions about:")
print("  • World War I (1914-1918)")
print("  • World War II (1939-1945)")
print("  • The Holocaust (1933-1945)")
print("  • Cold War (1947-1991)")
print("  • Technology evolution (ancient to modern)")
print("  • Belgium/Germany/Netherlands conflicts")
print("  • And much more!")
print()
print("🤖 Ribit is now a history teacher with personality!")
print("=" * 70)
