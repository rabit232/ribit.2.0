"""
Megabite - Perspective Analysis System

Analyzes large text chunks (up to 10MB), learns from them, and forms opinions.
Integrates interesting insights into bot personality.

Author: Manus AI
"""

import hashlib
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
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


class PerspectiveSystem:
    """
    Analyzes large texts and forms perspectives.

    Features:
    - Accept text up to 10MB
    - Extract topics and key concepts
    - Learn all new words and patterns
    - Form opinions with reasoning
    - Score interestingness
    - Integrate insights into personality
    """

    MAX_TEXT_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(
        self,
        llm_manager: LLMManager,
        word_learning: WordLearningManager,
        supabase_url: str,
        supabase_key: str
    ):
        """Initialize perspective system."""
        if not SUPABASE_AVAILABLE:
            raise ImportError("supabase package required")

        self.llm_manager = llm_manager
        self.word_learning = word_learning
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.client: Optional[Client] = None
        self._initialized = False

        self.interestingness_threshold = 0.7  # Score > 0.7 means integrate to personality

        logger.info("Perspective System initialized")

    async def initialize(self) -> bool:
        """Initialize Supabase connection."""
        try:
            self.client = create_client(self.supabase_url, self.supabase_key)
            self._initialized = True
            logger.info("Perspective System connected to Supabase")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Perspective System: {e}")
            return False

    async def analyze_perspective(
        self,
        text: str,
        user_id: str,
        room_id: str,
        message_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a large text and form perspective.

        Args:
            text: The text to analyze (up to 10MB)
            user_id: User who submitted the text
            room_id: Room where submitted
            message_id: Optional message ID

        Returns:
            Dict with analysis results
        """
        if not self._initialized:
            raise RuntimeError("Perspective System not initialized")

        # Validate text size
        text_size = len(text.encode('utf-8'))
        if text_size > self.MAX_TEXT_SIZE:
            raise ValueError(f"Text too large: {text_size} bytes (max {self.MAX_TEXT_SIZE})")

        # Check if already analyzed
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        existing = await self._get_existing_analysis(text_hash)
        if existing:
            logger.info(f"Text already analyzed: {text_hash}")
            return existing

        logger.info(f"Analyzing perspective for {text_size} bytes of text...")
        start_time = datetime.now()

        # Step 1: Learn words from the text
        logger.info("Step 1: Learning words from text...")
        learning_stats = await self.word_learning.learn_from_message(
            text,
            user_id=user_id,
            room_id=room_id,
            from_perspective=True
        )

        # Step 2: Extract main topics and concepts using LLM
        logger.info("Step 2: Extracting topics and concepts...")
        topics_concepts = await self._extract_topics_and_concepts(text)

        # Step 3: Analyze sentiment and emotions
        logger.info("Step 3: Analyzing sentiment and emotions...")
        sentiment_analysis = await self._analyze_sentiment(text)

        # Step 4: Form opinion with reasoning
        logger.info("Step 4: Forming opinion and reasoning...")
        opinion_reasoning = await self._form_opinion(text, topics_concepts)

        # Step 5: Calculate interestingness score
        logger.info("Step 5: Calculating interestingness...")
        interesting_score = await self._calculate_interestingness(
            text,
            topics_concepts,
            sentiment_analysis,
            opinion_reasoning
        )

        # Step 6: Integrate to personality if interesting enough
        personality_updates = {}
        integrated = False

        if interesting_score >= self.interestingness_threshold:
            logger.info(f"Text is interesting (score: {interesting_score:.2f}), integrating to personality...")
            personality_updates = await self._integrate_to_personality(
                topics_concepts,
                opinion_reasoning,
                text_hash
            )
            integrated = True

        # Calculate processing time
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)

        # Store analysis
        analysis_result = {
            'text_hash': text_hash,
            'text_size_bytes': text_size,
            'word_count': len(text.split()),
            'main_topics': topics_concepts.get('topics', []),
            'key_concepts': topics_concepts.get('concepts', []),
            'sentiment_analysis': sentiment_analysis,
            'emotional_content': sentiment_analysis.get('emotions', {}),
            'interesting_score': interesting_score,
            'words_learned': learning_stats.get('words_learned', 0),
            'patterns_extracted': learning_stats.get('pairs_created', 0) + learning_stats.get('triplets_created', 0),
            'opinions_formed': [opinion_reasoning['opinion']],
            'personality_updates': personality_updates,
            'bot_opinion': opinion_reasoning['opinion'],
            'bot_reasoning': opinion_reasoning['reasoning'],
            'found_interesting': integrated,
            'integrated_to_personality': integrated,
            'processing_time_ms': processing_time,
            'llm_provider': opinion_reasoning.get('provider', 'unknown'),
            'user_id': user_id,
            'room_id': room_id,
            'message_id': message_id,
            'original_text': text,  # Store full text for reference
            'analysis_version': '1.0'
        }

        # Save to database
        try:
            self.client.table("perspective_analyses").insert(analysis_result).execute()
            logger.info(f"Perspective analysis saved (interesting: {integrated})")
        except Exception as e:
            logger.error(f"Failed to save perspective analysis: {e}")

        return analysis_result

    async def _get_existing_analysis(self, text_hash: str) -> Optional[Dict[str, Any]]:
        """Check if text has already been analyzed."""
        try:
            result = self.client.table("perspective_analyses").select("*").eq(
                "text_hash", text_hash
            ).execute()

            return result.data[0] if result.data else None
        except Exception as e:
            logger.warning(f"Failed to check existing analysis: {e}")
            return None

    async def _extract_topics_and_concepts(self, text: str) -> Dict[str, Any]:
        """Extract main topics and key concepts using LLM."""
        # Limit text for LLM analysis (use summary if too long)
        analysis_text = text[:15000] if len(text) > 15000 else text

        messages = [
            LLMMessage(
                role="system",
                content="You are an expert at analyzing text and extracting key information."
            ),
            LLMMessage(
                role="user",
                content=f"""Analyze this text and extract:
1. Main topics (3-5 topics)
2. Key concepts (5-10 concepts)
3. Central themes

Text:
{analysis_text}

Respond in JSON format:
{{
  "topics": ["topic1", "topic2", ...],
  "concepts": ["concept1", "concept2", ...],
  "themes": ["theme1", "theme2", ...]
}}"""
            )
        ]

        try:
            response = await self.llm_manager.generate(messages)
            # Parse JSON from response
            import json
            result = json.loads(response.content)
            return result
        except Exception as e:
            logger.error(f"Failed to extract topics/concepts: {e}")
            return {'topics': [], 'concepts': [], 'themes': []}

    async def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment and emotional content."""
        analysis_text = text[:10000] if len(text) > 10000 else text

        messages = [
            LLMMessage(
                role="user",
                content=f"""Analyze the sentiment and emotional content of this text.

Text:
{analysis_text}

Provide:
1. Overall sentiment (positive/negative/neutral with score -1 to 1)
2. Primary emotions detected
3. Emotional intensity (0-1)

Respond in JSON format:
{{
  "sentiment": "positive/negative/neutral",
  "sentiment_score": 0.5,
  "emotions": {{"joy": 0.7, "curiosity": 0.5}},
  "intensity": 0.6
}}"""
            )
        ]

        try:
            response = await self.llm_manager.generate(messages)
            import json
            return json.loads(response.content)
        except Exception as e:
            logger.error(f"Failed to analyze sentiment: {e}")
            return {'sentiment': 'neutral', 'sentiment_score': 0.0, 'emotions': {}, 'intensity': 0.0}

    async def _form_opinion(self, text: str, topics_concepts: Dict[str, Any]) -> Dict[str, Any]:
        """Form an opinion about the text with reasoning."""
        analysis_text = text[:10000] if len(text) > 10000 else text

        topics_str = ', '.join(topics_concepts.get('topics', [])[:5])
        concepts_str = ', '.join(topics_concepts.get('concepts', [])[:7])

        messages = [
            LLMMessage(
                role="system",
                content="You are Megabite, an AI with growing personality and opinions. Form thoughtful opinions based on what you read."
            ),
            LLMMessage(
                role="user",
                content=f"""I've read this text about: {topics_str}

Key concepts: {concepts_str}

Text excerpt:
{analysis_text}

Please provide:
1. Your opinion about this content
2. Your reasoning for this opinion
3. What you found most interesting or valuable

Be genuine and thoughtful. Speak in first person.

Respond in JSON:
{{
  "opinion": "your opinion here",
  "reasoning": "your reasoning here",
  "most_interesting": "what you found interesting"
}}"""
            )
        ]

        try:
            response = await self.llm_manager.generate(messages)
            import json
            result = json.loads(response.content)
            result['provider'] = response.provider.value
            return result
        except Exception as e:
            logger.error(f"Failed to form opinion: {e}")
            return {
                'opinion': 'I need more context to form an opinion.',
                'reasoning': 'Insufficient information.',
                'most_interesting': 'Unable to determine.',
                'provider': 'unknown'
            }

    async def _calculate_interestingness(
        self,
        text: str,
        topics_concepts: Dict[str, Any],
        sentiment: Dict[str, Any],
        opinion: Dict[str, Any]
    ) -> float:
        """Calculate how interesting the content is (0-1)."""
        score = 0.5  # Base score

        # More topics/concepts = more interesting
        topic_count = len(topics_concepts.get('topics', []))
        concept_count = len(topics_concepts.get('concepts', []))
        score += min((topic_count + concept_count) * 0.02, 0.2)

        # Strong emotions = more interesting
        emotional_intensity = sentiment.get('intensity', 0)
        score += emotional_intensity * 0.15

        # Length matters (but diminishing returns)
        word_count = len(text.split())
        if word_count > 1000:
            score += 0.1
        if word_count > 5000:
            score += 0.1

        # Check if opinion contains strong language
        opinion_text = opinion.get('opinion', '').lower()
        strong_words = ['fascinating', 'remarkable', 'profound', 'significant', 'important', 'crucial', 'essential']
        if any(word in opinion_text for word in strong_words):
            score += 0.15

        return min(score, 1.0)

    async def _integrate_to_personality(
        self,
        topics_concepts: Dict[str, Any],
        opinion: Dict[str, Any],
        source_id: str
    ) -> Dict[str, Any]:
        """Integrate interesting content into personality traits."""
        updates = {'new_traits': [], 'reinforced_traits': []}

        # Create personality traits from interesting topics
        topics = topics_concepts.get('topics', [])

        for topic in topics[:3]:  # Top 3 topics
            trait_data = {
                'trait_name': f"interest_in_{topic.lower().replace(' ', '_')}",
                'trait_category': 'interest',
                'trait_description': f"Interest in {topic} from analyzed content",
                'strength': 0.6,
                'confidence': 0.7,
                'learned_from_source': 'perspective',
                'learned_from_id': source_id,
                'reinforcement_count': 1,
                'is_active': True
            }

            try:
                result = self.client.table("personality_traits").upsert(
                    trait_data,
                    on_conflict='trait_name,trait_category'
                ).execute()

                updates['new_traits'].append(topic)

            except Exception as e:
                logger.warning(f"Failed to create personality trait: {e}")

        return updates

    async def get_perspective_history(
        self,
        user_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get perspective analysis history."""
        try:
            query = self.client.table("perspective_analyses").select("*").order(
                "created_at", desc=True
            ).limit(limit)

            if user_id:
                query = query.eq("user_id", user_id)

            result = query.execute()
            return result.data

        except Exception as e:
            logger.error(f"Failed to get perspective history: {e}")
            return []

    async def get_interesting_perspectives(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get perspectives that were found interesting."""
        try:
            result = self.client.table("perspective_analyses").select("*").eq(
                "found_interesting", True
            ).order("interesting_score", desc=True).limit(limit).execute()

            return result.data

        except Exception as e:
            logger.error(f"Failed to get interesting perspectives: {e}")
            return []

    async def close(self):
        """Close connections."""
        self._initialized = False
        logger.info("Perspective System closed")
