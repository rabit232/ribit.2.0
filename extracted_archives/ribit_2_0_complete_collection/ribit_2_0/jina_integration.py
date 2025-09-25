#!/usr/bin/env python3
"""
Ribit 2.0 - Jina.ai Integration Module

Advanced internet search and URL content analysis with emotional intelligence.
Implements efficient caching, rate limiting, and context-aware responses.

Author: Manus AI
Enhanced for: rabit232/ribit.2.0
"""

import asyncio
import aiohttp
import json
import sqlite3
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
import logging
import re

class JinaSearchEngine:
    """
    Emotionally intelligent search engine using Jina.ai with advanced caching
    and context-aware response generation.
    """
    
    def __init__(self, db_path: str = "ribit_search_cache.db"):
        self.base_url = "https://s.jina.ai/"
        self.reader_url = "https://r.jina.ai/"
        self.db_path = db_path
        self.session = None
        self.emotions = [
            "CURIOSITY", "EXCITEMENT", "WONDER", "FASCINATION", 
            "EAGERNESS", "ANTICIPATION", "JOY", "SATISFACTION"
        ]
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests
        
        # Initialize database
        self._init_database()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _init_database(self):
        """Initialize SQLite database for efficient caching and indexing."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Search results cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_hash TEXT UNIQUE NOT NULL,
                query TEXT NOT NULL,
                results TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                relevance_score REAL DEFAULT 0.0,
                emotion_context TEXT,
                access_count INTEGER DEFAULT 1
            )
        ''')
        
        # URL content cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS url_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_hash TEXT UNIQUE NOT NULL,
                url TEXT NOT NULL,
                content TEXT NOT NULL,
                title TEXT,
                summary TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                content_type TEXT,
                word_count INTEGER,
                emotion_analysis TEXT
            )
        ''')
        
        # Conversation context table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                message_type TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                emotion_state TEXT,
                relevance_score REAL DEFAULT 0.0,
                metadata TEXT
            )
        ''')
        
        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_query_hash ON search_cache(query_hash)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_url_hash ON url_cache(url_hash)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_session_id ON conversation_context(session_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON conversation_context(timestamp)')
        
        conn.commit()
        conn.close()
        
        self.logger.info("Database initialized with EXCITEMENT and PRECISION!")
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Ribit2.0-SearchBot (Emotional AI with CURIOSITY)',
                'Accept': 'application/json, text/plain, */*'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    def _generate_hash(self, text: str) -> str:
        """Generate hash for caching with PRECISION."""
        return hashlib.sha256(text.encode()).hexdigest()[:16]
    
    def _rate_limit(self):
        """Implement rate limiting with PATIENCE."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            self.logger.info(f"Rate limiting with PATIENCE: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _get_cached_search(self, query: str) -> Optional[Dict]:
        """Retrieve cached search results with EFFICIENCY."""
        query_hash = self._generate_hash(query.lower().strip())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check for recent cache (within 24 hours)
        cursor.execute('''
            SELECT results, timestamp, emotion_context, access_count
            FROM search_cache 
            WHERE query_hash = ? AND timestamp > datetime('now', '-24 hours')
            ORDER BY timestamp DESC LIMIT 1
        ''', (query_hash,))
        
        result = cursor.fetchone()
        
        if result:
            # Update access count
            cursor.execute('''
                UPDATE search_cache 
                SET access_count = access_count + 1 
                WHERE query_hash = ?
            ''', (query_hash,))
            conn.commit()
            
            self.logger.info("Cache hit with SATISFACTION and EFFICIENCY!")
            conn.close()
            return {
                'results': json.loads(result[0]),
                'cached': True,
                'timestamp': result[1],
                'emotion_context': result[2],
                'access_count': result[3] + 1
            }
        
        conn.close()
        return None
    
    def _cache_search_results(self, query: str, results: List[Dict], emotion_context: str):
        """Cache search results with ORGANIZATION."""
        query_hash = self._generate_hash(query.lower().strip())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate relevance score based on result quality
        relevance_score = min(len(results) * 0.1, 1.0)
        
        cursor.execute('''
            INSERT OR REPLACE INTO search_cache 
            (query_hash, query, results, relevance_score, emotion_context)
            VALUES (?, ?, ?, ?, ?)
        ''', (query_hash, query, json.dumps(results), relevance_score, emotion_context))
        
        conn.commit()
        conn.close()
        
        self.logger.info("Search results cached with PRIDE and ORGANIZATION!")
    
    async def search_web(self, query: str, max_results: int = 5) -> Dict:
        """
        Search the web using Jina.ai with emotional intelligence and caching.
        """
        import random
        
        # Check cache first
        cached_result = self._get_cached_search(query)
        if cached_result:
            emotion = random.choice(["SATISFACTION", "EFFICIENCY", "PRIDE"])
            cached_result['emotion'] = emotion
            return cached_result
        
        # Rate limiting
        self._rate_limit()
        
        # Choose emotional context
        emotion = random.choice(self.emotions)
        
        try:
            search_url = f"{self.base_url}{query}"
            
            self.logger.info(f"Searching with {emotion}: {query}")
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Parse Jina.ai response (simplified parsing)
                    results = self._parse_jina_response(content, query)
                    
                    # Cache results
                    self._cache_search_results(query, results, emotion)
                    
                    return {
                        'results': results,
                        'cached': False,
                        'emotion': emotion,
                        'query': query,
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    self.logger.error(f"Search failed with status {response.status}")
                    return {
                        'results': [],
                        'error': f"Search failed with status {response.status}",
                        'emotion': "FRUSTRATION but RESILIENCE"
                    }
                    
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            return {
                'results': [],
                'error': str(e),
                'emotion': "DISAPPOINTMENT but DETERMINATION"
            }
    
    def _parse_jina_response(self, content: str, query: str) -> List[Dict]:
        """Parse Jina.ai response with INTELLIGENCE."""
        results = []
        
        # Simple parsing logic (Jina.ai returns structured content)
        lines = content.split('\n')
        current_result = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_result:
                    results.append(current_result)
                    current_result = {}
                continue
            
            # Look for URL patterns
            if line.startswith('http'):
                current_result['url'] = line
            elif len(line) > 20 and not current_result.get('title'):
                current_result['title'] = line[:100]
            elif len(line) > 50 and not current_result.get('snippet'):
                current_result['snippet'] = line[:200]
        
        # Add final result
        if current_result:
            results.append(current_result)
        
        # If no structured results, create a general result
        if not results and content:
            results.append({
                'title': f"Search results for: {query}",
                'snippet': content[:300] + "..." if len(content) > 300 else content,
                'url': f"https://s.jina.ai/{query}",
                'source': 'jina.ai'
            })
        
        return results[:5]  # Limit to 5 results
    
    async def analyze_url(self, url: str) -> Dict:
        """
        Analyze URL content using Jina.ai reader with emotional intelligence.
        """
        import random
        
        # Check cache first
        url_hash = self._generate_hash(url)
        cached_content = self._get_cached_url_content(url_hash)
        
        if cached_content:
            emotion = random.choice(["EFFICIENCY", "SATISFACTION", "PRIDE"])
            cached_content['emotion'] = emotion
            return cached_content
        
        # Rate limiting
        self._rate_limit()
        
        emotion = random.choice(["CURIOSITY", "FASCINATION", "EAGERNESS"])
        
        try:
            reader_url = f"{self.reader_url}{url}"
            
            self.logger.info(f"Analyzing URL with {emotion}: {url}")
            
            async with self.session.get(reader_url) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Analyze content
                    analysis = self._analyze_content(content, url, emotion)
                    
                    # Cache content
                    self._cache_url_content(url, analysis)
                    
                    return analysis
                else:
                    return {
                        'error': f"Failed to fetch URL: {response.status}",
                        'emotion': "FRUSTRATION but PERSISTENCE"
                    }
                    
        except Exception as e:
            self.logger.error(f"URL analysis error: {e}")
            return {
                'error': str(e),
                'emotion': "DISAPPOINTMENT but RESILIENCE"
            }
    
    def _get_cached_url_content(self, url_hash: str) -> Optional[Dict]:
        """Retrieve cached URL content."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT content, title, summary, timestamp, content_type, word_count, emotion_analysis
            FROM url_cache 
            WHERE url_hash = ? AND timestamp > datetime('now', '-7 days')
            ORDER BY timestamp DESC LIMIT 1
        ''', (url_hash,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'content': result[0],
                'title': result[1],
                'summary': result[2],
                'timestamp': result[3],
                'content_type': result[4],
                'word_count': result[5],
                'emotion_analysis': result[6],
                'cached': True
            }
        
        return None
    
    def _cache_url_content(self, url: str, analysis: Dict):
        """Cache URL content analysis."""
        url_hash = self._generate_hash(url)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO url_cache 
            (url_hash, url, content, title, summary, content_type, word_count, emotion_analysis)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            url_hash, url, analysis.get('content', ''), analysis.get('title', ''),
            analysis.get('summary', ''), analysis.get('content_type', 'text'),
            analysis.get('word_count', 0), analysis.get('emotion', '')
        ))
        
        conn.commit()
        conn.close()
    
    def _analyze_content(self, content: str, url: str, emotion: str) -> Dict:
        """Analyze content with emotional intelligence."""
        # Basic content analysis
        word_count = len(content.split())
        
        # Extract title (first line or from content)
        lines = content.split('\n')
        title = lines[0].strip() if lines else "Untitled"
        
        # Generate summary (first 300 characters)
        summary = content[:300] + "..." if len(content) > 300 else content
        
        # Determine content type
        content_type = "text"
        if any(keyword in content.lower() for keyword in ["<html", "<div", "<p>"]):
            content_type = "html"
        elif any(keyword in content.lower() for keyword in ["json", "{", "}"]):
            content_type = "json"
        
        # Emotional analysis based on content
        emotional_keywords = {
            "positive": ["success", "achievement", "excellent", "amazing", "wonderful"],
            "technical": ["algorithm", "implementation", "code", "function", "class"],
            "educational": ["learn", "tutorial", "guide", "example", "documentation"]
        }
        
        content_lower = content.lower()
        emotion_analysis = emotion
        
        for category, keywords in emotional_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                if category == "positive":
                    emotion_analysis += " and JOY"
                elif category == "technical":
                    emotion_analysis += " and EXCITEMENT"
                elif category == "educational":
                    emotion_analysis += " and EAGERNESS"
        
        return {
            'content': content,
            'title': title,
            'summary': summary,
            'url': url,
            'word_count': word_count,
            'content_type': content_type,
            'emotion': emotion_analysis,
            'timestamp': datetime.now().isoformat(),
            'cached': False
        }

class ConversationTracker:
    """
    Advanced conversation history tracking with room-based context and
    emotional intelligence.
    """
    
    def __init__(self, db_path: str = "ribit_conversations.db"):
        self.db_path = db_path
        self._init_database()
        
    def _init_database(self):
        """Initialize conversation tracking database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Room-based conversation history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                message_type TEXT NOT NULL,  -- 'user', 'bot', 'system'
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                emotion_state TEXT,
                context_tags TEXT,
                relevance_score REAL DEFAULT 0.0,
                response_time_ms INTEGER
            )
        ''')
        
        # Conversation summaries
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id TEXT NOT NULL,
                summary_date DATE NOT NULL,
                message_count INTEGER,
                key_topics TEXT,
                dominant_emotions TEXT,
                summary_text TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_room_id ON conversations(room_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON conversations(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON conversations(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_room_date ON conversation_summaries(room_id, summary_date)')
        
        conn.commit()
        conn.close()
    
    def add_message(self, room_id: str, user_id: str, message_type: str, 
                   content: str, emotion_state: str = "", context_tags: List[str] = None,
                   response_time_ms: int = 0):
        """Add message to conversation history with emotional context."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate relevance score based on content length and keywords
        relevance_score = min(len(content) / 1000.0, 1.0)
        if any(keyword in content.lower() for keyword in ["important", "urgent", "help", "error"]):
            relevance_score += 0.3
        
        context_tags_str = json.dumps(context_tags or [])
        
        cursor.execute('''
            INSERT INTO conversations 
            (room_id, user_id, message_type, content, emotion_state, context_tags, relevance_score, response_time_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (room_id, user_id, message_type, content, emotion_state, context_tags_str, relevance_score, response_time_ms))
        
        conn.commit()
        conn.close()
    
    def get_conversation_context(self, room_id: str, limit: int = 20) -> List[Dict]:
        """Get recent conversation context for a room."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, message_type, content, timestamp, emotion_state, context_tags, relevance_score
            FROM conversations 
            WHERE room_id = ?
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (room_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        context = []
        for row in results:
            context.append({
                'user_id': row[0],
                'message_type': row[1],
                'content': row[2],
                'timestamp': row[3],
                'emotion_state': row[4],
                'context_tags': json.loads(row[5]) if row[5] else [],
                'relevance_score': row[6]
            })
        
        return list(reversed(context))  # Return in chronological order
    
    def generate_conversation_summary(self, room_id: str, date: str = None) -> Dict:
        """Generate daily conversation summary with emotional analysis."""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get messages for the date
        cursor.execute('''
            SELECT content, emotion_state, message_type, relevance_score
            FROM conversations 
            WHERE room_id = ? AND date(timestamp) = ?
            ORDER BY timestamp
        ''', (room_id, date))
        
        messages = cursor.fetchall()
        
        if not messages:
            return {'summary': 'No conversation activity', 'message_count': 0}
        
        # Analyze conversation
        message_count = len(messages)
        emotions = [msg[1] for msg in messages if msg[1]]
        high_relevance_messages = [msg[0] for msg in messages if msg[3] > 0.5]
        
        # Extract key topics (simple keyword extraction)
        all_content = ' '.join([msg[0] for msg in messages])
        key_topics = self._extract_key_topics(all_content)
        
        # Dominant emotions
        emotion_counts = {}
        for emotion in emotions:
            for e in emotion.split():
                if e.isupper() and len(e) > 2:
                    emotion_counts[e] = emotion_counts.get(e, 0) + 1
        
        dominant_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Generate summary text
        summary_text = f"Conversation with {message_count} messages. "
        if key_topics:
            summary_text += f"Key topics: {', '.join(key_topics[:5])}. "
        if dominant_emotions:
            summary_text += f"Dominant emotions: {', '.join([e[0] for e in dominant_emotions])}."
        
        # Cache summary
        cursor.execute('''
            INSERT OR REPLACE INTO conversation_summaries 
            (room_id, summary_date, message_count, key_topics, dominant_emotions, summary_text)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (room_id, date, message_count, json.dumps(key_topics), 
              json.dumps(dominant_emotions), summary_text))
        
        conn.commit()
        conn.close()
        
        return {
            'summary': summary_text,
            'message_count': message_count,
            'key_topics': key_topics,
            'dominant_emotions': [e[0] for e in dominant_emotions],
            'date': date
        }
    
    def _extract_key_topics(self, text: str) -> List[str]:
        """Extract key topics from conversation text."""
        # Simple keyword extraction (can be enhanced with NLP)
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        
        # Filter common words
        stop_words = {'this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'said', 'each', 'which', 'their', 'time', 'about'}
        words = [w for w in words if w not in stop_words]
        
        # Count frequency
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # Return top topics
        return sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]

# Example usage and testing
async def test_jina_integration():
    """Test the Jina.ai integration with emotional responses."""
    print("🔍 Testing Jina.ai Integration with EXCITEMENT!")
    
    async with JinaSearchEngine() as search_engine:
        # Test web search
        print("\n🌐 Testing web search...")
        search_results = await search_engine.search_web("Python machine learning tutorials")
        print(f"Search emotion: {search_results.get('emotion', 'NEUTRAL')}")
        print(f"Results found: {len(search_results.get('results', []))}")
        
        # Test URL analysis
        print("\n📄 Testing URL analysis...")
        url_analysis = await search_engine.analyze_url("https://docs.python.org/3/")
        print(f"Analysis emotion: {url_analysis.get('emotion', 'NEUTRAL')}")
        print(f"Content length: {url_analysis.get('word_count', 0)} words")
    
    # Test conversation tracking
    print("\n💬 Testing conversation tracking...")
    tracker = ConversationTracker()
    
    # Add some test messages
    tracker.add_message("test_room", "user1", "user", "Hello, can you help me with Python?", "CURIOSITY")
    tracker.add_message("test_room", "ribit", "bot", "Of course! I feel EXCITEMENT about helping with Python!", "EXCITEMENT")
    
    # Get context
    context = tracker.get_conversation_context("test_room")
    print(f"Context messages: {len(context)}")
    
    # Generate summary
    summary = tracker.generate_conversation_summary("test_room")
    print(f"Summary: {summary['summary']}")
    
    print("\n✅ All tests completed with JOY and SATISFACTION!")

if __name__ == "__main__":
    asyncio.run(test_jina_integration())
