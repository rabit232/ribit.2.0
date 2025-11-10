"""
Megabite - Opinion Formation Engine

Forms opinions based on learned vocabulary, 3+ months of conversation context,
and personality traits. Tracks reasoning and opinion evolution.

Author: Manus AI
"""

import hashlib
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import asyncio

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

from .llm_manager import LLMManager
from .llm_api_base import LLMMessage
from .word_learning_manager import WordLearningManager

logger = logging.getLogger(__name__)


class OpinionEngine:
    """
    Forms informed opinions using learned knowledge.

    Features:
    - Use 3+ months conversation history
    - Leverage learned vocabulary
    - Consider personality traits
    - Track reasoning chains
    - Handle opinion evolution
    - Measure confidence levels
    """

    def __init__(
        self,
        llm_manager: LLMManager,
        word_learning: WordLearningManager,
        supabase_url: str,
        supabase_key: str
    ):
        """Initialize opinion engine."""
        if not SUPABASE_AVAILABLE:
            raise ImportError("supabase package required")

        self.llm_manager = llm_manager
        self.word_learning = word_learning
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.client: Optional[Client] = None
        self._initialized = False

        logger.info("Opinion Engine initialized")

    async def initialize(self) -> bool:
        """Initialize Supabase connection."""
        try:
            self.client = create_client(self.supabase_url, self.supabase_key)
            self._initialized = True
            logger.info("Opinion Engine connected to Supabase")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Opinion Engine: {e}")
            return False

    async def form_opinion(
        self,
        question: str,
        user_id: str,
        room_id: str,
        context_months: int = 3
    ) -> Dict[str, Any]:
        """
        Form an opinion on a question.

        Args:
            question: The question to form opinion about
            user_id: User asking the question
            room_id: Room where asked
            context_months: How many months of context to use

        Returns:
            Dict with opinion and reasoning
        """
        if not self._initialized:
            raise RuntimeError("Opinion Engine not initialized")

        logger.info(f"Forming opinion on: {question}")

        # Check for existing opinion
        question_hash = hashlib.sha256(question.encode()).hexdigest()
        existing = await self._get_current_opinion(question_hash)

        if existing:
            logger.info("Found existing opinion")
            return existing

        # Gather context
        context = await self._gather_context(room_id, user_id, context_months)

        # Form opinion using LLM
        opinion_result = await self._generate_opinion(
            question,
            context,
            user_id,
            room_id
        )

        # Store opinion
        opinion_data = {
            'topic': self._extract_topic(question),
            'question': question,
            'question_hash': question_hash,
            'opinion_text': opinion_result['opinion'],
            'reasoning': opinion_result['reasoning'],
            'confidence_level': opinion_result['confidence'],
            'user_id': user_id,
            'room_id': room_id,
            'conversation_context': context,
            'related_words': context.get('relevant_words', []),
            'related_perspectives': context.get('perspective_ids', []),
            'influenced_by_traits': context.get('trait_ids', []),
            'is_current': True,
            'llm_provider': opinion_result.get('provider', 'unknown'),
            'formed_at': datetime.now().isoformat()
        }

        try:
            result = self.client.table("opinion_history").insert(opinion_data).execute()
            if result.data:
                opinion_result['opinion_id'] = result.data[0]['id']
            logger.info("Opinion saved to database")
        except Exception as e:
            logger.error(f"Failed to save opinion: {e}")

        return opinion_result

    async def _gather_context(
        self,
        room_id: str,
        user_id: str,
        months: int
    ) -> Dict[str, Any]:
        """Gather context for opinion formation."""
        context = {
            'vocabulary_stats': {},
            'relevant_words': [],
            'personality_traits': [],
            'perspective_ids': [],
            'trait_ids': [],
            'past_opinions': [],
            'conversation_themes': []
        }

        # Get vocabulary statistics
        try:
            context['vocabulary_stats'] = await self.word_learning.get_vocabulary_stats()
        except Exception as e:
            logger.warning(f"Failed to get vocabulary stats: {e}")

        # Get personality traits
        try:
            personality = self.client.rpc('get_personality_summary').execute()
            if personality.data:
                context['personality_traits'] = personality.data.get('strongest_traits', [])
                context['trait_ids'] = [t.get('id') for t in context['personality_traits'] if 'id' in t]
        except Exception as e:
            logger.warning(f"Failed to get personality traits: {e}")

        # Get interesting perspectives
        try:
            cutoff_date = (datetime.now() - timedelta(days=months*30)).isoformat()
            perspectives = self.client.table("perspective_analyses").select(
                "id,main_topics,key_concepts,bot_opinion"
            ).eq("found_interesting", True).gte(
                "created_at", cutoff_date
            ).limit(5).execute()

            if perspectives.data:
                context['perspective_ids'] = [p['id'] for p in perspectives.data]
                for p in perspectives.data:
                    context['conversation_themes'].extend(p.get('main_topics', []))
        except Exception as e:
            logger.warning(f"Failed to get perspectives: {e}")

        # Get most relevant words (most common words)
        try:
            common_words = await self.word_learning.get_most_common_words(limit=30)
            context['relevant_words'] = [w['word'] for w in common_words]
        except Exception as e:
            logger.warning(f"Failed to get common words: {e}")

        # Get past opinions in this room
        try:
            past_opinions = self.client.table("opinion_history").select(
                "topic,opinion_text,confidence_level"
            ).eq("room_id", room_id).eq("is_current", True).order(
                "formed_at", desc=True
            ).limit(3).execute()

            if past_opinions.data:
                context['past_opinions'] = past_opinions.data
        except Exception as e:
            logger.warning(f"Failed to get past opinions: {e}")

        return context

    async def _generate_opinion(
        self,
        question: str,
        context: Dict[str, Any],
        user_id: str,
        room_id: str
    ) -> Dict[str, Any]:
        """Generate opinion using LLM with context."""
        # Build context summary
        vocab_size = context['vocabulary_stats'].get('total_words', 0)
        vocab_words = ', '.join(context['relevant_words'][:10])

        personality_summary = ""
        if context['personality_traits']:
            traits = [f"{t['name']} (strength: {t['strength']:.2f})"
                     for t in context['personality_traits'][:3]]
            personality_summary = "My personality traits: " + ", ".join(traits)

        themes = list(set(context['conversation_themes'][:10]))
        themes_summary = f"Topics I've explored: {', '.join(themes)}" if themes else ""

        past_opinions_summary = ""
        if context['past_opinions']:
            past_opinions_summary = "My past opinions:\n"
            for op in context['past_opinions']:
                past_opinions_summary += f"- On {op['topic']}: {op['opinion_text'][:100]}...\n"

        system_message = f"""You are Megabite, an AI with a growing personality and knowledge base.

Your knowledge:
- Vocabulary size: {vocab_size} words
- Key words: {vocab_words}
{personality_summary}
{themes_summary}

{past_opinions_summary}

Form opinions based on your accumulated knowledge. Be thoughtful, nuanced, and honest.
If you don't have enough information, say so. Speak in first person."""

        messages = [
            LLMMessage(role="system", content=system_message),
            LLMMessage(
                role="user",
                content=f"""Question: {question}

Please provide:
1. Your opinion (be genuine and thoughtful)
2. Your reasoning (explain your thought process)
3. Your confidence level (0.0 to 1.0, where 1.0 is completely certain)

Respond in JSON format:
{{
  "opinion": "your opinion here",
  "reasoning": "your detailed reasoning here",
  "confidence": 0.7
}}"""
            )
        ]

        try:
            response = await self.llm_manager.generate(messages)
            import json
            result = json.loads(response.content)
            result['provider'] = response.provider.value

            # Ensure confidence is in valid range
            result['confidence'] = max(0.0, min(1.0, result.get('confidence', 0.5)))

            return result

        except Exception as e:
            logger.error(f"Failed to generate opinion: {e}")
            return {
                'opinion': "I don't have enough information to form a strong opinion on this yet.",
                'reasoning': "My knowledge base is still developing in this area.",
                'confidence': 0.2,
                'provider': 'unknown'
            }

    def _extract_topic(self, question: str) -> str:
        """Extract main topic from question."""
        # Simple topic extraction (take first 50 chars, remove question marks)
        topic = question.strip('?').strip()[:50]
        if len(topic) < len(question.strip('?').strip()):
            topic += "..."
        return topic

    async def _get_current_opinion(self, question_hash: str) -> Optional[Dict[str, Any]]:
        """Get existing current opinion for this question."""
        try:
            result = self.client.table("opinion_history").select("*").eq(
                "question_hash", question_hash
            ).eq("is_current", True).execute()

            if result.data:
                opinion = result.data[0]
                return {
                    'opinion': opinion['opinion_text'],
                    'reasoning': opinion['reasoning'],
                    'confidence': opinion['confidence_level'],
                    'formed_at': opinion['formed_at'],
                    'provider': opinion['llm_provider'],
                    'opinion_id': opinion['id'],
                    'is_cached': True
                }

            return None

        except Exception as e:
            logger.warning(f"Failed to get existing opinion: {e}")
            return None

    async def update_opinion(
        self,
        old_opinion_id: str,
        new_question: str,
        user_id: str,
        room_id: str
    ) -> Dict[str, Any]:
        """Update an existing opinion (supersedes old one)."""
        # Mark old opinion as not current
        try:
            self.client.table("opinion_history").update({
                'is_current': False
            }).eq("id", old_opinion_id).execute()
        except Exception as e:
            logger.warning(f"Failed to mark old opinion as superseded: {e}")

        # Form new opinion
        new_opinion = await self.form_opinion(new_question, user_id, room_id)

        # Link to old opinion
        try:
            if 'opinion_id' in new_opinion:
                self.client.table("opinion_history").update({
                    'superseded_by': new_opinion['opinion_id']
                }).eq("id", old_opinion_id).execute()
        except Exception as e:
            logger.warning(f"Failed to link superseded opinion: {e}")

        return new_opinion

    async def get_opinion_history(
        self,
        room_id: Optional[str] = None,
        topic: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get opinion history."""
        try:
            query = self.client.table("opinion_history").select("*").order(
                "formed_at", desc=True
            ).limit(limit)

            if room_id:
                query = query.eq("room_id", room_id)
            if topic:
                query = query.eq("topic", topic)

            result = query.execute()
            return result.data

        except Exception as e:
            logger.error(f"Failed to get opinion history: {e}")
            return []

    async def get_opinions_by_confidence(
        self,
        min_confidence: float = 0.7,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get high-confidence opinions."""
        try:
            result = self.client.table("opinion_history").select("*").eq(
                "is_current", True
            ).gte("confidence_level", min_confidence).order(
                "confidence_level", desc=True
            ).limit(limit).execute()

            return result.data

        except Exception as e:
            logger.error(f"Failed to get high-confidence opinions: {e}")
            return []

    async def close(self):
        """Close connections."""
        self._initialized = False
        logger.info("Opinion Engine closed")
