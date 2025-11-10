"""
Megabite - Enhanced Mock LLM with Intelligence Scaling

Mock LLM that expands intelligence based on learned vocabulary and personality.

Author: Manus AI
"""

import logging
from typing import List, Dict, Any, Optional
import random

from .word_learning_manager import WordLearningManager

logger = logging.getLogger(__name__)


class EnhancedMockLLM:
    """
    Mock LLM with intelligence that scales based on learning.

    Features:
    - Response complexity scales with vocabulary
    - Uses learned word patterns
    - Integrates personality traits
    - Weights expand as knowledge grows
    """

    def __init__(self, word_learning: Optional[WordLearningManager] = None):
        """Initialize enhanced mock LLM."""
        self.word_learning = word_learning
        self.base_responses = {
            'greeting': [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Greetings! I'm here to assist."
            ],
            'question': [
                "That's an interesting question. Let me think about it.",
                "Based on what I know, here's my perspective...",
                "I have some thoughts on that topic."
            ],
            'statement': [
                "I understand what you're saying.",
                "That's worth considering.",
                "Interesting point."
            ]
        }

    async def generate_response(
        self,
        message: str,
        context: Optional[List[str]] = None
    ) -> str:
        """
        Generate response with intelligence scaling.

        Args:
            message: Input message
            context: Optional conversation context

        Returns:
            Generated response
        """
        # Get current intelligence quotient
        if self.word_learning:
            try:
                iq = await self.word_learning.get_intelligence_quotient()
                weight = iq.get('total_weight', 1.0)
                level = iq.get('intelligence_level', 'developing')
                vocab_size = iq.get('vocabulary_size', 0)
            except:
                weight = 1.0
                level = 'developing'
                vocab_size = 0
        else:
            weight = 1.0
            level = 'developing'
            vocab_size = 0

        # Determine response type
        message_lower = message.lower()
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            response_type = 'greeting'
        elif '?' in message:
            response_type = 'question'
        else:
            response_type = 'statement'

        # Get base response
        base = random.choice(self.base_responses[response_type])

        # Enhance based on intelligence level
        if level == 'developing':
            # Simple responses
            response = base

        elif level == 'intermediate':
            # Add some detail
            response = f"{base} "
            if vocab_size > 500:
                response += f"I've learned {vocab_size} words, which helps me understand better."

        elif level == 'advanced':
            # More sophisticated
            if self.word_learning:
                try:
                    # Try to use learned words
                    common_words = await self.word_learning.get_most_common_words(limit=10)
                    if common_words:
                        vocab_sample = ', '.join([w['word'] for w in common_words[:3]])
                        response = f"{base} My vocabulary includes words like: {vocab_sample}. "
                    else:
                        response = base
                except:
                    response = base
            else:
                response = base

            response += f"My intelligence weight is {weight:.2f}, which allows for nuanced understanding."

        else:  # expert
            # Very sophisticated
            response = f"{base}\n\n"
            response += f"Drawing from my vocabulary of {vocab_size} words "
            response += f"(intelligence level: {level}, weight: {weight:.2f}), "
            response += "I can provide a comprehensive perspective. "

            if self.word_learning:
                try:
                    # Include personality-influenced response
                    response += "My personality traits and learned patterns inform this response."
                except:
                    pass

        return response

    async def get_intelligence_summary(self) -> Dict[str, Any]:
        """Get summary of current intelligence metrics."""
        if not self.word_learning:
            return {
                'status': 'not_connected',
                'message': 'Word learning manager not available'
            }

        try:
            iq = await self.word_learning.get_intelligence_quotient()
            stats = await self.word_learning.get_vocabulary_stats()

            return {
                'status': 'ok',
                'intelligence_level': iq.get('intelligence_level', 'unknown'),
                'total_weight': iq.get('total_weight', 1.0),
                'vocabulary_size': iq.get('vocabulary_size', 0),
                'word_usage_total': iq.get('word_usage_total', 0),
                'weight_breakdown': {
                    'base': iq.get('base_weight', 1.0),
                    'vocabulary': iq.get('vocabulary_weight', 0.0),
                    'patterns': iq.get('pattern_weight', 0.0),
                    'personality': iq.get('personality_weight', 0.0)
                },
                'capabilities': self._get_capabilities_for_level(
                    iq.get('intelligence_level', 'developing')
                )
            }

        except Exception as e:
            logger.error(f"Error getting intelligence summary: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }

    def _get_capabilities_for_level(self, level: str) -> List[str]:
        """Get capabilities for intelligence level."""
        capabilities = {
            'developing': [
                'Basic conversation',
                'Simple responses'
            ],
            'intermediate': [
                'Vocabulary-aware responses',
                'Context understanding',
                'Pattern recognition'
            ],
            'advanced': [
                'Nuanced communication',
                'Learned pattern usage',
                'Personality integration',
                'Complex reasoning'
            ],
            'expert': [
                'Sophisticated dialogue',
                'Deep context awareness',
                'Strong personality expression',
                'Advanced pattern synthesis',
                'Opinion formation',
                'Perspective analysis'
            ]
        }

        return capabilities.get(level, capabilities['developing'])
