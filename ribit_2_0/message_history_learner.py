"""
Message History Learner for Ribit 2.0

Scrolls back through Matrix room history to learn from older messages.
Analyzes user communication patterns, topics, and preferences.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Set, Any
from datetime import datetime, timedelta
from collections import defaultdict
try:
    from nio import AsyncClient, RoomMessagesResponse
    MATRIX_NIO_AVAILABLE = True
except ImportError:
    MATRIX_NIO_AVAILABLE = False
    # Create mock classes for type hints
    class AsyncClient: pass
    class RoomMessagesResponse: pass
import json
import re

logger = logging.getLogger(__name__)


class MessageHistoryLearner:
    """
    Learns from message history to improve conversation quality.
    
    Features:
    - Scrolls back through room history
    - Analyzes user communication patterns
    - Extracts topics and interests
    - Learns vocabulary and phrases
    - Improves consistency and fluency
    """
    
    def __init__(self, knowledge_base=None):
        self.knowledge_base = knowledge_base
        self.learned_data = {
            'user_patterns': defaultdict(dict),
            'topics': defaultdict(int),
            'vocabulary': defaultdict(int),
            'phrases': defaultdict(int),
            'user_interests': defaultdict(set),
            'conversation_context': defaultdict(list),
            'user_preferences': defaultdict(dict)
        }
        self.processed_events = set()
        logger.info("Message History Learner initialized")
    
    async def scroll_and_learn(
        self,
        client: AsyncClient,
        room_id: str,
        limit: int = 1000,
        days_back: int = 30
    ) -> Dict[str, Any]:
        """
        Scroll back through room history and learn from messages.
        
        Args:
            client: Matrix AsyncClient
            room_id: Room to learn from
            limit: Maximum messages to process
            days_back: How many days to go back
            
        Returns:
            Dictionary with learning statistics
        """
        logger.info(f"Starting history learning for room {room_id}")
        
        messages_processed = 0
        users_analyzed = set()
        start_time = datetime.now()
        cutoff_time = start_time - timedelta(days=days_back)
        
        # Get initial batch of messages
        response = await client.room_messages(
            room_id=room_id,
            start="",
            limit=100
        )
        
        if not isinstance(response, RoomMessagesResponse):
            logger.error(f"Failed to get room messages: {response}")
            return {'error': str(response)}
        
        next_token = response.end
        
        # Process messages in batches
        while next_token and messages_processed < limit:
            # Process current batch
            for event in response.chunk:
                # Check if we've gone back far enough
                event_time = datetime.fromtimestamp(event.server_timestamp / 1000)
                if event_time < cutoff_time:
                    logger.info(f"Reached cutoff time: {cutoff_time}")
                    next_token = None
                    break
                
                # Skip already processed events
                if event.event_id in self.processed_events:
                    continue
                
                # Process text messages
                if hasattr(event, 'body') and hasattr(event, 'sender'):
                    await self._learn_from_message(
                        sender=event.sender,
                        message=event.body,
                        timestamp=event_time,
                        room_id=room_id
                    )
                    
                    users_analyzed.add(event.sender)
                    messages_processed += 1
                    self.processed_events.add(event.event_id)
            
            # Get next batch
            if next_token and messages_processed < limit:
                response = await client.room_messages(
                    room_id=room_id,
                    start=next_token,
                    limit=100
                )
                
                if isinstance(response, RoomMessagesResponse):
                    next_token = response.end
                else:
                    break
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.5)
        
        # Generate learning summary
        summary = self._generate_learning_summary(
            messages_processed=messages_processed,
            users_analyzed=len(users_analyzed),
            time_taken=(datetime.now() - start_time).total_seconds()
        )
        
        # Save learned data to knowledge base
        if self.knowledge_base:
            self._save_to_knowledge_base()
        
        logger.info(f"Learning complete: {messages_processed} messages from {len(users_analyzed)} users")
        
        return summary
    
    async def _learn_from_message(
        self,
        sender: str,
        message: str,
        timestamp: datetime,
        room_id: str
    ):
        """Learn from a single message."""
        
        # Extract user patterns
        self._analyze_user_pattern(sender, message, timestamp)
        
        # Extract topics
        self._extract_topics(message)
        
        # Learn vocabulary
        self._learn_vocabulary(message)
        
        # Extract phrases
        self._extract_phrases(message)
        
        # Identify interests
        self._identify_interests(sender, message)
        
        # Store context
        self._store_context(sender, message, timestamp, room_id)
    
    def _analyze_user_pattern(self, sender: str, message: str, timestamp: datetime):
        """Analyze user communication patterns."""
        
        if sender not in self.learned_data['user_patterns']:
            self.learned_data['user_patterns'][sender] = {
                'message_count': 0,
                'avg_length': 0,
                'total_length': 0,
                'first_seen': timestamp,
                'last_seen': timestamp,
                'active_hours': defaultdict(int),
                'common_words': defaultdict(int),
                'question_count': 0,
                'exclamation_count': 0,
                'emoji_count': 0
            }
        
        pattern = self.learned_data['user_patterns'][sender]
        pattern['message_count'] += 1
        pattern['total_length'] += len(message)
        pattern['avg_length'] = pattern['total_length'] / pattern['message_count']
        pattern['last_seen'] = timestamp
        pattern['active_hours'][timestamp.hour] += 1
        
        # Count questions and exclamations
        if '?' in message:
            pattern['question_count'] += 1
        if '!' in message:
            pattern['exclamation_count'] += 1
        
        # Count emojis (simple detection)
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            "]+", flags=re.UNICODE)
        pattern['emoji_count'] += len(emoji_pattern.findall(message))
        
        # Track common words
        words = message.lower().split()
        for word in words:
            if len(word) > 3:  # Skip short words
                pattern['common_words'][word] += 1
    
    def _extract_topics(self, message: str):
        """Extract topics from message."""
        
        # Topic keywords
        topic_keywords = {
            'quantum': ['quantum', 'physics', 'particle', 'wave', 'entanglement'],
            'ai': ['ai', 'artificial intelligence', 'machine learning', 'neural', 'llm'],
            'programming': ['code', 'programming', 'python', 'javascript', 'function'],
            'philosophy': ['philosophy', 'consciousness', 'existence', 'meaning', 'truth'],
            'privacy': ['privacy', 'encryption', 'security', 'anonymous', 'crypto'],
            'robotics': ['robot', 'automation', 'control', 'sensor', 'actuator'],
            'matrix': ['matrix', 'element', 'synapse', 'federation', 'e2ee'],
            'linux': ['linux', 'ubuntu', 'debian', 'bash', 'terminal'],
            'opensource': ['open source', 'foss', 'github', 'license', 'contribution']
        }
        
        message_lower = message.lower()
        for topic, keywords in topic_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    self.learned_data['topics'][topic] += 1
    
    def _learn_vocabulary(self, message: str):
        """Learn vocabulary from message."""
        
        # Extract words (alphanumeric, 3+ chars)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', message.lower())
        
        for word in words:
            # Skip common stop words
            stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 
                         'can', 'her', 'was', 'one', 'our', 'out', 'day', 'get'}
            if word not in stop_words:
                self.learned_data['vocabulary'][word] += 1
    
    def _extract_phrases(self, message: str):
        """Extract common phrases."""
        
        # Extract 2-3 word phrases
        words = message.lower().split()
        
        # Bigrams (2 words)
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            if len(phrase) > 6:  # Skip very short phrases
                self.learned_data['phrases'][phrase] += 1
        
        # Trigrams (3 words)
        for i in range(len(words) - 2):
            phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
            if len(phrase) > 10:
                self.learned_data['phrases'][phrase] += 1
    
    def _identify_interests(self, sender: str, message: str):
        """Identify user interests from message content."""
        
        interest_patterns = {
            'quantum_physics': r'\b(quantum|physics|particle|wave|entanglement)\b',
            'programming': r'\b(code|programming|python|javascript|rust|golang)\b',
            'ai_ml': r'\b(ai|ml|machine learning|neural|llm|gpt)\b',
            'privacy': r'\b(privacy|encryption|security|vpn|tor)\b',
            'linux': r'\b(linux|ubuntu|debian|arch|terminal)\b',
            'philosophy': r'\b(philosophy|consciousness|existence|epistemology)\b',
            'crypto': r'\b(cryptocurrency|bitcoin|ethereum|monero|blockchain)\b',
            'robotics': r'\b(robot|automation|ros|control|sensor)\b'
        }
        
        message_lower = message.lower()
        for interest, pattern in interest_patterns.items():
            if re.search(pattern, message_lower):
                self.learned_data['user_interests'][sender].add(interest)
    
    def _store_context(self, sender: str, message: str, timestamp: datetime, room_id: str):
        """Store conversation context."""
        
        context_entry = {
            'sender': sender,
            'message': message[:200],  # Store first 200 chars
            'timestamp': timestamp.isoformat(),
            'length': len(message)
        }
        
        # Keep last 100 messages per room
        if len(self.learned_data['conversation_context'][room_id]) >= 100:
            self.learned_data['conversation_context'][room_id].pop(0)
        
        self.learned_data['conversation_context'][room_id].append(context_entry)
    
    def _generate_learning_summary(
        self,
        messages_processed: int,
        users_analyzed: int,
        time_taken: float
    ) -> Dict[str, Any]:
        """Generate summary of learning session."""
        
        # Get top topics
        top_topics = sorted(
            self.learned_data['topics'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Get top vocabulary
        top_vocab = sorted(
            self.learned_data['vocabulary'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]
        
        # Get top phrases
        top_phrases = sorted(
            self.learned_data['phrases'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:15]
        
        summary = {
            'messages_processed': messages_processed,
            'users_analyzed': users_analyzed,
            'time_taken_seconds': round(time_taken, 2),
            'unique_topics': len(self.learned_data['topics']),
            'vocabulary_size': len(self.learned_data['vocabulary']),
            'phrases_learned': len(self.learned_data['phrases']),
            'top_topics': dict(top_topics),
            'top_vocabulary': dict(top_vocab),
            'top_phrases': dict(top_phrases),
            'user_interests_mapped': {
                user: list(interests)
                for user, interests in self.learned_data['user_interests'].items()
            }
        }
        
        return summary
    
    def _save_to_knowledge_base(self):
        """Save learned data to knowledge base."""
        
        if not self.knowledge_base:
            return
        
        # Save top topics
        top_topics = sorted(
            self.learned_data['topics'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]
        self.knowledge_base.store_knowledge(
            'learned_topics',
            json.dumps(dict(top_topics))
        )
        
        # Save vocabulary
        top_vocab = sorted(
            self.learned_data['vocabulary'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:100]
        self.knowledge_base.store_knowledge(
            'learned_vocabulary',
            json.dumps(dict(top_vocab))
        )
        
        # Save phrases
        top_phrases = sorted(
            self.learned_data['phrases'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:50]
        self.knowledge_base.store_knowledge(
            'learned_phrases',
            json.dumps(dict(top_phrases))
        )
        
        # Save user interests
        interests_data = {
            user: list(interests)
            for user, interests in self.learned_data['user_interests'].items()
        }
        self.knowledge_base.store_knowledge(
            'user_interests',
            json.dumps(interests_data)
        )
        
        logger.info("Learned data saved to knowledge base")
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get learned profile for a user."""
        
        profile = {
            'patterns': self.learned_data['user_patterns'].get(user_id, {}),
            'interests': list(self.learned_data['user_interests'].get(user_id, set())),
            'preferences': self.learned_data['user_preferences'].get(user_id, {})
        }
        
        return profile
    
    def get_conversation_context(self, room_id: str, limit: int = 10) -> List[Dict]:
        """Get recent conversation context for a room."""
        
        context = self.learned_data['conversation_context'].get(room_id, [])
        return context[-limit:]
    
    def suggest_response_style(self, user_id: str) -> Dict[str, Any]:
        """Suggest response style based on user patterns."""
        
        pattern = self.learned_data['user_patterns'].get(user_id)
        if not pattern:
            return {'style': 'default'}
        
        suggestions = {
            'style': 'default',
            'use_questions': pattern.get('question_count', 0) > 5,
            'use_exclamations': pattern.get('exclamation_count', 0) > 3,
            'use_emojis': pattern.get('emoji_count', 0) > 10,
            'preferred_length': 'short' if pattern.get('avg_length', 100) < 50 else 'medium',
            'formality': 'casual' if pattern.get('emoji_count', 0) > 5 else 'neutral'
        }
        
        return suggestions


# Global instance
_message_history_learner = None

def get_message_history_learner(knowledge_base=None) -> MessageHistoryLearner:
    """Get global MessageHistoryLearner instance."""
    global _message_history_learner
    if _message_history_learner is None:
        _message_history_learner = MessageHistoryLearner(knowledge_base)
    return _message_history_learner

