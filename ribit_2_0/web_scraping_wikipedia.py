"""
Enhanced Web Scraping and Wikipedia Search for Ribit 2.0

Provides robust web scraping and Wikipedia search capabilities.
"""

from __future__ import annotations  # For Python 3.8 compatibility
import logging
import asyncio
import aiohttp
import wikipediaapi
import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse, quote

logger = logging.getLogger(__name__)


class WebScrapingWikipedia:
    """Enhanced web scraping and Wikipedia search functionality."""
    
    def __init__(self, user_agent: str = "Ribit2.0Bot/1.0 (https://github.com/rabit232/ribit.2.0)"):
        self.user_agent = user_agent
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent=user_agent
        )
        self.session = None
        logger.info("Web Scraping and Wikipedia module initialized")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={'User-Agent': self.user_agent}
            )
        return self.session
    
    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    # Wikipedia Functions
    
    def search_wikipedia(self, query: str, results: int = 5) -> List[str]:
        """
        Search Wikipedia and return page titles.
        
        Args:
            query: Search query
            results: Number of results to return
            
        Returns:
            List of Wikipedia page titles
        """
        try:
            # Use Wikipedia API to search
            search_url = f"https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'opensearch',
                'search': query,
                'limit': results,
                'namespace': 0,
                'format': 'json'
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            titles = data[1] if len(data) > 1 else []
            
            logger.info(f"Wikipedia search for '{query}' returned {len(titles)} results")
            return titles
            
        except Exception as e:
            logger.error(f"Wikipedia search failed: {e}")
            return []
    
    def get_wikipedia_summary(self, title: str, sentences: int = 3) -> Optional[Dict[str, Any]]:
        """
        Get Wikipedia page summary.
        
        Args:
            title: Wikipedia page title
            sentences: Number of sentences in summary
            
        Returns:
            Dictionary with title, summary, and URL
        """
        try:
            page = self.wiki.page(title)
            
            if not page.exists():
                logger.warning(f"Wikipedia page '{title}' does not exist")
                return None
            
            # Get summary (first N sentences)
            summary = page.summary
            if sentences > 0:
                summary_sentences = summary.split('. ')[:sentences]
                summary = '. '.join(summary_sentences)
                if not summary.endswith('.'):
                    summary += '.'
            
            result = {
                'title': page.title,
                'summary': summary,
                'url': page.fullurl,
                'exists': True
            }
            
            logger.info(f"Retrieved Wikipedia summary for '{title}'")
            return result
            
        except Exception as e:
            logger.error(f"Failed to get Wikipedia summary for '{title}': {e}")
            return None
    
    def get_wikipedia_content(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Get full Wikipedia page content.
        
        Args:
            title: Wikipedia page title
            
        Returns:
            Dictionary with title, content, sections, and URL
        """
        try:
            page = self.wiki.page(title)
            
            if not page.exists():
                logger.warning(f"Wikipedia page '{title}' does not exist")
                return None
            
            # Get sections
            sections = []
            for section in page.sections:
                sections.append({
                    'title': section.title,
                    'text': section.text[:500] + '...' if len(section.text) > 500 else section.text
                })
            
            result = {
                'title': page.title,
                'summary': page.summary,
                'content': page.text[:2000] + '...' if len(page.text) > 2000 else page.text,
                'sections': sections[:5],  # First 5 sections
                'url': page.fullurl,
                'categories': list(page.categories.keys())[:10],
                'links': list(page.links.keys())[:20]
            }
            
            logger.info(f"Retrieved full Wikipedia content for '{title}'")
            return result
            
        except Exception as e:
            logger.error(f"Failed to get Wikipedia content for '{title}': {e}")
            return None
    
    # Web Scraping Functions
    
    async def scrape_url(self, url: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
        """
        Scrape content from a URL.
        
        Args:
            url: URL to scrape
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary with title, text, and metadata
        """
        try:
            session = await self._get_session()
            
            async with session.get(url, timeout=timeout) as response:
                if response.status != 200:
                    logger.warning(f"Failed to fetch {url}: HTTP {response.status}")
                    return None
                
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                
                # Extract title
                title = soup.find('title')
                title_text = title.get_text().strip() if title else urlparse(url).netloc
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                # Get text
                text = soup.get_text()
                
                # Clean up text
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                # Limit text length
                if len(text) > 5000:
                    text = text[:5000] + '...'
                
                # Extract metadata
                meta_description = soup.find('meta', attrs={'name': 'description'})
                description = meta_description['content'] if meta_description and 'content' in meta_description.attrs else ''
                
                result = {
                    'url': url,
                    'title': title_text,
                    'text': text,
                    'description': description,
                    'word_count': len(text.split()),
                    'success': True
                }
                
                logger.info(f"Successfully scraped {url}")
                return result
                
        except asyncio.TimeoutError:
            logger.error(f"Timeout scraping {url}")
            return {'url': url, 'error': 'timeout', 'success': False}
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return {'url': url, 'error': str(e), 'success': False}
    
    def scrape_url_sync(self, url: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
        """
        Synchronous version of scrape_url.
        
        Args:
            url: URL to scrape
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary with title, text, and metadata
        """
        try:
            response = requests.get(
                url,
                headers={'User-Agent': self.user_agent},
                timeout=timeout
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else urlparse(url).netloc
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit text length
            if len(text) > 5000:
                text = text[:5000] + '...'
            
            # Extract metadata
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description['content'] if meta_description and 'content' in meta_description.attrs else ''
            
            result = {
                'url': url,
                'title': title_text,
                'text': text,
                'description': description,
                'word_count': len(text.split()),
                'success': True
            }
            
            logger.info(f"Successfully scraped {url} (sync)")
            return result
            
        except requests.Timeout:
            logger.error(f"Timeout scraping {url}")
            return {'url': url, 'error': 'timeout', 'success': False}
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return {'url': url, 'error': str(e), 'success': False}
    
    async def scrape_multiple_urls(self, urls: List[str], timeout: int = 10) -> List[Dict[str, Any]]:
        """
        Scrape multiple URLs concurrently.
        
        Args:
            urls: List of URLs to scrape
            timeout: Request timeout in seconds
            
        Returns:
            List of scraping results
        """
        tasks = [self.scrape_url(url, timeout) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        valid_results = []
        for result in results:
            if isinstance(result, dict):
                valid_results.append(result)
            else:
                logger.error(f"Exception in scraping: {result}")
        
        return valid_results
    
    # Combined Search Functions
    
    def search_and_summarize(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Search Wikipedia and return summary of best match.
        
        Args:
            query: Search query
            
        Returns:
            Dictionary with search results and best match summary
        """
        try:
            # Search for pages
            titles = self.search_wikipedia(query, results=5)
            
            if not titles:
                return {
                    'query': query,
                    'found': False,
                    'message': 'No Wikipedia pages found'
                }
            
            # Get summary of first result
            summary = self.get_wikipedia_summary(titles[0])
            
            result = {
                'query': query,
                'found': True,
                'search_results': titles,
                'best_match': summary,
                'alternative_titles': titles[1:] if len(titles) > 1 else []
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Search and summarize failed: {e}")
            return {
                'query': query,
                'found': False,
                'error': str(e)
            }


# Global instance
_web_scraping_wikipedia = None

def get_web_scraping_wikipedia() -> WebScrapingWikipedia:
    """Get global WebScrapingWikipedia instance."""
    global _web_scraping_wikipedia
    if _web_scraping_wikipedia is None:
        _web_scraping_wikipedia = WebScrapingWikipedia()
    return _web_scraping_wikipedia
