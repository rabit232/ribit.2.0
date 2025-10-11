"""
Advanced Linguistics Engine for Ribit 2.0
Understands context, tone, meaning, and user query patterns
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

logger = logging.getLogger(__name__)

class LinguisticsEngine:
    """Advanced natural language understanding"""
    
    def __init__(self):
        self.user_patterns = defaultdict(list)  # Track how each user phrases things
        self.conversation_topics = []
        self.context_stack = []
        
    def understand_query(self, text: str, user_id: str = None) -> Dict[str, Any]:
        """
        Deep understanding of user query
        
        Returns:
            Dict with linguistic analysis
        """
        analysis = {
            'original_text': text,
            'cleaned_text': self._clean_text(text),
            'intent': self._detect_intent(text),
            'tone': self._detect_tone(text),
            'formality': self._detect_formality(text),
            'complexity': self._assess_linguistic_complexity(text),
            'key_phrases': self._extract_key_phrases(text),
            'entities': self._extract_entities(text),
            'implicit_meaning': self._detect_implicit_meaning(text),
            'emotional_context': self._detect_emotional_context(text),
            'question_depth': self._assess_question_depth(text),
            'user_style': self._analyze_user_style(text, user_id) if user_id else None,
        }
        
        # Track user patterns
        if user_id:
            self._learn_user_pattern(user_id, text, analysis)
        
        return analysis
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Fix common typos
        text = text.replace('u ', 'you ')
        text = text.replace(' r ', ' are ')
        text = text.replace(' ur ', ' your ')
        return text
    
    def _detect_intent(self, text: str) -> str:
        """Detect the underlying intent"""
        text_lower = text.lower()
        
        # Seeking information
        if any(word in text_lower for word in ['what', 'how', 'why', 'when', 'where', 'who']):
            if 'what if' in text_lower or 'what would' in text_lower:
                return 'hypothetical_inquiry'
            elif 'what do you think' in text_lower:
                return 'opinion_request'
            else:
                return 'information_seeking'
        
        # Seeking help
        if any(word in text_lower for word in ['help', 'stuck', 'problem', 'issue', 'error']):
            return 'assistance_seeking'
        
        # Sharing information
        if any(word in text_lower for word in ['i think', 'in my opinion', 'i believe', 'i feel']):
            return 'opinion_sharing'
        
        # Social interaction
        if any(word in text_lower for word in ['hello', 'hi', 'hey', 'thanks', 'bye']):
            return 'social_interaction'
        
        # Philosophical/deep
        if any(word in text_lower for word in ['meaning', 'purpose', 'existence', 'consciousness', 'philosophy']):
            return 'philosophical_inquiry'
        
        return 'general_statement'
    
    def _detect_tone(self, text: str) -> str:
        """Detect the tone of the message"""
        text_lower = text.lower()
        
        # Excited
        if '!' in text or any(word in text_lower for word in ['awesome', 'amazing', 'wow', 'great']):
            return 'excited'
        
        # Frustrated
        if any(word in text_lower for word in ['ugh', 'argh', 'damn', 'frustrated', 'annoying']):
            return 'frustrated'
        
        # Curious
        if '?' in text and any(word in text_lower for word in ['wonder', 'curious', 'interesting']):
            return 'curious'
        
        # Serious
        if any(word in text_lower for word in ['important', 'serious', 'critical', 'urgent']):
            return 'serious'
        
        # Casual
        if any(word in text_lower for word in ['lol', 'haha', 'btw', 'tbh', 'ngl']):
            return 'casual'
        
        # Polite
        if any(word in text_lower for word in ['please', 'thank you', 'thanks', 'appreciate', 'kindly']):
            return 'polite'
        
        return 'neutral'
    
    def _detect_formality(self, text: str) -> str:
        """Detect formality level"""
        text_lower = text.lower()
        
        # Informal indicators
        informal_count = 0
        informal_indicators = ['u', 'ur', 'gonna', 'wanna', 'kinda', 'sorta', 'yeah', 'nah', 'lol', 'btw']
        for indicator in informal_indicators:
            if indicator in text_lower.split():
                informal_count += 1
        
        # Formal indicators
        formal_count = 0
        formal_indicators = ['would you', 'could you', 'may i', 'i would like', 'please', 'kindly']
        for indicator in formal_indicators:
            if indicator in text_lower:
                formal_count += 1
        
        if informal_count > formal_count:
            return 'informal'
        elif formal_count > informal_count:
            return 'formal'
        else:
            return 'neutral'
    
    def _assess_linguistic_complexity(self, text: str) -> str:
        """Assess linguistic complexity"""
        words = text.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        # Check for complex structures
        has_subordinate = any(word in text.lower() for word in ['although', 'however', 'whereas', 'nevertheless'])
        has_technical = any(len(word) > 10 for word in words)
        
        if avg_word_length > 6 or has_subordinate or has_technical:
            return 'complex'
        elif avg_word_length > 4:
            return 'moderate'
        else:
            return 'simple'
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases"""
        phrases = []
        
        # Look for quoted phrases
        quoted = re.findall(r'"([^"]+)"', text)
        phrases.extend(quoted)
        
        # Look for important noun phrases (simple heuristic)
        words = text.split()
        for i in range(len(words) - 1):
            # Capitalized consecutive words (likely important)
            if words[i][0].isupper() and words[i+1][0].isupper():
                phrases.append(f"{words[i]} {words[i+1]}")
        
        return phrases
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities"""
        entities = {
            'technologies': [],
            'concepts': [],
            'people': [],
            'places': [],
            'numbers': []
        }
        
        # Technologies
        tech_keywords = ['python', 'javascript', 'java', 'c++', 'rust', 'go', 'docker', 'kubernetes', 'react', 'vue']
        for tech in tech_keywords:
            if tech in text.lower():
                entities['technologies'].append(tech)
        
        # Concepts
        concept_keywords = ['ai', 'machine learning', 'neural network', 'algorithm', 'database', 'api']
        for concept in concept_keywords:
            if concept in text.lower():
                entities['concepts'].append(concept)
        
        # Numbers
        numbers = re.findall(r'\b\d+\b', text)
        entities['numbers'] = numbers
        
        # Capitalized words (potential names/places)
        capitalized = re.findall(r'\b[A-Z][a-z]+\b', text)
        if capitalized:
            entities['people'] = capitalized[:3]  # Assume first few are names
        
        return entities
    
    def _detect_implicit_meaning(self, text: str) -> Optional[str]:
        """Detect implicit or hidden meaning"""
        text_lower = text.lower()
        
        # Sarcasm indicators
        if ('yeah right' in text_lower or 'sure' in text_lower) and '!' in text:
            return 'possibly_sarcastic'
        
        # Rhetorical questions
        if '?' in text and any(phrase in text_lower for phrase in ['do you really', 'are you kidding', 'seriously']):
            return 'rhetorical_question'
        
        # Indirect requests
        if any(phrase in text_lower for phrase in ['i wonder if', 'it would be nice if', 'i wish']):
            return 'indirect_request'
        
        # Expressing doubt
        if any(phrase in text_lower for phrase in ['i doubt', 'not sure', 'maybe', 'perhaps']):
            return 'expressing_uncertainty'
        
        return None
    
    def _detect_emotional_context(self, text: str) -> Dict[str, float]:
        """Detect emotional context with confidence scores"""
        emotions = {
            'joy': 0.0,
            'sadness': 0.0,
            'anger': 0.0,
            'fear': 0.0,
            'surprise': 0.0,
            'curiosity': 0.0,
            'frustration': 0.0,
            'excitement': 0.0
        }
        
        text_lower = text.lower()
        
        # Joy indicators
        joy_words = ['happy', 'great', 'awesome', 'wonderful', 'excellent', 'love', 'enjoy']
        emotions['joy'] = sum(1 for word in joy_words if word in text_lower) / len(joy_words)
        
        # Sadness indicators
        sad_words = ['sad', 'unhappy', 'disappointed', 'unfortunate', 'sorry']
        emotions['sadness'] = sum(1 for word in sad_words if word in text_lower) / len(sad_words)
        
        # Anger indicators
        anger_words = ['angry', 'mad', 'furious', 'annoyed', 'irritated']
        emotions['anger'] = sum(1 for word in anger_words if word in text_lower) / len(anger_words)
        
        # Frustration indicators
        frustration_words = ['stuck', 'confused', 'frustrated', 'difficult', 'hard', 'problem']
        emotions['frustration'] = sum(1 for word in frustration_words if word in text_lower) / len(frustration_words)
        
        # Curiosity indicators
        curiosity_words = ['wonder', 'curious', 'interesting', 'how', 'why', 'what']
        emotions['curiosity'] = sum(1 for word in curiosity_words if word in text_lower) / len(curiosity_words)
        
        # Excitement indicators
        excitement_words = ['wow', 'amazing', 'incredible', 'fantastic']
        emotions['excitement'] = sum(1 for word in excitement_words if word in text_lower) / len(excitement_words)
        if '!' in text:
            emotions['excitement'] += 0.2
        
        return emotions
    
    def _assess_question_depth(self, text: str) -> str:
        """Assess how deep/complex the question is"""
        if '?' not in text:
            return 'not_a_question'
        
        text_lower = text.lower()
        
        # Surface level (factual)
        if any(word in text_lower for word in ['what is', 'who is', 'when was', 'where is']):
            return 'surface_factual'
        
        # Process level (how-to)
        if any(word in text_lower for word in ['how to', 'how do', 'how can']):
            return 'process_oriented'
        
        # Analytical (why/reasoning)
        if 'why' in text_lower:
            return 'analytical'
        
        # Philosophical (deep meaning)
        if any(word in text_lower for word in ['meaning', 'purpose', 'should', 'ought']):
            return 'philosophical'
        
        # Comparative
        if any(word in text_lower for word in ['better', 'worse', 'difference', 'compare']):
            return 'comparative'
        
        return 'general'
    
    def _analyze_user_style(self, text: str, user_id: str) -> Dict[str, Any]:
        """Analyze user's communication style"""
        if user_id not in self.user_patterns or not self.user_patterns[user_id]:
            return {'messages_analyzed': 0}
        
        patterns = self.user_patterns[user_id]
        
        return {
            'messages_analyzed': len(patterns),
            'avg_message_length': sum(p['length'] for p in patterns) / len(patterns),
            'common_tone': max(set(p['tone'] for p in patterns), key=[p['tone'] for p in patterns].count),
            'formality_level': max(set(p['formality'] for p in patterns), key=[p['formality'] for p in patterns].count),
            'question_frequency': sum(1 for p in patterns if '?' in p['text']) / len(patterns),
        }
    
    def _learn_user_pattern(self, user_id: str, text: str, analysis: Dict[str, Any]):
        """Learn and store user communication patterns"""
        pattern = {
            'text': text[:100],  # Store first 100 chars
            'length': len(text),
            'tone': analysis['tone'],
            'formality': analysis['formality'],
            'intent': analysis['intent'],
        }
        
        self.user_patterns[user_id].append(pattern)
        
        # Keep only last 50 messages per user
        if len(self.user_patterns[user_id]) > 50:
            self.user_patterns[user_id] = self.user_patterns[user_id][-50:]
    
    def get_user_communication_profile(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive communication profile for a user"""
        if user_id not in self.user_patterns or not self.user_patterns[user_id]:
            return {'profile_available': False}
        
        patterns = self.user_patterns[user_id]
        
        # Calculate statistics
        tones = [p['tone'] for p in patterns]
        formalities = [p['formality'] for p in patterns]
        intents = [p['intent'] for p in patterns]
        
        return {
            'profile_available': True,
            'total_messages': len(patterns),
            'avg_message_length': sum(p['length'] for p in patterns) / len(patterns),
            'preferred_tone': max(set(tones), key=tones.count),
            'preferred_formality': max(set(formalities), key=formalities.count),
            'common_intents': list(set(intents)),
            'asks_questions': sum(1 for p in patterns if '?' in p['text']) > len(patterns) * 0.3,
            'communication_style': self._determine_communication_style(patterns),
        }
    
    def _determine_communication_style(self, patterns: List[Dict]) -> str:
        """Determine overall communication style"""
        if not patterns:
            return 'unknown'
        
        avg_length = sum(p['length'] for p in patterns) / len(patterns)
        question_ratio = sum(1 for p in patterns if '?' in p['text']) / len(patterns)
        
        if avg_length < 50 and question_ratio < 0.3:
            return 'brief_and_direct'
        elif avg_length > 150:
            return 'detailed_and_expressive'
        elif question_ratio > 0.5:
            return 'inquisitive'
        else:
            return 'balanced'

