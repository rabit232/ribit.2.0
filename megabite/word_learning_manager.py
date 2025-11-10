"""
Megabite - Word Learning Manager

Learns words from conversations and builds vocabulary database with Supabase persistence.
Expands bot intelligence based on vocabulary size.

Author: Manus AI
"""

import re
import hashlib
import logging
from typing import List, Dict, Any, Optional, Set, Tuple
from datetime import datetime
from collections import Counter
import asyncio

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

logger = logging.getLogger(__name__)


class WordLearningManager:
    """
    Manages word learning with Supabase persistence.

    Features:
    - Learn words from messages with context
    - Track word frequency and relationships
    - Build word pairs and triplets
    - Calculate importance scores
    - Expand mock LLM weights based on vocabulary
    - Integrate with vector database
    """

    def __init__(self, supabase_url: str, supabase_key: str):
        """Initialize word learning manager."""
        if not SUPABASE_AVAILABLE:
            raise ImportError("supabase package required for word learning")

        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.client: Optional[Client] = None
        self._initialized = False

        # Stop words to ignore
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'can', 'could', 'should', 'may', 'might', 'must', 'i', 'you', 'he',
            'she', 'it', 'we', 'they', 'them', 'their', 'this', 'that', 'these',
            'those'
        }

        logger.info("Word Learning Manager initialized")

    async def initialize(self) -> bool:
        """Initialize Supabase connection."""
        try:
            self.client = create_client(self.supabase_url, self.supabase_key)

            # Verify connection
            result = self.client.table("learned_words").select("id").limit(1).execute()

            self._initialized = True
            logger.info("Word Learning Manager connected to Supabase")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Word Learning Manager: {e}")
            return False

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        # Remove special characters but keep apostrophes
        text = re.sub(r"[^\w\s']", ' ', text.lower())

        # Split into words
        words = text.split()

        # Filter out stop words and very short words
        words = [w for w in words if len(w) > 2 and w not in self.stop_words]

        return words

    def _calculate_importance(self, word: str, context: List[str]) -> float:
        """Calculate importance score for a word."""
        score = 1.0

        # Longer words tend to be more specific/important
        if len(word) > 8:
            score += 0.3
        elif len(word) > 5:
            score += 0.1

        # Technical or domain-specific words
        if any(char.isupper() for char in word):
            score += 0.2

        # Words with numbers (technical terms, dates, etc.)
        if any(char.isdigit() for char in word):
            score += 0.1

        return min(score, 2.0)

    async def learn_from_message(
        self,
        message: str,
        user_id: Optional[str] = None,
        room_id: Optional[str] = None,
        from_perspective: bool = False
    ) -> Dict[str, Any]:
        """
        Learn words from a message.

        Args:
            message: The message text
            user_id: User who sent the message
            room_id: Room where message was sent
            from_perspective: Whether this is from perspective analysis

        Returns:
            Dict with learning statistics
        """
        if not self._initialized:
            raise RuntimeError("Word Learning Manager not initialized")

        words = self._tokenize(message)
        if not words:
            return {'words_learned': 0, 'new_words': 0}

        stats = {
            'words_learned': len(words),
            'new_words': 0,
            'words_updated': 0,
            'pairs_created': 0,
            'triplets_created': 0
        }

        # Learn individual words
        for i, word in enumerate(words):
            context_words = []
            if i > 0:
                context_words.append(words[i-1])
            if i < len(words) - 1:
                context_words.append(words[i+1])

            try:
                # Learn word using Supabase function
                result = self.client.rpc(
                    'learn_word',
                    {
                        'p_word': word,
                        'p_context': {'surrounding': context_words},
                        'p_example': message[:200],  # First 200 chars
                        'p_user_id': user_id,
                        'p_room_id': room_id
                    }
                ).execute()

                if result.data:
                    stats['words_updated'] += 1

            except Exception as e:
                logger.warning(f"Failed to learn word '{word}': {e}")

        # Learn word pairs
        for i in range(len(words) - 1):
            try:
                await self._learn_word_relationship(
                    'pair',
                    [words[i], words[i+1]],
                    message[:200]
                )
                stats['pairs_created'] += 1
            except Exception as e:
                logger.debug(f"Failed to learn word pair: {e}")

        # Learn word triplets
        for i in range(len(words) - 2):
            try:
                await self._learn_word_relationship(
                    'triplet',
                    [words[i], words[i+1], words[i+2]],
                    message[:200]
                )
                stats['triplets_created'] += 1
            except Exception as e:
                logger.debug(f"Failed to learn word triplet: {e}")

        return stats

    async def _learn_word_relationship(
        self,
        rel_type: str,
        words: List[str],
        context: str
    ):
        """Learn a word relationship (pair, triplet, etc.)."""
        words_normalized = [w.lower() for w in words]

        data = {
            'relationship_type': rel_type,
            'words': words,
            'words_normalized': words_normalized,
            'occurrence_count': 1,
            'last_used': datetime.now().isoformat(),
            'example_contexts': [context]
        }

        # Upsert relationship
        self.client.table("word_relationships").upsert(
            data,
            on_conflict='relationship_type,words_normalized'
        ).execute()

    async def learn_from_history(
        self,
        messages: List[Dict[str, Any]],
        months_back: int = 3
    ) -> Dict[str, Any]:
        """
        Learn from historical messages.

        Args:
            messages: List of message dicts with 'text', 'user_id', 'room_id'
            months_back: How many months of history to learn from

        Returns:
            Learning statistics
        """
        total_stats = {
            'messages_processed': 0,
            'total_words_learned': 0,
            'new_words': 0,
            'pairs_created': 0,
            'triplets_created': 0
        }

        for msg in messages:
            try:
                stats = await self.learn_from_message(
                    msg['text'],
                    msg.get('user_id'),
                    msg.get('room_id')
                )

                total_stats['messages_processed'] += 1
                total_stats['total_words_learned'] += stats['words_learned']
                total_stats['new_words'] += stats.get('new_words', 0)
                total_stats['pairs_created'] += stats.get('pairs_created', 0)
                total_stats['triplets_created'] += stats.get('triplets_created', 0)

            except Exception as e:
                logger.warning(f"Failed to learn from message: {e}")

        return total_stats

    async def get_vocabulary_stats(self) -> Dict[str, Any]:
        """Get vocabulary statistics."""
        try:
            result = self.client.rpc('get_word_stats').execute()
            return result.data if result.data else {}
        except Exception as e:
            logger.error(f"Failed to get vocabulary stats: {e}")
            return {}

    async def get_word_info(self, word: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a learned word."""
        try:
            result = self.client.table("learned_words").select("*").eq(
                "word_normalized", word.lower()
            ).execute()

            return result.data[0] if result.data else None

        except Exception as e:
            logger.error(f"Failed to get word info: {e}")
            return None

    async def search_words(
        self,
        query: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Search learned words by text."""
        try:
            result = self.client.table("learned_words").select("*").text_search(
                'word', query
            ).limit(limit).execute()

            return result.data

        except Exception as e:
            logger.error(f"Failed to search words: {e}")
            return []

    async def get_most_common_words(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get most commonly used words."""
        try:
            result = self.client.table("learned_words").select(
                "word,count,importance_score,example_sentences"
            ).order("count", desc=True).limit(limit).execute()

            return result.data

        except Exception as e:
            logger.error(f"Failed to get most common words: {e}")
            return []

    async def get_recent_words(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recently learned words."""
        try:
            result = self.client.table("learned_words").select(
                "word,count,created_at,example_sentences"
            ).order("created_at", desc=True).limit(limit).execute()

            return result.data

        except Exception as e:
            logger.error(f"Failed to get recent words: {e}")
            return []

    async def get_intelligence_quotient(self) -> Dict[str, Any]:
        """
        Calculate bot's intelligence quotient based on vocabulary.

        Returns:
            Dict with IQ metrics and weight expansion factor
        """
        try:
            stats = await self.get_vocabulary_stats()

            total_words = stats.get('total_words', 0)
            total_occurrences = stats.get('total_occurrences', 0)

            # Base intelligence metrics
            iq_metrics = {
                'vocabulary_size': total_words,
                'word_usage_total': total_occurrences,
                'average_word_frequency': stats.get('average_occurrences', 0),
                'base_weight': 1.0,
                'vocabulary_weight': 0.0,
                'pattern_weight': 0.0,
                'personality_weight': 0.0,
                'total_weight': 1.0
            }

            # Calculate weight expansions
            # +0.1 per 1000 words learned
            iq_metrics['vocabulary_weight'] = (total_words / 1000) * 0.1

            # Get pattern complexity
            patterns_result = self.client.table("word_relationships").select(
                "id"
            ).execute()
            pattern_count = len(patterns_result.data) if patterns_result.data else 0
            iq_metrics['pattern_weight'] = (pattern_count / 5000) * 0.2

            # Get personality strength
            personality_result = self.client.rpc('get_personality_summary').execute()
            if personality_result.data:
                active_traits = personality_result.data.get('active_traits', 0)
                iq_metrics['personality_weight'] = (active_traits / 20) * 0.3

            # Calculate total weight
            iq_metrics['total_weight'] = (
                iq_metrics['base_weight'] +
                iq_metrics['vocabulary_weight'] +
                iq_metrics['pattern_weight'] +
                iq_metrics['personality_weight']
            )

            # Add intelligence level description
            weight = iq_metrics['total_weight']
            if weight < 1.2:
                iq_metrics['intelligence_level'] = 'developing'
            elif weight < 1.5:
                iq_metrics['intelligence_level'] = 'intermediate'
            elif weight < 2.0:
                iq_metrics['intelligence_level'] = 'advanced'
            else:
                iq_metrics['intelligence_level'] = 'expert'

            return iq_metrics

        except Exception as e:
            logger.error(f"Failed to calculate intelligence quotient: {e}")
            return {'total_weight': 1.0, 'intelligence_level': 'unknown'}

    async def export_vocabulary(self, format: str = 'json') -> str:
        """Export learned vocabulary."""
        try:
            words = await self.get_most_common_words(limit=1000)

            if format == 'json':
                import json
                return json.dumps(words, indent=2)
            elif format == 'csv':
                import csv
                import io
                output = io.StringIO()
                if words:
                    writer = csv.DictWriter(output, fieldnames=words[0].keys())
                    writer.writeheader()
                    writer.writerows(words)
                return output.getvalue()
            else:
                return str(words)

        except Exception as e:
            logger.error(f"Failed to export vocabulary: {e}")
            return ""

    async def close(self):
        """Close connections."""
        self._initialized = False
        logger.info("Word Learning Manager closed")
