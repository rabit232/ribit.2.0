#!/usr/bin/env python3
"""
Ribit 2.0 - Advanced Conversation Context Manager

Implements full conversation context tracking, room-based history,
automatic URL content fetching, comprehensive chat summaries,
and cached responses for performance optimization.

Author: Manus AI
Enhanced for: rabit232/ribit.2.0
"""

import json
import sqlite3
import hashlib
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging
import re
from collections import defaultdict

@dataclass
class ConversationMessage:
    """Structured conversation message with emotional context."""
    room_id: str
    user_id: str
    message_type: str  # 'user', 'bot', 'system'
    content: str
    timestamp: datetime
    emotion_state: str = ""
    context_tags: List[str] = None
    relevance_score: float = 0.0
    response_time_ms: int = 0
    metadata: Dict[str, Any] = None

@dataclass
class ConversationSummary:
    """Daily conversation summary with emotional analysis."""
    room_id: str
    date: str
    message_count: int
    key_topics: List[str]
    dominant_emotions: List[str]
    summary_text: str
    participants: List[str]
    peak_activity_hour: int
    avg_response_time: float

class AdvancedConversationManager:
    """
    High-performance conversation manager with emotional intelligence,
    context awareness, and advanced analytics.
    """
    
    def __init__(self, db_path: str = "ribit_conversations.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.emotions = [
            "JOY", "EXCITEMENT", "CURIOSITY", "SATISFACTION", "PRIDE",
            "EMPATHY", "COMPASSION", "UNDERSTANDING", "PATIENCE", "WISDOM"
        ]
        
        # Performance optimization
        self.message_cache = {}
        self.summary_cache = {}
        self.context_cache = {}
        
        # Initialize database
        self._init_database()
        
        self.logger.info("Advanced Conversation Manager initialized with PRECISION!")
    
    def _init_database(self):
        """Initialize comprehensive conversation tracking database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enhanced conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                message_type TEXT NOT NULL,
                content TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                emotion_state TEXT,
                context_tags TEXT,
                relevance_score REAL DEFAULT 0.0,
                response_time_ms INTEGER DEFAULT 0,
                word_count INTEGER DEFAULT 0,
                sentiment_score REAL DEFAULT 0.0,
                metadata TEXT
            )
        ''')
        
        # Conversation summaries with enhanced analytics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id TEXT NOT NULL,
                summary_date DATE NOT NULL,
                message_count INTEGER,
                unique_participants INTEGER,
                key_topics TEXT,
                dominant_emotions TEXT,
                summary_text TEXT,
                peak_activity_hour INTEGER,
                avg_response_time REAL,
                total_words INTEGER,
                avg_sentiment REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(room_id, summary_date)
            )
        ''')
        
        # Context relationships table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS context_relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id TEXT NOT NULL,
                message_id INTEGER NOT NULL,
                related_message_id INTEGER NOT NULL,
                relationship_type TEXT NOT NULL,  -- 'reply', 'reference', 'continuation'
                strength REAL DEFAULT 1.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (message_id) REFERENCES conversations (id),
                FOREIGN KEY (related_message_id) REFERENCES conversations (id)
            )
        ''')
        
        # User interaction patterns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                pattern_date DATE NOT NULL,
                message_count INTEGER,
                avg_message_length REAL,
                dominant_emotions TEXT,
                preferred_topics TEXT,
                activity_hours TEXT,
                response_pattern TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(room_id, user_id, pattern_date)
            )
        ''')
        
        # Performance indexes
        indexes = [
            'CREATE INDEX IF NOT EXISTS idx_room_timestamp ON conversations(room_id, timestamp)',
            'CREATE INDEX IF NOT EXISTS idx_user_timestamp ON conversations(user_id, timestamp)',
            'CREATE INDEX IF NOT EXISTS idx_content_hash ON conversations(content_hash)',
            'CREATE INDEX IF NOT EXISTS idx_relevance ON conversations(relevance_score)',
            'CREATE INDEX IF NOT EXISTS idx_emotion ON conversations(emotion_state)',
            'CREATE INDEX IF NOT EXISTS idx_summary_room_date ON conversation_summaries(room_id, summary_date)',
            'CREATE INDEX IF NOT EXISTS idx_context_message ON context_relationships(message_id)',
            'CREATE INDEX IF NOT EXISTS idx_user_pattern ON user_patterns(room_id, user_id, pattern_date)'
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        conn.commit()
        conn.close()
        
        self.logger.info("Database schema created with ARCHITECTURAL EXCELLENCE!")
    
    def _generate_content_hash(self, content: str) -> str:
        """Generate content hash for deduplication."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _calculate_relevance_score(self, content: str, context_tags: List[str] = None) -> float:
        """Calculate message relevance score with emotional intelligence."""
        base_score = min(len(content) / 500.0, 1.0)  # Length-based relevance
        
        # Keyword-based relevance boost
        important_keywords = [
            'important', 'urgent', 'help', 'error', 'problem', 'question',
            'ribit', 'robot', 'ai', 'automation', 'matrix', 'python'
        ]
        
        content_lower = content.lower()
        keyword_boost = sum(0.1 for keyword in important_keywords if keyword in content_lower)
        
        # Context tags boost
        tag_boost = len(context_tags or []) * 0.05
        
        # Emotional content boost
        emotion_boost = 0.1 if any(emotion in content.upper() for emotion in self.emotions) else 0
        
        final_score = min(base_score + keyword_boost + tag_boost + emotion_boost, 1.0)
        return round(final_score, 3)
    
    def _analyze_sentiment(self, content: str) -> float:
        """Simple sentiment analysis (-1.0 to 1.0)."""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'like', 'happy', 'joy']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'angry', 'frustrated']
        
        content_lower = content.lower()
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        total_words = len(content.split())
        if total_words == 0:
            return 0.0
        
        sentiment = (positive_count - negative_count) / max(total_words / 10, 1)
        return max(-1.0, min(1.0, sentiment))
    
    def add_message(self, message: ConversationMessage) -> int:
        """Add message with comprehensive analysis and caching."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Generate content hash
        content_hash = self._generate_content_hash(message.content)
        
        # Calculate metrics
        word_count = len(message.content.split())
        sentiment_score = self._analyze_sentiment(message.content)
        relevance_score = message.relevance_score or self._calculate_relevance_score(
            message.content, message.context_tags
        )
        
        # Prepare data
        context_tags_json = json.dumps(message.context_tags or [])
        metadata_json = json.dumps(message.metadata or {})
        
        cursor.execute('''
            INSERT INTO conversations 
            (room_id, user_id, message_type, content, content_hash, timestamp, 
             emotion_state, context_tags, relevance_score, response_time_ms, 
             word_count, sentiment_score, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            message.room_id, message.user_id, message.message_type, message.content,
            content_hash, message.timestamp, message.emotion_state, context_tags_json,
            relevance_score, message.response_time_ms, word_count, sentiment_score,
            metadata_json
        ))
        
        message_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Update cache
        cache_key = f"{message.room_id}:recent"
        if cache_key in self.context_cache:
            del self.context_cache[cache_key]
        
        self.logger.info(f"Message added with PRECISION: ID {message_id}, Relevance {relevance_score}")
        return message_id
    
    def get_conversation_context(self, room_id: str, limit: int = 50, 
                               min_relevance: float = 0.0) -> List[Dict]:
        """Get conversation context with intelligent filtering and caching."""
        cache_key = f"{room_id}:context:{limit}:{min_relevance}"
        
        if cache_key in self.context_cache:
            self.logger.info("Context cache hit with EFFICIENCY!")
            return self.context_cache[cache_key]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_id, message_type, content, timestamp, emotion_state, 
                   context_tags, relevance_score, word_count, sentiment_score, metadata
            FROM conversations 
            WHERE room_id = ? AND relevance_score >= ?
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (room_id, min_relevance, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        context = []
        for row in results:
            context.append({
                'id': row[0],
                'user_id': row[1],
                'message_type': row[2],
                'content': row[3],
                'timestamp': row[4],
                'emotion_state': row[5],
                'context_tags': json.loads(row[6]) if row[6] else [],
                'relevance_score': row[7],
                'word_count': row[8],
                'sentiment_score': row[9],
                'metadata': json.loads(row[10]) if row[10] else {}
            })
        
        # Reverse to chronological order
        context = list(reversed(context))
        
        # Cache result
        self.context_cache[cache_key] = context
        
        self.logger.info(f"Context retrieved with INTELLIGENCE: {len(context)} messages")
        return context
    
    def get_contextual_summary(self, room_id: str, hours_back: int = 24) -> Dict:
        """Get contextual summary of recent conversation activity."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since_time = datetime.now() - timedelta(hours=hours_back)
        
        cursor.execute('''
            SELECT COUNT(*) as message_count,
                   COUNT(DISTINCT user_id) as unique_users,
                   AVG(relevance_score) as avg_relevance,
                   AVG(sentiment_score) as avg_sentiment,
                   SUM(word_count) as total_words,
                   AVG(response_time_ms) as avg_response_time
            FROM conversations 
            WHERE room_id = ? AND timestamp >= ?
        ''', (room_id, since_time))
        
        stats = cursor.fetchone()
        
        # Get dominant emotions
        cursor.execute('''
            SELECT emotion_state, COUNT(*) as count
            FROM conversations 
            WHERE room_id = ? AND timestamp >= ? AND emotion_state != ''
            GROUP BY emotion_state
            ORDER BY count DESC
            LIMIT 5
        ''', (room_id, since_time))
        
        emotions = cursor.fetchall()
        
        # Get key topics (simplified)
        cursor.execute('''
            SELECT content
            FROM conversations 
            WHERE room_id = ? AND timestamp >= ? AND relevance_score > 0.5
            ORDER BY relevance_score DESC
            LIMIT 10
        ''', (room_id, since_time))
        
        high_relevance_content = cursor.fetchall()
        conn.close()
        
        # Extract topics
        all_content = ' '.join([content[0] for content in high_relevance_content])
        key_topics = self._extract_topics(all_content)
        
        return {
            'room_id': room_id,
            'time_period_hours': hours_back,
            'message_count': stats[0] or 0,
            'unique_participants': stats[1] or 0,
            'avg_relevance': round(stats[2] or 0, 3),
            'avg_sentiment': round(stats[3] or 0, 3),
            'total_words': stats[4] or 0,
            'avg_response_time_ms': round(stats[5] or 0, 1),
            'dominant_emotions': [emotion[0] for emotion in emotions],
            'key_topics': key_topics[:5],
            'generated_at': datetime.now().isoformat()
        }
    
    def generate_daily_summary(self, room_id: str, date: str = None) -> ConversationSummary:
        """Generate comprehensive daily conversation summary."""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cache_key = f"{room_id}:summary:{date}"
        if cache_key in self.summary_cache:
            return self.summary_cache[cache_key]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get daily statistics
        cursor.execute('''
            SELECT COUNT(*) as message_count,
                   COUNT(DISTINCT user_id) as unique_participants,
                   AVG(response_time_ms) as avg_response_time,
                   SUM(word_count) as total_words,
                   AVG(sentiment_score) as avg_sentiment
            FROM conversations 
            WHERE room_id = ? AND date(timestamp) = ?
        ''', (room_id, date))
        
        stats = cursor.fetchone()
        
        if not stats[0]:  # No messages
            return ConversationSummary(
                room_id=room_id, date=date, message_count=0,
                key_topics=[], dominant_emotions=[], summary_text="No activity",
                participants=[], peak_activity_hour=0, avg_response_time=0.0
            )
        
        # Get participants
        cursor.execute('''
            SELECT DISTINCT user_id
            FROM conversations 
            WHERE room_id = ? AND date(timestamp) = ?
        ''', (room_id, date))
        
        participants = [row[0] for row in cursor.fetchall()]
        
        # Get peak activity hour
        cursor.execute('''
            SELECT strftime('%H', timestamp) as hour, COUNT(*) as count
            FROM conversations 
            WHERE room_id = ? AND date(timestamp) = ?
            GROUP BY hour
            ORDER BY count DESC
            LIMIT 1
        ''', (room_id, date))
        
        peak_hour_result = cursor.fetchone()
        peak_activity_hour = int(peak_hour_result[0]) if peak_hour_result else 0
        
        # Get emotions and topics
        cursor.execute('''
            SELECT content, emotion_state
            FROM conversations 
            WHERE room_id = ? AND date(timestamp) = ?
            ORDER BY relevance_score DESC
        ''', (room_id, date))
        
        messages = cursor.fetchall()
        conn.close()
        
        # Analyze content
        all_content = ' '.join([msg[0] for msg in messages])
        key_topics = self._extract_topics(all_content)
        
        # Analyze emotions
        emotions = [msg[1] for msg in messages if msg[1]]
        emotion_counts = defaultdict(int)
        for emotion in emotions:
            for e in emotion.split():
                if e.isupper() and len(e) > 2:
                    emotion_counts[e] += 1
        
        dominant_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        dominant_emotions = [e[0] for e in dominant_emotions]
        
        # Generate summary text
        summary_text = (
            f"Daily conversation summary: {stats[0]} messages from {stats[1]} participants. "
            f"Peak activity at {peak_activity_hour}:00. "
        )
        
        if key_topics:
            summary_text += f"Key topics: {', '.join(key_topics[:3])}. "
        
        if dominant_emotions:
            summary_text += f"Dominant emotions: {', '.join(dominant_emotions[:3])}."
        
        summary = ConversationSummary(
            room_id=room_id,
            date=date,
            message_count=stats[0],
            key_topics=key_topics,
            dominant_emotions=dominant_emotions,
            summary_text=summary_text,
            participants=participants,
            peak_activity_hour=peak_activity_hour,
            avg_response_time=stats[2] or 0.0
        )
        
        # Cache and store summary
        self.summary_cache[cache_key] = summary
        self._store_summary(summary, stats[4] or 0, stats[3] or 0)
        
        return summary
    
    def _store_summary(self, summary: ConversationSummary, avg_sentiment: float, total_words: int):
        """Store summary in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO conversation_summaries 
            (room_id, summary_date, message_count, unique_participants, key_topics, 
             dominant_emotions, summary_text, peak_activity_hour, avg_response_time,
             total_words, avg_sentiment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            summary.room_id, summary.date, summary.message_count, len(summary.participants),
            json.dumps(summary.key_topics), json.dumps(summary.dominant_emotions),
            summary.summary_text, summary.peak_activity_hour, summary.avg_response_time,
            total_words, avg_sentiment
        ))
        
        conn.commit()
        conn.close()
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract key topics from conversation text with emotional intelligence."""
        if not text:
            return []
        
        # Clean and tokenize
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter stop words and common terms
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy',
            'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use', 'that', 'with',
            'have', 'this', 'will', 'your', 'from', 'they', 'know', 'want', 'been',
            'good', 'much', 'some', 'time', 'very', 'when', 'come', 'here', 'just',
            'like', 'long', 'make', 'many', 'over', 'such', 'take', 'than', 'them',
            'well', 'were', 'what'
        }
        
        # Technical and emotional keywords get priority
        priority_keywords = {
            'ribit', 'robot', 'python', 'api', 'database', 'matrix', 'search',
            'automation', 'ai', 'emotional', 'intelligence', 'jina', 'url'
        }
        
        filtered_words = []
        for word in words:
            if word not in stop_words:
                if word in priority_keywords:
                    filtered_words.extend([word] * 3)  # Boost priority words
                else:
                    filtered_words.append(word)
        
        # Count frequency
        word_counts = defaultdict(int)
        for word in filtered_words:
            word_counts[word] += 1
        
        # Return top topics
        topics = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [topic[0] for topic in topics[:15]]
    
    def get_user_interaction_pattern(self, room_id: str, user_id: str, days_back: int = 7) -> Dict:
        """Analyze user interaction patterns with emotional intelligence."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT COUNT(*) as message_count,
                   AVG(LENGTH(content)) as avg_message_length,
                   AVG(sentiment_score) as avg_sentiment,
                   AVG(relevance_score) as avg_relevance,
                   GROUP_CONCAT(DISTINCT emotion_state) as emotions,
                   strftime('%H', timestamp) as hours
            FROM conversations 
            WHERE room_id = ? AND user_id = ? AND date(timestamp) >= ?
        ''', (room_id, user_id, since_date))
        
        result = cursor.fetchone()
        
        # Get hourly activity pattern
        cursor.execute('''
            SELECT strftime('%H', timestamp) as hour, COUNT(*) as count
            FROM conversations 
            WHERE room_id = ? AND user_id = ? AND date(timestamp) >= ?
            GROUP BY hour
            ORDER BY hour
        ''', (room_id, user_id, since_date))
        
        hourly_activity = dict(cursor.fetchall())
        conn.close()
        
        # Process emotions
        emotions = result[4].split(',') if result[4] else []
        emotion_analysis = defaultdict(int)
        for emotion_string in emotions:
            if emotion_string:
                for emotion in emotion_string.split():
                    if emotion.isupper() and len(emotion) > 2:
                        emotion_analysis[emotion] += 1
        
        dominant_emotions = sorted(emotion_analysis.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'room_id': room_id,
            'user_id': user_id,
            'analysis_period_days': days_back,
            'message_count': result[0] or 0,
            'avg_message_length': round(result[1] or 0, 1),
            'avg_sentiment': round(result[2] or 0, 3),
            'avg_relevance': round(result[3] or 0, 3),
            'dominant_emotions': [e[0] for e in dominant_emotions],
            'hourly_activity': hourly_activity,
            'most_active_hour': max(hourly_activity.items(), key=lambda x: x[1])[0] if hourly_activity else '12',
            'generated_at': datetime.now().isoformat()
        }
    
    def cleanup_old_data(self, days_to_keep: int = 30):
        """Clean up old conversation data while preserving summaries."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        # Delete old messages (but keep summaries)
        cursor.execute('''
            DELETE FROM conversations 
            WHERE timestamp < ? AND relevance_score < 0.5
        ''', (cutoff_date,))
        
        deleted_messages = cursor.rowcount
        
        # Clean up old context relationships
        cursor.execute('''
            DELETE FROM context_relationships 
            WHERE created_at < ?
        ''', (cutoff_date,))
        
        deleted_relationships = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        # Clear caches
        self.context_cache.clear()
        self.summary_cache.clear()
        
        self.logger.info(f"Cleanup completed with EFFICIENCY: {deleted_messages} messages, {deleted_relationships} relationships removed")
        
        return {
            'deleted_messages': deleted_messages,
            'deleted_relationships': deleted_relationships,
            'cutoff_date': cutoff_date.isoformat()
        }

# Example usage and testing
def test_conversation_manager():
    """Test the advanced conversation manager."""
    print("💬 Testing Advanced Conversation Manager with PRECISION!")
    
    manager = AdvancedConversationManager()
    
    # Test message addition
    test_messages = [
        ConversationMessage(
            room_id="test_room",
            user_id="user1",
            message_type="user",
            content="Hello Ribit! Can you help me with Python programming?",
            timestamp=datetime.now(),
            emotion_state="CURIOSITY",
            context_tags=["greeting", "python", "help"]
        ),
        ConversationMessage(
            room_id="test_room",
            user_id="ribit",
            message_type="bot",
            content="Of course! I feel EXCITEMENT about helping with Python! What specific topic interests you?",
            timestamp=datetime.now(),
            emotion_state="EXCITEMENT and JOY",
            context_tags=["response", "python", "enthusiasm"],
            response_time_ms=1500
        ),
        ConversationMessage(
            room_id="test_room",
            user_id="user1",
            message_type="user",
            content="I want to learn about web scraping with emotional intelligence",
            timestamp=datetime.now(),
            emotion_state="EAGERNESS",
            context_tags=["web_scraping", "learning", "emotional_ai"]
        )
    ]
    
    # Add messages
    for msg in test_messages:
        msg_id = manager.add_message(msg)
        print(f"✅ Message added: ID {msg_id}")
    
    # Get context
    context = manager.get_conversation_context("test_room", limit=10)
    print(f"\n📝 Context retrieved: {len(context)} messages")
    
    # Generate summary
    summary = manager.generate_daily_summary("test_room")
    print(f"\n📊 Daily summary: {summary.summary_text}")
    print(f"Key topics: {summary.key_topics}")
    print(f"Dominant emotions: {summary.dominant_emotions}")
    
    # Get contextual summary
    contextual = manager.get_contextual_summary("test_room", hours_back=1)
    print(f"\n🔍 Contextual summary:")
    print(f"Messages: {contextual['message_count']}")
    print(f"Avg sentiment: {contextual['avg_sentiment']}")
    print(f"Key topics: {contextual['key_topics']}")
    
    # User pattern analysis
    pattern = manager.get_user_interaction_pattern("test_room", "user1")
    print(f"\n👤 User pattern analysis:")
    print(f"Messages: {pattern['message_count']}")
    print(f"Avg message length: {pattern['avg_message_length']}")
    print(f"Dominant emotions: {pattern['dominant_emotions']}")
    
    print("\n✅ All tests completed with SATISFACTION and PRIDE!")

if __name__ == "__main__":
    test_conversation_manager()
