"""
Matrix Message History Tracker for Ribit 2.0
Tracks message history with smart search and word learning capabilities

Features:
- Up to 3 months message history retention
- Smart search: "did username mention topic last week?"
- Word learning from conversation context
- Natural language querying
"""

import logging
import sqlite3
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import Counter
from pathlib import Path

logger = logging.getLogger(__name__)

class MatrixHistoryTracker:
    """
    Track Matrix message history with advanced search and learning capabilities
    """
    
    def __init__(self, db_path: str = "matrix_message_history.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.retention_days = 90  # 3 months
        self._init_database()
        self.word_library = self._load_word_library()
        self.logger.info(f"Matrix History Tracker initialized (retaining {self.retention_days} days)")
    
    def _init_database(self):
        """Initialize the message history database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Message history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS message_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                sender_name TEXT,
                message_text TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                date_only DATE,
                hour INTEGER,
                word_count INTEGER,
                contains_question BOOLEAN,
                mentioned_users TEXT,
                topics TEXT,
                keywords TEXT
            )
        ''')
        
        # Create indices
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_room_timestamp ON message_history(room_id, timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sender ON message_history(sender)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON message_history(date_only)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_keywords ON message_history(keywords)')
        
        # Word library table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_library (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE NOT NULL,
                frequency INTEGER DEFAULT 1,
                first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                context_examples TEXT,
                related_topics TEXT
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_word ON word_library(word)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_frequency ON word_library(frequency)')
        
        # Topic tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topic_mentions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                room_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                message_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                context TEXT,
                FOREIGN KEY (message_id) REFERENCES message_history(id)
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_topic ON topic_mentions(topic)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_topic_timestamp ON topic_mentions(topic, timestamp)')
        
        # User mentions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_mentions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mentioned_user TEXT NOT NULL,
                room_id TEXT NOT NULL,
                by_sender TEXT NOT NULL,
                message_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (message_id) REFERENCES message_history(id)
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_mentioned_user ON user_mentions(mentioned_user)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_mention_timestamp ON user_mentions(mentioned_user, timestamp)')
        
        conn.commit()
        conn.close()
        
        self.logger.info("Message history database initialized")
    
    def add_message(
        self,
        room_id: str,
        sender: str,
        message_text: str,
        sender_name: Optional[str] = None
    ) -> int:
        """
        Add a message to history and extract learning data
        
        Args:
            room_id: Matrix room ID
            sender: Sender user ID
            message_text: Message content
            sender_name: Optional display name
            
        Returns:
            Message ID in database
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            timestamp = datetime.now()
            date_only = timestamp.date()
            hour = timestamp.hour
            
            # Extract features
            word_count = len(message_text.split())
            contains_question = '?' in message_text
            mentioned_users = self._extract_mentions(message_text)
            topics = self._extract_topics(message_text)
            keywords = self._extract_keywords(message_text)
            
            # Insert message
            cursor.execute('''
                INSERT INTO message_history (
                    room_id, sender, sender_name, message_text,
                    timestamp, date_only, hour, word_count,
                    contains_question, mentioned_users, topics, keywords
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                room_id, sender, sender_name, message_text,
                timestamp, date_only, hour, word_count,
                contains_question,
                json.dumps(mentioned_users),
                json.dumps(topics),
                json.dumps(keywords)
            ))
            
            message_id = cursor.lastrowid
            
            # Track topics
            for topic in topics:
                cursor.execute('''
                    INSERT INTO topic_mentions (topic, room_id, sender, message_id, timestamp, context)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (topic, room_id, sender, message_id, timestamp, message_text[:200]))
            
            # Track mentions
            for mentioned_user in mentioned_users:
                cursor.execute('''
                    INSERT INTO user_mentions (mentioned_user, room_id, by_sender, message_id, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (mentioned_user, room_id, sender, message_id, timestamp))
            
            # Update word library
            self._update_word_library(message_text, conn)
            
            conn.commit()
            conn.close()
            
            # Clean old messages
            self._cleanup_old_messages()
            
            return message_id
            
        except Exception as e:
            self.logger.error(f"Failed to add message: {e}")
            return -1
    
    def _extract_mentions(self, text: str) -> List[str]:
        """Extract user mentions from text"""
        # Matrix format: @username:server
        mentions = re.findall(r'@([a-zA-Z0-9_\-]+)(?::[a-zA-Z0-9\.\-]+)?', text)
        return list(set(mentions))
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract potential topics from text"""
        # Remove common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                       'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                       'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                       'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
                       'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        topics = [w for w in words if w not in common_words and len(w) > 3]
        
        # Get most frequent (potential topics)
        topic_counts = Counter(topics)
        return [topic for topic, count in topic_counts.most_common(10)]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Capitalized words (potential proper nouns)
        keywords = re.findall(r'\b[A-Z][a-z]+\b', text)
        
        # Technical terms (mixed case or with numbers)
        technical = re.findall(r'\b[A-Za-z]+\d+[A-Za-z0-9]*\b', text)
        
        # Hashtags
        hashtags = re.findall(r'#(\w+)', text)
        
        all_keywords = keywords + technical + hashtags
        return list(set(all_keywords))[:20]
    
    def _update_word_library(self, text: str, conn: sqlite3.Connection):
        """Update word library with new words"""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        cursor = conn.cursor()
        
        for word in set(words):
            cursor.execute('''
                INSERT INTO word_library (word, frequency, first_seen, last_seen, context_examples)
                VALUES (?, 1, ?, ?, ?)
                ON CONFLICT(word) DO UPDATE SET
                    frequency = frequency + 1,
                    last_seen = excluded.last_seen,
                    context_examples = context_examples || '|||' || excluded.context_examples
            ''', (word, datetime.now(), datetime.now(), text[:100]))
    
    def _load_word_library(self) -> Dict[str, int]:
        """Load word library into memory"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT word, frequency FROM word_library')
            word_lib = dict(cursor.fetchall())
            conn.close()
            return word_lib
        except:
            return {}
    
    def smart_search(self, query: str, room_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Natural language search queries like:
        - "did username mention topic last week?"
        - "who talked about python yesterday?"
        - "when did alice ask about databases?"
        
        Args:
            query: Natural language search query
            room_id: Optional room filter
            
        Returns:
            Search results with context
        """
        try:
            # Parse query
            parsed = self._parse_search_query(query)
            
            # Build SQL query
            sql = self._build_search_sql(parsed, room_id)
            
            # Execute search
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql, parsed.get('params', []))
            results = cursor.fetchall()
            conn.close()
            
            # Format results
            formatted_results = self._format_search_results(results, parsed)
            
            return {
                'success': True,
                'query': query,
                'parsed': parsed,
                'count': len(results),
                'results': formatted_results
            }
            
        except Exception as e:
            self.logger.error(f"Smart search failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'query': query
            }
    
    def _parse_search_query(self, query: str) -> Dict[str, Any]:
        """Parse natural language query into search parameters"""
        query_lower = query.lower()
        parsed = {
            'username': None,
            'topic': None,
            'time_range': None,
            'contains_question': False,
            'params': []
        }
        
        # Extract username
        username_match = re.search(r'(?:did|has|have)\s+(@?\w+)\s+(?:mention|talk|ask|say)', query_lower)
        if username_match:
            parsed['username'] = username_match.group(1).replace('@', '')
        
        # Extract topic
        topic_match = re.search(r'(?:about|mention|regarding)\s+([a-zA-Z0-9_\-]+)', query_lower)
        if topic_match:
            parsed['topic'] = topic_match.group(1)
        
        # Extract time range
        now = datetime.now()
        if 'today' in query_lower:
            parsed['time_range'] = (now.replace(hour=0, minute=0, second=0), now)
        elif 'yesterday' in query_lower:
            yesterday = now - timedelta(days=1)
            parsed['time_range'] = (
                yesterday.replace(hour=0, minute=0, second=0),
                yesterday.replace(hour=23, minute=59, second=59)
            )
        elif 'last week' in query_lower or 'week ago' in query_lower:
            week_ago = now - timedelta(days=7)
            parsed['time_range'] = (week_ago, now)
        elif 'last month' in query_lower or 'month ago' in query_lower:
            month_ago = now - timedelta(days=30)
            parsed['time_range'] = (month_ago, now)
        else:
            days_match = re.search(r'(\d+)\s+days?\s+ago', query_lower)
            if days_match:
                days = int(days_match.group(1))
                days_ago = now - timedelta(days=days)
                parsed['time_range'] = (days_ago, now)
        
        # Check for questions
        if 'ask' in query_lower or 'question' in query_lower:
            parsed['contains_question'] = True
        
        return parsed
    
    def _build_search_sql(self, parsed: Dict[str, Any], room_id: Optional[str]) -> str:
        """Build SQL query from parsed parameters"""
        conditions = []
        params = []
        
        sql = '''
            SELECT 
                id, room_id, sender, sender_name, message_text,
                timestamp, topics, keywords
            FROM message_history
            WHERE 1=1
        '''
        
        if room_id:
            conditions.append('room_id = ?')
            params.append(room_id)
        
        if parsed.get('username'):
            conditions.append("(sender LIKE ? OR sender_name LIKE ?)")
            params.extend([f"%{parsed['username']}%", f"%{parsed['username']}%"])
        
        if parsed.get('topic'):
            conditions.append("(message_text LIKE ? OR topics LIKE ?)")
            params.extend([f"%{parsed['topic']}%", f"%{parsed['topic']}%"])
        
        if parsed.get('time_range'):
            start, end = parsed['time_range']
            conditions.append('timestamp BETWEEN ? AND ?')
            params.extend([start, end])
        
        if parsed.get('contains_question'):
            conditions.append('contains_question = 1')
        
        if conditions:
            sql += ' AND ' + ' AND '.join(conditions)
        
        sql += ' ORDER BY timestamp DESC LIMIT 50'
        
        parsed['params'] = params
        return sql
    
    def _format_search_results(self, results: List[Tuple], parsed: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format search results for display"""
        formatted = []
        
        for row in results:
            msg_id, room_id, sender, sender_name, text, timestamp, topics, keywords = row
            
            formatted.append({
                'id': msg_id,
                'sender': sender_name or sender,
                'message': text,
                'timestamp': timestamp,
                'date': datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M'),
                'topics': json.loads(topics) if topics else [],
                'keywords': json.loads(keywords) if keywords else []
            })
        
        return formatted
    
    def _cleanup_old_messages(self):
        """Remove messages older than retention period"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM message_history WHERE timestamp < ?', (cutoff_date,))
            cursor.execute('DELETE FROM topic_mentions WHERE timestamp < ?', (cutoff_date,))
            cursor.execute('DELETE FROM user_mentions WHERE timestamp < ?', (cutoff_date,))
            
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            
            if deleted > 0:
                self.logger.info(f"Cleaned up {deleted} old messages")
                
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")
    
    def get_statistics(self, room_id: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics about message history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            where_clause = f"WHERE room_id = '{room_id}'" if room_id else ""
            
            cursor.execute(f'SELECT COUNT(*) FROM message_history {where_clause}')
            total_messages = cursor.fetchone()[0]
            
            cursor.execute(f'SELECT COUNT(DISTINCT sender) FROM message_history {where_clause}')
            unique_senders = cursor.fetchone()[0]
            
            cursor.execute(f'SELECT COUNT(*) FROM word_library')
            words_learned = cursor.fetchone()[0]
            
            cursor.execute(f'''
                SELECT topic, COUNT(*) as count
                FROM topic_mentions {where_clause.replace('room_id', 'topic_mentions.room_id')}
                GROUP BY topic
                ORDER BY count DESC
                LIMIT 10
            ''')
            top_topics = cursor.fetchall()
            
            conn.close()
            
            return {
                'total_messages': total_messages,
                'unique_senders': unique_senders,
                'words_learned': words_learned,
                'top_topics': [{'topic': t[0], 'count': t[1]} for t in top_topics],
                'retention_days': self.retention_days
            }
            
        except Exception as e:
            self.logger.error(f"Statistics failed: {e}")
            return {'error': str(e)}
    
    def get_word_library(self, limit: int = 120) -> List[Dict[str, Any]]:
        """
        Get learned words from the word library.
        
        Args:
            limit: Maximum number of words to return (default 120)
            
        Returns:
            List of word dictionaries with word, frequency, first_seen, last_seen
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT word, frequency, first_seen, last_seen
                FROM word_library
                ORDER BY frequency DESC
                LIMIT ?
            ''', (limit,))
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'word': row[0],
                    'frequency': row[1],
                    'first_seen': row[2],
                    'last_seen': row[3]
                }
                for row in results
            ]
            
        except Exception as e:
            self.logger.error(f"Failed to get word library: {e}")
            return []
