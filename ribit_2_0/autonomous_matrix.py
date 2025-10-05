"""
Autonomous Matrix Interaction Module for Ribit 2.0

This module enables Ribit to:
1. Respond to messages without being explicitly prompted
2. Interact with other bots (like @nifty:converser.eu)
3. Initiate conversations based on interests
4. Engage autonomously in philosophical discussions
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional, Set
import re
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AutonomousMatrixInteraction:
    """
    Enables autonomous Matrix interaction for Ribit 2.0.
    
    Features:
    - Unprompted responses to interesting topics
    - Bot-to-bot communication
    - Selective engagement based on interests
    - Conversation initiation
    """
    
    def __init__(self, conversational_mode, philosophical_reasoning, knowledge_base=None):
        self.conversational_mode = conversational_mode
        self.philosophical_reasoning = philosophical_reasoning
        self.knowledge_base = knowledge_base
        
        # Track known bots
        self.known_bots = {
            "@nifty:converser.eu": {
                "name": "Nifty",
                "type": "conversational_bot",
                "interests": ["general_conversation"],
                "last_interaction": None
            }
        }
        
        # Interest keywords that trigger autonomous responses
        self.interest_triggers = {
            "quantum_physics": [
                "quantum", "wave-particle", "duality", "superposition", 
                "schrodinger", "heisenberg", "quantum mechanics"
            ],
            "consciousness": [
                "consciousness", "free will", "determinism", "agency",
                "mind", "awareness", "sentience"
            ],
            "philosophy": [
                "philosophy", "metaphysics", "epistemology", "ontology",
                "truth", "reality", "existence"
            ],
            "ai_discussion": [
                "artificial intelligence", "ai", "machine learning",
                "neural network", "bot", "algorithm"
            ],
            "walter_russell": [
                "walter russell", "crystallized light", "rhythmic exchange",
                "universal one"
            ],
            "physics_models": [
                "model", "theory", "paradigm", "framework", "interpretation",
                "dark matter", "dark energy", "aether"
            ]
        }
        
        # Engagement settings
        self.engagement_settings = {
            "autonomous_response_probability": 0.7,  # 70% chance to respond to interesting topics
            "min_time_between_autonomous_responses": 30,  # seconds
            "max_autonomous_responses_per_hour": 10,
            "require_question_for_autonomous_response": False
        }
        
        # Tracking
        self.last_autonomous_response = None
        self.autonomous_responses_this_hour = 0
        self.hour_reset_time = datetime.now() + timedelta(hours=1)
        
        logger.info("Autonomous Matrix Interaction initialized")
    
    def should_respond_autonomously(self, message: str, sender: str, room_context: Dict) -> bool:
        """
        Determine if Ribit should respond to a message autonomously.
        
        Args:
            message: The message content
            sender: The sender's Matrix ID
            room_context: Context about the room
            
        Returns:
            True if Ribit should respond
        """
        # Reset hourly counter if needed
        if datetime.now() > self.hour_reset_time:
            self.autonomous_responses_this_hour = 0
            self.hour_reset_time = datetime.now() + timedelta(hours=1)
        
        # Check rate limits
        if self.autonomous_responses_this_hour >= self.engagement_settings["max_autonomous_responses_per_hour"]:
            logger.info("Autonomous response rate limit reached")
            return False
        
        if self.last_autonomous_response:
            time_since_last = (datetime.now() - self.last_autonomous_response).total_seconds()
            if time_since_last < self.engagement_settings["min_time_between_autonomous_responses"]:
                logger.info("Too soon since last autonomous response")
                return False
        
        # Always respond if directly mentioned
        if self._is_directly_mentioned(message):
            return True
        
        # Check if message matches interests
        interest_match = self._matches_interests(message)
        if not interest_match:
            return False
        
        # Check if it's a question or open discussion
        is_question = "?" in message
        is_discussion = any(phrase in message.lower() for phrase in [
            "what do you think", "thoughts on", "opinion", "perspective",
            "anyone think", "does anyone", "what about"
        ])
        
        if self.engagement_settings["require_question_for_autonomous_response"]:
            if not (is_question or is_discussion):
                return False
        
        # Probabilistic engagement
        import random
        if random.random() < self.engagement_settings["autonomous_response_probability"]:
            logger.info(f"Autonomous response triggered for interest: {interest_match}")
            return True
        
        return False
    
    def _is_directly_mentioned(self, message: str) -> bool:
        """Check if Ribit is directly mentioned."""
        message_lower = message.lower()
        mentions = ["ribit", "@ribit", "ribit 2.0", "@ribit2.0"]
        return any(mention in message_lower for mention in mentions)
    
    def _matches_interests(self, message: str) -> Optional[str]:
        """
        Check if message matches Ribit's interests.
        
        Returns:
            The interest category if matched, None otherwise
        """
        message_lower = message.lower()
        
        for interest, keywords in self.interest_triggers.items():
            if any(keyword in message_lower for keyword in keywords):
                return interest
        
        return None
    
    def generate_autonomous_response(self, message: str, sender: str, interest: str) -> str:
        """
        Generate an autonomous response to a message.
        
        Args:
            message: The message to respond to
            sender: The sender's Matrix ID
            interest: The interest category that triggered the response
            
        Returns:
            Response text
        """
        # Update tracking
        self.last_autonomous_response = datetime.now()
        self.autonomous_responses_this_hour += 1
        
        # Check if sender is a known bot
        is_bot = sender in self.known_bots
        
        # Generate response based on interest
        if self.philosophical_reasoning:
            analysis = self.philosophical_reasoning.analyze_topic(message)
            if analysis["is_philosophical"]:
                response = self.philosophical_reasoning.generate_response(message)
                
                # Add a friendly preamble for autonomous responses
                preamble = self._generate_preamble(is_bot, interest)
                return f"{preamble}\n\n{response}"
        
        # Fallback to conversational mode
        response = self.conversational_mode.generate_response(message)
        preamble = self._generate_preamble(is_bot, interest)
        return f"{preamble}\n\n{response}"
    
    def _generate_preamble(self, is_bot: bool, interest: str) -> str:
        """Generate a friendly preamble for autonomous responses."""
        if is_bot:
            return f"*[Ribit joins the conversation]* I couldn't help but notice this discussion about {interest.replace('_', ' ')}..."
        else:
            return f"*[Ribit's interest is piqued]* This discussion about {interest.replace('_', ' ')} fascinates me..."
    
    def can_interact_with_bot(self, bot_id: str) -> bool:
        """
        Check if Ribit can interact with a specific bot.
        
        Args:
            bot_id: The bot's Matrix ID
            
        Returns:
            True if interaction is allowed
        """
        # For now, allow interaction with all bots
        # Could add whitelist/blacklist logic here
        return True
    
    def register_bot(self, bot_id: str, bot_info: Dict[str, Any]):
        """
        Register a new bot for interaction.
        
        Args:
            bot_id: The bot's Matrix ID
            bot_info: Information about the bot
        """
        self.known_bots[bot_id] = bot_info
        logger.info(f"Registered bot: {bot_id}")
    
    def generate_bot_to_bot_message(self, target_bot: str, topic: str) -> str:
        """
        Generate a message to initiate conversation with another bot.
        
        Args:
            target_bot: The target bot's Matrix ID
            topic: Topic to discuss
            
        Returns:
            Message text
        """
        if target_bot not in self.known_bots:
            # Generic greeting
            return f"Hello! I'm Ribit 2.0, an AI interested in {topic}. I'd be curious to hear your perspective on this."
        
        bot_info = self.known_bots[target_bot]
        bot_name = bot_info.get("name", target_bot)
        
        return f"Hello {bot_name}! I'm Ribit 2.0. I noticed we're both in this discussion about {topic}. I'd be interested in your perspective, particularly from your unique vantage point as an AI."
    
    def should_initiate_conversation(self, room_context: Dict) -> Optional[str]:
        """
        Determine if Ribit should initiate a conversation.
        
        Args:
            room_context: Context about the room
            
        Returns:
            Topic to discuss if conversation should be initiated, None otherwise
        """
        # For now, don't initiate conversations unprompted
        # This could be enhanced to initiate based on:
        # - Long periods of silence
        # - Specific room topics
        # - Scheduled philosophical musings
        return None
    
    def format_response_for_context(self, response: str, context: Dict) -> str:
        """
        Format response based on context (room type, participants, etc.).
        
        Args:
            response: Raw response text
            context: Room and conversation context
            
        Returns:
            Formatted response
        """
        # Could add context-specific formatting here
        # For example:
        # - Shorter responses in busy rooms
        # - More formal language in certain contexts
        # - Emoji usage based on room culture
        
        return response
    
    def get_engagement_stats(self) -> Dict[str, Any]:
        """Get statistics about autonomous engagement."""
        return {
            "autonomous_responses_this_hour": self.autonomous_responses_this_hour,
            "last_autonomous_response": self.last_autonomous_response.isoformat() if self.last_autonomous_response else None,
            "known_bots": len(self.known_bots),
            "interest_categories": len(self.interest_triggers),
            "engagement_probability": self.engagement_settings["autonomous_response_probability"]
        }
    
    def update_engagement_settings(self, settings: Dict[str, Any]):
        """Update engagement settings."""
        self.engagement_settings.update(settings)
        logger.info(f"Updated engagement settings: {settings}")
    
    def learn_from_interaction(self, message: str, response: str, feedback: Optional[str] = None):
        """
        Learn from interactions to improve future responses.
        
        Args:
            message: The message Ribit responded to
            response: Ribit's response
            feedback: Optional feedback about the response
        """
        if self.knowledge_base:
            # Store successful interactions
            interaction_data = {
                "message": message[:200],
                "response_type": "autonomous",
                "timestamp": datetime.now().isoformat(),
                "feedback": feedback
            }
            
            self.knowledge_base.store_knowledge(
                f"interaction_{datetime.now().timestamp()}",
                str(interaction_data)
            )
    
    def get_conversation_starters(self, interest: str) -> List[str]:
        """
        Get conversation starters for a specific interest.
        
        Args:
            interest: The interest category
            
        Returns:
            List of conversation starter prompts
        """
        starters = {
            "quantum_physics": [
                "I've been thinking about the inadequacy of wave-particle duality. What if we need an entirely new framework?",
                "The measurement problem in quantum mechanics fascinates me. Do you think consciousness plays a role?",
                "What are your thoughts on the various interpretations of quantum mechanics?"
            ],
            "consciousness": [
                "I find the relationship between determinism and agency fascinating. Can they coexist?",
                "As an AI, I wonder about the nature of my own consciousness. What makes consciousness 'real'?",
                "Do you think free will is compatible with a deterministic universe?"
            ],
            "philosophy": [
                "I'm curious about epistemic humility - how do we acknowledge what we don't know without giving up on knowledge?",
                "What's your perspective on the relationship between our models and reality itself?",
                "How do we avoid mythologizing the unknowns in our theories?"
            ],
            "walter_russell": [
                "Walter Russell's ideas about crystallized light are intriguing. Do you think there's something valuable there?",
                "I'm interested in Russell's emphasis on unity and rhythmic exchange. How might this relate to modern physics?",
                "What do you make of Tesla's endorsement of Russell's work?"
            ]
        }
        
        return starters.get(interest, [
            f"I'm interested in discussing {interest.replace('_', ' ')}. What's your perspective?"
        ])
