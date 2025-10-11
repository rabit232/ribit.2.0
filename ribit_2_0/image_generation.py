"""
Image Generation Module for Ribit 2.0

Provides image generation capabilities using various APIs.
"""

import logging
import os
import requests
import base64
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class ImageGeneration:
    """Image generation using various APIs."""
    
    def __init__(self):
        self.output_dir = Path("generated_images")
        self.output_dir.mkdir(exist_ok=True)
        logger.info("Image Generation module initialized")
    
    def generate_image_placeholder(
        self,
        prompt: str,
        width: int = 512,
        height: int = 512,
        filename: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate a placeholder image (for testing).
        
        In production, this would call an actual image generation API.
        
        Args:
            prompt: Text prompt for image generation
            width: Image width
            height: Image height
            filename: Optional output filename
            
        Returns:
            Path to generated image or None
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a simple placeholder image
            img = Image.new('RGB', (width, height), color=(73, 109, 137))
            draw = ImageDraw.Draw(img)
            
            # Add text
            text = f"Generated:\n{prompt[:50]}"
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((width - text_width) / 2, (height - text_height) / 2)
            
            draw.text(position, text, fill=(255, 255, 255), font=font)
            
            # Save image
            if filename is None:
                import hashlib
                filename = f"img_{hashlib.md5(prompt.encode()).hexdigest()[:8]}.png"
            
            filepath = self.output_dir / filename
            img.save(filepath)
            
            logger.info(f"Generated placeholder image: {filepath}")
            return str(filepath)
            
        except ImportError:
            logger.error("PIL/Pillow not installed. Install with: pip install Pillow")
            return None
        except Exception as e:
            logger.error(f"Failed to generate placeholder image: {e}")
            return None
    
    def generate_with_dalle(
        self,
        prompt: str,
        api_key: Optional[str] = None,
        size: str = "512x512",
        n: int = 1
    ) -> Optional[Dict[str, Any]]:
        """
        Generate image using DALL-E API.
        
        Args:
            prompt: Text prompt
            api_key: OpenAI API key
            size: Image size (256x256, 512x512, 1024x1024)
            n: Number of images
            
        Returns:
            Dictionary with image URLs and metadata
        """
        try:
            if api_key is None:
                api_key = os.getenv("OPENAI_API_KEY")
            
            if not api_key:
                logger.warning("No OpenAI API key provided")
                return None
            
            url = "https://api.openai.com/v1/images/generations"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "prompt": prompt,
                "n": n,
                "size": size
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Generated {n} image(s) with DALL-E")
            return result
            
        except Exception as e:
            logger.error(f"DALL-E generation failed: {e}")
            return None
    
    def generate_with_stability(
        self,
        prompt: str,
        api_key: Optional[str] = None,
        width: int = 512,
        height: int = 512
    ) -> Optional[str]:
        """
        Generate image using Stability AI API.
        
        Args:
            prompt: Text prompt
            api_key: Stability AI API key
            width: Image width
            height: Image height
            
        Returns:
            Path to generated image or None
        """
        try:
            if api_key is None:
                api_key = os.getenv("STABILITY_API_KEY")
            
            if not api_key:
                logger.warning("No Stability AI API key provided")
                return None
            
            url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            data = {
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "height": height,
                "width": width,
                "samples": 1,
                "steps": 30
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            # Save the first image
            if result.get("artifacts"):
                image_data = base64.b64decode(result["artifacts"][0]["base64"])
                
                import hashlib
                filename = f"stability_{hashlib.md5(prompt.encode()).hexdigest()[:8]}.png"
                filepath = self.output_dir / filename
                
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                logger.info(f"Generated image with Stability AI: {filepath}")
                return str(filepath)
            
            return None
            
        except Exception as e:
            logger.error(f"Stability AI generation failed: {e}")
            return None
    
    def generate_image(
        self,
        prompt: str,
        method: str = "placeholder",
        **kwargs
    ) -> Optional[str]:
        """
        Generate image using specified method.
        
        Args:
            prompt: Text prompt
            method: Generation method (placeholder, dalle, stability)
            **kwargs: Additional arguments for specific method
            
        Returns:
            Path to generated image or None
        """
        logger.info(f"Generating image with method '{method}': {prompt}")
        
        if method == "placeholder":
            return self.generate_image_placeholder(prompt, **kwargs)
        elif method == "dalle":
            result = self.generate_with_dalle(prompt, **kwargs)
            if result and result.get("data"):
                # Download the image
                image_url = result["data"][0]["url"]
                return self._download_image(image_url, prompt)
            return None
        elif method == "stability":
            return self.generate_with_stability(prompt, **kwargs)
        else:
            logger.error(f"Unknown generation method: {method}")
            return None
    
    def _download_image(self, url: str, prompt: str) -> Optional[str]:
        """Download image from URL."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            import hashlib
            filename = f"downloaded_{hashlib.md5(prompt.encode()).hexdigest()[:8]}.png"
            filepath = self.output_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Downloaded image: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to download image: {e}")
            return None


# Global instance
_image_generation = None

def get_image_generation() -> ImageGeneration:
    """Get global ImageGeneration instance."""
    global _image_generation
    if _image_generation is None:
        _image_generation = ImageGeneration()
    return _image_generation
