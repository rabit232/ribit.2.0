#!/usr/bin/env python3
"""
Test script for Ribit's web knowledge and Wikipedia integration
"""

import sys
sys.path.insert(0, '/home/ubuntu/ribit.2.0')

from ribit_2_0.web_knowledge import WebKnowledge
from ribit_2_0.intelligent_responder import IntelligentResponder

print("=" * 70)
print("🌐 Testing Ribit's Web Knowledge & Wikipedia Integration")
print("=" * 70)
print()

# Initialize
web_knowledge = WebKnowledge()
intelligent = IntelligentResponder()

print("
