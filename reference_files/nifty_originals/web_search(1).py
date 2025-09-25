"""Web search and URL fetching functionality"""
import asyncio
import aiohttp
import re
from urllib.parse import quote, urlparse
from config.settings import JINA_API_KEY, SEARCH_TIMEOUT, URL_FETCH_TIMEOUT
from utils.helpers import filter_bot_triggers, detect_language_from_url

async def search_with_jina(query, num_results=5):
    """Search using Jina.ai's search API with timeout"""
    # Import here to avoid circular dependency
    from modules.settings_manager import settings_manager
    
    # Check if web search is enabled
    if not settings_manager.is_web_search_enabled():
        return None
    
    filtered_query = filter_bot_triggers(query)
    
    timeout = aiohttp.ClientTimeout(total=SEARCH_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            # Jina search API
            search_url = f"https://s.jina.ai/{quote(filtered_query)}"
            
            headers = {
                "Authorization": f"Bearer {JINA_API_KEY}",
                "Accept": "application/json"
            }
            
            async with session.get(search_url, headers=headers) as response:
                if response.status == 200:
                    # Try to parse as JSON first
                    content_type = response.headers.get('Content-Type', '')
                    if 'application/json' in content_type:
                        data = await response.json()
                        results = []
                        if 'data' in data:
                            for item in data['data'][:num_results]:
                                result = {
                                    'title': filter_bot_triggers(item.get('title', 'No title')),
                                    'url': item.get('url', ''),
                                    'snippet': filter_bot_triggers(item.get('description', item.get('content', 'No description available'))[:300])
                                }
                                if 'publishedDate' in item:
                                    result['date'] = item['publishedDate']
                                results.append(result)
                        return results
                    else:
                        # If not JSON, parse the text response
                        text = await response.text()
                        # Extract results from text format if needed
                        return [{
                            'title': f"Search results for: {query}",
                            'url': search_url,
                            'snippet': text[:300]
                        }]
                else:
                    print(f"Jina search returned status {response.status}")
                    print(f"Response: {await response.text()}")
                    return None
        
        except asyncio.TimeoutError:
            print(f"[ERROR] Jina search timed out after {SEARCH_TIMEOUT} seconds")
            return None
        except Exception as e:
            print(f"Error searching with Jina: {e}")
            return None

async def fetch_url_with_jina(url):
    """Fetch and parse content from URL using Jina.ai reader with timeout"""
    # Import here to avoid circular dependency
    from modules.settings_manager import settings_manager
    
    # Check if web search is enabled
    if not settings_manager.is_web_search_enabled():
        return None
    
    timeout = aiohttp.ClientTimeout(total=URL_FETCH_TIMEOUT)
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
            if JINA_API_KEY:
                headers['Authorization'] = f'Bearer {JINA_API_KEY}'
            
            async with session.get(reader_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Extract content based on response structure
                    content = data.get('content', '')
                    title = data.get('title', urlparse(url).netloc)
                    
                    # Detect content type
                    content_type = 'article'
                    if any(ext in url for ext in ['.py', '.js', '.rs', '.c', '.cpp', '.java']):
                        content_type = 'code'
                        language = detect_language_from_url(url)
                        return {
                            'type': content_type,
                            'content': content[:5000],  # Limit content size
                            'title': title,
                            'language': language
                        }
                    
                    # Check if it's code content
                    if data.get('code', {}).get('language'):
                        return {
                            'type': 'code',
                            'content': content[:5000],  # Limit content size
                            'title': title,
                            'language': data['code']['language']
                        }
                    
                    # Add extra metadata if available
                    result = {
                        'type': content_type,
                        'content': content[:5000],  # Limit content size
                        'title': title
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
                    print(f"Jina reader returned status {response.status} for {url}")
                    return None
        
        except asyncio.TimeoutError:
            print(f"[ERROR] URL fetch timed out after {URL_FETCH_TIMEOUT} seconds for {url}")
            return None
        except Exception as e:
            print(f"Error fetching URL with Jina: {e}")
            return None

async def fetch_url_content(url):
    """Fetch and parse content from any URL using Jina.ai"""
    return await fetch_url_with_jina(url)

async def search_technical_docs(query):
    """Search technical documentation using Jina with site-specific queries"""
    # Import here to avoid circular dependency
    from modules.settings_manager import settings_manager
    
    # Check if web search is enabled
    if not settings_manager.is_web_search_enabled():
        return None
    
    tech_queries = [
        f"{query} site:stackoverflow.com",
        f"{query} site:docs.python.org OR site:github.com",
        f"{query} programming documentation tutorial"
    ]
    
    # Try the first query that returns results
    for tech_query in tech_queries[:2]:
        results = await search_with_jina(tech_query, num_results=5)
        if results:
            return results
    
    # Fallback to general technical search
    return await search_with_jina(f"{query} programming solution", num_results=5)

async def needs_web_search(prompt, room_context=None):
    """Determine if a query actually needs web search for current information"""
    # Import here to avoid circular dependency
    from modules.settings_manager import settings_manager
    
    # First check if web search is enabled
    if not settings_manager.is_web_search_enabled():
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
    
    # Check for questions about specific current entities (companies, people, events)
    entity_patterns = [
        r'what.{0,10}happening with',
        r'how is .{0,20} doing',
        r'status of',
        r'news about',
        r'updates? on',
        r'latest.{0,10}from'
    ]
    has_entity_query = any(re.search(pattern, prompt_lower) for pattern in entity_patterns)
    
    # Don't search for:
    # - General knowledge questions (unless they need current info)
    # - Programming/technical questions (unless about latest versions)
    # - Philosophical or opinion questions
    # - Questions about the bot itself
    
    no_search_patterns = [
        r'what is (?:a|an|the)? (?:function|variable|loop|class)',  # Basic programming concepts
        r'how (?:do|does|to) .{0,20} work',  # How things work in general
        r'why (?:is|are|do|does)',  # Why questions rarely need current info
        r'explain',  # Explanations don't need current info
        r'define',  # Definitions are static
        r'who (?:is|are) you',  # Bot identity questions
        r'what (?:is|are) you',  # Bot identity questions
        r'help me with',  # Help requests usually don't need web search
        r'debug',  # Debugging help
        r'fix',  # Fix requests
    ]
    
    is_general_knowledge = any(re.search(pattern, prompt_lower) for pattern in no_search_patterns)
    
    # Special case: version-specific technical questions might need search
    if 'latest version' in prompt_lower or 'new features' in prompt_lower:
        return True
    
    # Only search if we need current info AND it's not a general knowledge question
    should_search = (needs_current_info or has_entity_query) and not is_general_knowledge
    
    if should_search:
        print(f"[DEBUG] Web search needed - Current info: {needs_current_info}, Entity query: {has_entity_query}")
    
    return should_search
