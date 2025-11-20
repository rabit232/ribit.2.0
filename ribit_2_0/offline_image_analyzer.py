"""
Offline Image Analyzer for Ribit 2.0
Analyzes images without requiring external APIs - fully offline

Features:
- Color detection and dominant colors
- Shape detection (edges, contours)
- Text region detection (basic OCR-like functionality)
- Object pose estimation
- Scene composition analysis
"""

import logging
import numpy as np
from PIL import Image, ImageStat, ImageFilter, ImageDraw
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import io

logger = logging.getLogger(__name__)

class OfflineImageAnalyzer:
    """
    Analyze images offline using computer vision techniques.
    No external APIs required - perfect for privacy and offline use.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Offline Image Analyzer initialized")
    
    def analyze_image(self, image_path_or_bytes: Any) -> Dict[str, Any]:
        """
        Comprehensive image analysis
        
        Args:
            image_path_or_bytes: Path to image file or bytes object
            
        Returns:
            Dictionary with complete analysis results
        """
        try:
            # Load image
            if isinstance(image_path_or_bytes, (str, Path)):
                image = Image.open(image_path_or_bytes)
            elif isinstance(image_path_or_bytes, bytes):
                image = Image.open(io.BytesIO(image_path_or_bytes))
            else:
                image = image_path_or_bytes
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Perform various analyses
            analysis = {
                'basic_info': self._get_basic_info(image),
                'colors': self._analyze_colors(image),
                'shapes': self._detect_shapes(image),
                'text_regions': self._detect_text_regions(image),
                'composition': self._analyze_composition(image),
                'features': self._detect_features(image)
            }
            
            # Generate natural language description
            analysis['description'] = self._generate_description(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Image analysis failed: {e}")
            return {'error': str(e), 'description': 'Unable to analyze image'}
    
    def _get_basic_info(self, image: Image.Image) -> Dict[str, Any]:
        """Get basic image information"""
        return {
            'width': image.width,
            'height': image.height,
            'mode': image.mode,
            'format': image.format or 'Unknown',
            'aspect_ratio': round(image.width / image.height, 2) if image.height > 0 else 0
        }
    
    def _analyze_colors(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze colors in the image"""
        try:
            # Get dominant colors by downsampling and quantizing
            small_image = image.resize((150, 150), Image.Resampling.LANCZOS)
            
            # Convert to RGB numpy array
            img_array = np.array(small_image)
            pixels = img_array.reshape(-1, 3)
            
            # Get statistics
            stats = ImageStat.Stat(image)
            
            # Calculate dominant colors using simple clustering
            dominant_colors = self._get_dominant_colors(pixels, n_colors=5)
            
            # Determine overall brightness
            brightness = sum(stats.mean) / 3
            
            # Determine overall tone
            if brightness > 200:
                tone = "very bright"
            elif brightness > 150:
                tone = "bright"
            elif brightness > 100:
                tone = "moderate"
            elif brightness > 50:
                tone = "dark"
            else:
                tone = "very dark"
            
            return {
                'dominant_colors': dominant_colors,
                'average_color': [int(c) for c in stats.mean],
                'brightness': round(brightness, 2),
                'tone': tone,
                'color_variance': round(sum(stats.stddev) / 3, 2)
            }
            
        except Exception as e:
            self.logger.error(f"Color analysis failed: {e}")
            return {'dominant_colors': [], 'tone': 'unknown'}
    
    def _get_dominant_colors(self, pixels: np.ndarray, n_colors: int = 5) -> List[Dict[str, Any]]:
        """Extract dominant colors using simple clustering"""
        try:
            from collections import Counter
            
            # Quantize colors to reduce complexity
            quantized = (pixels // 32) * 32
            
            # Count colors
            colors_list = [tuple(color) for color in quantized]
            color_counts = Counter(colors_list)
            
            # Get top colors
            dominant = []
            total_pixels = len(pixels)
            if total_pixels == 0:
                return []
            
            for color, count in color_counts.most_common(n_colors):
                rgb = color
                color_name = self._rgb_to_name(rgb)
                percentage = (count / total_pixels) * 100
                
                dominant.append({
                    'rgb': list(rgb),
                    'name': color_name,
                    'percentage': round(percentage, 1)
                })
            
            return dominant
            
        except Exception as e:
            self.logger.error(f"Dominant color extraction failed: {e}")
            return []
    
    def _rgb_to_name(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB to approximate color name"""
        # Cast to Python ints to avoid uint8 overflow
        r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
        
        # Simple color naming based on RGB values
        if r > 200 and g > 200 and b > 200:
            return "white"
        elif r < 50 and g < 50 and b < 50:
            return "black"
        elif r < 100 and g < 100 and b < 100:
            return "gray"
        elif r > g + 50 and r > b + 50:
            if r > 150:
                return "red"
            else:
                return "dark red"
        elif g > r + 50 and g > b + 50:
            if g > 150:
                return "green"
            else:
                return "dark green"
        elif b > r + 50 and b > g + 50:
            if b > 150:
                return "blue"
            else:
                return "dark blue"
        elif r > 150 and g > 150 and b < 100:
            return "yellow"
        elif r > 150 and g < 100 and b > 150:
            return "magenta"
        elif r < 100 and g > 150 and b > 150:
            return "cyan"
        elif r > 150 and g > 100 and b < 100:
            return "orange"
        elif r > 100 and g < 100 and b > 100:
            return "purple"
        elif r > 100 and g > 100 and b < 50:
            return "brown"
        else:
            return "mixed color"
    
    def _detect_shapes(self, image: Image.Image) -> Dict[str, Any]:
        """Detect basic shapes in the image"""
        try:
            # Convert to grayscale for edge detection
            gray = image.convert('L')
            
            # Apply edge detection
            edges = gray.filter(ImageFilter.FIND_EDGES)
            
            # Get edge statistics
            edge_array = np.array(edges)
            edge_density = np.mean(edge_array > 30)
            
            # Determine shape complexity
            if edge_density > 0.3:
                complexity = "very complex"
                shape_count = "many shapes"
            elif edge_density > 0.2:
                complexity = "complex"
                shape_count = "several shapes"
            elif edge_density > 0.1:
                complexity = "moderate"
                shape_count = "some shapes"
            else:
                complexity = "simple"
                shape_count = "few shapes"
            
            # Detect lines vs curves
            sobel_h = gray.filter(ImageFilter.Kernel((3, 3), [-1, 0, 1, -2, 0, 2, -1, 0, 1]))
            sobel_v = gray.filter(ImageFilter.Kernel((3, 3), [-1, -2, -1, 0, 0, 0, 1, 2, 1]))
            
            sobel_h_array = np.array(sobel_h)
            sobel_v_array = np.array(sobel_v)
            
            h_lines = np.mean(sobel_h_array > 50)
            v_lines = np.mean(sobel_v_array > 50)
            
            if h_lines > 0.1 or v_lines > 0.1:
                line_presence = "contains straight lines"
            else:
                line_presence = "contains curves"
            
            return {
                'edge_density': round(edge_density, 3),
                'complexity': complexity,
                'shape_count': shape_count,
                'line_presence': line_presence,
                'has_geometric_shapes': edge_density > 0.15
            }
            
        except Exception as e:
            self.logger.error(f"Shape detection failed: {e}")
            return {'complexity': 'unknown'}
    
    def _detect_text_regions(self, image: Image.Image) -> Dict[str, Any]:
        """Detect regions that might contain text"""
        try:
            # Convert to grayscale
            gray = image.convert('L')
            
            # Apply contrast enhancement
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(gray)
            enhanced = enhancer.enhance(2.0)
            
            # Convert to numpy array
            img_array = np.array(enhanced)
            
            # Detect high-contrast regions (potential text)
            # Text usually has sharp transitions
            threshold = 128
            binary = (img_array > threshold).astype(np.uint8) * 255
            
            # Count transitions (potential characters)
            h_transitions = np.sum(np.abs(np.diff(binary, axis=1)) > 0)
            v_transitions = np.sum(np.abs(np.diff(binary, axis=0)) > 0)
            
            total_pixels = image.width * image.height
            if total_pixels == 0:
                raise ValueError("Invalid image dimensions")
            transition_density = (h_transitions + v_transitions) / total_pixels
            
            # Estimate text presence
            if transition_density > 0.1:
                text_likelihood = "high"
                contains_text = True
            elif transition_density > 0.05:
                text_likelihood = "moderate"
                contains_text = True
            elif transition_density > 0.02:
                text_likelihood = "low"
                contains_text = False
            else:
                text_likelihood = "very low"
                contains_text = False
            
            return {
                'transition_density': round(transition_density, 4),
                'text_likelihood': text_likelihood,
                'contains_text': contains_text,
                'note': 'Basic text detection - for accurate OCR, install pytesseract'
            }
            
        except Exception as e:
            self.logger.error(f"Text detection failed: {e}")
            return {'contains_text': False}
    
    def _analyze_composition(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze image composition"""
        try:
            # Get brightness distribution
            gray = image.convert('L')
            histogram = gray.histogram()
            
            # Find where most of the content is (rule of thirds approximation)
            img_array = np.array(gray)
            h, w = img_array.shape
            
            # Divide into thirds
            top_third = img_array[:h//3, :]
            middle_third = img_array[h//3:2*h//3, :]
            bottom_third = img_array[2*h//3:, :]
            
            left_third = img_array[:, :w//3]
            center_third = img_array[:, w//3:2*w//3]
            right_third = img_array[:, 2*w//3:]
            
            # Calculate variance in each region (higher = more detail/interest)
            regions = {
                'top': np.var(top_third),
                'middle': np.var(middle_third),
                'bottom': np.var(bottom_third),
                'left': np.var(left_third),
                'center': np.var(center_third),
                'right': np.var(right_third)
            }
            
            # Find region of interest
            v_focus = max(regions, key=lambda k: regions[k] if k in ['top', 'middle', 'bottom'] else 0)
            h_focus = max(regions, key=lambda k: regions[k] if k in ['left', 'center', 'right'] else 0)
            
            return {
                'vertical_focus': v_focus,
                'horizontal_focus': h_focus,
                'focus_description': f"{v_focus} {h_focus}",
                'balanced': abs(regions['left'] - regions['right']) < regions['center'] * 0.3
            }
            
        except Exception as e:
            self.logger.error(f"Composition analysis failed: {e}")
            return {'focus_description': 'unknown'}
    
    def _detect_features(self, image: Image.Image) -> Dict[str, Any]:
        """Detect various image features"""
        try:
            features = {}
            
            # Check for human-like shapes (basic skin tone detection)
            img_array = np.array(image)
            pixels = img_array.reshape(-1, 3)
            
            if len(pixels) == 0:
                return {}
            
            # Skin tone range (very basic)
            skin_pixels = np.sum(
                (pixels[:, 0] > 95) & (pixels[:, 0] < 255) &
                (pixels[:, 1] > 40) & (pixels[:, 1] < 220) &
                (pixels[:, 2] > 20) & (pixels[:, 2] < 200) &
                (pixels[:, 0] > pixels[:, 1]) &
                (pixels[:, 0] > pixels[:, 2])
            )
            skin_percentage = (skin_pixels / len(pixels)) * 100
            
            features['likely_contains_people'] = skin_percentage > 5
            features['skin_tone_percentage'] = round(skin_percentage, 2)
            
            # Check for nature (green dominance)
            green_pixels = np.sum(pixels[:, 1] > (pixels[:, 0] + 20)) + np.sum(pixels[:, 1] > (pixels[:, 2] + 20))
            green_percentage = (green_pixels / (len(pixels) * 2)) * 100
            
            features['likely_nature_scene'] = green_percentage > 15
            features['vegetation_percentage'] = round(green_percentage, 2)
            
            # Check for sky (blue in upper portion)
            upper_pixels = img_array[:img_array.shape[0]//3, :, :].reshape(-1, 3)
            if len(upper_pixels) > 0:
                blue_upper = np.sum(upper_pixels[:, 2] > 150)
                features['likely_has_sky'] = (blue_upper / len(upper_pixels)) > 0.3
            else:
                features['likely_has_sky'] = False
            
            return features
            
        except Exception as e:
            self.logger.error(f"Feature detection failed: {e}")
            return {}
    
    def _generate_description(self, analysis: Dict[str, Any]) -> str:
        """Generate natural language description from analysis"""
        try:
            parts = []
            
            # Basic info
            basic = analysis.get('basic_info', {})
            width = basic.get('width', 0)
            height = basic.get('height', 0)
            aspect = basic.get('aspect_ratio', 1.0)
            
            # Fix orientation detection - use more accurate thresholds
            if aspect > 1.3:
                orientation = "wide landscape"
            elif aspect < 0.8:
                orientation = "tall portrait"
            elif 0.95 <= aspect <= 1.05:
                orientation = "square"
            else:
                orientation = "rectangular"
            
            parts.append(f"This is a {orientation} image ({width}x{height} pixels)")
            
            # Colors
            colors = analysis.get('colors', {})
            tone = colors.get('tone', 'moderate')
            dominant = colors.get('dominant_colors', [])
            
            if dominant:
                color_names = [c['name'] for c in dominant[:3]]
                parts.append(f"with {tone} tones featuring {', '.join(color_names)} colors")
            
            # Composition
            comp = analysis.get('composition', {})
            focus = comp.get('focus_description', '')
            if focus:
                parts.append(f"The main content appears in the {focus} region")
            
            # Shapes
            shapes = analysis.get('shapes', {})
            complexity = shapes.get('complexity', '')
            line_presence = shapes.get('line_presence', '')
            if complexity:
                parts.append(f"The image has a {complexity} composition {line_presence}")
            
            # Text
            text_info = analysis.get('text_regions', {})
            if text_info.get('contains_text'):
                parts.append("There appear to be text regions visible")
            
            # Features
            features = analysis.get('features', {})
            if features.get('likely_contains_people'):
                parts.append("It likely contains people or human figures")
            if features.get('likely_nature_scene'):
                parts.append("It appears to be a nature or outdoor scene")
            if features.get('likely_has_sky'):
                parts.append("with visible sky")
            
            description = ". ".join(parts) + "."
            
            return description
            
        except Exception as e:
            self.logger.error(f"Description generation failed: {e}")
            return "Image analyzed but description generation failed"
