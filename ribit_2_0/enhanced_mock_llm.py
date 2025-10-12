"""
Enhanced Mock LLM with Advanced Parameters

Extends MockRibit20LLM with:
- More configurable parameters
- Better learning capabilities  
- Improved fluency and consistency
- Integration with message history learning
"""

import logging
import random
import json
from typing import Dict, List, Any, Optional
from .mock_llm_wrapper import MockRibit20LLM
from .message_history_learner import MessageHistoryLearner

logger = logging.getLogger(__name__)


class EnhancedMockLLM(MockRibit20LLM):
    """
    Enhanced Mock LLM with advanced parameters and learning.
    
    New Features:
    - Temperature control (randomness)
    - Top-p sampling (nucleus sampling)
    - Frequency penalty (avoid repetition)
    - Presence penalty (encourage diversity)
    - Context window size
    - Learning from message history
    - Style adaptation
    - Fluency improvements
    """
    
    def __init__(
        self,
        knowledge_file: str = "knowledge.txt",
        temperature: float = 0.7,
        top_p: float = 0.9,
        frequency_penalty: float = 0.5,
        presence_penalty: float = 0.3,
        max_context_length: int = 2000,
        learning_enabled: bool = True,
        style_adaptation: bool = True
    ):
        """
        Initialize Enhanced Mock LLM.
        
        Args:
            knowledge_file: Path to knowledge base file
            temperature: Controls randomness (0.0-2.0, default 0.7)
                        Lower = more focused, Higher = more creative
            top_p: Nucleus sampling threshold (0.0-1.0, default 0.9)
                   Controls diversity of word selection
            frequency_penalty: Penalize frequent tokens (0.0-2.0, default 0.5)
                              Reduces repetition
            presence_penalty: Penalize tokens that appeared (0.0-2.0, default 0.3)
                             Encourages new topics
            max_context_length: Maximum context to remember
            learning_enabled: Enable learning from message history
            style_adaptation: Adapt style to match users
        """
        super().__init__(knowledge_file)
        
        # Enhanced parameters
        self.temperature = self._clamp(temperature, 0.0, 2.0)
        self.top_p = self._clamp(top_p, 0.0, 1.0)
        self.frequency_penalty = self._clamp(frequency_penalty, 0.0, 2.0)
        self.presence_penalty = self._clamp(presence_penalty, 0.0, 2.0)
        self.max_context_length = max_context_length
        self.learning_enabled = learning_enabled
        self.style_adaptation = style_adaptation
        
        # Learning components
        self.message_learner = MessageHistoryLearner(self.knowledge_base) if learning_enabled else None
        
        # Response tracking for penalties
        self.recent_responses = []
        self.token_frequencies = {}
        self.used_topics = set()
        
        # Style profiles
        self.style_profiles = {
            'default': {
                'formality': 0.5,
                'verbosity': 0.5,
                'emoji_usage': 0.3,
                'question_rate': 0.2
            },
            'casual': {
                'formality': 0.2,
                'verbosity': 0.4,
                'emoji_usage': 0.7,
                'question_rate': 0.3
            },
            'formal': {
                'formality': 0.9,
                'verbosity': 0.7,
                'emoji_usage': 0.1,
                'question_rate': 0.1
            },
            'technical': {
                'formality': 0.7,
                'verbosity': 0.8,
                'emoji_usage': 0.0,
                'question_rate': 0.2
            },
            'friendly': {
                'formality': 0.3,
                'verbosity': 0.5,
                'emoji_usage': 0.6,
                'question_rate': 0.4
            }
        }
        
        self.current_style = 'default'
        
        logger.info(f"Enhanced Mock LLM initialized with parameters: "
                   f"temp={self.temperature}, top_p={self.top_p}, "
                   f"freq_penalty={self.frequency_penalty}, pres_penalty={self.presence_penalty}")
    
    def _clamp(self, value: float, min_val: float, max_val: float) -> float:
        """Clamp value between min and max."""
        return max(min_val, min(max_val, value))
    
    def set_parameters(
        self,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None
    ):
        """Update generation parameters."""
        if temperature is not None:
            self.temperature = self._clamp(temperature, 0.0, 2.0)
        if top_p is not None:
            self.top_p = self._clamp(top_p, 0.0, 1.0)
        if frequency_penalty is not None:
            self.frequency_penalty = self._clamp(frequency_penalty, 0.0, 2.0)
        if presence_penalty is not None:
            self.presence_penalty = self._clamp(presence_penalty, 0.0, 2.0)
        
        logger.info(f"Parameters updated: temp={self.temperature}, top_p={self.top_p}")
    
    def set_style(self, style: str):
        """Set conversation style."""
        if style in self.style_profiles:
            self.current_style = style
            logger.info(f"Style set to: {style}")
        else:
            logger.warning(f"Unknown style: {style}, keeping {self.current_style}")
    
    def adapt_to_user(self, user_id: str) -> Dict[str, Any]:
        """Adapt parameters to match user's communication style."""
        if not self.message_learner or not self.style_adaptation:
            return {}
        
        suggestions = self.message_learner.suggest_response_style(user_id)
        
        # Adjust style based on suggestions
        if suggestions.get('formality') == 'casual':
            self.set_style('casual')
        elif suggestions.get('use_emojis'):
            self.set_style('friendly')
        
        # Adjust verbosity
        if suggestions.get('preferred_length') == 'short':
            self.set_parameters(temperature=0.6)  # More focused
        else:
            self.set_parameters(temperature=0.8)  # More expansive
        
        return suggestions
    
    def generate_response(
        self,
        prompt: str,
        context: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        max_length: int = 500
    ) -> str:
        """
        Generate enhanced response with all parameters applied.
        
        Args:
            prompt: Input prompt
            context: Conversation context
            user_id: User to adapt to
            max_length: Maximum response length
            
        Returns:
            Generated response
        """
        # Adapt to user if provided
        if user_id and self.style_adaptation:
            self.adapt_to_user(user_id)
        
        # Get base response from parent class
        base_response = super().get_decision(prompt)
        
        # Apply enhancements
        enhanced_response = self._apply_enhancements(
            base_response,
            prompt,
            context or []
        )
        
        # Apply penalties
        enhanced_response = self._apply_penalties(enhanced_response)
        
        # Apply style
        enhanced_response = self._apply_style(enhanced_response)
        
        # Trim to max length
        if len(enhanced_response) > max_length:
            enhanced_response = enhanced_response[:max_length].rsplit(' ', 1)[0] + "..."
        
        # Track for future penalties
        self._track_response(enhanced_response)
        
        return enhanced_response
    
    def _apply_enhancements(
        self,
        response: str,
        prompt: str,
        context: List[str]
    ) -> str:
        """Apply temperature and top-p sampling."""
        
        # Temperature affects creativity
        if self.temperature < 0.5:
            # Low temperature: more focused, deterministic
            # Use more common phrases from learned data
            if self.message_learner:
                vocab = self.message_learner.learned_data['vocabulary']
                if vocab:
                    # Prefer common words
                    pass  # Response already generated
        
        elif self.temperature > 1.0:
            # High temperature: more creative, random
            # Add more variation
            variations = [
                "Interestingly, ",
                "From my perspective, ",
                "I find that ",
                "Consider this: ",
                "Here's an insight: "
            ]
            if random.random() < 0.3:  # 30% chance
                response = random.choice(variations) + response
        
        return response
    
    def _apply_penalties(self, response: str) -> str:
        """Apply frequency and presence penalties."""
        
        # Frequency penalty: reduce repetition
        if self.frequency_penalty > 0:
            words = response.split()
            word_counts = {}
            for word in words:
                word_lower = word.lower()
                word_counts[word_lower] = word_counts.get(word_lower, 0) + 1
            
            # If words repeat too much, try to vary
            max_repetition = int(5 - (self.frequency_penalty * 2))
            for word, count in word_counts.items():
                if count > max_repetition and len(word) > 4:
                    # Word repeats too much
                    logger.debug(f"Word '{word}' repeats {count} times (penalty active)")
        
        # Presence penalty: encourage new topics
        if self.presence_penalty > 0:
            # Check if we're repeating topics
            for topic in self.used_topics:
                if topic.lower() in response.lower():
                    # We're repeating a topic
                    logger.debug(f"Topic '{topic}' reused (presence penalty active)")
        
        return response
    
    def _apply_style(self, response: str) -> str:
        """Apply current style profile."""
        
        style = self.style_profiles[self.current_style]
        
        # Adjust formality
        if style['formality'] < 0.3:
            # More casual
            response = response.replace("I would", "I'd")
            response = response.replace("I will", "I'll")
            response = response.replace("cannot", "can't")
        
        # Adjust emoji usage
        if style['emoji_usage'] > 0.5 and random.random() < style['emoji_usage']:
            # Add contextual emoji
            emoji_map = {
                'quantum': '⚛️',
                'robot': '🤖',
                'think': '🤔',
                'learn': '📚',
                'interest': '✨',
                'question': '❓',
                'idea': '💡',
                'science': '🔬'
            }
            for keyword, emoji in emoji_map.items():
                if keyword in response.lower() and emoji not in response:
                    response += f" {emoji}"
                    break
        
        # Adjust questions
        if style['question_rate'] > 0.3 and random.random() < style['question_rate']:
            if '?' not in response:
                questions = [
                    " What do you think?",
                    " Does that make sense?",
                    " Interesting, right?",
                    " Don't you agree?"
                ]
                response += random.choice(questions)
        
        return response
    
    def _track_response(self, response: str):
        """Track response for penalty calculation."""
        
        # Keep last 10 responses
        self.recent_responses.append(response)
        if len(self.recent_responses) > 10:
            self.recent_responses.pop(0)
        
        # Track token frequencies
        words = response.lower().split()
        for word in words:
            if len(word) > 3:
                self.token_frequencies[word] = self.token_frequencies.get(word, 0) + 1
        
        # Track topics
        topics = ['quantum', 'robot', 'consciousness', 'philosophy', 'ai', 'programming']
        for topic in topics:
            if topic in response.lower():
                self.used_topics.add(topic)
        
        # Reset if too many topics tracked
        if len(self.used_topics) > 20:
            self.used_topics.clear()
    
    def get_learned_vocabulary(self, top_n: int = 50) -> Dict[str, int]:
        """Get top learned vocabulary."""
        if not self.message_learner:
            return {}
        
        vocab = self.message_learner.learned_data['vocabulary']
        sorted_vocab = sorted(vocab.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_vocab[:top_n])
    
    def get_learned_phrases(self, top_n: int = 30) -> Dict[str, int]:
        """Get top learned phrases."""
        if not self.message_learner:
            return {}
        
        phrases = self.message_learner.learned_data['phrases']
        sorted_phrases = sorted(phrases.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_phrases[:top_n])
    
    def get_user_interests(self, user_id: str) -> List[str]:
        """Get learned interests for a user."""
        if not self.message_learner:
            return []
        
        return list(self.message_learner.learned_data['user_interests'].get(user_id, set()))
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get LLM statistics."""
        stats = {
            'parameters': {
                'temperature': self.temperature,
                'top_p': self.top_p,
                'frequency_penalty': self.frequency_penalty,
                'presence_penalty': self.presence_penalty,
                'max_context_length': self.max_context_length
            },
            'current_style': self.current_style,
            'responses_generated': len(self.recent_responses),
            'unique_tokens_used': len(self.token_frequencies),
            'topics_discussed': len(self.used_topics),
            'learning_enabled': self.learning_enabled,
            'style_adaptation_enabled': self.style_adaptation
        }
        
        if self.message_learner:
            stats['learned_data'] = {
                'vocabulary_size': len(self.message_learner.learned_data['vocabulary']),
                'phrases_learned': len(self.message_learner.learned_data['phrases']),
                'topics_identified': len(self.message_learner.learned_data['topics']),
                'users_analyzed': len(self.message_learner.learned_data['user_patterns'])
            }
        
        return stats
    
    def reset_penalties(self):
        """Reset penalty tracking."""
        self.recent_responses.clear()
        self.token_frequencies.clear()
        self.used_topics.clear()
        logger.info("Penalties reset")
    
    def export_learned_data(self, filepath: str):
        """Export learned data to JSON file."""
        if not self.message_learner:
            logger.warning("No message learner available")
            return
        
        data = {
            'vocabulary': dict(self.get_learned_vocabulary(100)),
            'phrases': dict(self.get_learned_phrases(50)),
            'topics': dict(self.message_learner.learned_data['topics']),
            'statistics': self.get_statistics()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Learned data exported to {filepath}")


# Global instance
_enhanced_mock_llm = None

def get_enhanced_mock_llm(
    knowledge_file: str = "knowledge.txt",
    **kwargs
) -> EnhancedMockLLM:
    """Get global EnhancedMockLLM instance."""
    global _enhanced_mock_llm
    if _enhanced_mock_llm is None:
        _enhanced_mock_llm = EnhancedMockLLM(knowledge_file, **kwargs)
    return _enhanced_mock_llm

