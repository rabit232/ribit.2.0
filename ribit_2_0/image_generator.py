"""
AI Image Generator for Ribit 2.0
Uses Perchance AI image generator to create images from text descriptions
"""

import os
import time
import logging
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Generate AI images using Perchance text-to-image generator"""
    
    def __init__(self):
        self.generator_url = "https://perchance.org/ai-text-to-image-generator"
        self.download_dir = Path.home() / "ribit_generated_images"
        self.download_dir.mkdir(exist_ok=True)
        
    async def generate_image(self, description: str, style: str = "default") -> Dict[str, Any]:
        """
        Generate an AI image from text description
        
        Args:
            description: Text description of the image to generate
            style: Art style (default, anime, photorealistic, etc.)
            
        Returns:
            Dict with success status, file path, and any errors
        """
        try:
            logger.info(f"Generating image for: {description}")
            
            # Import selenium for browser automation
            try:
                from selenium import webdriver
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.common.keys import Keys
            except ImportError:
                return {
                    'success': False,
                    'error': 'Selenium not installed. Install with: pip install selenium',
                    'file_path': None
                }
            
            # Set up headless Chrome
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            
            # Set download directory
            prefs = {
                "download.default_directory": str(self.download_dir),
                "download.prompt_for_download": False,
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            driver = None
            try:
                # Start browser
                driver = webdriver.Chrome(options=chrome_options)
                driver.set_page_load_timeout(30)
                
                logger.info(f"Opening {self.generator_url}")
                driver.get(self.generator_url)
                
                # Wait for page to load
                await asyncio.sleep(3)
                
                # Find the description text area
                logger.info("Finding description input field")
                description_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[placeholder*='description'], textarea[placeholder*='Description'], #description, .description-input"))
                )
                
                # Clear and enter description
                description_field.clear()
                description_field.send_keys(description)
                logger.info(f"Entered description: {description}")
                
                await asyncio.sleep(1)
                
                # Find and click generate button
                logger.info("Looking for generate button")
                generate_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'GENERATE', 'generate'), 'generate')]"))
                )
                
                generate_button.click()
                logger.info("Clicked generate button")
                
                # Wait for image to be generated (this may take a while)
                logger.info("Waiting for image generation...")
                await asyncio.sleep(15)  # Give it time to generate
                
                # Try to find the generated image
                logger.info("Looking for generated image")
                try:
                    # Look for image element
                    image_element = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "img.generated-image, .output-image img, .result-image img, img[src*='blob:'], img[src*='data:image']"))
                    )
                    
                    # Get image source
                    image_src = image_element.get_attribute('src')
                    logger.info(f"Found image: {image_src[:100]}...")
                    
                    # Download the image
                    if image_src.startswith('data:image'):
                        # Handle base64 encoded image
                        import base64
                        import re
                        
                        # Extract base64 data
                        match = re.match(r'data:image/(\w+);base64,(.+)', image_src)
                        if match:
                            image_format = match.group(1)
                            image_data = base64.b64decode(match.group(2))
                            
                            # Save to file
                            filename = f"generated_{int(time.time())}.{image_format}"
                            file_path = self.download_dir / filename
                            
                            with open(file_path, 'wb') as f:
                                f.write(image_data)
                            
                            logger.info(f"Saved image to: {file_path}")
                            
                            return {
                                'success': True,
                                'file_path': str(file_path),
                                'description': description,
                                'error': None
                            }
                    
                    elif image_src.startswith('http'):
                        # Download from URL
                        import requests
                        
                        response = requests.get(image_src, timeout=30)
                        if response.status_code == 200:
                            # Determine file extension from content type
                            content_type = response.headers.get('content-type', '')
                            ext = 'png'
                            if 'jpeg' in content_type or 'jpg' in content_type:
                                ext = 'jpg'
                            elif 'webp' in content_type:
                                ext = 'webp'
                            
                            filename = f"generated_{int(time.time())}.{ext}"
                            file_path = self.download_dir / filename
                            
                            with open(file_path, 'wb') as f:
                                f.write(response.content)
                            
                            logger.info(f"Downloaded image to: {file_path}")
                            
                            return {
                                'success': True,
                                'file_path': str(file_path),
                                'description': description,
                                'error': None
                            }
                    
                    # Try right-click download approach
                    logger.info("Trying alternative download method...")
                    
                    # Look for download button
                    try:
                        download_button = driver.find_element(By.XPATH, "//button[contains(translate(., 'DOWNLOAD', 'download'), 'download')] | //a[contains(translate(., 'DOWNLOAD', 'download'), 'download')]")
                        download_button.click()
                        logger.info("Clicked download button")
                        
                        # Wait for download
                        await asyncio.sleep(5)
                        
                        # Find the downloaded file
                        files = list(self.download_dir.glob("*"))
                        if files:
                            # Get most recent file
                            latest_file = max(files, key=lambda p: p.stat().st_mtime)
                            logger.info(f"Found downloaded file: {latest_file}")
                            
                            return {
                                'success': True,
                                'file_path': str(latest_file),
                                'description': description,
                                'error': None
                            }
                    except Exception as e:
                        logger.debug(f"Download button not found: {e}")
                    
                    return {
                        'success': False,
                        'error': 'Could not download generated image',
                        'file_path': None
                    }
                    
                except Exception as e:
                    logger.error(f"Error finding/downloading image: {e}")
                    return {
                        'success': False,
                        'error': f'Could not find generated image: {str(e)}',
                        'file_path': None
                    }
                
            finally:
                if driver:
                    driver.quit()
                    logger.info("Browser closed")
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return {
                'success': False,
                'error': str(e),
                'file_path': None
            }
    
    def cleanup_image(self, file_path: str) -> bool:
        """
        Delete the generated image file to save space
        
        Args:
            file_path: Path to the image file
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted image: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting image: {e}")
            return False
    
    def cleanup_old_images(self, max_age_hours: int = 24):
        """
        Clean up old generated images
        
        Args:
            max_age_hours: Delete images older than this many hours
        """
        try:
            now = time.time()
            max_age_seconds = max_age_hours * 3600
            
            for file_path in self.download_dir.glob("*"):
                if file_path.is_file():
                    age = now - file_path.stat().st_mtime
                    if age > max_age_seconds:
                        file_path.unlink()
                        logger.info(f"Cleaned up old image: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up old images: {e}")
    
    def is_image_generation_request(self, text: str) -> bool:
        """Check if the text is requesting image generation"""
        text_lower = text.lower()
        
        keywords = [
            'generate image',
            'create image',
            'make image',
            'draw image',
            'generate picture',
            'create picture',
            'make picture',
            'draw picture',
            'generate art',
            'create art',
            'make art',
            'ai image',
            'ai art',
            'text to image',
            'image of',
            'picture of',
        ]
        
        return any(keyword in text_lower for keyword in keywords)
    
    def extract_description(self, text: str) -> str:
        """Extract the image description from the request text"""
        text_lower = text.lower()
        
        # Remove common command phrases
        for phrase in ['generate image of', 'create image of', 'make image of', 
                      'draw image of', 'generate picture of', 'create picture of',
                      'make picture of', 'generate art of', 'create art of',
                      'ai image of', 'ai art of', 'image of', 'picture of']:
            if phrase in text_lower:
                # Find the phrase and return everything after it
                idx = text_lower.index(phrase) + len(phrase)
                return text[idx:].strip()
        
        # If no specific phrase found, return the whole text
        return text.strip()

