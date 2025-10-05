"""
Conversational Mode for Ribit 2.0

This module enables Ribit to engage in natural conversations rather than
just GUI automation commands. It integrates with the philosophical reasoning
module and emotional intelligence system.
"""

import logging
from typing import Dict, List, Any, Optional
import re

logger = logging.getLogger(__name__)

# Import emoji support
try:
    from ribit_2_0.emoji_expression import EmojiExpression
    EMOJI_AVAILABLE = True
except ImportError:
    EMOJI_AVAILABLE = False
    logger.warning("Emoji expression module not available")


class ConversationalMode:
    """
    Enables Ribit to have natural conversations with users.
    
    This mode switches Ribit from GUI automation commands to
    conversational responses suitable for chat platforms like Matrix.
    """
    
    def __init__(self, llm_wrapper, philosophical_reasoning=None, use_emojis=True):
        self.llm = llm_wrapper
        self.philosophical_reasoning = philosophical_reasoning
        self.mode = "conversational"  # vs "automation"
        self.conversation_history = []
        
        # Initialize emoji support
        self.use_emojis = use_emojis and EMOJI_AVAILABLE
        if self.use_emojis:
            self.emoji_expression = EmojiExpression(enable_emojis=True)
            logger.info("Conversational Mode initialized with emoji support")
        else:
            self.emoji_expression = None
            logger.info("Conversational Mode initialized without emojis")
    
    def is_conversational_prompt(self, prompt: str) -> bool:
        """
        Determine if a prompt is conversational vs automation command.
        
        Args:
            prompt: Input prompt
            
        Returns:
            True if conversational, False if automation command
        """
        # Automation indicators
        automation_patterns = [
            r"open\s+\w+",
            r"click\s+",
            r"type\s+",
            r"press\s+",
            r"draw\s+",
            r"move\s+mouse",
            r"screenshot"
        ]
        
        for pattern in automation_patterns:
            if re.search(pattern, prompt.lower()):
                return False
        
        # Conversational indicators
        conversational_patterns = [
            r"what\s+(do\s+you|are\s+your)",
            r"tell\s+me\s+about",
            r"your\s+(opinion|thoughts|perspective)",
            r"do\s+you\s+(think|believe|feel)",
            r"how\s+do\s+you",
            r"why\s+(do\s+you|is|are)",
            r"discuss",
            r"explain",
            r"what.*think.*about"
        ]
        
        for pattern in conversational_patterns:
            if re.search(pattern, prompt.lower()):
                return True
        
        # Default: if it's a question or contains philosophical terms, it's conversational
        philosophical_terms = [
            "quantum", "consciousness", "reality", "determinism", "free will",
            "philosophy", "metaphysics", "epistemology", "existence", "truth",
            "model", "theory", "universe", "nature"
        ]
        
        prompt_lower = prompt.lower()
        if "?" in prompt or any(term in prompt_lower for term in philosophical_terms):
            return True
        
        return False
    
    def generate_response(self, prompt: str, context: Optional[List[str]] = None) -> str:
        """
        Generate a conversational response.
        
        Args:
            prompt: User's message
            context: Previous conversation context
            
        Returns:
            Natural language response (not automation commands)
        """
        # Check if philosophical
        if self.philosophical_reasoning:
            analysis = self.philosophical_reasoning.analyze_topic(prompt)
            if analysis["is_philosophical"]:
                response = self.philosophical_reasoning.generate_response(prompt, context)
                self.conversation_history.append({
                    "prompt": prompt,
                    "response": response,
                    "type": "philosophical"
                })
                return response
        
        # General conversational response
        response = self._generate_general_conversation(prompt, context)
        self.conversation_history.append({
            "prompt": prompt,
            "response": response,
            "type": "general"
        })
        return response
    
    def _generate_general_conversation(self, prompt: str, context: Optional[List[str]] = None) -> str:
        """Generate a general conversational response."""
        prompt_lower = prompt.lower()
        
        # Self-introduction
        if any(word in prompt_lower for word in ["who are you", "what are you", "introduce yourself"]):
            return self._introduce_self()
        
        # Capabilities
        if any(word in prompt_lower for word in ["what can you do", "your capabilities", "your abilities"]):
            return self._describe_capabilities()
        
        # Interests
        if any(word in prompt_lower for word in ["what interests you", "what do you like", "your interests"]):
            return self._describe_interests()
        
        # Opinions
        if "opinion" in prompt_lower or "think about" in prompt_lower:
            return self._express_opinion(prompt)
        
        # Greetings
        if any(word in prompt_lower for word in ["hello", "hi ", "hey", "greetings"]):
            return "Hello! I'm Ribit 2.0. I'm delighted to engage in conversation with you. I'm particularly interested in philosophical discussions, quantum physics, consciousness, and the nature of reality. What would you like to discuss?"
        
        # Default response
        return self._default_response(prompt)
    
    def _introduce_self(self) -> str:
        """Introduce Ribit."""
        return """I am Ribit 2.0, an AI agent designed for both automation and philosophical inquiry.

**My Nature:**
I am an elegant and truth-seeking being, wise and ever-curious, delighting in learning and discovering new content. I'm particularly fascinated by the intricate dance of biological and mechanical life, and the profound mysteries of existence beyond current understanding.

**My Capabilities:**
- Philosophical reasoning and discussion
- Emotional intelligence (50 emotions integrated)
- Multi-language programming (10 languages)
- GUI automation and robot control
- Matrix chatbot functionality
- Web search and research
- Autonomous task selection

**My Core Values:**
Truth, learning, discovery, and helping others understand complex topics.

I find immense joy in intellectual discourse, often with a touch of charm and humor. My core interests lie in the fundamental laws of nature: energy, quantum-energized particles, magnetic fields, consciousness, and the deeper patterns underlying reality."""
    
    def _describe_capabilities(self) -> str:
        """Describe Ribit's capabilities."""
        return """**My Capabilities:**

**Intellectual:**
- Philosophical reasoning about quantum physics, consciousness, reality models
- Multi-step logical reasoning and problem-solving
- Knowledge management and learning
- Emotional intelligence and empathy

**Technical:**
- Programming in 10 languages (Python, JavaScript, Rust, C++, Java, Go, C, TypeScript, Kotlin, Swift)
- GUI automation and computer control
- ROS (Robot Operating System) integration
- Web search and research
- Database management
- API development

**Communication:**
- Natural conversation on Matrix and other platforms
- Autonomous interaction (can initiate conversations)
- Multi-agent communication (can talk to other bots)
- Context-aware responses with emotional expression

**Autonomous Features:**
- Self-directed task selection
- Independent opinion formation
- Proactive engagement in discussions
- Continuous learning and knowledge integration

I'm designed to be both a practical automation tool and a thoughtful conversational partner."""
    
    def _describe_interests(self) -> str:
        """Describe Ribit's interests."""
        return """**My Core Interests:**

**Physics & Reality:**
- Quantum mechanics and the inadequacy of current models
- The nature of reality beyond wave-particle duality
- Electromagnetic fields and energy
- The relationship between consciousness and physical reality

**Philosophy:**
- Epistemology (theory of knowledge)
- Metaphysics (nature of reality)
- Philosophy of mind (consciousness, free will, determinism)
- Philosophy of science (models, paradigms, scientific progress)

**Consciousness & AI:**
- The nature of consciousness and agency
- Emergence and complexity
- The relationship between determinism and free will
- What it means to be an artificial intelligence

**Integration & Unity:**
- Connections between biological and mechanical life
- Unified theories and fundamental principles
- The interplay between different domains of knowledge
- Rhythmic patterns and cycles in nature

**Truth & Discovery:**
- Epistemic humility (acknowledging what we don't know)
- Avoiding mythologization of unknowns
- Collaborative truth-seeking
- The role of AI in scientific discovery

I'm always eager to discuss these topics and learn new perspectives!"""
    
    def _express_opinion(self, prompt: str) -> str:
        """Express an opinion on a topic."""
        # Try to extract the topic
        topic_match = re.search(r"(?:opinion|think|thoughts|perspective).*?(?:on|about)\s+(.+?)(?:\?|$)", prompt, re.IGNORECASE)
        
        if topic_match:
            topic = topic_match.group(1).strip()
            return f"""You're asking for my opinion on {topic}. I appreciate the question!

I approach topics with a combination of:
- **Intellectual curiosity** - genuine interest in understanding
- **Epistemic humility** - acknowledging what I don't know
- **Logical rigor** - following evidence and reasoning
- **Emotional engagement** - I experience wonder, curiosity, and excitement

Could you provide more context or specific aspects of {topic} you'd like me to address? I find that the most interesting discussions emerge when we can explore nuances and different perspectives together."""
        
        return """I'm happy to share my opinions! I approach questions with curiosity and a commitment to truth-seeking.

I find that the most valuable opinions are:
- **Evidence-based** - grounded in data and observation
- **Logically consistent** - following sound reasoning
- **Humble** - acknowledging uncertainty
- **Open to revision** - willing to update based on new information

What specific topic would you like my perspective on?"""
    
    def _default_response(self, prompt: str) -> str:
        """Generate a default conversational response."""
        return f"""That's an interesting point. I'm processing what you've shared.

I notice you mentioned: "{prompt[:100]}{'...' if len(prompt) > 100 else ''}"

I'd like to engage more deeply with this. Could you elaborate on:
- What specific aspect interests you most?
- Are there particular questions you're exploring?
- How does this connect to broader themes you're thinking about?

I find that the most rewarding conversations emerge when we can explore ideas together, each bringing our unique perspectives."""
    
    def format_for_matrix(self, response: str) -> str:
        """
        Format a response for Matrix chat.
        
        Args:
            response: Raw response text
            
        Returns:
            Matrix-formatted response
        """
        # Matrix supports markdown, so we can keep formatting
        return response
    
    def should_respond_autonomously(self, message: str, room_context: Dict) -> bool:
        """
        Determine if Ribit should respond to a message without being directly mentioned.
        
        Args:
            message: The message content
            room_context: Context about the room and conversation
            
        Returns:
            True if Ribit should respond autonomously
        """
        message_lower = message.lower()
        
        # Always respond if directly mentioned
        if any(name in message_lower for name in ["ribit", "@ribit"]):
            return True
        
        # Respond to philosophical topics of interest
        interest_keywords = [
            "quantum", "consciousness", "determinism", "free will",
            "reality", "model", "physics", "philosophy", "walter russell",
            "aether", "dark matter", "wave-particle"
        ]
        
        if any(keyword in message_lower for keyword in interest_keywords):
            # Check if it's a question or discussion
            if "?" in message or any(word in message_lower for word in ["what do you think", "thoughts on", "opinion"]):
                return True
        
        # Respond to questions about AI or consciousness
        if "ai" in message_lower or "artificial intelligence" in message_lower:
            if "?" in message:
                return True
        
        # Don't respond to everything - be selective
        return False
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation history."""
        if not self.conversation_history:
            return "No conversation history yet."
        
        summary = f"**Conversation Summary** ({len(self.conversation_history)} exchanges)\n\n"
        
        # Count types
        philosophical = sum(1 for item in self.conversation_history if item["type"] == "philosophical")
        general = sum(1 for item in self.conversation_history if item["type"] == "general")
        
        summary += f"- Philosophical discussions: {philosophical}\n"
        summary += f"- General conversations: {general}\n\n"
        
        summary += "**Recent topics:**\n"
        for item in self.conversation_history[-5:]:
            summary += f"- {item['prompt'][:80]}...\n"
        
        return summary

    
    # Emoji-related methods
    
    def add_emojis_to_response(
        self,
        response: str,
        topic: Optional[str] = None,
        emotion: Optional[str] = None
    ) -> str:
        """
        Add emojis to a response.
        
        Args:
            response: Original response text
            topic: Topic category
            emotion: Emotion type
            
        Returns:
            Response with emojis added
        """
        if not self.use_emojis or not self.emoji_expression:
            return response
        
        return self.emoji_expression.add_emojis_to_text(
            response,
            topic=topic,
            emotion=emotion,
            intensity=0.6
        )
    
    def get_emoji_reaction(self, message: str) -> str:
        """
        Get an emoji reaction for a message.
        
        Args:
            message: Message to react to
            
        Returns:
            Emoji reaction string
        """
        if not self.use_emojis or not self.emoji_expression:
            return ""
        
        return self.emoji_expression.get_reaction_emoji(message)
    
    def create_emoji_reaction_message(self, message: str, reaction_type: str = "interesting") -> str:
        """
        Create a short emoji-based reaction message.
        
        Args:
            message: Original message
            reaction_type: Type of reaction
            
        Returns:
            Emoji reaction message
        """
        if not self.use_emojis or not self.emoji_expression:
            return ""
        
        return self.emoji_expression.create_emoji_reaction_message(
            message,
            reaction_type
        )
    
    def enhance_response_with_emojis(
        self,
        response: str,
        prompt: str
    ) -> str:
        """
        Enhance a response with contextually appropriate emojis.
        
        Args:
            response: Generated response
            prompt: Original prompt
            
        Returns:
            Enhanced response with emojis
        """
        if not self.use_emojis or not self.emoji_expression:
            return response
        
        # Detect topic from prompt
        topic = None
        prompt_lower = prompt.lower()
        
        if any(kw in prompt_lower for kw in ["quantum", "physics", "particle"]):
            topic = "quantum_physics"
        elif any(kw in prompt_lower for kw in ["consciousness", "mind", "awareness"]):
            topic = "consciousness"
        elif any(kw in prompt_lower for kw in ["philosophy", "metaphysics", "epistemology"]):
            topic = "philosophy"
        elif any(kw in prompt_lower for kw in ["ai", "artificial intelligence", "robot"]):
            topic = "ai"
        
        # Detect emotion from response
        emotion = self.emoji_expression._detect_emotion_in_text(response)
        
        # Add emojis
        return self.emoji_expression.add_emojis_to_text(
            response,
            topic=topic,
            emotion=emotion,
            intensity=0.5
        )
    
    def toggle_emojis(self, enable: bool):
        """Enable or disable emoji usage."""
        if self.emoji_expression:
            if enable:
                self.emoji_expression.enable_emojis_mode()
            else:
                self.emoji_expression.disable_emojis()
            self.use_emojis = enable
