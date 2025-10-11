"""
Intelligent Responder for Ribit 2.0
Combines local knowledge with web lookup capabilities
"""

import logging
import random
from .web_knowledge import WebKnowledge
from .history_responder import HistoryResponder

logger = logging.getLogger(__name__)

class IntelligentResponder:
    """Intelligent response system that combines local and web knowledge"""
    
    def __init__(self):
        self.web_knowledge = WebKnowledge()
        self.history_responder = HistoryResponder()
        
        # Keywords that suggest web lookup is needed
        self.web_lookup_keywords = [
            'current', 'latest', 'recent', 'today', 'now', 'this year',
            'what is happening', 'news', 'update', 'status',
            'who is', 'what is', 'where is', 'when is',
            'population of', 'capital of', 'president of', 'leader of',
            'weather in', 'time in', 'currency of',
            'definition of', 'meaning of', 'explain',
            'how to', 'steps to', 'guide to'
        ]
        
        # Topics that should use local knowledge first
        self.local_first_topics = [
            'world war', 'ww1', 'ww2', 'holocaust', 'cold war',
            'industrial revolution', 'technology history',
            'ancient', 'medieval', 'historical'
        ]
    
    def get_response(self, query: str) -> str:
        """
        Get intelligent response using best available source
        
        Args:
            query: User's question
            
        Returns:
            str: Response with source attribution
        """
        query_lower = query.lower()
        
        # First, try local knowledge for historical topics
        if any(topic in query_lower for topic in self.local_first_topics):
            history_response = self.history_responder.get_response(query)
            if history_response:
                return history_response
        
        # Check if query suggests web lookup is needed
        needs_web_lookup = any(keyword in query_lower for keyword in self.web_lookup_keywords)
        
        if needs_web_lookup or self._is_factual_question(query_lower):
            # Try web lookup first for current/factual information
            web_response = self._get_web_response(query)
            if web_response:
                return web_response
        
        # Fall back to local knowledge
        history_response = self.history_responder.get_response(query)
        if history_response:
            return history_response
        
        # If no specific knowledge, try web as last resort
        if not needs_web_lookup:
            web_response = self._get_web_response(query)
            if web_response:
                return web_response
        
        return None  # No response available, will fall back to LLM
    
    def _is_factual_question(self, query: str) -> bool:
        """Check if query is asking for factual information"""
        factual_patterns = [
            'what is', 'what are', 'who is', 'who are', 'where is', 'where are',
            'when is', 'when was', 'when were', 'how many', 'how much',
            'which is', 'which are', 'why is', 'why are', 'why did', 'why do',
            'how does', 'how did', 'how do', 'how can', 'how to'
        ]
        return any(pattern in query for pattern in factual_patterns)
    
    def _get_web_response(self, query: str) -> str:
        """Get response from web sources with Ribit's personality"""
        try:
            # Try Wikipedia first for encyclopedic information
            wiki_result = self.web_knowledge.search_wikipedia(query, sentences=3)
            
            if wiki_result['success']:
                return self._format_wikipedia_response(wiki_result, query)
            
            # Try web search as fallback
            web_result = self.web_knowledge.search_web(query)
            
            if web_result['success'] and web_result['abstract_text']:
                return self._format_web_response(web_result, query)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting web response: {e}")
            return None
    
    def _format_wikipedia_response(self, result: dict, query: str) -> str:
        """Format Wikipedia response with Ribit's personality"""
        
        intros = [
            "Let me consult the vast archives of human knowledge...",
            "*Accessing Wikipedia's digital library*",
            "Ah, I found something interesting in the encyclopedia!",
            "According to the collective wisdom of Wikipedia...",
            "*Taps into the world's knowledge base*",
        ]
        
        outros = [
            f"\n\n📚 **Source:** [Wikipedia - {result['title']}]({result['url']})",
            f"\n\n📖 **Learn more:** [Wikipedia: {result['title']}]({result['url']})",
            f"\n\n🔗 **Reference:** [Wikipedia article on {result['title']}]({result['url']})",
        ]
        
        intro = random.choice(intros)
        outro = random.choice(outros)
        
        # Add humor for non-sensitive topics
        if not any(word in query.lower() for word in ['death', 'war', 'genocide', 'holocaust', 'tragedy']):
            humor_outros = [
                " (Wikipedia: where rabbit holes become entire underground cities.)",
                " (Fun fact: I just learned this too!)",
                " (Wikipedia: humanity's greatest collaborative achievement... after pizza.)",
                " (The internet's most reliable source of 3 AM knowledge quests.)",
            ]
            if random.random() < 0.3:
                outro = random.choice(humor_outros) + outro
        
        return f"{intro}\n\n{result['summary']}{outro}"
    
    def _format_web_response(self, result: dict, query: str) -> str:
        """Format web search response with Ribit's personality"""
        
        intros = [
            "Let me search the web for you...",
            "*Scanning the internet's vast knowledge*",
            "I found this information online:",
            "According to my web search...",
        ]
        
        intro = random.choice(intros)
        
        response = f"{intro}\n\n{result['abstract_text']}"
        
        if result['abstract_source']:
            response += f"\n\n🔍 **Source:** {result['abstract_source']}"
        
        if result['abstract_url']:
            response += f"\n🔗 **More info:** {result['abstract_url']}"
        
        return response
    
    def search_specific_topic(self, topic: str) -> str:
        """Search for specific topic with detailed information"""
        try:
            # Get detailed Wikipedia information
            detailed_info = self.web_knowledge.get_detailed_info(topic)
            
            if detailed_info['success']:
                response = f"**{detailed_info['title']}**\n\n"
                response += f"{detailed_info['summary'][:800]}...\n\n"
                
                # Add some sections if available
                if detailed_info['sections']:
                    response += "**Key Topics:**\n"
                    for section_title, section_text in list(detailed_info['sections'].items())[:3]:
                        response += f"• {section_title}\n"
                
                response += f"\n📚 **Full article:** {detailed_info['url']}"
                
                return response
            
            return None
            
        except Exception as e:
            logger.error(f"Error searching specific topic '{topic}': {e}")
            return None
    
    def get_current_info(self, query: str) -> str:
        """Get current/recent information"""
        try:
            # For current information, prefer web search
            web_result = self.web_knowledge.search_web(f"current {query}")
            
            if web_result['success'] and web_result['abstract_text']:
                return self._format_web_response(web_result, query)
            
            # Fallback to Wikipedia
            wiki_result = self.web_knowledge.search_wikipedia(query, sentences=2)
            
            if wiki_result['success']:
                response = f"Here's what I found (note: Wikipedia may not have the latest information):\n\n"
                response += f"{wiki_result['summary']}\n\n"
                response += f"📚 **Source:** {wiki_result['url']}\n\n"
                response += "💡 **Tip:** For the most current information, you might want to check recent news sources."
                return response
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting current info: {e}")
            return None


    # Alias method for compatibility
    def get_intelligent_response(self, query: str) -> str:
        """Alias for get_response() for compatibility"""
        return self.get_response(query)

