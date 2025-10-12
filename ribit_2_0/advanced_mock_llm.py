"""
Advanced Mock LLM with Comprehensive Parameters

Extends EnhancedMockLLM with even more parameters and capabilities:
- Repetition penalty
- Length penalty
- Diversity penalty
- Context window management
- Token limits
- Response caching
- Beam search simulation
- Sampling strategies
- Error handling
- Performance monitoring
"""

import logging
import random
import json
import hashlib
import time
from typing import Dict, List, Any, Optional, Tuple
from collections import deque, defaultdict
from .enhanced_mock_llm import EnhancedMockLLM

logger = logging.getLogger(__name__)


class AdvancedMockLLM(EnhancedMockLLM):
    """
    Advanced Mock LLM with comprehensive parameter control.
    
    Additional Features:
    - Repetition penalty (n-gram level)
    - Length penalty (encourage/discourage long responses)
    - Diversity penalty (beam search diversity)
    - Min/max length constraints
    - Token-level control
    - Response caching
    - Performance monitoring
    - Error recovery
    - Context window sliding
    - Multiple sampling strategies
    """
    
    def __init__(
        self,
        knowledge_file: str = "knowledge.txt",
        # Existing parameters
        temperature: float = 0.7,
        top_p: float = 0.9,
        frequency_penalty: float = 0.5,
        presence_penalty: float = 0.3,
        # New parameters
        repetition_penalty: float = 1.2,
        length_penalty: float = 1.0,
        diversity_penalty: float = 0.0,
        min_length: int = 10,
        max_length: int = 500,
        max_tokens: Optional[int] = None,
        top_k: int = 50,
        num_beams: int = 1,
        no_repeat_ngram_size: int = 3,
        # Advanced settings
        enable_caching: bool = True,
        cache_size: int = 100,
        enable_monitoring: bool = True,
        context_window: int = 2000,
        sliding_window: bool = True,
        # Sampling strategy
        sampling_strategy: str = "nucleus",  # nucleus, top_k, greedy, beam
        # Learning settings
        learning_enabled: bool = True,
        style_adaptation: bool = True,
        # Error handling
        max_retries: int = 3,
        fallback_response: Optional[str] = None
    ):
        """
        Initialize Advanced Mock LLM.
        
        Args:
            repetition_penalty: Penalty for repeating tokens (1.0 = no penalty, >1.0 = penalize)
            length_penalty: Penalty for length (>1.0 = prefer longer, <1.0 = prefer shorter)
            diversity_penalty: Encourage diverse responses in beam search
            min_length: Minimum response length in characters
            max_length: Maximum response length in characters
            max_tokens: Maximum tokens (words) in response
            top_k: Top-K sampling parameter
            num_beams: Number of beams for beam search
            no_repeat_ngram_size: Size of n-grams that cannot repeat
            enable_caching: Enable response caching
            cache_size: Maximum cache entries
            enable_monitoring: Enable performance monitoring
            context_window: Maximum context length
            sliding_window: Use sliding window for context
            sampling_strategy: Sampling strategy to use
            max_retries: Maximum retries on error
            fallback_response: Fallback response on error
        """
        super().__init__(
            knowledge_file=knowledge_file,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            max_context_length=context_window,
            learning_enabled=learning_enabled,
            style_adaptation=style_adaptation
        )
        
        # New parameters
        self.repetition_penalty = self._clamp(repetition_penalty, 1.0, 2.0)
        self.length_penalty = self._clamp(length_penalty, 0.5, 2.0)
        self.diversity_penalty = self._clamp(diversity_penalty, 0.0, 1.0)
        self.min_length = max(1, min_length)
        self.max_length = max(self.min_length, max_length)
        self.max_tokens = max_tokens
        self.top_k = max(1, top_k)
        self.num_beams = max(1, num_beams)
        self.no_repeat_ngram_size = max(0, no_repeat_ngram_size)
        
        # Advanced settings
        self.enable_caching = enable_caching
        self.cache_size = cache_size
        self.enable_monitoring = enable_monitoring
        self.context_window = context_window
        self.sliding_window = sliding_window
        self.sampling_strategy = sampling_strategy
        self.max_retries = max_retries
        self.fallback_response = fallback_response or "I apologize, but I'm having trouble generating a response right now."
        
        # Response cache
        self.response_cache = {} if enable_caching else None
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Performance monitoring
        self.response_times = deque(maxlen=100)
        self.error_count = 0
        self.total_requests = 0
        self.successful_requests = 0
        
        # N-gram tracking for repetition penalty
        self.ngram_history = defaultdict(int)
        
        # Context management
        self.context_buffer = deque(maxlen=context_window)
        
        logger.info(f"Advanced Mock LLM initialized with {len(self.__dict__)} parameters")
    
    def set_advanced_parameters(
        self,
        repetition_penalty: Optional[float] = None,
        length_penalty: Optional[float] = None,
        diversity_penalty: Optional[float] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        top_k: Optional[int] = None,
        num_beams: Optional[int] = None,
        sampling_strategy: Optional[str] = None
    ):
        """Update advanced parameters."""
        if repetition_penalty is not None:
            self.repetition_penalty = self._clamp(repetition_penalty, 1.0, 2.0)
        if length_penalty is not None:
            self.length_penalty = self._clamp(length_penalty, 0.5, 2.0)
        if diversity_penalty is not None:
            self.diversity_penalty = self._clamp(diversity_penalty, 0.0, 1.0)
        if min_length is not None:
            self.min_length = max(1, min_length)
        if max_length is not None:
            self.max_length = max(self.min_length, max_length)
        if top_k is not None:
            self.top_k = max(1, top_k)
        if num_beams is not None:
            self.num_beams = max(1, num_beams)
        if sampling_strategy is not None:
            if sampling_strategy in ['nucleus', 'top_k', 'greedy', 'beam']:
                self.sampling_strategy = sampling_strategy
        
        logger.info(f"Advanced parameters updated")
    
    def generate_response(
        self,
        prompt: str,
        context: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        max_length: Optional[int] = None,
        use_cache: bool = True
    ) -> str:
        """
        Generate response with all advanced features.
        
        Args:
            prompt: Input prompt
            context: Conversation context
            user_id: User to adapt to
            max_length: Override max length
            use_cache: Use cached response if available
            
        Returns:
            Generated response
        """
        start_time = time.time()
        self.total_requests += 1
        
        try:
            # Check cache
            if use_cache and self.enable_caching:
                cached = self._check_cache(prompt, context, user_id)
                if cached:
                    self.cache_hits += 1
                    logger.debug("Cache hit")
                    return cached
                self.cache_misses += 1
            
            # Manage context window
            if context:
                self._update_context_buffer(context)
            
            # Generate response with retries
            response = None
            for attempt in range(self.max_retries):
                try:
                    response = self._generate_with_strategy(
                        prompt, context, user_id, max_length
                    )
                    break
                except Exception as e:
                    logger.warning(f"Generation attempt {attempt + 1} failed: {e}")
                    if attempt == self.max_retries - 1:
                        response = self.fallback_response
            
            if response is None:
                response = self.fallback_response
            
            # Apply length constraints
            response = self._apply_length_constraints(response, max_length)
            
            # Apply repetition penalty
            response = self._apply_repetition_penalty(response)
            
            # Track n-grams
            self._track_ngrams(response)
            
            # Cache response
            if self.enable_caching:
                self._cache_response(prompt, context, user_id, response)
            
            # Monitor performance
            if self.enable_monitoring:
                elapsed = time.time() - start_time
                self.response_times.append(elapsed)
            
            self.successful_requests += 1
            return response
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Response generation failed: {e}")
            return self.fallback_response
    
    def _generate_with_strategy(
        self,
        prompt: str,
        context: Optional[List[str]],
        user_id: Optional[str],
        max_length: Optional[int]
    ) -> str:
        """Generate response using selected sampling strategy."""
        
        if self.sampling_strategy == 'greedy':
            return self._greedy_sampling(prompt, context, user_id, max_length)
        elif self.sampling_strategy == 'top_k':
            return self._top_k_sampling(prompt, context, user_id, max_length)
        elif self.sampling_strategy == 'beam':
            return self._beam_search(prompt, context, user_id, max_length)
        else:  # nucleus (default)
            return super().generate_response(prompt, context, user_id, max_length or self.max_length)
    
    def _greedy_sampling(
        self,
        prompt: str,
        context: Optional[List[str]],
        user_id: Optional[str],
        max_length: Optional[int]
    ) -> str:
        """Greedy sampling - always pick most likely token."""
        # For mock LLM, use most common response
        response = super().generate_response(prompt, context, user_id, max_length or self.max_length)
        # Greedy would pick first/best option
        return response
    
    def _top_k_sampling(
        self,
        prompt: str,
        context: Optional[List[str]],
        user_id: Optional[str],
        max_length: Optional[int]
    ) -> str:
        """Top-K sampling - sample from top K tokens."""
        # Generate multiple candidates
        candidates = []
        for _ in range(min(self.top_k, 5)):  # Generate up to 5 candidates
            response = super().generate_response(prompt, context, user_id, max_length or self.max_length)
            candidates.append(response)
        
        # Pick one randomly (simulating top-K)
        return random.choice(candidates) if candidates else super().generate_response(prompt, context, user_id, max_length or self.max_length)
    
    def _beam_search(
        self,
        prompt: str,
        context: Optional[List[str]],
        user_id: Optional[str],
        max_length: Optional[int]
    ) -> str:
        """Beam search - maintain multiple hypotheses."""
        # Generate multiple beams
        beams = []
        for i in range(self.num_beams):
            response = super().generate_response(prompt, context, user_id, max_length or self.max_length)
            score = self._score_response(response, prompt)
            beams.append((score, response))
        
        # Sort by score and pick best
        beams.sort(reverse=True, key=lambda x: x[0])
        return beams[0][1] if beams else super().generate_response(prompt, context, user_id, max_length or self.max_length)
    
    def _score_response(self, response: str, prompt: str) -> float:
        """Score a response for beam search."""
        score = 1.0
        
        # Length penalty
        length_score = len(response) / self.max_length
        score *= (length_score ** self.length_penalty)
        
        # Diversity bonus
        unique_words = len(set(response.lower().split()))
        total_words = len(response.split())
        if total_words > 0:
            diversity_score = unique_words / total_words
            score *= (1.0 + self.diversity_penalty * diversity_score)
        
        # Relevance to prompt (simple keyword matching)
        prompt_words = set(prompt.lower().split())
        response_words = set(response.lower().split())
        overlap = len(prompt_words & response_words)
        if len(prompt_words) > 0:
            relevance = overlap / len(prompt_words)
            score *= (1.0 + relevance)
        
        return score
    
    def _apply_length_constraints(self, response: str, max_length: Optional[int]) -> str:
        """Apply min/max length constraints."""
        max_len = max_length or self.max_length
        
        # Apply max length
        if len(response) > max_len:
            # Try to cut at sentence boundary
            response = response[:max_len]
            last_period = response.rfind('.')
            last_question = response.rfind('?')
            last_exclaim = response.rfind('!')
            last_sentence = max(last_period, last_question, last_exclaim)
            
            if last_sentence > max_len * 0.7:  # If we can keep >70% of text
                response = response[:last_sentence + 1]
            else:
                # Cut at word boundary
                response = response.rsplit(' ', 1)[0]
                if not response.endswith(('.', '!', '?')):
                    response += '...'
        
        # Apply min length
        if len(response) < self.min_length:
            # Pad with additional context (in real LLM this would generate more)
            response += " I'd be happy to elaborate further if you'd like."
        
        # Apply token limit
        if self.max_tokens:
            words = response.split()
            if len(words) > self.max_tokens:
                response = ' '.join(words[:self.max_tokens])
                if not response.endswith(('.', '!', '?')):
                    response += '...'
        
        return response
    
    def _apply_repetition_penalty(self, response: str) -> str:
        """Apply n-gram repetition penalty."""
        if self.no_repeat_ngram_size == 0 or self.repetition_penalty <= 1.0:
            return response
        
        words = response.split()
        n = self.no_repeat_ngram_size
        
        # Check for repeating n-grams
        seen_ngrams = set()
        filtered_words = []
        
        for i in range(len(words)):
            if i < n - 1:
                filtered_words.append(words[i])
                continue
            
            ngram = tuple(words[i-n+1:i+1])
            
            # If n-gram repeats, try to vary it
            if ngram in seen_ngrams and random.random() < (self.repetition_penalty - 1.0):
                # Skip this word (simulating penalty)
                logger.debug(f"Penalizing repeated n-gram: {' '.join(ngram)}")
                continue
            
            seen_ngrams.add(ngram)
            filtered_words.append(words[i])
        
        return ' '.join(filtered_words)
    
    def _track_ngrams(self, response: str):
        """Track n-grams for future penalty calculation."""
        if self.no_repeat_ngram_size == 0:
            return
        
        words = response.lower().split()
        n = self.no_repeat_ngram_size
        
        for i in range(len(words) - n + 1):
            ngram = tuple(words[i:i+n])
            self.ngram_history[ngram] += 1
    
    def _check_cache(
        self,
        prompt: str,
        context: Optional[List[str]],
        user_id: Optional[str]
    ) -> Optional[str]:
        """Check if response is cached."""
        if not self.response_cache:
            return None
        
        cache_key = self._get_cache_key(prompt, context, user_id)
        return self.response_cache.get(cache_key)
    
    def _cache_response(
        self,
        prompt: str,
        context: Optional[List[str]],
        user_id: Optional[str],
        response: str
    ):
        """Cache a response."""
        if not self.response_cache:
            return
        
        # Limit cache size
        if len(self.response_cache) >= self.cache_size:
            # Remove oldest entry (FIFO)
            oldest_key = next(iter(self.response_cache))
            del self.response_cache[oldest_key]
        
        cache_key = self._get_cache_key(prompt, context, user_id)
        self.response_cache[cache_key] = response
    
    def _get_cache_key(
        self,
        prompt: str,
        context: Optional[List[str]],
        user_id: Optional[str]
    ) -> str:
        """Generate cache key."""
        key_parts = [prompt]
        if context:
            key_parts.extend(context[-3:])  # Last 3 context messages
        if user_id:
            key_parts.append(user_id)
        
        key_string = '|'.join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _update_context_buffer(self, context: List[str]):
        """Update context buffer with sliding window."""
        if not self.sliding_window:
            return
        
        for msg in context:
            self.context_buffer.append(msg)
    
    def get_context(self, limit: Optional[int] = None) -> List[str]:
        """Get recent context."""
        if limit:
            return list(self.context_buffer)[-limit:]
        return list(self.context_buffer)
    
    def clear_cache(self):
        """Clear response cache."""
        if self.response_cache:
            self.response_cache.clear()
            logger.info("Response cache cleared")
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        
        stats = {
            'total_requests': self.total_requests,
            'successful_requests': self.successful_requests,
            'error_count': self.error_count,
            'success_rate': self.successful_requests / self.total_requests if self.total_requests > 0 else 0,
            'avg_response_time': round(avg_response_time, 3),
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_hit_rate': self.cache_hits / (self.cache_hits + self.cache_misses) if (self.cache_hits + self.cache_misses) > 0 else 0,
            'cache_size': len(self.response_cache) if self.response_cache else 0,
            'ngrams_tracked': len(self.ngram_history),
            'context_buffer_size': len(self.context_buffer)
        }
        
        return stats
    
    def get_all_parameters(self) -> Dict[str, Any]:
        """Get all LLM parameters."""
        base_stats = super().get_statistics()
        
        params = {
            'base_parameters': base_stats['parameters'],
            'advanced_parameters': {
                'repetition_penalty': self.repetition_penalty,
                'length_penalty': self.length_penalty,
                'diversity_penalty': self.diversity_penalty,
                'min_length': self.min_length,
                'max_length': self.max_length,
                'max_tokens': self.max_tokens,
                'top_k': self.top_k,
                'num_beams': self.num_beams,
                'no_repeat_ngram_size': self.no_repeat_ngram_size,
                'sampling_strategy': self.sampling_strategy
            },
            'system_settings': {
                'enable_caching': self.enable_caching,
                'cache_size': self.cache_size,
                'enable_monitoring': self.enable_monitoring,
                'context_window': self.context_window,
                'sliding_window': self.sliding_window,
                'max_retries': self.max_retries
            },
            'performance': self.get_performance_stats(),
            'current_style': self.current_style
        }
        
        return params
    
    def reset_monitoring(self):
        """Reset performance monitoring."""
        self.response_times.clear()
        self.error_count = 0
        self.total_requests = 0
        self.successful_requests = 0
        self.cache_hits = 0
        self.cache_misses = 0
        logger.info("Performance monitoring reset")
    
    def diagnose(self) -> Dict[str, Any]:
        """Run diagnostics and return health report."""
        perf = self.get_performance_stats()
        params = self.get_all_parameters()
        
        issues = []
        warnings = []
        
        # Check success rate
        if perf['success_rate'] < 0.9:
            issues.append(f"Low success rate: {perf['success_rate']:.1%}")
        
        # Check cache efficiency
        if perf['cache_hit_rate'] < 0.2 and self.enable_caching:
            warnings.append(f"Low cache hit rate: {perf['cache_hit_rate']:.1%}")
        
        # Check response time
        if perf['avg_response_time'] > 1.0:
            warnings.append(f"Slow response time: {perf['avg_response_time']:.3f}s")
        
        # Check error rate
        error_rate = perf['error_count'] / perf['total_requests'] if perf['total_requests'] > 0 else 0
        if error_rate > 0.1:
            issues.append(f"High error rate: {error_rate:.1%}")
        
        health_status = "healthy" if not issues else "degraded" if not any("High" in i for i in issues) else "unhealthy"
        
        return {
            'status': health_status,
            'issues': issues,
            'warnings': warnings,
            'performance': perf,
            'recommendations': self._get_recommendations(perf, params)
        }
    
    def _get_recommendations(self, perf: Dict, params: Dict) -> List[str]:
        """Get optimization recommendations."""
        recommendations = []
        
        if perf['cache_hit_rate'] < 0.3 and self.enable_caching:
            recommendations.append("Consider increasing cache size for better performance")
        
        if perf['avg_response_time'] > 0.5:
            recommendations.append("Consider reducing num_beams or using greedy sampling")
        
        if len(self.ngram_history) > 10000:
            recommendations.append("Consider clearing n-gram history to free memory")
        
        return recommendations


# Global instance
_advanced_mock_llm = None

def get_advanced_mock_llm(knowledge_file: str = "knowledge.txt", **kwargs) -> AdvancedMockLLM:
    """Get global AdvancedMockLLM instance."""
    global _advanced_mock_llm
    if _advanced_mock_llm is None:
        _advanced_mock_llm = AdvancedMockLLM(knowledge_file, **kwargs)
    return _advanced_mock_llm

