"""
Image Analysis Provider Abstraction
Supports multiple backends: offline analyzer, WebAI-to-API fallback

Author: Manus AI for rabit232/ribit.2.0
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
from PIL import Image

logger = logging.getLogger(__name__)


class ImageAnalysisProvider(ABC):
    """Abstract base class for image analysis providers."""
    
    @abstractmethod
    async def analyze_image(self, image: Image.Image) -> Dict[str, Any]:
        """
        Analyze an image and return structured results.
        
        Args:
            image: PIL Image object to analyze
            
        Returns:
            Dictionary with analysis results including:
            - description: Text description
            - colors: Color analysis
            - features: Detected features
            - shapes: Shape analysis
            - composition: Composition analysis
            - error: Error message if analysis failed
        """
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if this provider is available and healthy."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the provider name for logging."""
        pass


class OfflineImageProvider(ImageAnalysisProvider):
    """Offline image analysis using local ML models."""
    
    def __init__(self, analyzer):
        """Initialize with an offline image analyzer instance."""
        self.analyzer = analyzer
        self.name = "Offline Analyzer"
    
    async def analyze_image(self, image: Image.Image) -> Dict[str, Any]:
        """Run offline image analysis in a thread pool to avoid blocking."""
        import asyncio
        
        try:
            if not self.analyzer:
                return {
                    'error': 'Offline analyzer not initialized',
                    'description': 'Image analysis unavailable'
                }
            
            result = await asyncio.to_thread(self.analyzer.analyze_image, image)
            
            if not result or 'error' in result:
                return {
                    'error': result.get('error', 'Analysis failed'),
                    'description': result.get('description', 'Could not analyze image')
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Offline analysis failed: {e}")
            return {
                'error': str(e),
                'description': 'Offline analysis encountered an error'
            }
    
    async def is_available(self) -> bool:
        """Offline analyzer is always available if initialized."""
        return self.analyzer is not None
    
    def get_name(self) -> str:
        return self.name


class WebAIImageProvider(ImageAnalysisProvider):
    """Fallback image analysis using WebAI-to-API service (Gemini/ChatGPT/Claude)."""
    
    def __init__(self, api_url: str = "http://localhost:5000", model: str = "gemini-pro-vision", timeout: int = 30):
        """
        Initialize WebAI image provider.
        
        Args:
            api_url: Base URL of WebAI-to-API service
            model: Model to use (gemini-pro-vision, gpt-4-vision, etc.)
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip('/')
        self.model = model
        self.timeout = timeout
        self.name = f"WebAI ({model})"
        self.available = False
    
    async def analyze_image(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze image using WebAI-to-API service."""
        import aiohttp
        import base64
        import io
        
        try:
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this image and describe:\n1. Main colors (top 3)\n2. What objects/subjects are present\n3. If there are people\n4. If it's a nature scene\n5. If there's text visible\n6. Overall composition and mood\n\nProvide a natural, conversational description."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 500
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/v1/chat/completions",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        description = result.get('choices', [{}])[0].get('message', {}).get('content', 'No description available')
                        
                        return {
                            'description': description,
                            'colors': {},
                            'features': {},
                            'shapes': {},
                            'composition': {},
                            'provider': self.name
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"WebAI API error {response.status}: {error_text}")
                        return {
                            'error': f'API returned status {response.status}',
                            'description': 'Could not analyze image via WebAI'
                        }
                        
        except Exception as e:
            logger.error(f"WebAI analysis failed: {e}")
            return {
                'error': str(e),
                'description': 'WebAI analysis encountered an error'
            }
    
    async def is_available(self) -> bool:
        """Check if WebAI-to-API service is reachable."""
        import aiohttp
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/v1/models",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    self.available = response.status == 200
                    return self.available
        except Exception as e:
            logger.debug(f"WebAI service not available: {e}")
            self.available = False
            return False
    
    def get_name(self) -> str:
        return self.name


class FallbackImageProvider(ImageAnalysisProvider):
    """Composite provider that tries multiple providers in order."""
    
    def __init__(self, providers: list):
        """
        Initialize fallback provider with ordered list of providers.
        
        Args:
            providers: List of ImageAnalysisProvider instances to try in order
        """
        self.providers = providers
        self.name = "Fallback Provider"
    
    async def analyze_image(self, image: Image.Image) -> Dict[str, Any]:
        """Try each provider in order until one succeeds."""
        errors = []
        
        for provider in self.providers:
            try:
                if not await provider.is_available():
                    logger.debug(f"{provider.get_name()} is not available, skipping")
                    continue
                
                logger.info(f"Trying image analysis with {provider.get_name()}")
                result = await provider.analyze_image(image)
                
                if result and 'error' not in result:
                    logger.info(f"✅ Image analyzed successfully by {provider.get_name()}")
                    return result
                else:
                    error_msg = result.get('error', 'Unknown error')
                    errors.append(f"{provider.get_name()}: {error_msg}")
                    logger.warning(f"{provider.get_name()} failed: {error_msg}")
                    
            except Exception as e:
                error_msg = str(e)
                errors.append(f"{provider.get_name()}: {error_msg}")
                logger.error(f"{provider.get_name()} crashed: {e}")
        
        return {
            'error': '; '.join(errors),
            'description': f'All {len(self.providers)} providers failed to analyze the image'
        }
    
    async def is_available(self) -> bool:
        """At least one provider must be available."""
        for provider in self.providers:
            if await provider.is_available():
                return True
        return False
    
    def get_name(self) -> str:
        provider_names = [p.get_name() for p in self.providers]
        return f"Fallback ({' → '.join(provider_names)})"
