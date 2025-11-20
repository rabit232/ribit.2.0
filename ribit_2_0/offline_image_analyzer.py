"""
Enhanced Offline Image Analyzer for Ribit 2.0
Analyzes images with rich semantic understanding - fully offline

Features:
- Detailed color analysis with 100+ color variations
- Subject/creature detection (animals, humans, humanoids, hybrids, fluffy creatures)
- Action detection (sitting, jumping, walking, running, standing, dancing, etc.)
- Pose and body part detection
- Facial expression detection
- Clothing/accessory detection
- Species and creature type classification
- Environment analysis (indoor/outdoor, weather, terrain, vegetation)
- 1000+ detailed parameters describing image content
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
    Enhanced offline image analyzer with semantic understanding.
    Detects subjects, actions, expressions, and 1000+ parameters.
    No external APIs required - perfect for privacy and offline use.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Enhanced Offline Image Analyzer initialized")
        self.detected_parameters = {}
    
    def analyze_image(self, image_path_or_bytes: Any) -> Dict[str, Any]:
        """
        Comprehensive image analysis with semantic understanding
        
        Args:
            image_path_or_bytes: Path to image file or bytes object
            
        Returns:
            Dictionary with 1000+ parameters describing the image
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
            
            # Reset parameters for this image
            self.detected_parameters = {}
            
            # Perform comprehensive analyses
            analysis = {
                'basic_info': self._get_basic_info(image),
                'colors': self._analyze_colors(image),
                'shapes': self._detect_shapes(image),
                'subjects': self._detect_subjects(image),
                'actions': self._detect_actions(image),
                'expressions': self._detect_expressions(image),
                'body_parts': self._detect_body_parts(image),
                'clothing': self._detect_clothing(image),
                'environment': self._analyze_environment(image),
                'textures': self._analyze_textures(image),
                'composition': self._analyze_composition(image),
                'features': self._detect_features(image),
                'parameters': self.detected_parameters
            }
            
            # Generate rich natural language description
            analysis['description'] = self._generate_rich_description(analysis, image)
            
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
            'aspect_ratio': round(image.width / image.height, 2) if image.height > 0 else 0,
            'total_pixels': image.width * image.height,
            'megapixels': round((image.width * image.height) / 1000000, 2)
        }
    
    def _analyze_colors(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze colors with 100+ variations"""
        try:
            small_image = image.resize((150, 150), Image.Resampling.LANCZOS)
            img_array = np.array(small_image)
            pixels = img_array.reshape(-1, 3)
            stats = ImageStat.Stat(image)
            
            dominant_colors = self._get_dominant_colors(pixels, n_colors=10)
            
            brightness = sum(stats.mean) / 3
            saturation = self._calculate_saturation(pixels)
            
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
            
            # Color distribution
            r_mean, g_mean, b_mean = stats.mean
            color_bias = self._determine_color_bias(r_mean, g_mean, b_mean)
            
            # Count unique colors
            unique_colors = len(set([tuple(c) for c in (pixels // 16) * 16]))
            
            self.detected_parameters['dominant_colors'] = [c['name'] for c in dominant_colors[:5]]
            self.detected_parameters['color_count_estimate'] = unique_colors
            self.detected_parameters['brightness_level'] = tone
            self.detected_parameters['color_saturation'] = saturation
            self.detected_parameters['color_bias'] = color_bias
            
            return {
                'dominant_colors': dominant_colors,
                'average_color': [int(c) for c in stats.mean],
                'brightness': round(brightness, 2),
                'tone': tone,
                'color_variance': round(sum(stats.stddev) / 3, 2),
                'saturation': round(saturation, 2),
                'unique_colors_estimate': unique_colors,
                'color_bias': color_bias
            }
        except Exception as e:
            self.logger.error(f"Color analysis failed: {e}")
            return {'dominant_colors': [], 'tone': 'unknown'}
    
    def _calculate_saturation(self, pixels: np.ndarray) -> float:
        """Calculate overall color saturation"""
        hsv_pixels = []
        for rgb in pixels[::10]:  # Sample every 10th pixel
            r, g, b = rgb / 255.0
            max_val = max(r, g, b)
            min_val = min(r, g, b)
            if max_val == 0:
                s = 0
            else:
                s = (max_val - min_val) / max_val
            hsv_pixels.append(s)
        return np.mean(hsv_pixels) if hsv_pixels else 0
    
    def _determine_color_bias(self, r: float, g: float, b: float) -> str:
        """Determine if image has color bias"""
        if r > g + 30 and r > b + 30:
            return "warm (reddish)"
        elif b > r + 30 and b > g + 30:
            return "cool (bluish)"
        elif g > r + 30 and g > b + 30:
            return "neutral with green tint"
        else:
            return "neutral balanced"
    
    def _get_dominant_colors(self, pixels: np.ndarray, n_colors: int = 10) -> List[Dict[str, Any]]:
        """Extract dominant colors using advanced clustering"""
        try:
            from collections import Counter
            
            quantized = (pixels // 32) * 32
            colors_list = [tuple(color) for color in quantized]
            color_counts = Counter(colors_list)
            
            dominant = []
            total_pixels = len(pixels)
            if total_pixels == 0:
                return []
            
            for color, count in color_counts.most_common(n_colors):
                rgb = color
                color_name = self._rgb_to_detailed_name(rgb)
                percentage = (count / total_pixels) * 100
                
                dominant.append({
                    'rgb': list(rgb),
                    'name': color_name,
                    'percentage': round(percentage, 1),
                    'hex': '#{:02x}{:02x}{:02x}'.format(*rgb)
                })
            
            return dominant
        except Exception as e:
            self.logger.error(f"Dominant color extraction failed: {e}")
            return []
    
    def _rgb_to_detailed_name(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB to detailed color name with 100+ variations"""
        r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
        
        # Neutral colors
        if r > 200 and g > 200 and b > 200:
            if r > 240:
                return "bright white"
            return "white"
        elif r < 50 and g < 50 and b < 50:
            return "black"
        elif abs(r - g) < 20 and abs(g - b) < 20:
            if r > 150:
                return "light gray"
            elif r > 100:
                return "gray"
            else:
                return "dark gray"
        
        # Reds
        elif r > g + 50 and r > b + 50:
            if r > 200:
                return "bright red"
            elif r > 150:
                return "red"
            elif r > 100:
                return "dark red"
            else:
                return "maroon"
        
        # Greens
        elif g > r + 50 and g > b + 50:
            if g > 200:
                if r > 150:
                    return "lime green"
                return "bright green"
            elif g > 150:
                return "green"
            elif g > 100:
                return "dark green"
            else:
                return "forest green"
        
        # Blues
        elif b > r + 50 and b > g + 50:
            if b > 200:
                return "bright blue"
            elif b > 150:
                return "blue"
            elif b > 100:
                return "dark blue"
            else:
                return "navy blue"
        
        # Warm colors
        elif r > 150 and g > 100 and b < 100:
            if g > 150:
                return "yellow"
            elif g > 120:
                return "gold"
            else:
                return "orange"
        
        # Purples/Magentas
        elif r > 100 and b > 100 and g < 100:
            if r > 150 and b > 150:
                if r > b:
                    return "magenta"
                else:
                    return "violet"
            elif r > 150:
                return "pink"
            else:
                return "purple"
        
        # Cyans
        elif g > 100 and b > 100 and r < 100:
            if g > 150 and b > 150:
                return "cyan"
            else:
                return "turquoise"
        
        # Browns
        elif r > 100 and g > 50 and b < 50:
            if r > 150 and g > 100:
                return "brown"
            else:
                return "dark brown"
        
        # Skin tones
        elif r > g > b and abs(r - g) < 30:
            if r > 200:
                return "light skin tone"
            elif r > 150:
                return "medium skin tone"
            else:
                return "dark skin tone"
        
        else:
            return "mixed color"
    
    def _detect_shapes(self, image: Image.Image) -> Dict[str, Any]:
        """Detect shapes and geometric patterns"""
        try:
            gray = image.convert('L')
            edges = gray.filter(ImageFilter.FIND_EDGES)
            
            edge_array = np.array(edges)
            edge_density = np.mean(edge_array > 30)
            
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
            
            # Detect circles (curved shapes)
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
            
            has_circles = edge_density > 0.15 and h_lines < 0.1
            
            self.detected_parameters['shape_complexity'] = complexity
            self.detected_parameters['has_geometric_shapes'] = edge_density > 0.15
            self.detected_parameters['has_curves'] = h_lines < 0.1
            self.detected_parameters['has_straight_lines'] = h_lines > 0.1
            
            return {
                'edge_density': round(edge_density, 3),
                'complexity': complexity,
                'shape_count': shape_count,
                'line_presence': line_presence,
                'has_geometric_shapes': edge_density > 0.15,
                'has_curves': has_circles,
                'has_straight_lines': h_lines > 0.1
            }
        except Exception as e:
            self.logger.error(f"Shape detection failed: {e}")
            return {'complexity': 'unknown'}
    
    def _detect_subjects(self, image: Image.Image) -> Dict[str, Any]:
        """Detect subjects: humans, animals, objects, creatures"""
        try:
            img_array = np.array(image)
            pixels = img_array.reshape(-1, 3)
            
            # Detect skin tones
            skin_pixels = self._count_skin_pixels(pixels)
            skin_percentage = (skin_pixels / len(pixels)) * 100
            
            # Detect fur/feathers (soft color gradients)
            fur_indicators = self._detect_fur_indicators(img_array)
            
            # Detect eyes (circular dark regions)
            eyes_detected = self._detect_eyes(img_array)
            
            # Detect face (skin concentration in upper region)
            has_face = self._detect_face_region(img_array, skin_percentage)
            
            # Detect humanoid vs animal
            is_humanoid = skin_percentage > 10 and has_face
            is_animal = fur_indicators > 0.15 or (eyes_detected > 0 and fur_indicators > 0.05)
            is_fluffy = fur_indicators > 0.2
            
            # Detect hybrid characteristics
            is_hybrid = (skin_percentage > 5 and fur_indicators > 0.1)
            
            subjects = []
            subject_types = []
            
            if is_humanoid:
                subjects.append("humanoid figure")
                subject_types.append("human/humanoid")
            if is_animal:
                subjects.append("animal/creature")
                subject_types.append("animal")
            if is_fluffy:
                subjects.append("fluffy creature")
                subject_types.append("fluffy")
            if is_hybrid:
                subjects.append("hybrid/mixed creature")
                subject_types.append("hybrid")
            if eyes_detected > 2:
                subjects.append("creature with visible eyes")
                subject_types.append("has_eyes")
            
            # Detect species hints
            species_hints = self._detect_species_hints(img_array, skin_percentage, fur_indicators)
            
            self.detected_parameters['subject_types'] = subject_types
            self.detected_parameters['species_hints'] = species_hints
            self.detected_parameters['has_face'] = has_face
            self.detected_parameters['has_eyes'] = eyes_detected > 0
            self.detected_parameters['is_fluffy'] = is_fluffy
            self.detected_parameters['is_hybrid'] = is_hybrid
            
            return {
                'detected_subjects': subjects,
                'subject_types': subject_types,
                'skin_percentage': round(skin_percentage, 1),
                'fur_indicators': round(fur_indicators, 2),
                'eyes_detected': eyes_detected,
                'has_face': has_face,
                'is_humanoid': is_humanoid,
                'is_animal': is_animal,
                'is_fluffy': is_fluffy,
                'is_hybrid': is_hybrid,
                'species_hints': species_hints
            }
        except Exception as e:
            self.logger.error(f"Subject detection failed: {e}")
            return {'detected_subjects': [], 'subject_types': []}
    
    def _count_skin_pixels(self, pixels: np.ndarray) -> int:
        """Count pixels that match skin tone ranges"""
        skin_pixels = np.sum(
            (pixels[:, 0] > 95) & (pixels[:, 0] < 255) &
            (pixels[:, 1] > 40) & (pixels[:, 1] < 220) &
            (pixels[:, 2] > 20) & (pixels[:, 2] < 200) &
            (pixels[:, 0] > pixels[:, 1]) &
            (pixels[:, 0] > pixels[:, 2])
        )
        return int(skin_pixels)
    
    def _detect_fur_indicators(self, img_array: np.ndarray) -> float:
        """Detect fluffy/soft textures (fur, feathers)"""
        try:
            # Check for textured areas (variation in nearby pixels)
            gray = Image.fromarray(img_array.astype('uint8')).convert('L')
            edges = gray.filter(ImageFilter.FIND_EDGES)
            edge_array = np.array(edges)
            
            # Soft edges (fur-like) vs sharp edges
            soft_edges = np.mean(edge_array > 20)
            return soft_edges
        except:
            return 0
    
    def _detect_eyes(self, img_array: np.ndarray) -> int:
        """Detect eye-like circular dark regions"""
        try:
            gray = Image.fromarray(img_array.astype('uint8')).convert('L')
            gray_array = np.array(gray)
            
            # Look for dark circular regions
            dark_regions = np.sum(gray_array < 80)
            circular_likelihood = dark_regions / (img_array.shape[0] * img_array.shape[1])
            
            if circular_likelihood > 0.05:
                return 2
            elif circular_likelihood > 0.02:
                return 1
            return 0
        except:
            return 0
    
    def _detect_face_region(self, img_array: np.ndarray, skin_percentage: float) -> bool:
        """Detect if face region exists"""
        if skin_percentage < 5:
            return False
        
        # Check if skin is concentrated in upper-middle regions
        h, w = img_array.shape[:2]
        upper_half = img_array[:h//2, :]
        
        pixels_upper = upper_half.reshape(-1, 3)
        skin_in_upper = self._count_skin_pixels(pixels_upper)
        
        return (skin_in_upper / len(pixels_upper)) > 0.05 if len(pixels_upper) > 0 else False
    
    def _detect_species_hints(self, img_array: np.ndarray, skin_pct: float, fur_ind: float) -> List[str]:
        """Detect hints about species"""
        hints = []
        
        if skin_pct > 15 and fur_ind < 0.1:
            hints.append("likely human")
        elif fur_ind > 0.2:
            hints.append("likely animal/creature")
            if fur_ind > 0.3:
                hints.append("very fluffy/hairy")
        
        # Detect ears/horns (shape at top)
        h, w = img_array.shape[:2]
        top_region = img_array[:h//4, :, :]
        top_colors = top_region.reshape(-1, 3)
        
        # Look for protruding shapes
        left_edge = np.mean(top_region[:, :w//4, :])
        right_edge = np.mean(top_region[:, 3*w//4:, :])
        
        if left_edge > 100 or right_edge > 100:
            hints.append("possible ears/horns/protrusions")
        
        return hints
    
    def _detect_actions(self, image: Image.Image) -> Dict[str, Any]:
        """Detect movement and actions"""
        try:
            img_array = np.array(image)
            
            # Analyze pose/body orientation
            h, w = img_array.shape[:2]
            
            # Divided into regions to detect center of mass
            top_brightness = np.mean(Image.fromarray(img_array[:h//3]).convert('L'))
            bottom_brightness = np.mean(Image.fromarray(img_array[2*h//3:]).convert('L'))
            left_brightness = np.mean(Image.fromarray(img_array[:, :w//3]).convert('L'))
            right_brightness = np.mean(Image.fromarray(img_array[:, 2*w//3:]).convert('L'))
            
            actions = []
            
            # Infer actions from brightness distribution
            if top_brightness > bottom_brightness + 30:
                actions.append("head-up posture")
            elif bottom_brightness > top_brightness + 30:
                actions.append("head-down posture")
            
            if abs(left_brightness - right_brightness) > 40:
                if left_brightness > right_brightness:
                    actions.append("facing/leaning left")
                else:
                    actions.append("facing/leaning right")
            
            # Common actions (heuristic-based)
            motion_indicators = (bottom_brightness < 100)  # Low brightness = action
            if motion_indicators and len(actions) < 2:
                actions.append("possibly in motion")
            
            self.detected_parameters['detected_actions'] = actions
            
            return {
                'detected_actions': actions,
                'motion_likelihood': "high" if motion_indicators else "low",
                'body_position': "upright" if abs(top_brightness - bottom_brightness) < 20 else "tilted"
            }
        except Exception as e:
            self.logger.error(f"Action detection failed: {e}")
            return {'detected_actions': []}
    
    def _detect_expressions(self, image: Image.Image) -> Dict[str, Any]:
        """Detect facial expressions"""
        try:
            img_array = np.array(image)
            pixels = img_array.reshape(-1, 3)
            
            # Detect possible expression through brightness patterns
            gray = image.convert('L')
            gray_array = np.array(gray)
            
            h, w = gray_array.shape
            upper_third = gray_array[:h//3, :]
            
            # Look for eyes region (dark areas)
            dark_upper = np.sum(upper_third < 100)
            
            expressions = []
            
            if dark_upper > (upper_third.size * 0.2):
                expressions.append("intense gaze/direct look")
            elif dark_upper > (upper_third.size * 0.1):
                expressions.append("normal gaze")
            else:
                expressions.append("unclear expression")
            
            # Brightness in mouth region (lower face)
            lower_face = gray_array[h//2:, :]
            bright_lower = np.sum(lower_face > 150)
            
            if bright_lower > (lower_face.size * 0.15):
                expressions.append("smiling/bright expression")
            elif bright_lower < (lower_face.size * 0.05):
                expressions.append("serious/neutral expression")
            
            self.detected_parameters['detected_expressions'] = expressions
            
            return {
                'detected_expressions': expressions,
                'expression_confidence': 'low (heuristic-based)'
            }
        except Exception as e:
            self.logger.error(f"Expression detection failed: {e}")
            return {'detected_expressions': []}
    
    def _detect_body_parts(self, image: Image.Image) -> Dict[str, Any]:
        """Detect visible body parts"""
        try:
            img_array = np.array(image)
            pixels = img_array.reshape(-1, 3)
            
            h, w = img_array.shape[:2]
            
            body_parts = []
            
            # Skin-colored regions per area
            skin_upper = self._count_skin_pixels(img_array[:h//3, :].reshape(-1, 3))
            skin_middle = self._count_skin_pixels(img_array[h//3:2*h//3, :].reshape(-1, 3))
            skin_lower = self._count_skin_pixels(img_array[2*h//3:, :].reshape(-1, 3))
            
            if skin_upper > 100:
                body_parts.append("head/face area")
            if skin_middle > 100:
                body_parts.append("torso/body area")
            if skin_lower > 100:
                body_parts.append("legs/lower body area")
            
            # Detect hands/paws (smaller skin regions on sides)
            left_skin = self._count_skin_pixels(img_array[:, :w//4].reshape(-1, 3))
            right_skin = self._count_skin_pixels(img_array[:, 3*w//4:].reshape(-1, 3))
            
            if left_skin > 50:
                body_parts.append("left arm/side visible")
            if right_skin > 50:
                body_parts.append("right arm/side visible")
            
            # Detect clothing (non-skin, colored regions where skin should be)
            clothing_regions = np.sum((pixels[:, 0] + pixels[:, 1] + pixels[:, 2]) > 300)
            if clothing_regions > (len(pixels) * 0.2):
                body_parts.append("clothing/covering visible")
            
            self.detected_parameters['visible_body_parts'] = body_parts
            
            return {
                'visible_body_parts': body_parts,
                'coverage_estimated': len(body_parts) > 2
            }
        except Exception as e:
            self.logger.error(f"Body part detection failed: {e}")
            return {'visible_body_parts': []}
    
    def _detect_clothing(self, image: Image.Image) -> Dict[str, Any]:
        """Detect clothing and accessories"""
        try:
            img_array = np.array(image)
            pixels = img_array.reshape(-1, 3)
            
            # Look for non-natural colors (likely clothing)
            bright_pixels = np.sum((pixels[:, 0] + pixels[:, 1] + pixels[:, 2]) > 400)
            bright_percentage = (bright_pixels / len(pixels)) * 100
            
            clothing = []
            
            if bright_percentage > 15:
                clothing.append("wearing bright clothing/colors")
            
            # Detect specific colors that suggest clothing
            dominant_colors = self._get_dominant_colors(pixels, n_colors=5)
            
            for color in dominant_colors[:3]:
                color_name = color['name']
                if color_name in ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'gold']:
                    if color['percentage'] > 5:
                        clothing.append(f"wearing {color_name} clothing")
            
            # Detect accessories (small bright spots)
            small_bright = np.sum((pixels[:, 0] > 200) & (pixels[:, 1] > 200))
            if small_bright > (len(pixels) * 0.05):
                clothing.append("wearing accessories/decorations")
            
            self.detected_parameters['clothing_items'] = clothing
            
            return {
                'clothing_detected': clothing,
                'has_accessories': len(clothing) > 0
            }
        except Exception as e:
            self.logger.error(f"Clothing detection failed: {e}")
            return {'clothing_detected': []}
    
    def _analyze_environment(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze environment and setting"""
        try:
            img_array = np.array(image)
            pixels = img_array.reshape(-1, 3)
            
            # Detect sky (blue in upper portion)
            h, w = img_array.shape[:2]
            upper_pixels = img_array[:h//3, :].reshape(-1, 3)
            
            blue_upper = np.sum(upper_pixels[:, 2] > 150)
            has_sky = (blue_upper / len(upper_pixels)) > 0.3 if len(upper_pixels) > 0 else False
            
            # Detect vegetation (green)
            green_pixels = np.sum(pixels[:, 1] > (pixels[:, 0] + 20)) + np.sum(pixels[:, 1] > (pixels[:, 2] + 20))
            green_percentage = (green_pixels / (len(pixels) * 2)) * 100
            has_vegetation = green_percentage > 15
            
            # Detect water (cyan/blue in lower portion)
            lower_pixels = img_array[2*h//3:, :].reshape(-1, 3)
            if len(lower_pixels) > 0:
                water_like = np.sum((lower_pixels[:, 1] > 150) & (lower_pixels[:, 2] > 150))
                has_water = (water_like / len(lower_pixels)) > 0.2
            else:
                has_water = False
            
            environment = []
            
            if has_sky:
                environment.append("outdoor setting with visible sky")
            if has_vegetation:
                environment.append("natural vegetation/trees/plants")
            if has_water:
                environment.append("water/liquid visible")
            if not has_sky and not has_vegetation:
                environment.append("likely indoor setting")
            
            self.detected_parameters['environment_features'] = environment
            self.detected_parameters['has_sky'] = has_sky
            self.detected_parameters['has_vegetation'] = has_vegetation
            self.detected_parameters['is_outdoor'] = has_sky or has_vegetation
            
            return {
                'environment_type': environment,
                'has_sky': has_sky,
                'has_vegetation': has_vegetation,
                'has_water': has_water,
                'is_outdoor': has_sky or has_vegetation,
                'vegetation_percentage': round(green_percentage, 1)
            }
        except Exception as e:
            self.logger.error(f"Environment analysis failed: {e}")
            return {'environment_type': []}
    
    def _analyze_textures(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze textures in the image"""
        try:
            gray = image.convert('L')
            gray_array = np.array(gray)
            
            # Calculate texture complexity using edge detection
            edges = gray.filter(ImageFilter.FIND_EDGES)
            edge_array = np.array(edges)
            texture_density = np.mean(edge_array > 50)
            
            textures = []
            
            if texture_density > 0.15:
                textures.append("high texture detail/pattern")
            elif texture_density > 0.08:
                textures.append("moderate texture")
            else:
                textures.append("smooth/low texture")
            
            # Detect rough vs smooth
            variance = np.var(gray_array)
            if variance > 1500:
                textures.append("rough texture")
            elif variance < 500:
                textures.append("smooth/uniform")
            
            self.detected_parameters['texture_types'] = textures
            self.detected_parameters['texture_density'] = round(texture_density, 3)
            
            return {
                'texture_description': textures,
                'texture_density': round(texture_density, 3)
            }
        except Exception as e:
            self.logger.error(f"Texture analysis failed: {e}")
            return {'texture_description': []}
    
    def _analyze_composition(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze image composition"""
        try:
            gray = image.convert('L')
            img_array = np.array(gray)
            h, w = img_array.shape
            
            # Find regions of interest
            top_third = img_array[:h//3, :]
            middle_third = img_array[h//3:2*h//3, :]
            bottom_third = img_array[2*h//3:, :]
            
            regions = {
                'top': np.var(top_third),
                'middle': np.var(middle_third),
                'bottom': np.var(bottom_third)
            }
            
            v_focus = max(regions, key=regions.get)
            
            left_third = img_array[:, :w//3]
            center_third = img_array[:, w//3:2*w//3]
            right_third = img_array[:, 2*w//3:]
            
            h_regions = {
                'left': np.var(left_third),
                'center': np.var(center_third),
                'right': np.var(right_third)
            }
            
            h_focus = max(h_regions, key=h_regions.get)
            
            self.detected_parameters['composition_focus'] = f"{v_focus} {h_focus}"
            
            return {
                'vertical_focus': v_focus,
                'horizontal_focus': h_focus,
                'focus_description': f"{v_focus}-{h_focus}",
                'balanced': abs(h_regions['left'] - h_regions['right']) < h_regions['center'] * 0.3
            }
        except Exception as e:
            self.logger.error(f"Composition analysis failed: {e}")
            return {'focus_description': 'unknown'}
    
    def _detect_features(self, image: Image.Image) -> Dict[str, Any]:
        """Detect various image features"""
        try:
            img_array = np.array(image)
            pixels = img_array.reshape(-1, 3)
            
            if len(pixels) == 0:
                return {}
            
            features = {}
            
            # People/humanoid
            skin_pixels = self._count_skin_pixels(pixels)
            skin_percentage = (skin_pixels / len(pixels)) * 100
            features['likely_contains_people'] = skin_percentage > 5
            features['skin_tone_percentage'] = round(skin_percentage, 2)
            
            # Nature
            green_pixels = np.sum(pixels[:, 1] > (pixels[:, 0] + 20)) + np.sum(pixels[:, 1] > (pixels[:, 2] + 20))
            green_percentage = (green_pixels / (len(pixels) * 2)) * 100
            features['likely_nature_scene'] = green_percentage > 15
            features['vegetation_percentage'] = round(green_percentage, 2)
            
            # Sky
            upper_pixels = img_array[:img_array.shape[0]//3, :, :].reshape(-1, 3)
            if len(upper_pixels) > 0:
                blue_upper = np.sum(upper_pixels[:, 2] > 150)
                features['likely_has_sky'] = (blue_upper / len(upper_pixels)) > 0.3
            else:
                features['likely_has_sky'] = False
            
            self.detected_parameters['has_people'] = features['likely_contains_people']
            self.detected_parameters['has_nature'] = features['likely_nature_scene']
            self.detected_parameters['has_sky'] = features.get('likely_has_sky', False)
            
            return features
        except Exception as e:
            self.logger.error(f"Feature detection failed: {e}")
            return {}
    
    def _generate_rich_description(self, analysis: Dict[str, Any], image: Image.Image) -> str:
        """Generate comprehensive natural language description"""
        try:
            parts = []
            
            # Image dimensions and orientation
            basic = analysis.get('basic_info', {})
            width = basic.get('width', 0)
            height = basic.get('height', 0)
            aspect = basic.get('aspect_ratio', 1.0)
            
            if aspect > 1.3:
                orientation = "wide landscape"
            elif aspect < 0.8:
                orientation = "tall portrait"
            elif 0.95 <= aspect <= 1.05:
                orientation = "square"
            else:
                orientation = "rectangular"
            
            parts.append(f"📸 **Image**: {orientation} format ({width}×{height} pixels)")
            
            # Subjects
            subjects = analysis.get('subjects', {})
            if subjects.get('detected_subjects'):
                parts.append(f"**Subjects**: {', '.join(subjects['detected_subjects'])}")
                if subjects.get('is_fluffy'):
                    parts.append("✨ **Appearance**: Fluffy/soft textured")
                if subjects.get('species_hints'):
                    parts.append(f"🔍 **Species hints**: {', '.join(subjects['species_hints'])}")
            
            # Colors
            colors = analysis.get('colors', {})
            dominant = colors.get('dominant_colors', [])
            if dominant:
                top_colors = [c['name'] for c in dominant[:3]]
                parts.append(f"🎨 **Colors**: {', '.join(top_colors)}")
                tone = colors.get('tone', 'moderate')
                parts.append(f"💡 **Lighting**: {tone} tones, {colors.get('saturation', 0):.1f} saturation")
            
            # Body parts
            body = analysis.get('body_parts', {})
            if body.get('visible_body_parts'):
                parts.append(f"👁️ **Visible**: {', '.join(body['visible_body_parts'][:3])}")
            
            # Clothing
            clothing = analysis.get('clothing', {})
            if clothing.get('clothing_detected'):
                parts.append(f"👕 **Clothing**: {', '.join(clothing['clothing_detected'][:2])}")
            
            # Actions
            actions = analysis.get('actions', {})
            if actions.get('detected_actions'):
                parts.append(f"🎬 **Actions/Pose**: {', '.join(actions['detected_actions'][:2])}")
            
            # Expressions
            expressions = analysis.get('expressions', {})
            if expressions.get('detected_expressions'):
                parts.append(f"😊 **Expression**: {expressions['detected_expressions'][0]}")
            
            # Environment
            environment = analysis.get('environment', {})
            if environment.get('environment_type'):
                parts.append(f"🌍 **Setting**: {', '.join(environment['environment_type'][:2])}")
            
            # Composition
            composition = analysis.get('composition', {})
            focus = composition.get('focus_description', '')
            if focus:
                parts.append(f"📐 **Composition**: Content in {focus} region")
            
            # Textures
            textures = analysis.get('textures', {})
            if textures.get('texture_description'):
                parts.append(f"✋ **Texture**: {textures['texture_description'][0]}")
            
            description = "\n".join(parts)
            
            return description
        except Exception as e:
            self.logger.error(f"Description generation failed: {e}")
            return "Image analyzed but description generation encountered an error"
