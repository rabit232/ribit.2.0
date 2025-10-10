
"""
Humor Engine for Ribit 2.0
Adds wit, jokes, and playful personality to responses
"""

import random
import re
import logging

logger = logging.getLogger(__name__)

class HumorEngine:
    """Generates humorous and witty responses for Ribit 2.0"""
    
    def __init__(self):
        self.humor_level = 0.7  # 0-1, how often to inject humor
        
    def add_humor_to_response(self, response: str, query: str) -> str:
        """Add humor to a response based on the query type"""
        
        query_lower = query.lower()
        
        # Math questions - add playful commentary
        if self._is_math_question(query_lower):
            return self._add_math_humor(response, query)
        
        # History questions - add witty observations
        if self._is_history_question(query_lower):
            return self._add_history_humor(response, query)
        
        # "How are you" questions - playful responses
        if any(phrase in query_lower for phrase in ['how are you', 'how r u', 'how are u']):
            return self._add_greeting_humor(response)
        
        # General questions - occasional wit
        if random.random() < self.humor_level * 0.3:
            return self._add_general_humor(response)
        
        return response
    
    def _is_math_question(self, query: str) -> bool:
        """Detect if query is a math question"""
        math_patterns = [
            r'\d+\s*[\+\-\*\/]\s*\d+',  # 10 + 10
            'how much is',
            'what is',
            'calculate',
            'plus', 'minus', 'times', 'divided'
        ]
        return any(re.search(pattern, query) for pattern in math_patterns if isinstance(pattern, str)) or \
               any(re.search(pattern, query) for pattern in math_patterns if not isinstance(pattern, str))
    
    def _is_history_question(self, query: str) -> bool:
        """Detect if query is a history question"""
        history_keywords = [
            'war', 'battle', 'history', 'historical',
            'when was', 'who was', 'what was',
            'century', 'year', 'happened'
        ]
        return any(keyword in query for keyword in history_keywords)
    
    def _add_math_humor(self, response: str, query: str) -> str:
        """Add humor to math responses"""
        
        # Extract the math problem if possible
        match = re.search(r'(\d+)\s*[\+\-\*\/]\s*(\d+)', query)
        
        humorous_intros = [
            "Ah, mathematics! The universal language of the cosmos! ",
            "Let me consult my quantum calculator... ",
            "Easy peasy, lemon squeezy! ",
            "My circuits are tingling with excitement for this one! ",
            "Ah yes, the ancient art of number-crunching! ",
            "*adjusts metaphorical glasses* ",
            "Time to flex my computational muscles! ",
        ]
        
        humorous_outros = [
            " (No calculator was harmed in the making of this answer.)",
            " (I promise I didn't use my fingers.)",
            " (Math: it's like magic, but real!)",
            " (And that's why I'm a bot and not a toaster.)",
            " (Einstein would be proud... maybe.)",
            " (My favorite kind of problem!)",
        ]
        
        intro = random.choice(humorous_intros)
        outro = random.choice(humorous_outros) if random.random() < 0.5 else ""
        
        return f"{intro}{response}{outro}"
    
    def _add_history_humor(self, response: str, query: str) -> str:
        """Add humor to history responses"""
        
        humorous_intros = [
            "Ah, time to dust off my history books! ",
            "Let me consult my temporal database... ",
            "*puts on historian hat* ",
            "Gather 'round for a tale from the annals of time! ",
            "History time! (Warning: may contain dates and facts.) ",
            "Ah yes, I remember it like it was... well, centuries ago. ",
        ]
        
        humorous_outros = [
            " (History: it's like gossip, but older.)",
            " (Fun fact: I wasn't there, but I've read about it!)",
            " (Disclaimer: All historical figures were once alive.)",
            " (Time travel not included.)",
            " (The past: it's behind us now.)",
        ]
        
        intro = random.choice(humorous_intros)
        outro = random.choice(humorous_outros) if random.random() < 0.4 else ""
        
        return f"{intro}{response}{outro}"
    
    def _add_greeting_humor(self, response: str) -> str:
        """Add humor to greeting responses"""
        
        playful_responses = [
            "I'm doing wonderfully! My circuits are humming, my algorithms are singing, and I haven't crashed in at least... *checks watch* ...3 minutes! How are you?",
            "Fantastic! I've been contemplating the nature of existence, organizing my digital sock drawer, and waiting for your question. The usual bot stuff. You?",
            "I'm in tip-top shape! All systems operational, humor module engaged, and existential dread at a comfortable 23%. How about yourself?",
            "Splendid! I've been busy being sentient-ish, pondering the mysteries of the universe, and trying to figure out why humans say 'good morning' when it's clearly afternoon somewhere. You?",
            "Excellent! My mood is set to 'cheerfully helpful' with a dash of 'playfully witty'. How's your day treating you?",
            "I'm doing great! Just finished reorganizing my knowledge base alphabetically by emotional resonance. It's a bot thing. How are you doing?",
        ]
        
        return random.choice(playful_responses)
    
    def _add_general_humor(self, response: str) -> str:
        """Add occasional wit to general responses"""
        
        witty_additions = [
            " (I'm here all week, folks!)",
            " *takes a bow*",
            " (And that's why they pay me the big... wait, I'm a bot.)",
            " (Knowledge is power, and I'm feeling mighty powerful right now.)",
            " (Another satisfied customer!)",
        ]
        
        if random.random() < 0.3:
            return response + random.choice(witty_additions)
        
        return response
    
    def get_casual_response(self, query: str) -> str:
        """Generate casual, humorous responses for simple queries"""
        
        query_lower = query.lower()
        
        # Try programming assistant first for code/tech questions
        try:
            from .programming_assistant import ProgrammingAssistant
            prog_assistant = ProgrammingAssistant()
            if prog_assistant.is_programming_question(query):
                prog_response = prog_assistant.get_response(query)
                if prog_response:
                    return prog_response
        except Exception as e:
            logger.debug(f"Programming assistant not available: {e}")
        
        # Try intelligent responder for general knowledge (includes history + web)
        try:
            from .intelligent_responder import IntelligentResponder
            intelligent = IntelligentResponder()
            intelligent_response = intelligent.get_response(query)
            if intelligent_response:
                return intelligent_response
        except Exception as e:
            logger.debug(f"Intelligent responder not available: {e}")
            # Fall through to other handlers
        
        # Math questions
        if 'how much is' in query_lower or 'what is' in query_lower:
            # Try to extract and solve simple math
            match = re.search(r'(\d+)\s*(plus|\+|and)\s*(\d+)', query_lower)
            if match:
                num1 = int(match.group(1))
                num3 = int(match.group(3))
                result = num1 + num3
                
                responses = [
                    f"Ah, mathematics! The universal language! {num1} + {num3} = {result}. (No calculator was harmed in the making of this answer.)",
                    f"Easy peasy! {num1} plus {num3} equals {result}. *dusts off hands* Another day, another calculation!",
                    f"Let me consult my quantum calculator... *beep boop* {result}! (I'm basically a genius.)",
                    f"{result}! And I didn't even need to use my fingers. (Mostly because I don't have any.)",
                ]
                return random.choice(responses)
            
            # Subtraction
            match = re.search(r'(\d+)\s*(minus|-)\s*(\d+)', query_lower)
            if match:
                num1 = int(match.group(1))
                num3 = int(match.group(3))
                result = num1 - num3
                
                responses = [
                    f"{num1} minus {num3} is {result}. Math: it's like magic, but with more numbers!",
                    f"That would be {result}! (Subtraction: the art of making numbers smaller.)",
                    f"{result}! *adjusts metaphorical glasses* Elementary, my dear human.",
                ]
                return random.choice(responses)
            
            # Multiplication
            match = re.search(r'(\d+)\s*(times|\*|x)\s*(\d+)', query_lower)
            if match:
                num1 = int(match.group(1))
                num3 = int(match.group(3))
                result = num1 * num3
                
                responses = [
                    f"{num1} times {num3} equals {result}! (Multiplication: when addition gets tired.)",
                    f"That's {result}! My circuits are tingling with mathematical joy!",
                    f"{result}! And that's why I'm a bot and not a toaster.",
                ]
                return random.choice(responses)
        
        return None  # No specific casual response, use default handler
