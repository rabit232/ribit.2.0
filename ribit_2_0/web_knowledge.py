"""
Web Knowledge Module for Ribit 2.0
Provides Wikipedia access and web scraping capabilities
"""

import wikipediaapi
import requests
from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)

class WebKnowledge:
    """Access Wikipedia and web content for expanded knowledge"""
    
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent='Ribit2.0Bot/1.0 (Educational bot for Matrix chat)'
        )
        self.cache = {}  # Cache responses to avoid repeated lookups
        
    def search_wikipedia(self, query: str, sentences: int = 3) -> dict:
        """
        Search Wikipedia and return summary
        
        Args:
            query: Search term
            sentences: Number of sentences to return (default 3)
            
        Returns:
            dict with 'success', 'summary', 'url', 'title'
        """
        try:
            # Check cache first
            cache_key = f"wiki_{query.lower()}_{sentences}"
            if cache_key in self.cache:
                logger.info(f"Returning cached Wikipedia result for: {query}")
                return self.cache[cache_key]
            
            # Search Wikipedia
            page = self.wiki.page(query)
            
            if not page.exists():
                # Try searching for similar pages
                search_results = self._search_wikipedia_titles(query)
                if search_results:
                    page = self.wiki.page(search_results[0])
                    if not page.exists():
                        return {
                            'success': False,
                            'error': 'Page not found',
                            'suggestions': search_results[:5]
                        }
                else:
                    return {
                        'success': False,
                        'error': 'No results found'
                    }
            
            # Get summary (first N sentences)
            summary = page.summary
            if sentences:
                # Split into sentences and take first N
                sentences_list = re.split(r'(?<=[.!?])\s+', summary)
                summary = ' '.join(sentences_list[:sentences])
            
            # Get categories safely
            categories = []
            try:
                if hasattr(page, 'categories') and page.categories:
                    cat_keys = list(page.categories.keys())
                    categories = cat_keys[:5] if len(cat_keys) > 5 else cat_keys
            except:
                pass
            
            result = {
                'success': True,
                'title': page.title,
                'summary': summary,
                'url': page.fullurl,
                'categories': categories
            }
            
            # Cache the result
            self.cache[cache_key] = result
            logger.info(f"Successfully retrieved Wikipedia page: {page.title}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error searching Wikipedia for '{query}': {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _search_wikipedia_titles(self, query: str) -> list:
        """Search for Wikipedia page titles matching query"""
        try:
            # Use Wikipedia's search API
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'opensearch',
                'search': query,
                'limit': 5,
                'format': 'json'
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data[1] if len(data) > 1 else []
        except Exception as e:
            logger.error(f"Error searching Wikipedia titles: {e}")
        return []
    
    def get_detailed_info(self, query: str) -> dict:
        """
        Get detailed information from Wikipedia including sections
        
        Returns:
            dict with full page content and sections
        """
        try:
            page = self.wiki.page(query)
            
            if not page.exists():
                return {
                    'success': False,
                    'error': 'Page not found'
                }
            
            # Get sections
            sections = {}
            for section in page.sections:
                sections[section.title] = section.text[:500]  # First 500 chars of each section
            
            return {
                'success': True,
                'title': page.title,
                'summary': page.summary,
                'url': page.fullurl,
                'sections': sections,
                'categories': list(page.categories.keys())[:10]
            }
            
        except Exception as e:
            logger.error(f"Error getting detailed info for '{query}': {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def scrape_webpage(self, url: str) -> dict:
        """
        Scrape content from a webpage
        
        Args:
            url: URL to scrape
            
        Returns:
            dict with 'success', 'title', 'text', 'links'
        """
        try:
            # Check cache
            if url in self.cache:
                logger.info(f"Returning cached webpage: {url}")
                return self.cache[url]
            
            headers = {
                'User-Agent': 'Ribit2.0Bot/1.0 (Educational bot)'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else 'No title'
            
            # Extract main text (remove scripts, styles, etc.)
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
            
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up text
            text = re.sub(r'\s+', ' ', text)
            text = text[:5000]  # Limit to 5000 characters
            
            # Extract links
            links = []
            for link in soup.find_all('a', href=True)[:20]:  # First 20 links
                links.append({
                    'text': link.get_text(strip=True),
                    'url': link['href']
                })
            
            result = {
                'success': True,
                'url': url,
                'title': title,
                'text': text,
                'links': links
            }
            
            # Cache result
            self.cache[url] = result
            logger.info(f"Successfully scraped webpage: {url}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error scraping webpage '{url}': {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_web(self, query: str) -> dict:
        """
        Search the web using DuckDuckGo (doesn't require API key)
        
        Args:
            query: Search query
            
        Returns:
            dict with search results
        """
        try:
            # Use DuckDuckGo Instant Answer API
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1,
                'skip_disambig': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            result = {
                'success': True,
                'query': query,
                'abstract': data.get('Abstract', ''),
                'abstract_text': data.get('AbstractText', ''),
                'abstract_source': data.get('AbstractSource', ''),
                'abstract_url': data.get('AbstractURL', ''),
                'heading': data.get('Heading', ''),
                'related_topics': []
            }
            
            # Extract related topics
            for topic in data.get('RelatedTopics', [])[:5]:
                if 'Text' in topic:
                    result['related_topics'].append({
                        'text': topic.get('Text', ''),
                        'url': topic.get('FirstURL', '')
                    })
            
            logger.info(f"Successfully searched web for: {query}")
            return result
            
        except Exception as e:
            logger.error(f"Error searching web for '{query}': {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_answer(self, query: str) -> str:
        """
        Get a concise answer to a query using Wikipedia
        
        Args:
            query: Question or search term
            
        Returns:
            str: Concise answer or error message
        """
        try:
            # Try Wikipedia first
            wiki_result = self.search_wikipedia(query, sentences=2)
            
            if wiki_result['success']:
                answer = f"{wiki_result['summary']}\n\n📚 Source: {wiki_result['url']}"
                return answer
            
            # Try web search as fallback
            web_result = self.search_web(query)
            
            if web_result['success'] and web_result['abstract_text']:
                answer = f"{web_result['abstract_text']}\n\n🔍 Source: {web_result['abstract_source']}"
                return answer
            
            return "I couldn't find reliable information about that. Could you rephrase your question?"
            
        except Exception as e:
            logger.error(f"Error getting answer for '{query}': {e}")
            return f"I encountered an error while searching: {str(e)}"
    
    def clear_cache(self):
        """Clear the response cache"""
        self.cache.clear()
        logger.info("Web knowledge cache cleared")


# Convenience functions for easy integration
def wikipedia_lookup(query: str, sentences: int = 3) -> dict:
    """Quick Wikipedia lookup"""
    wk = WebKnowledge()
    return wk.search_wikipedia(query, sentences)


def web_search(query: str) -> dict:
    """Quick web search"""
    wk = WebKnowledge()
    return wk.search_web(query)


def get_quick_answer(query: str) -> str:
    """Get quick answer from web sources"""
    wk = WebKnowledge()
    return wk.get_answer(query)
