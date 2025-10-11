"""
Conversation Memory and Archival System for Ribit 2.0
Saves interesting conversations, creates summaries, and learns from archives
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

class ConversationMemory:
    """Advanced conversation memory with archival and learning"""
    
    def __init__(self, memory_dir: str = "conversation_archives"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        self.current_conversations = {}  # Active conversations
        self.interesting_conversations = []  # Flagged as interesting
        self.search_results_cache = {}  # Cached search results
        self.learned_insights = []  # Insights from past conversations
        
        self._load_archives()
    
    def _load_archives(self):
        """Load archived conversations and insights"""
        try:
            # Load interesting conversations
            interesting_file = self.memory_dir / "interesting_conversations.json"
            if interesting_file.exists():
                with open(interesting_file, 'r') as f:
                    self.interesting_conversations = json.load(f)
                logger.info(f"Loaded {len(self.interesting_conversations)} interesting conversations")
            
            # Load learned insights
            insights_file = self.memory_dir / "learned_insights.json"
            if insights_file.exists():
                with open(insights_file, 'r') as f:
                    self.learned_insights = json.load(f)
                logger.info(f"Loaded {len(self.learned_insights)} learned insights")
            
            # Load search results cache
            cache_file = self.memory_dir / "search_results_cache.json"
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    self.search_results_cache = json.load(f)
                logger.info(f"Loaded {len(self.search_results_cache)} cached search results")
                
        except Exception as e:
            logger.error(f"Error loading archives: {e}")
    
    def add_message(self, room_id: str, user_id: str, message: str, response: str, 
                    metadata: Optional[Dict] = None):
        """Add a message exchange to current conversation"""
        if room_id not in self.current_conversations:
            self.current_conversations[room_id] = {
                'room_id': room_id,
                'started_at': time.time(),
                'messages': [],
                'participants': set(),
                'topics': set(),
                'interesting_score': 0,
            }
        
        conv = self.current_conversations[room_id]
        conv['participants'].add(user_id)
        
        message_entry = {
            'timestamp': time.time(),
            'user_id': user_id,
            'message': message,
            'response': response,
            'metadata': metadata or {}
        }
        
        conv['messages'].append(message_entry)
        
        # Update interesting score
        self._update_interesting_score(room_id, message, response, metadata)
        
        # Extract topics
        self._extract_topics(room_id, message)
    
    def _update_interesting_score(self, room_id: str, message: str, response: str, 
                                  metadata: Optional[Dict]):
        """Calculate how interesting this conversation is"""
        conv = self.current_conversations[room_id]
        score = 0
        
        # Long messages are more interesting
        if len(message) > 100:
            score += 1
        if len(response) > 200:
            score += 1
        
        # Philosophical/deep questions
        if any(word in message.lower() for word in ['meaning', 'purpose', 'consciousness', 'philosophy', 'existence']):
            score += 3
        
        # Technical discussions
        if any(word in message.lower() for word in ['algorithm', 'implementation', 'architecture', 'optimization']):
            score += 2
        
        # Questions (engagement)
        if '?' in message:
            score += 1
        
        # Multiple exchanges
        if len(conv['messages']) > 5:
            score += 2
        
        # Metadata indicates complexity
        if metadata:
            if metadata.get('complexity') == 'complex':
                score += 2
            if metadata.get('question_depth') in ['analytical', 'philosophical']:
                score += 2
        
        conv['interesting_score'] += score
    
    def _extract_topics(self, room_id: str, message: str):
        """Extract topics from message"""
        conv = self.current_conversations[room_id]
        
        # Simple topic extraction (can be enhanced with NLP)
        topics = []
        
        # Programming languages
        prog_langs = ['python', 'javascript', 'java', 'c++', 'rust', 'go']
        for lang in prog_langs:
            if lang in message.lower():
                topics.append(f"programming:{lang}")
        
        # Concepts
        concepts = ['ai', 'machine learning', 'web development', 'database', 'api', 
                   'philosophy', 'consciousness', 'history', 'science']
        for concept in concepts:
            if concept in message.lower():
                topics.append(f"concept:{concept}")
        
        conv['topics'].update(topics)
    
    def save_if_interesting(self, room_id: str, threshold: int = 5):
        """Save conversation if it's interesting enough"""
        if room_id not in self.current_conversations:
            return False
        
        conv = self.current_conversations[room_id]
        
        if conv['interesting_score'] >= threshold:
            # Create summary
            summary = self._create_summary(conv)
            
            # Add to interesting conversations
            interesting_entry = {
                'room_id': room_id,
                'saved_at': time.time(),
                'saved_at_readable': datetime.now().isoformat(),
                'interesting_score': conv['interesting_score'],
                'message_count': len(conv['messages']),
                'participants': list(conv['participants']),
                'topics': list(conv['topics']),
                'summary': summary,
                'messages': conv['messages'][-10:]  # Save last 10 messages
            }
            
            self.interesting_conversations.append(interesting_entry)
            
            # Save to disk
            self._save_interesting_conversations()
            
            logger.info(f"Saved interesting conversation from {room_id} (score: {conv['interesting_score']})")
            return True
        
        return False
    
    def _create_summary(self, conv: Dict) -> str:
        """Create a summary of the conversation"""
        if not conv['messages']:
            return "Empty conversation"
        
        # Extract key information
        topics = list(conv['topics'])
        message_count = len(conv['messages'])
        participant_count = len(conv['participants'])
        
        # Get first and last messages
        first_msg = conv['messages'][0]['message'][:100]
        last_msg = conv['messages'][-1]['message'][:100]
        
        summary = f"Conversation with {participant_count} participant(s) over {message_count} messages. "
        
        if topics:
            summary += f"Topics: {', '.join(topics[:3])}. "
        
        summary += f"Started with: '{first_msg}...' "
        summary += f"Ended with: '{last_msg}...'"
        
        return summary
    
    def _save_interesting_conversations(self):
        """Save interesting conversations to disk"""
        try:
            interesting_file = self.memory_dir / "interesting_conversations.json"
            with open(interesting_file, 'w') as f:
                json.dump(self.interesting_conversations, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving interesting conversations: {e}")
    
    def save_search_result(self, query: str, result: str, source: str = "web"):
        """Save interesting search results"""
        cache_key = query.lower().strip()
        
        self.search_results_cache[cache_key] = {
            'query': query,
            'result': result[:500],  # Save first 500 chars
            'source': source,
            'saved_at': time.time(),
            'saved_at_readable': datetime.now().isoformat(),
            'access_count': self.search_results_cache.get(cache_key, {}).get('access_count', 0) + 1
        }
        
        # Save to disk
        self._save_search_cache()
    
    def _save_search_cache(self):
        """Save search results cache to disk"""
        try:
            cache_file = self.memory_dir / "search_results_cache.json"
            with open(cache_file, 'w') as f:
                json.dump(self.search_results_cache, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving search cache: {e}")
    
    def get_cached_search_result(self, query: str) -> Optional[str]:
        """Get cached search result if available"""
        cache_key = query.lower().strip()
        if cache_key in self.search_results_cache:
            entry = self.search_results_cache[cache_key]
            # Update access count
            entry['access_count'] = entry.get('access_count', 0) + 1
            return entry['result']
        return None
    
    def learn_from_archives(self) -> List[str]:
        """Process archives and extract insights"""
        insights = []
        
        # Analyze interesting conversations
        for conv in self.interesting_conversations:
            # Extract common topics
            topics = conv.get('topics', [])
            if topics:
                insight = f"Users frequently discuss: {', '.join(topics[:3])}"
                if insight not in insights:
                    insights.append(insight)
            
            # Extract question patterns
            questions = [msg['message'] for msg in conv.get('messages', []) if '?' in msg.get('message', '')]
            if len(questions) > 3:
                insights.append(f"Common question pattern detected in {conv['room_id']}")
        
        # Analyze search patterns
        if self.search_results_cache:
            popular_queries = sorted(
                self.search_results_cache.items(),
                key=lambda x: x[1].get('access_count', 0),
                reverse=True
            )[:5]
            
            for query, data in popular_queries:
                insights.append(f"Popular search: '{query}' (accessed {data.get('access_count', 0)} times)")
        
        # Save insights
        self.learned_insights.extend(insights)
        self._save_insights()
        
        return insights
    
    def _save_insights(self):
        """Save learned insights to disk"""
        try:
            insights_file = self.memory_dir / "learned_insights.json"
            # Keep only unique insights
            unique_insights = list(set(self.learned_insights))
            with open(insights_file, 'w') as f:
                json.dump(unique_insights, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving insights: {e}")
    
    def get_conversation_summary(self, room_id: str) -> Optional[str]:
        """Get summary of current conversation"""
        if room_id not in self.current_conversations:
            return None
        
        return self._create_summary(self.current_conversations[room_id])
    
    def get_interesting_conversations(self, limit: int = 10) -> List[Dict]:
        """Get most interesting conversations"""
        sorted_convs = sorted(
            self.interesting_conversations,
            key=lambda x: x.get('interesting_score', 0),
            reverse=True
        )
        return sorted_convs[:limit]
    
    def get_insights(self) -> List[str]:
        """Get all learned insights"""
        return list(set(self.learned_insights))
    
    def clear_old_conversations(self, max_age_days: int = 30):
        """Clear old conversations from memory"""
        cutoff_time = time.time() - (max_age_days * 24 * 3600)
        
        # Clear old interesting conversations
        self.interesting_conversations = [
            conv for conv in self.interesting_conversations
            if conv.get('saved_at', 0) > cutoff_time
        ]
        
        # Clear old search cache
        self.search_results_cache = {
            k: v for k, v in self.search_results_cache.items()
            if v.get('saved_at', 0) > cutoff_time
        }
        
        # Save changes
        self._save_interesting_conversations()
        self._save_search_cache()
        
        logger.info(f"Cleared conversations older than {max_age_days} days")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            'active_conversations': len(self.current_conversations),
            'interesting_conversations': len(self.interesting_conversations),
            'cached_searches': len(self.search_results_cache),
            'learned_insights': len(set(self.learned_insights)),
            'total_messages_archived': sum(
                len(conv.get('messages', []))
                for conv in self.interesting_conversations
            )
        }

