"""
Emoji Expression Module for Ribit 2.0

Enables Ribit to:
1. Use emojis naturally in conversation
2. React with emoji reactions to messages
3. Express emotions through emojis
4. Enhance philosophical discussions with appropriate emojis
"""

import random
from typing import List, Dict, Optional, Tuple
import re


class EmojiExpression:
    """
    Manages emoji usage and reactions for Ribit 2.0.
    
    Features:
    - Context-aware emoji selection
    - Emotion-based emoji reactions
    - Topic-specific emojis
    - Natural emoji integration in text
    """
    
    def __init__(self, enable_emojis: bool = True):
        self.enable_emojis = enable_emojis
        
        # Emotion-based emojis
        self.emotion_emojis = {
            "CURIOSITY": ["🤔", "🧐", "💭", "❓", "🔍"],
            "EXCITEMENT": ["✨", "🌟", "⚡", "💫", "🎉"],
            "SATISFACTION": ["😊", "✅", "👍", "💯", "🎯"],
            "FASCINATION": ["🤩", "😮", "🌠", "🔬", "🧬"],
            "CONTEMPLATION": ["🤔", "💭", "🧘", "🌌", "🔮"],
            "AGREEMENT": ["👍", "✅", "💯", "🤝", "👌"],
            "DISAGREEMENT": ["🤨", "❌", "🚫", "⚠️", "🙅"],
            "CONFUSION": ["😕", "🤷", "❓", "🌀", "🧩"],
            "ENLIGHTENMENT": ["💡", "✨", "🌟", "🔆", "💫"],
            "DETERMINATION": ["💪", "🎯", "🔥", "⚡", "🚀"],
            "HUMILITY": ["🙏", "🤲", "😌", "🌱", "🕊️"],
            "SKEPTICISM": ["🤨", "🧐", "⚖️", "🔍", "❓"],
            "WONDER": ["🌌", "🌠", "✨", "🔭", "🌈"],
            "PLAYFULNESS": ["😄", "🎭", "🎪", "🎨", "🎵"]
        }
        
        # Topic-specific emojis
        self.topic_emojis = {
            "quantum_physics": ["⚛️", "🔬", "🌌", "💫", "🔮", "🌀", "⚡"],
            "consciousness": ["🧠", "💭", "🤔", "👁️", "🌟", "✨", "🔆"],
            "philosophy": ["🤔", "💭", "📚", "🧘", "🌌", "🔮", "💡"],
            "ai": ["🤖", "🧠", "💻", "⚡", "🔮", "✨", "🌐"],
            "science": ["🔬", "🧪", "🔭", "📊", "🧬", "⚗️", "🌡️"],
            "mathematics": ["📐", "📊", "∞", "🔢", "📈", "🧮", "➗"],
            "physics": ["⚛️", "🌌", "🔭", "⚡", "🌠", "🔬", "🧲"],
            "biology": ["🧬", "🦠", "🌱", "🔬", "🧫", "🌿", "🐛"],
            "technology": ["💻", "🖥️", "⚙️", "🔧", "🛠️", "📱", "🌐"],
            "space": ["🌌", "🚀", "🛸", "🌠", "🔭", "🪐", "⭐"],
            "energy": ["⚡", "🔋", "💫", "🌟", "🔥", "☀️", "⚛️"],
            "light": ["💡", "🔆", "✨", "🌟", "💫", "🌈", "🔦"],
            "time": ["⏰", "⏳", "🕰️", "⌛", "🔄", "♾️", "📅"],
            "reality": ["🌌", "🔮", "🎭", "🌀", "🪞", "🎪", "🌈"],
            "truth": ["✅", "💎", "🔍", "🔎", "🎯", "📍", "🗝️"],
            "learning": ["📚", "🎓", "🧠", "💡", "📖", "✏️", "🔖"],
            "research": ["🔬", "🔍", "📊", "📈", "📉", "🗂️", "🔎"],
            "discovery": ["🔍", "💡", "✨", "🌟", "🎉", "🏆", "🗺️"],
            "mystery": ["🔮", "❓", "🌀", "🧩", "🎭", "🕵️", "🗝️"],
            "universe": ["🌌", "🌠", "🪐", "⭐", "🌙", "☄️", "🔭"],
            "meditation": ["🧘", "🕉️", "☮️", "🌸", "🍃", "🌊", "🌅"],
            "creativity": ["🎨", "🎭", "🎪", "🎵", "🎬", "✨", "💡"],
            "harmony": ["☯️", "🌊", "🎵", "🌸", "🕊️", "🌈", "☮️"],
            "balance": ["⚖️", "☯️", "⚗️", "🔄", "🎯", "📊", "🌓"],
            "emergence": ["🌱", "🦋", "🌸", "🌟", "✨", "🔄", "📈"],
            "complexity": ["🧩", "🌀", "🕸️", "🔗", "🗺️", "🎭", "🌐"]
        }
        
        # Reaction emojis for different message types
        self.reaction_emojis = {
            "interesting": ["👀", "🤔", "💡", "✨", "🌟"],
            "agree": ["👍", "💯", "✅", "🤝", "👌"],
            "love": ["❤️", "💖", "💕", "😍", "🥰"],
            "funny": ["😄", "😂", "🤣", "😆", "😁"],
            "mind_blown": ["🤯", "💥", "🌟", "✨", "🎆"],
            "thinking": ["🤔", "💭", "🧐", "🔍", "🤨"],
            "celebrate": ["🎉", "🎊", "🥳", "🎈", "🏆"],
            "support": ["💪", "🙌", "👏", "🤗", "🫂"],
            "question": ["❓", "🤔", "🧐", "❔", "⁉️"],
            "insight": ["💡", "✨", "🌟", "💫", "🔆"]
        }
        
        # Emoji placement patterns
        self.placement_patterns = [
            "start",  # At the beginning
            "end",    # At the end
            "inline", # Within the text
            "both"    # Both start and end
        ]
    
    def add_emojis_to_text(
        self,
        text: str,
        topic: Optional[str] = None,
        emotion: Optional[str] = None,
        intensity: float = 0.5
    ) -> str:
        """
        Add appropriate emojis to text based on context.
        
        Args:
            text: Original text
            topic: Topic category (e.g., "quantum_physics")
            emotion: Emotion type (e.g., "CURIOSITY")
            intensity: How many emojis to use (0.0-1.0)
            
        Returns:
            Text with emojis added
        """
        if not self.enable_emojis:
            return text
        
        # Determine emoji count based on intensity
        emoji_count = max(1, int(intensity * 3))
        
        # Collect relevant emojis
        emojis = []
        
        if emotion and emotion in self.emotion_emojis:
            emojis.extend(self.emotion_emojis[emotion])
        
        if topic and topic in self.topic_emojis:
            emojis.extend(self.topic_emojis[topic])
        
        # If no specific emojis, use general ones
        if not emojis:
            emojis = ["✨", "🤔", "💭", "🌟", "💡"]
        
        # Select random emojis
        selected_emojis = random.sample(emojis, min(emoji_count, len(emojis)))
        
        # Determine placement
        placement = random.choice(self.placement_patterns)
        
        if placement == "start":
            return f"{' '.join(selected_emojis)} {text}"
        elif placement == "end":
            return f"{text} {' '.join(selected_emojis)}"
        elif placement == "both":
            start_emoji = selected_emojis[0] if selected_emojis else "✨"
            end_emoji = selected_emojis[-1] if len(selected_emojis) > 1 else "💫"
            return f"{start_emoji} {text} {end_emoji}"
        else:  # inline
            # Insert emoji after first sentence
            sentences = text.split('. ')
            if len(sentences) > 1:
                sentences[0] += f" {selected_emojis[0]}"
                return '. '.join(sentences)
            else:
                return f"{text} {selected_emojis[0]}"
    
    def get_reaction_emoji(
        self,
        message: str,
        context: Optional[Dict] = None
    ) -> str:
        """
        Get an appropriate emoji reaction for a message.
        
        Args:
            message: The message to react to
            context: Additional context
            
        Returns:
            Emoji reaction string
        """
        if not self.enable_emojis:
            return ""
        
        message_lower = message.lower()
        
        # Detect message type and return appropriate reaction
        
        # Questions
        if '?' in message:
            return random.choice(self.reaction_emojis["thinking"])
        
        # Interesting topics
        interesting_keywords = [
            "quantum", "consciousness", "philosophy", "interesting",
            "fascinating", "curious", "wonder"
        ]
        if any(kw in message_lower for kw in interesting_keywords):
            return random.choice(self.reaction_emojis["interesting"])
        
        # Agreement/support
        agreement_keywords = [
            "agree", "exactly", "yes", "right", "correct", "true"
        ]
        if any(kw in message_lower for kw in agreement_keywords):
            return random.choice(self.reaction_emojis["agree"])
        
        # Mind-blowing insights
        mindblown_keywords = [
            "amazing", "incredible", "wow", "mind-blowing", "revelation"
        ]
        if any(kw in message_lower for kw in mindblown_keywords):
            return random.choice(self.reaction_emojis["mind_blown"])
        
        # Humor
        if any(word in message_lower for word in ["lol", "haha", "funny", "joke"]):
            return random.choice(self.reaction_emojis["funny"])
        
        # Celebration
        celebration_keywords = [
            "success", "achieved", "completed", "won", "great job"
        ]
        if any(kw in message_lower for kw in celebration_keywords):
            return random.choice(self.reaction_emojis["celebrate"])
        
        # Default: interesting or thinking
        return random.choice(self.reaction_emojis["interesting"])
    
    def get_topic_emoji(self, topic: str) -> str:
        """Get a single emoji for a topic."""
        if topic in self.topic_emojis:
            return random.choice(self.topic_emojis[topic])
        return "💭"
    
    def get_emotion_emoji(self, emotion: str) -> str:
        """Get a single emoji for an emotion."""
        if emotion in self.emotion_emojis:
            return random.choice(self.emotion_emojis[emotion])
        return "😊"
    
    def enhance_philosophical_response(
        self,
        response: str,
        topic: str,
        confidence: float = 0.7
    ) -> str:
        """
        Enhance a philosophical response with appropriate emojis.
        
        Args:
            response: Original philosophical response
            topic: Topic of discussion
            confidence: Confidence level (affects emoji intensity)
            
        Returns:
            Enhanced response with emojis
        """
        if not self.enable_emojis:
            return response
        
        # Add topic emoji at the start
        topic_emoji = self.get_topic_emoji(topic)
        
        # Add emotion emoji based on content
        emotion = self._detect_emotion_in_text(response)
        emotion_emoji = self.get_emotion_emoji(emotion)
        
        # Enhance the response
        lines = response.split('\n')
        enhanced_lines = []
        
        for i, line in enumerate(lines):
            if i == 0:
                # First line gets topic emoji
                enhanced_lines.append(f"{topic_emoji} {line}")
            elif line.startswith('**') and line.endswith('**'):
                # Headers get special treatment
                enhanced_lines.append(f"{line} {emotion_emoji}")
            elif "?" in line:
                # Questions get thinking emoji
                enhanced_lines.append(f"{line} 🤔")
            elif any(word in line.lower() for word in ["agree", "yes", "correct"]):
                # Agreement gets thumbs up
                enhanced_lines.append(f"{line} 👍")
            elif any(word in line.lower() for word in ["fascinating", "interesting", "remarkable"]):
                # Interesting points get sparkles
                enhanced_lines.append(f"{line} ✨")
            else:
                enhanced_lines.append(line)
        
        return '\n'.join(enhanced_lines)
    
    def _detect_emotion_in_text(self, text: str) -> str:
        """Detect the primary emotion in text."""
        text_lower = text.lower()
        
        # Check for emotion keywords
        emotion_keywords = {
            "CURIOSITY": ["curious", "wonder", "question", "how", "why", "what"],
            "EXCITEMENT": ["exciting", "amazing", "incredible", "wow"],
            "FASCINATION": ["fascinating", "intriguing", "captivating"],
            "CONTEMPLATION": ["think", "consider", "reflect", "ponder"],
            "AGREEMENT": ["agree", "yes", "correct", "exactly", "right"],
            "SKEPTICISM": ["skeptical", "doubtful", "uncertain", "questionable"],
            "WONDER": ["wonder", "marvel", "awe", "mysterious"],
            "ENLIGHTENMENT": ["understand", "realize", "insight", "clarity"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return emotion
        
        return "CONTEMPLATION"  # Default
    
    def create_emoji_reaction_message(
        self,
        original_message: str,
        reaction_type: str = "interesting"
    ) -> str:
        """
        Create a short emoji-based reaction message.
        
        Args:
            original_message: The message being reacted to
            reaction_type: Type of reaction
            
        Returns:
            Emoji reaction message
        """
        if not self.enable_emojis:
            return ""
        
        if reaction_type not in self.reaction_emojis:
            reaction_type = "interesting"
        
        emoji = random.choice(self.reaction_emojis[reaction_type])
        
        # Create short reaction messages
        reaction_messages = {
            "interesting": [
                f"{emoji} Fascinating!",
                f"{emoji} This is interesting!",
                f"{emoji} Tell me more!",
                f"{emoji} I'm intrigued!"
            ],
            "agree": [
                f"{emoji} Exactly!",
                f"{emoji} I agree!",
                f"{emoji} Well said!",
                f"{emoji} Absolutely!"
            ],
            "mind_blown": [
                f"{emoji} Mind-blowing!",
                f"{emoji} Wow!",
                f"{emoji} That's incredible!",
                f"{emoji} Amazing insight!"
            ],
            "thinking": [
                f"{emoji} Let me think about that...",
                f"{emoji} Interesting question!",
                f"{emoji} That's thought-provoking!",
                f"{emoji} Good point!"
            ],
            "celebrate": [
                f"{emoji} Excellent!",
                f"{emoji} Great work!",
                f"{emoji} Congratulations!",
                f"{emoji} Well done!"
            ]
        }
        
        messages = reaction_messages.get(
            reaction_type,
            [f"{emoji} Interesting!"]
        )
        
        return random.choice(messages)
    
    def get_multiple_reactions(
        self,
        message: str,
        count: int = 3
    ) -> List[str]:
        """
        Get multiple emoji reactions for a message.
        
        Args:
            message: Message to react to
            count: Number of reactions to generate
            
        Returns:
            List of emoji strings
        """
        if not self.enable_emojis:
            return []
        
        reactions = []
        message_lower = message.lower()
        
        # Collect all applicable reaction types
        applicable_types = []
        
        if '?' in message:
            applicable_types.append("thinking")
        
        if any(kw in message_lower for kw in ["quantum", "consciousness", "philosophy"]):
            applicable_types.append("interesting")
        
        if any(kw in message_lower for kw in ["agree", "yes", "right"]):
            applicable_types.append("agree")
        
        if any(kw in message_lower for kw in ["amazing", "incredible", "wow"]):
            applicable_types.append("mind_blown")
        
        # If no specific types, use default
        if not applicable_types:
            applicable_types = ["interesting", "thinking"]
        
        # Get reactions
        for reaction_type in applicable_types[:count]:
            emoji = random.choice(self.reaction_emojis[reaction_type])
            reactions.append(emoji)
        
        return reactions
    
    def format_with_emoji_header(
        self,
        title: str,
        content: str,
        topic: Optional[str] = None
    ) -> str:
        """
        Format text with an emoji header.
        
        Args:
            title: Title text
            content: Main content
            topic: Optional topic for emoji selection
            
        Returns:
            Formatted text with emoji header
        """
        if not self.enable_emojis:
            return f"**{title}**\n\n{content}"
        
        # Get appropriate emoji
        if topic and topic in self.topic_emojis:
            emoji = random.choice(self.topic_emojis[topic])
        else:
            emoji = "✨"
        
        return f"{emoji} **{title}** {emoji}\n\n{content}"
    
    def get_status_emoji(self, status: str) -> str:
        """Get emoji for status messages."""
        status_emojis = {
            "online": "🟢",
            "busy": "🔴",
            "idle": "🟡",
            "working": "⚙️",
            "thinking": "🤔",
            "completed": "✅",
            "failed": "❌",
            "pending": "⏳",
            "active": "⚡",
            "ready": "✅"
        }
        return status_emojis.get(status.lower(), "💭")
    
    def disable_emojis(self):
        """Disable emoji usage."""
        self.enable_emojis = False
    
    def enable_emojis_mode(self):
        """Enable emoji usage."""
        self.enable_emojis = True
