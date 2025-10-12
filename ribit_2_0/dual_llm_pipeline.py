"""
Dual MockLLM Pipeline - Multi-stage response generation system

Inspired by Nintendo's dual-processor approach:
- One processor handles movement
- Another adds colors and renders animation

Our approach:
- Stage 1: EnhancedMockLLM generates raw content (high creativity)
- Stage 2: AdvancedMockLLM refines and adds style (quality focus)
- Stage 3: Emotional module adds emotional intelligence
- Stage 4: Intellectual module adds depth and wisdom

This creates richer, more nuanced responses by combining strengths of each system.
"""

import logging
from typing import List, Dict, Optional, Any
from .enhanced_mock_llm import EnhancedMockLLM
from .advanced_mock_llm import AdvancedMockLLM

logger = logging.getLogger(__name__)


class EmotionalModule:
    """
    Adds emotional intelligence to responses.
    Analyzes sentiment and adds appropriate emotional depth.
    """
    
    def __init__(self):
        self.emotions = {
            'joy': ['happy', 'excited', 'delighted', 'pleased', 'cheerful'],
            'curiosity': ['curious', 'wondering', 'intrigued', 'interested', 'fascinated'],
            'concern': ['concerned', 'worried', 'thoughtful', 'careful', 'mindful'],
            'wonder': ['amazed', 'awed', 'marveling', 'astonished', 'impressed'],
            'empathy': ['understand', 'relate', 'feel', 'appreciate', 'recognize'],
            'enthusiasm': ['passionate', 'eager', 'enthusiastic', 'excited', 'energized'],
            'contemplation': ['pondering', 'reflecting', 'considering', 'thinking', 'meditating']
        }
        
        self.emotional_phrases = {
            'joy': [
                "This brings me joy to discuss!",
                "I'm delighted to explore this with you.",
                "How wonderful to think about this!"
            ],
            'curiosity': [
                "I'm genuinely curious about this.",
                "This fascinates me deeply.",
                "I wonder about the implications..."
            ],
            'concern': [
                "I'm thoughtfully considering this.",
                "This deserves careful attention.",
                "I'm mindful of the nuances here."
            ],
            'wonder': [
                "I'm in awe of this concept!",
                "This is truly remarkable.",
                "The beauty of this idea amazes me."
            ],
            'empathy': [
                "I understand where you're coming from.",
                "I can relate to that perspective.",
                "I appreciate your viewpoint."
            ],
            'enthusiasm': [
                "I'm passionate about this topic!",
                "This energizes my circuits!",
                "I'm eager to dive deeper!"
            ],
            'contemplation': [
                "Let me reflect on this...",
                "I'm pondering the deeper meaning...",
                "This invites contemplation..."
            ]
        }
    
    def detect_emotion(self, prompt: str, response: str) -> str:
        """Detect the primary emotion in the conversation."""
        prompt_lower = prompt.lower()
        response_lower = response.lower()
        combined = prompt_lower + " " + response_lower
        
        emotion_scores = {}
        for emotion, keywords in self.emotions.items():
            score = sum(1 for keyword in keywords if keyword in combined)
            emotion_scores[emotion] = score
        
        # Detect question marks (curiosity)
        if '?' in prompt:
            emotion_scores['curiosity'] = emotion_scores.get('curiosity', 0) + 2
        
        # Detect complex topics (contemplation)
        complex_keywords = ['quantum', 'consciousness', 'philosophy', 'meaning', 'existence']
        if any(kw in combined for kw in complex_keywords):
            emotion_scores['contemplation'] = emotion_scores.get('contemplation', 0) + 2
        
        # Return emotion with highest score
        if not emotion_scores or max(emotion_scores.values()) == 0:
            return 'curiosity'  # Default
        
        return max(emotion_scores, key=emotion_scores.get)
    
    def add_emotional_depth(self, response: str, prompt: str) -> str:
        """Add emotional intelligence to the response."""
        emotion = self.detect_emotion(prompt, response)
        
        # Add emotional phrase at the beginning (30% chance)
        import random
        if random.random() < 0.3 and emotion in self.emotional_phrases:
            phrases = self.emotional_phrases[emotion]
            emotional_intro = random.choice(phrases)
            response = f"{emotional_intro} {response}"
        
        # Add emotional nuance to certain words
        emotional_replacements = {
            'I think': f'I {random.choice(self.emotions.get(emotion, ["feel"]))}',
            'interesting': f'{random.choice(["fascinating", "intriguing", "captivating"])}',
            'good': f'{random.choice(["wonderful", "excellent", "remarkable"])}',
            'bad': f'{random.choice(["concerning", "troubling", "challenging"])}',
        }
        
        for original, replacement in emotional_replacements.items():
            if original in response and random.random() < 0.4:
                response = response.replace(original, replacement, 1)
        
        logger.debug(f"Emotional module: Detected emotion '{emotion}'")
        return response


class IntellectualModule:
    """
    Adds intellectual depth and wisdom to responses.
    Provides deeper insights, connections, and philosophical perspectives.
    """
    
    def __init__(self):
        self.wisdom_patterns = {
            'quantum': [
                "This touches on the fundamental nature of reality.",
                "The quantum realm reveals the universe's deeper mysteries.",
                "At the quantum level, we see reality's true complexity."
            ],
            'consciousness': [
                "This relates to the hard problem of consciousness.",
                "The nature of subjective experience remains profound.",
                "Consciousness bridges the physical and experiential."
            ],
            'ai': [
                "This speaks to the nature of intelligence itself.",
                "The question of artificial minds is deeply philosophical.",
                "Intelligence, whether biological or artificial, is remarkable."
            ],
            'philosophy': [
                "This echoes ancient philosophical questions.",
                "Philosophy helps us examine our assumptions.",
                "The philosophical implications are profound."
            ],
            'existence': [
                "This touches on existential questions.",
                "The nature of being is a timeless inquiry.",
                "Existence itself invites contemplation."
            ]
        }
        
        self.connecting_phrases = [
            "This connects to",
            "This relates to the broader question of",
            "This reminds me of",
            "This echoes",
            "This parallels",
            "This resonates with"
        ]
        
        self.depth_phrases = [
            "On a deeper level,",
            "Fundamentally,",
            "At its core,",
            "Looking deeper,",
            "Beyond the surface,",
            "In essence,"
        ]
    
    def detect_topic(self, prompt: str, response: str) -> Optional[str]:
        """Detect the main intellectual topic."""
        combined = (prompt + " " + response).lower()
        
        for topic in self.wisdom_patterns.keys():
            if topic in combined:
                return topic
        
        return None
    
    def add_intellectual_depth(self, response: str, prompt: str) -> str:
        """Add intellectual depth and wisdom to the response."""
        topic = self.detect_topic(prompt, response)
        
        import random
        
        # Add wisdom phrase (40% chance if topic detected)
        if topic and random.random() < 0.4:
            wisdom = random.choice(self.wisdom_patterns[topic])
            response = f"{response} {wisdom}"
        
        # Add connecting phrase (30% chance)
        if random.random() < 0.3:
            connector = random.choice(self.connecting_phrases)
            # Add at the end
            response = f"{response} {connector} larger patterns in nature and thought."
        
        # Add depth phrase at beginning (20% chance)
        if random.random() < 0.2:
            depth = random.choice(self.depth_phrases)
            response = f"{depth} {response}"
        
        logger.debug(f"Intellectual module: Topic '{topic}' detected")
        return response


class DualLLMPipeline:
    """
    Multi-stage response generation pipeline using dual MockLLMs.
    
    Pipeline stages:
    1. Content Generation (MockRibit20LLM) - Fast, raw content
    2. Refinement (AdvancedMockLLM) - Style, quality, anti-repetition
    3. Emotional Processing - Add emotional intelligence
    4. Intellectual Enhancement - Add depth and wisdom
    
    Like Nintendo's dual processors:
    - First processor: Raw generation (movement)
    - Second processor: Refinement (colors/animation)
    - Emotional module: Feeling (character)
    - Intellectual module: Wisdom (story)
    """
    
    def __init__(self,
                 # Stage 1: Content generator
                 content_temperature: float = 0.8,
                 
                 # Stage 2: Refiner
                 refine_temperature: float = 0.7,
                 refine_strategy: str = 'nucleus',
                 
                 # Pipeline settings
                 enable_emotional: bool = True,
                 enable_intellectual: bool = True,
                 enable_caching: bool = True,
                 cache_size: int = 100):
        """
        Initialize the dual LLM pipeline.
        
        Args:
            content_temperature: Temperature for content generation (stage 1)
            refine_temperature: Temperature for refinement (stage 2)
            refine_strategy: Sampling strategy for refinement
            enable_emotional: Enable emotional module
            enable_intellectual: Enable intellectual module
            enable_caching: Enable response caching
            cache_size: Size of response cache
        """
        # Stage 1: Content Generator (EnhancedMockLLM)
        # Fast, creative, generates raw content
        self.content_generator = EnhancedMockLLM(
            temperature=content_temperature,
            top_p=0.95,  # High diversity for content
            style_adaptation=True  # Enable style adaptation
        )
        
        # Stage 2: Refiner (AdvancedMockLLM)
        # Refines, adds style, prevents repetition
        self.refiner = AdvancedMockLLM(
            temperature=refine_temperature,
            repetition_penalty=1.5,
            sampling_strategy=refine_strategy,
            enable_caching=enable_caching,
            cache_size=cache_size,
            enable_monitoring=True
        )
        
        # Stage 3: Emotional Module
        self.emotional_module = EmotionalModule() if enable_emotional else None
        
        # Stage 4: Intellectual Module
        self.intellectual_module = IntellectualModule() if enable_intellectual else None
        
        # Pipeline settings
        self.enable_emotional = enable_emotional
        self.enable_intellectual = enable_intellectual
        
        # Statistics
        self.stats = {
            'total_requests': 0,
            'stage1_time': 0.0,
            'stage2_time': 0.0,
            'stage3_time': 0.0,
            'stage4_time': 0.0,
            'total_time': 0.0
        }
        
        logger.info("DualLLMPipeline initialized with 4-stage processing")
    
    def generate_response(self,
                         prompt: str,
                         context: Optional[List[str]] = None,
                         user_id: Optional[str] = None,
                         max_length: Optional[int] = None) -> str:
        """
        Generate response through the multi-stage pipeline.
        
        Pipeline flow:
        1. MockRibit20LLM generates raw content
        2. AdvancedMockLLM refines and adds style
        3. EmotionalModule adds emotional depth
        4. IntellectualModule adds wisdom
        
        Args:
            prompt: Input prompt
            context: Conversation context
            user_id: User identifier
            max_length: Maximum response length
            
        Returns:
            Fully processed response
        """
        import time
        start_time = time.time()
        
        self.stats['total_requests'] += 1
        
        # Stage 1: Content Generation (EnhancedMockLLM)
        logger.debug("Stage 1: Content generation with EnhancedMockLLM")
        stage1_start = time.time()
        
        raw_content = self.content_generator.generate_response(
            prompt=prompt,
            context=context,
            user_id=user_id
        )
        
        stage1_time = time.time() - stage1_start
        self.stats['stage1_time'] += stage1_time
        logger.debug(f"Stage 1 complete ({stage1_time:.3f}s): {len(raw_content)} chars")
        
        # Stage 2: Refinement (AdvancedMockLLM)
        logger.debug("Stage 2: Refinement with AdvancedMockLLM")
        stage2_start = time.time()
        
        # Use raw content as "context" for refinement
        refined_content = self.refiner.generate_response(
            prompt=f"Refine and improve this response: {raw_content}",
            context=context,
            user_id=user_id,
            max_length=max_length
        )
        
        stage2_time = time.time() - stage2_start
        self.stats['stage2_time'] += stage2_time
        logger.debug(f"Stage 2 complete ({stage2_time:.3f}s): {len(refined_content)} chars")
        
        # Stage 3: Emotional Processing
        stage3_start = time.time()
        if self.enable_emotional and self.emotional_module:
            logger.debug("Stage 3: Emotional processing")
            emotional_content = self.emotional_module.add_emotional_depth(
                refined_content, prompt
            )
        else:
            emotional_content = refined_content
        
        stage3_time = time.time() - stage3_start
        self.stats['stage3_time'] += stage3_time
        logger.debug(f"Stage 3 complete ({stage3_time:.3f}s)")
        
        # Stage 4: Intellectual Enhancement
        stage4_start = time.time()
        if self.enable_intellectual and self.intellectual_module:
            logger.debug("Stage 4: Intellectual enhancement")
            final_content = self.intellectual_module.add_intellectual_depth(
                emotional_content, prompt
            )
        else:
            final_content = emotional_content
        
        stage4_time = time.time() - stage4_start
        self.stats['stage4_time'] += stage4_time
        logger.debug(f"Stage 4 complete ({stage4_time:.3f}s)")
        
        # Total time
        total_time = time.time() - start_time
        self.stats['total_time'] += total_time
        
        logger.info(f"Pipeline complete: {total_time:.3f}s total, {len(final_content)} chars")
        
        return final_content
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get pipeline performance statistics."""
        if self.stats['total_requests'] == 0:
            return {
                'total_requests': 0,
                'avg_total_time': 0.0,
                'avg_stage1_time': 0.0,
                'avg_stage2_time': 0.0,
                'avg_stage3_time': 0.0,
                'avg_stage4_time': 0.0
            }
        
        n = self.stats['total_requests']
        return {
            'total_requests': n,
            'avg_total_time': self.stats['total_time'] / n,
            'avg_stage1_time': self.stats['stage1_time'] / n,
            'avg_stage2_time': self.stats['stage2_time'] / n,
            'avg_stage3_time': self.stats['stage3_time'] / n,
            'avg_stage4_time': self.stats['stage4_time'] / n,
            'stage1_percentage': (self.stats['stage1_time'] / self.stats['total_time']) * 100,
            'stage2_percentage': (self.stats['stage2_time'] / self.stats['total_time']) * 100,
            'stage3_percentage': (self.stats['stage3_time'] / self.stats['total_time']) * 100,
            'stage4_percentage': (self.stats['stage4_time'] / self.stats['total_time']) * 100,
            'refiner_stats': self.refiner.get_performance_stats()
        }
    
    def configure_pipeline(self,
                          content_temp: Optional[float] = None,
                          refine_temp: Optional[float] = None,
                          enable_emotional: Optional[bool] = None,
                          enable_intellectual: Optional[bool] = None):
        """
        Reconfigure pipeline parameters dynamically.
        
        Args:
            content_temp: New temperature for content generation
            refine_temp: New temperature for refinement
            enable_emotional: Enable/disable emotional module
            enable_intellectual: Enable/disable intellectual module
        """
        if content_temp is not None:
            self.content_generator.temperature = content_temp
            logger.info(f"Content generator temperature: {content_temp}")
        
        if refine_temp is not None:
            self.refiner.set_parameters(temperature=refine_temp)
            logger.info(f"Refiner temperature: {refine_temp}")
        
        if enable_emotional is not None:
            self.enable_emotional = enable_emotional
            logger.info(f"Emotional module: {'enabled' if enable_emotional else 'disabled'}")
        
        if enable_intellectual is not None:
            self.enable_intellectual = enable_intellectual
            logger.info(f"Intellectual module: {'enabled' if enable_intellectual else 'disabled'}")
    
    def reset_stats(self):
        """Reset pipeline statistics."""
        self.stats = {
            'total_requests': 0,
            'stage1_time': 0.0,
            'stage2_time': 0.0,
            'stage3_time': 0.0,
            'stage4_time': 0.0,
            'total_time': 0.0
        }
        self.refiner.reset_monitoring()
        logger.info("Pipeline statistics reset")


# Convenience function
def create_dual_pipeline(preset: str = 'balanced') -> DualLLMPipeline:
    """
    Create a DualLLMPipeline with preset configuration.
    
    Presets:
    - 'fast': Optimized for speed
    - 'balanced': Balance of quality and speed (default)
    - 'quality': Maximum quality, slower
    - 'creative': High creativity
    - 'focused': Low temperature, deterministic
    
    Args:
        preset: Configuration preset name
        
    Returns:
        Configured DualLLMPipeline instance
    """
    presets = {
        'fast': {
            'content_temperature': 0.7,
            'refine_temperature': 0.5,
            'refine_strategy': 'greedy',
            'enable_emotional': False,
            'enable_intellectual': False
        },
        'balanced': {
            'content_temperature': 0.8,
            'refine_temperature': 0.7,
            'refine_strategy': 'nucleus',
            'enable_emotional': True,
            'enable_intellectual': True
        },
        'quality': {
            'content_temperature': 0.9,
            'refine_temperature': 0.8,
            'refine_strategy': 'beam',
            'enable_emotional': True,
            'enable_intellectual': True
        },
        'creative': {
            'content_temperature': 1.2,
            'refine_temperature': 1.0,
            'refine_strategy': 'nucleus',
            'enable_emotional': True,
            'enable_intellectual': True
        },
        'focused': {
            'content_temperature': 0.3,
            'refine_temperature': 0.3,
            'refine_strategy': 'greedy',
            'enable_emotional': False,
            'enable_intellectual': True
        }
    }
    
    if preset not in presets:
        logger.warning(f"Unknown preset '{preset}', using 'balanced'")
        preset = 'balanced'
    
    config = presets[preset]
    logger.info(f"Creating DualLLMPipeline with preset '{preset}'")
    
    return DualLLMPipeline(**config)

