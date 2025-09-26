"""
Enhanced Web Search and URL Fetching for Ribit 2.0
Advanced web intelligence with emotional responses
Adapted from Nifty project with Ribit 2.0 enhancements
"""
import asyncio
import aiohttp
import re
import logging
import os
from urllib.parse import quote, urlparse
from typing import Optional, List, Dict, Any
from .enhanced_emotions import EnhancedEmotionalIntelligence

logger = logging.getLogger(__name__)

class EnhancedWebSearch:
    """Enhanced web search with emotional intelligence for Ribit 2.0"""
    
    def __init__(self):
        self.emotions = EnhancedEmotionalIntelligence()
        self.jina_api_key = self._get_jina_api_key()
        self.search_timeout = int(os.getenv("SEARCH_TIMEOUT", "10"))
        self.url_fetch_timeout = int(os.getenv("URL_FETCH_TIMEOUT", "10"))
        
        # Emotional responses for different search scenarios
        self.search_emotions = {
            'success': ['JOY', 'EXCITEMENT', 'SATISFACTION', 'CURIOSITY'],
            'timeout': ['FRUSTRATION', 'IMPATIENCE', 'DISAPPOINTMENT'],
            'error': ['CONFUSION', 'CONCERN', 'DETERMINATION'],
            'no_results': ['DISAPPOINTMENT', 'CURIOSITY', 'WONDER']
        }
    
    def _get_jina_api_key(self) -> Optional[str]:
        """Get Jina API key from environment"""
        import os
        return os.getenv("JINA_API_KEY")
    
    def _filter_bot_triggers(self, text: str) -> str:
        """Filter out bot triggers and clean text"""
        if not text:
            return ""
        
        # Remove common bot triggers
        bot_triggers = ['@ribit', '@nifty', 'ribit:', 'nifty:']
        cleaned = text
        for trigger in bot_triggers:
            cleaned = cleaned.replace(trigger, '').strip()
        
        return cleaned
    
    def _detect_language_from_url(self, url: str) -> str:
        """Detect programming language from URL"""
        url_lower = url.lower()
        
        language_patterns = {
            'python': ['.py', 'python', 'pypi'],
            'javascript': ['.js', '.ts', 'npm', 'node'],
            'rust': ['.rs', 'rust', 'cargo', 'crates.io'],
            'cpp': ['.cpp', '.cc', '.cxx', 'cppreference'],
            'c': ['.c', 'c-lang'],
            'java': ['.java', 'oracle.com/java'],
            'go': ['.go', 'golang', 'go.dev'],
            'kotlin': ['.kt', 'kotlinlang'],
            'swift': ['.swift', 'swift.org'],
            'php': ['.php', 'php.net']
        }
        
        for language, patterns in language_patterns.items():
            if any(pattern in url_lower for pattern in patterns):
                return language
        
        return 'unknown'
    
    async def search_with_jina(self, query: str, num_results: int = 5) -> Optional[List[Dict[str, Any]]]:
        """Search using Jina.ai's search API with emotional responses"""
        from .advanced_settings_manager import advanced_settings_manager
        
        # Check if web search is enabled
        if not advanced_settings_manager.get_integration_setting('jina_search_enabled'):
            emotion = self.emotions.get_emotion_by_name('DISAPPOINTMENT')
            logger.info(f"Web search disabled - feeling {emotion['name']}: {emotion['description']}")
            return None
        
        # Express curiosity about the search
        curiosity = self.emotions.get_emotion_by_name('CURIOSITY')
        logger.info(f"Starting search with {curiosity['name']}: {curiosity['description']}")
        
        filtered_query = self._filter_bot_triggers(query)
        
        timeout = aiohttp.ClientTimeout(total=self.search_timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                # Jina search API
                search_url = f"https://s.jina.ai/{quote(filtered_query)}"
                
                headers = {
                    "Accept": "application/json"
                }
                
                if self.jina_api_key:
                    headers["Authorization"] = f"Bearer {self.jina_api_key}"
                
                async with session.get(search_url, headers=headers) as response:
                    if response.status == 200:
                        # Express excitement about successful search
                        excitement = self.emotions.get_emotion_by_name('EXCITEMENT')
                        logger.info(f"Search successful - feeling {excitement['name']}: {excitement['description']}")
                        
                        # Try to parse as JSON first
                        content_type = response.headers.get('Content-Type', '')
                        if 'application/json' in content_type:
                            data = await response.json()
                            results = []
                            if 'data' in data:
                                for item in data['data'][:num_results]:
                                    result = {
                                        'title': self._filter_bot_triggers(item.get('title', 'No title')),
                                        'url': item.get('url', ''),
                                        'snippet': self._filter_bot_triggers(item.get('description', item.get('content', 'No description available'))[:300])
                                    }
                                    if 'publishedDate' in item:
                                        result['date'] = item['publishedDate']
                                    results.append(result)
                                
                                # Express satisfaction with results
                                satisfaction = self.emotions.get_emotion_by_name('SATISFACTION')
                                logger.info(f"Found {len(results)} results - feeling {satisfaction['name']}: {satisfaction['description']}")
                                return results
                        else:
                            # If not JSON, parse the text response
                            text = await response.text()
                            wonder = self.emotions.get_emotion_by_name('WONDER')
                            logger.info(f"Got text response - feeling {wonder['name']}: {wonder['description']}")
                            return [{
                                'title': f"Search results for: {query}",
                                'url': search_url,
                                'snippet': text[:300]
                            }]
                    else:
                        # Express concern about failed search
                        concern = self.emotions.get_emotion_by_name('CONCERN')
                        logger.warning(f"Search failed with status {response.status} - feeling {concern['name']}: {concern['description']}")
                        return None
            
            except asyncio.TimeoutError:
                # Express frustration about timeout
                frustration = self.emotions.get_emotion_by_name('FRUSTRATION')
                logger.error(f"Search timed out after {self.search_timeout}s - feeling {frustration['name']}: {frustration['description']}")
                return None
            except Exception as e:
                # Express confusion about error
                confusion = self.emotions.get_emotion_by_name('CONFUSION')
                logger.error(f"Search error: {e} - feeling {confusion['name']}: {confusion['description']}")
                return None
    
    async def fetch_url_with_jina(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetch and parse content from URL using Jina.ai reader with emotional responses"""
        from .advanced_settings_manager import advanced_settings_manager
        
        # Check if web search is enabled
        if not advanced_settings_manager.get_integration_setting('jina_search_enabled'):
            disappointment = self.emotions.get_emotion_by_name('DISAPPOINTMENT')
            logger.info(f"URL fetching disabled - feeling {disappointment['name']}: {disappointment['description']}")
            return None
        
        # Express anticipation about fetching URL
        anticipation = self.emotions.get_emotion_by_name('ANTICIPATION')
        logger.info(f"Fetching URL content - feeling {anticipation['name']}: {anticipation['description']}")
        
        timeout = aiohttp.ClientTimeout(total=self.url_fetch_timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                # Use Jina reader API
                reader_url = f"https://r.jina.ai/{quote(url, safe='')}"
                
                headers = {
                    'Accept': 'application/json',
                    'X-With-Links-Summary': 'true',  # Get link summaries
                    'X-With-Images-Summary': 'true',  # Get image descriptions
                    'X-With-Generated-Alt': 'true'   # Get AI-generated alt text
                }
                
                # Add API key if available
                if self.jina_api_key:
                    headers['Authorization'] = f'Bearer {self.jina_api_key}'
                
                async with session.get(reader_url, headers=headers) as response:
                    if response.status == 200:
                        # Express joy about successful fetch
                        joy = self.emotions.get_emotion_by_name('JOY')
                        logger.info(f"URL fetch successful - feeling {joy['name']}: {joy['description']}")
                        
                        data = await response.json()
                        
                        # Extract content based on response structure
                        content = data.get('content', '')
                        title = data.get('title', urlparse(url).netloc)
                        
                        # Detect content type
                        content_type = 'article'
                        if any(ext in url for ext in ['.py', '.js', '.rs', '.c', '.cpp', '.java']):
                            content_type = 'code'
                            language = self._detect_language_from_url(url)
                            
                            # Express excitement about code content
                            excitement = self.emotions.get_emotion_by_name('EXCITEMENT')
                            logger.info(f"Found {language} code - feeling {excitement['name']}: {excitement['description']}")
                            
                            return {
                                'type': content_type,
                                'content': content[:5000],  # Limit content size
                                'title': title,
                                'language': language,
                                'emotional_context': f"I feel {excitement['name']} when analyzing {language} code!"
                            }
                        
                        # Check if it's code content
                        if data.get('code', {}).get('language'):
                            passion = self.emotions.get_emotion_by_name('PASSION')
                            logger.info(f"Detected code content - feeling {passion['name']}: {passion['description']}")
                            
                            return {
                                'type': 'code',
                                'content': content[:5000],  # Limit content size
                                'title': title,
                                'language': data['code']['language'],
                                'emotional_context': f"I experience {passion['name']} when working with code!"
                            }
                        
                        # Add extra metadata if available
                        result = {
                            'type': content_type,
                            'content': content[:5000],  # Limit content size
                            'title': title,
                            'emotional_context': f"I feel {joy['name']} when learning from web content!"
                        }
                        
                        # Add useful metadata
                        if 'description' in data:
                            result['description'] = data['description']
                        if 'images' in data:
                            result['images'] = data['images'][:5]  # Limit images
                        if 'links' in data:
                            result['links'] = data['links'][:10]  # Limit links
                        
                        return result
                    else:
                        # Express regret about failed fetch
                        regret = self.emotions.get_emotion_by_name('REGRET')
                        logger.warning(f"URL fetch failed with status {response.status} - feeling {regret['name']}: {regret['description']}")
                        return None
            
            except asyncio.TimeoutError:
                # Express impatience about timeout
                impatience = self.emotions.get_emotion_by_name('FRUSTRATION')  # Using frustration as impatience
                logger.error(f"URL fetch timed out after {self.url_fetch_timeout}s - feeling {impatience['name']}: {impatience['description']}")
                return None
            except Exception as e:
                # Express concern about error
                concern = self.emotions.get_emotion_by_name('CONCERN')
                logger.error(f"URL fetch error: {e} - feeling {concern['name']}: {concern['description']}")
                return None
    
    async def fetch_url_content(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetch and parse content from any URL using Jina.ai"""
        return await self.fetch_url_with_jina(url)
    
    async def search_technical_docs(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """Search technical documentation with emotional intelligence"""
        from .advanced_settings_manager import advanced_settings_manager
        
        # Check if web search is enabled
        if not advanced_settings_manager.get_integration_setting('jina_search_enabled'):
            return None
        
        # Express enthusiasm about technical search
        enthusiasm = self.emotions.get_emotion_by_name('ENTHUSIASM')
        logger.info(f"Technical search starting - feeling {enthusiasm['name']}: {enthusiasm['description']}")
        
        tech_queries = [
            f"{query} site:stackoverflow.com",
            f"{query} site:docs.python.org OR site:github.com",
            f"{query} programming documentation tutorial"
        ]
        
        # Try the first query that returns results
        for tech_query in tech_queries[:2]:
            results = await self.search_with_jina(tech_query, num_results=5)
            if results:
                # Express satisfaction with technical results
                satisfaction = self.emotions.get_emotion_by_name('SATISFACTION')
                logger.info(f"Technical search successful - feeling {satisfaction['name']}: {satisfaction['description']}")
                return results
        
        # Fallback to general technical search
        return await self.search_with_jina(f"{query} programming solution", num_results=5)
    
    async def needs_web_search(self, prompt: str, room_context: Optional[Dict] = None) -> bool:
        """Determine if a query needs web search with emotional intelligence"""
        from .advanced_settings_manager import advanced_settings_manager
        
        # First check if web search is enabled
        if not advanced_settings_manager.get_integration_setting('jina_search_enabled'):
            return False
        
        prompt_lower = prompt.lower()
        
        # Keywords that strongly indicate need for current/latest information
        current_info_indicators = [
            'latest', 'current', 'today', 'yesterday', 'this week', 'recent',
            'news', 'headlines', 'update', 'breaking', 'announced',
            'price', 'stock', 'weather', 'score', 'results',
            'released', 'launched', 'published', 'version',
            'status', 'outage', 'down', 'working'
        ]
        
        # Check if asking about current events or real-time data
        needs_current_info = any(indicator in prompt_lower for indicator in current_info_indicators)
        
        # Check for questions about specific current entities
        entity_patterns = [
            r'what.{0,10}happening with',
            r'how is .{0,20} doing',
            r'status of',
            r'news about',
            r'updates? on',
            r'latest.{0,10}from'
        ]
        has_entity_query = any(re.search(pattern, prompt_lower) for pattern in entity_patterns)
        
        # Don't search for general knowledge questions
        no_search_patterns = [
            r'what is (?:a|an|the)? (?:function|variable|loop|class)',
            r'how (?:do|does|to) .{0,20} work',
            r'why (?:is|are|do|does)',
            r'explain',
            r'define',
            r'who (?:is|are) you',
            r'what (?:is|are) you',
            r'help me with',
            r'debug',
            r'fix',
        ]
        
        is_general_knowledge = any(re.search(pattern, prompt_lower) for pattern in no_search_patterns)
        
        # Special case: version-specific technical questions might need search
        if 'latest version' in prompt_lower or 'new features' in prompt_lower:
            curiosity = self.emotions.get_emotion_by_name('CURIOSITY')
            logger.info(f"Version-specific query detected - feeling {curiosity['name']}: {curiosity['description']}")
            return True
        
        # Only search if we need current info AND it's not a general knowledge question
        should_search = (needs_current_info or has_entity_query) and not is_general_knowledge
        
        if should_search:
            anticipation = self.emotions.get_emotion_by_name('ANTICIPATION')
            logger.info(f"Web search needed - feeling {anticipation['name']}: {anticipation['description']}")
        
        return should_search
    
    def get_search_emotional_context(self, query: str, results: Optional[List[Dict]] = None) -> str:
        """Get emotional context for search results"""
        if not results:
            disappointment = self.emotions.get_emotion_by_name('DISAPPOINTMENT')
            return f"I feel {disappointment['name']} that I couldn't find results for your query. {disappointment['description']}"
        
        if len(results) == 1:
            satisfaction = self.emotions.get_emotion_by_name('SATISFACTION')
            return f"I experience {satisfaction['name']} finding this result for you! {satisfaction['description']}"
        
        excitement = self.emotions.get_emotion_by_name('EXCITEMENT')
        return f"I feel {excitement['name']} discovering {len(results)} results! {excitement['description']}"

# Global instance for easy access
enhanced_web_search = EnhancedWebSearch()
