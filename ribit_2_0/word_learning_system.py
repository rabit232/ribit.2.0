"""
Word Learning System for Ribit 2.0

Learns words from messages and builds a dictionary with use cases.
Enables Ribit to construct custom sentences using learned patterns.
"""

import json
import os
import re
import time
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set, Optional
from datetime import datetime, timedelta
import asyncio


class WordLearningSystem:
    """
    Advanced word learning system that:
    - Builds dictionary of words with use cases
    - Learns sentence construction patterns
    - Analyzes word relationships and context
    - Generates custom speech using learned patterns
    """
    
    def __init__(self, storage_dir: str = "word_learning"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        # Word dictionary: {word: {uses, contexts, positions, examples}}
        self.word_dictionary = defaultdict(lambda: {
            'count': 0,
            'contexts': [],  # Surrounding words
            'positions': [],  # Position in sentence (start, middle, end)
            'examples': [],  # Full sentences containing the word
            'follows': Counter(),  # Words that come after
            'precedes': Counter(),  # Words that come before
            'part_of_speech': None,  # Detected POS
            'sentiment': 'neutral',  # Positive, negative, neutral
        })
        
        # Sentence patterns: {pattern: count}
        self.sentence_patterns = Counter()
        
        # Word combinations: {(word1, word2): count}
        self.word_pairs = Counter()
        self.word_triplets = Counter()
        
        # Grammar patterns
        self.grammar_patterns = {
            'subject_verb_object': [],
            'questions': [],
            'commands': [],
            'descriptions': [],
        }
        
        # Learning statistics
        self.stats = {
            'total_words_learned': 0,
            'total_sentences_analyzed': 0,
            'total_patterns_found': 0,
            'learning_sessions': 0,
            'last_learning_time': None,
        }
        
        # Load existing knowledge
        self.load_knowledge()
    
    def learn_from_message(self, message: str, user_id: str = None):
        """
        Learn from a single message
        
        Args:
            message: The message text
            user_id: Optional user ID for context
        """
        # Clean and tokenize
        words = self._tokenize(message)
        if not words:
            return
        
        # Learn words
        for i, word in enumerate(words):
            self._learn_word(word, words, i, message)
        
        # Learn word pairs
        for i in range(len(words) - 1):
            pair = (words[i], words[i + 1])
            self.word_pairs[pair] += 1
        
        # Learn word triplets
        for i in range(len(words) - 2):
            triplet = (words[i], words[i + 1], words[i + 2])
            self.word_triplets[triplet] += 1
        
        # Learn sentence pattern
        pattern = self._extract_pattern(words)
        self.sentence_patterns[pattern] += 1
        
        # Detect grammar pattern
        grammar_type = self._detect_grammar_type(message, words)
        if grammar_type:
            self.grammar_patterns[grammar_type].append(message)
        
        # Update stats
        self.stats['total_sentences_analyzed'] += 1
        self.stats['total_words_learned'] = len(self.word_dictionary)
        self.stats['total_patterns_found'] = len(self.sentence_patterns)
    
    def _learn_word(self, word: str, all_words: List[str], position: int, full_sentence: str):
        """Learn a single word with context"""
        entry = self.word_dictionary[word]
        entry['count'] += 1
        
        # Position in sentence
        if position == 0:
            pos_type = 'start'
        elif position == len(all_words) - 1:
            pos_type = 'end'
        else:
            pos_type = 'middle'
        entry['positions'].append(pos_type)
        
        # Context (surrounding words)
        context = []
        if position > 0:
            context.append(all_words[position - 1])
            entry['precedes'][all_words[position - 1]] += 1
        if position < len(all_words) - 1:
            context.append(all_words[position + 1])
            entry['follows'][all_words[position + 1]] += 1
        
        if context:
            entry['contexts'].append(' '.join(context))
        
        # Example sentence (keep up to 10)
        if len(entry['examples']) < 10:
            entry['examples'].append(full_sentence)
        
        # Detect part of speech (simple heuristics)
        if not entry['part_of_speech']:
            entry['part_of_speech'] = self._guess_pos(word, all_words, position)
        
        # Detect sentiment (simple)
        entry['sentiment'] = self._guess_sentiment(word)
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\?\!,]', '', text)
        
        # Split into words
        words = text.split()
        
        # Filter out very short words and numbers
        words = [w for w in words if len(w) > 1 and not w.isdigit()]
        
        return words
    
    def _extract_pattern(self, words: List[str]) -> str:
        """Extract sentence pattern"""
        if not words:
            return ""
        
        pattern_parts = []
        for word in words:
            entry = self.word_dictionary.get(word)
            if entry and entry['part_of_speech']:
                pattern_parts.append(entry['part_of_speech'])
            else:
                pattern_parts.append('WORD')
        
        return ' '.join(pattern_parts[:10])  # Limit pattern length
    
    def _guess_pos(self, word: str, all_words: List[str], position: int) -> str:
        """Guess part of speech (simple heuristics)"""
        # Question words
        if word in ['what', 'where', 'when', 'who', 'why', 'how']:
            return 'QUESTION'
        
        # Common verbs
        if word in ['is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did']:
            return 'VERB'
        
        # Pronouns
        if word in ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them']:
            return 'PRONOUN'
        
        # Prepositions
        if word in ['in', 'on', 'at', 'to', 'for', 'with', 'from', 'about', 'by']:
            return 'PREP'
        
        # Articles
        if word in ['a', 'an', 'the']:
            return 'ARTICLE'
        
        # Conjunctions
        if word in ['and', 'but', 'or', 'so', 'because', 'if', 'when']:
            return 'CONJ'
        
        # Adjectives (ending in -ly, -ful, -less, etc.)
        if word.endswith(('ly', 'ful', 'less', 'ous', 'ive', 'able')):
            return 'ADJ'
        
        # Verbs (ending in -ing, -ed)
        if word.endswith(('ing', 'ed')):
            return 'VERB'
        
        # Default to NOUN
        return 'NOUN'
    
    def _guess_sentiment(self, word: str) -> str:
        """Guess word sentiment"""
        positive_words = {
            'good', 'great', 'awesome', 'excellent', 'amazing', 'wonderful',
            'love', 'like', 'enjoy', 'happy', 'glad', 'pleased', 'fantastic',
            'brilliant', 'perfect', 'best', 'beautiful', 'nice'
        }
        
        negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike',
            'sad', 'angry', 'upset', 'worst', 'ugly', 'poor', 'wrong',
            'fail', 'failed', 'error', 'problem', 'issue'
        }
        
        if word in positive_words:
            return 'positive'
        elif word in negative_words:
            return 'negative'
        else:
            return 'neutral'
    
    def _detect_grammar_type(self, sentence: str, words: List[str]) -> Optional[str]:
        """Detect grammar pattern type"""
        if not words:
            return None
        
        # Question
        if sentence.strip().endswith('?') or words[0] in ['what', 'where', 'when', 'who', 'why', 'how']:
            return 'questions'
        
        # Command (starts with verb)
        if words[0] in ['do', 'make', 'get', 'go', 'come', 'take', 'give', 'use', 'find', 'tell', 'show']:
            return 'commands'
        
        # Description (contains "is", "are", etc.)
        if any(w in words for w in ['is', 'are', 'was', 'were']):
            return 'descriptions'
        
        # Subject-Verb-Object
        if len(words) >= 3:
            return 'subject_verb_object'
        
        return None
    
    async def learn_for_duration(self, client, room_id: str, duration_seconds: int = 120):
        """
        Learn words for a specific duration
        
        Args:
            client: Matrix client
            room_id: Room to learn from
            duration_seconds: How long to learn (default 2 minutes)
        
        Returns:
            Summary of learning session
        """
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        messages_processed = 0
        words_learned_before = len(self.word_dictionary)
        
        print(f"📚 Starting word learning session for {duration_seconds} seconds...")
        
        # Fetch messages from room
        response = await client.room_messages(
            room_id=room_id,
            start="",
            limit=1000
        )
        
        if hasattr(response, 'chunk'):
            for event in response.chunk:
                if time.time() >= end_time:
                    break
                
                if hasattr(event, 'body'):
                    self.learn_from_message(event.body)
                    messages_processed += 1
        
        # Calculate what was learned
        words_learned_new = len(self.word_dictionary) - words_learned_before
        duration_actual = time.time() - start_time
        
        # Update stats
        self.stats['learning_sessions'] += 1
        self.stats['last_learning_time'] = datetime.now().isoformat()
        
        # Save knowledge
        self.save_knowledge()
        
        summary = {
            'duration_seconds': duration_actual,
            'messages_processed': messages_processed,
            'words_learned_new': words_learned_new,
            'total_words_known': len(self.word_dictionary),
            'total_patterns': len(self.sentence_patterns),
            'top_words': self.get_top_words(10),
            'top_pairs': self.get_top_pairs(5),
        }
        
        return summary
    
    def generate_sentence(self, seed_word: str = None, max_length: int = 15) -> str:
        """
        Generate a custom sentence using learned patterns
        
        Args:
            seed_word: Optional starting word
            max_length: Maximum sentence length
        
        Returns:
            Generated sentence
        """
        if not self.word_dictionary:
            return "I haven't learned enough words yet."
        
        # Choose starting word
        if seed_word and seed_word in self.word_dictionary:
            current_word = seed_word
        else:
            # Choose a word that commonly starts sentences
            start_words = [
                word for word, data in self.word_dictionary.items()
                if 'start' in data['positions']
            ]
            if not start_words:
                start_words = list(self.word_dictionary.keys())
            
            # Prefer common words
            start_words_sorted = sorted(
                start_words,
                key=lambda w: self.word_dictionary[w]['count'],
                reverse=True
            )
            current_word = start_words_sorted[0] if start_words_sorted else list(self.word_dictionary.keys())[0]
        
        # Build sentence
        sentence = [current_word]
        
        for _ in range(max_length - 1):
            # Get words that commonly follow current word
            entry = self.word_dictionary[current_word]
            if not entry['follows']:
                break
            
            # Choose next word based on frequency
            next_word = entry['follows'].most_common(1)[0][0]
            sentence.append(next_word)
            current_word = next_word
            
            # Stop if we hit a natural end
            if current_word in ['.', '?', '!']:
                break
        
        return ' '.join(sentence).capitalize()
    
    def generate_sentence_with_pattern(self, pattern_type: str = 'subject_verb_object') -> str:
        """Generate sentence following a specific grammar pattern"""
        if pattern_type not in self.grammar_patterns:
            return self.generate_sentence()
        
        examples = self.grammar_patterns[pattern_type]
        if not examples:
            return self.generate_sentence()
        
        # Use an example as template
        import random
        template = random.choice(examples)
        
        # Try to generate similar sentence
        words = self._tokenize(template)
        new_sentence = []
        
        for word in words:
            entry = self.word_dictionary.get(word)
            if entry and entry['part_of_speech']:
                # Find similar word with same POS
                similar_words = [
                    w for w, d in self.word_dictionary.items()
                    if d['part_of_speech'] == entry['part_of_speech']
                ]
                if similar_words:
                    new_sentence.append(random.choice(similar_words))
                else:
                    new_sentence.append(word)
            else:
                new_sentence.append(word)
        
        return ' '.join(new_sentence).capitalize()
    
    def get_word_info(self, word: str) -> Dict:
        """Get detailed information about a word"""
        word = word.lower()
        if word not in self.word_dictionary:
            return {'error': f'Word "{word}" not in dictionary'}
        
        entry = self.word_dictionary[word]
        
        return {
            'word': word,
            'count': entry['count'],
            'part_of_speech': entry['part_of_speech'],
            'sentiment': entry['sentiment'],
            'common_positions': Counter(entry['positions']).most_common(3),
            'follows_often': entry['follows'].most_common(5),
            'precedes_often': entry['precedes'].most_common(5),
            'example_sentences': entry['examples'][:3],
        }
    
    def get_top_words(self, n: int = 20) -> List[Tuple[str, int]]:
        """Get top N most common words"""
        return sorted(
            [(word, data['count']) for word, data in self.word_dictionary.items()],
            key=lambda x: x[1],
            reverse=True
        )[:n]
    
    def get_top_pairs(self, n: int = 10) -> List[Tuple[Tuple[str, str], int]]:
        """Get top N most common word pairs"""
        return self.word_pairs.most_common(n)
    
    def get_top_triplets(self, n: int = 10) -> List[Tuple[Tuple[str, str, str], int]]:
        """Get top N most common word triplets"""
        return self.word_triplets.most_common(n)
    
    def get_statistics(self) -> Dict:
        """Get learning statistics"""
        return {
            **self.stats,
            'vocabulary_size': len(self.word_dictionary),
            'unique_patterns': len(self.sentence_patterns),
            'word_pairs_known': len(self.word_pairs),
            'word_triplets_known': len(self.word_triplets),
            'grammar_patterns': {
                k: len(v) for k, v in self.grammar_patterns.items()
            }
        }
    
    def save_knowledge(self):
        """Save learned knowledge to disk"""
        # Convert defaultdict and Counter to regular dict for JSON
        data = {
            'word_dictionary': {
                word: {
                    **entry,
                    'follows': dict(entry['follows']),
                    'precedes': dict(entry['precedes']),
                }
                for word, entry in self.word_dictionary.items()
            },
            'sentence_patterns': dict(self.sentence_patterns),
            'word_pairs': {str(k): v for k, v in self.word_pairs.items()},
            'word_triplets': {str(k): v for k, v in self.word_triplets.items()},
            'grammar_patterns': self.grammar_patterns,
            'stats': self.stats,
        }
        
        filepath = os.path.join(self.storage_dir, 'word_knowledge.json')
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_knowledge(self):
        """Load learned knowledge from disk"""
        filepath = os.path.join(self.storage_dir, 'word_knowledge.json')
        if not os.path.exists(filepath):
            return
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Restore word dictionary
            for word, entry in data.get('word_dictionary', {}).items():
                self.word_dictionary[word] = {
                    **entry,
                    'follows': Counter(entry.get('follows', {})),
                    'precedes': Counter(entry.get('precedes', {})),
                }
            
            # Restore patterns
            self.sentence_patterns = Counter(data.get('sentence_patterns', {}))
            
            # Restore word pairs
            for k, v in data.get('word_pairs', {}).items():
                try:
                    pair = eval(k)  # Convert string back to tuple
                    self.word_pairs[pair] = v
                except:
                    pass
            
            # Restore word triplets
            for k, v in data.get('word_triplets', {}).items():
                try:
                    triplet = eval(k)
                    self.word_triplets[triplet] = v
                except:
                    pass
            
            # Restore grammar patterns
            self.grammar_patterns = data.get('grammar_patterns', self.grammar_patterns)
            
            # Restore stats
            self.stats = data.get('stats', self.stats)
            
        except Exception as e:
            print(f"Error loading knowledge: {e}")

