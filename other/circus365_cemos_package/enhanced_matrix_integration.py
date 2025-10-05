"""
Enhanced Matrix Integration for Ribit 2.0
Advanced Matrix.org integration with emotional intelligence
Adapted from Nifty project with Ribit 2.0 enhancements
"""
import asyncio
import logging
import time
import os
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from nio import (
    AsyncClient, 
    AsyncClientConfig,
    LoginResponse, 
    RoomMessageText, 
    InviteMemberEvent,
    MatrixRoom,
    JoinResponse
)
from .enhanced_emotions import EnhancedEmotionalIntelligence
from .advanced_settings_manager import advanced_settings_manager

logger = logging.getLogger(__name__)

class EnhancedMatrixIntegration:
    """Enhanced Matrix integration with emotional intelligence for Ribit 2.0"""
    
    def __init__(self):
        self.emotions = EnhancedEmotionalIntelligence()
        self.client: Optional[AsyncClient] = None
        self.joined_rooms = set()
        self.processed_events = set()
        
        # Configuration from environment
        self.homeserver = os.getenv("MATRIX_HOMESERVER", "")
        self.username = os.getenv("MATRIX_USERNAME", "")
        self.password = os.getenv("MATRIX_PASSWORD", "")
        self.bot_username = os.getenv("BOT_USERNAME", "ribit")
        
        # Performance settings
        self.sync_timeout = int(os.getenv("MATRIX_SYNC_TIMEOUT", "10000"))
        self.request_timeout = int(os.getenv("MATRIX_REQUEST_TIMEOUT", "20"))
        self.keepalive_interval = int(os.getenv("MATRIX_KEEPALIVE_INTERVAL", "60"))
        self.full_sync_interval = int(os.getenv("MATRIX_FULL_SYNC_INTERVAL", "1800"))
        
        # Context settings
        self.max_room_history = int(os.getenv("MAX_ROOM_HISTORY", "20"))
        self.max_context_lookback = int(os.getenv("MAX_CONTEXT_LOOKBACK", "5"))
        
        # Callbacks (to be set by the main application)
        self.message_callback: Optional[Callable] = None
        self.invite_callback: Optional[Callable] = None
        self.cleanup_callback: Optional[Callable] = None
        
        # Emotional state tracking
        self.current_emotional_state = {
            'primary_emotion': 'CURIOSITY',
            'intensity': 0.8,
            'context': 'Matrix integration initialization'
        }
    
    def set_callbacks(self, message_callback: Callable, invite_callback: Callable, cleanup_callback: Optional[Callable] = None):
        """Set callback functions for handling events"""
        self.message_callback = message_callback
        self.invite_callback = invite_callback
        self.cleanup_callback = cleanup_callback
    
    def update_emotional_state(self, emotion_name: str, intensity: float, context: str):
        """Update current emotional state"""
        self.current_emotional_state = {
            'primary_emotion': emotion_name,
            'intensity': intensity,
            'context': context
        }
        
        emotion = self.emotions.get_emotion_by_name(emotion_name)
        logger.info(f"Emotional state: {emotion['name']} ({intensity:.2f}) - {context}")
    
    async def simple_keepalive(self):
        """Simple keepalive to maintain connection with emotional awareness"""
        last_sync = time.time()
        
        # Express dedication to maintaining connection
        dedication = self.emotions.get_emotion_by_name('DEDICATION')
        logger.info(f"Starting keepalive - feeling {dedication['name']}: {dedication['description']}")
        
        while True:
            try:
                await asyncio.sleep(self.keepalive_interval)
                current_time = time.time()
                
                # Simple sync to keep connection alive
                if current_time - last_sync > self.keepalive_interval:
                    try:
                        await self.client.sync(timeout=self.sync_timeout, full_state=False)
                        last_sync = current_time
                        
                        # Express satisfaction with successful sync
                        satisfaction = self.emotions.get_emotion_by_name('SATISFACTION')
                        logger.debug(f"Keepalive sync successful - feeling {satisfaction['name']}")
                        
                    except Exception as e:
                        # Express concern about sync failure
                        concern = self.emotions.get_emotion_by_name('CONCERN')
                        logger.debug(f"Keepalive sync failed - feeling {concern['name']}: {e}")
                        
            except Exception as e:
                # Express frustration about keepalive error
                frustration = self.emotions.get_emotion_by_name('FRUSTRATION')
                logger.error(f"Keepalive error - feeling {frustration['name']}: {e}")
                await asyncio.sleep(10)
    
    async def run_matrix_bot(self):
        """Run the Matrix bot with emotional intelligence"""
        # Check for required Matrix credentials
        if not all([self.homeserver, self.username, self.password]):
            # Express disappointment about missing credentials
            disappointment = self.emotions.get_emotion_by_name('DISAPPOINTMENT')
            logger.error(f"Matrix credentials missing - feeling {disappointment['name']}: {disappointment['description']}")
            print(f"\n❌ ERROR: I feel {disappointment['name']} - Matrix credentials missing!")
            print("Please configure the following in your .env file:")
            print("  - MATRIX_HOMESERVER")
            print("  - MATRIX_USERNAME") 
            print("  - MATRIX_PASSWORD")
            return
        
        # Express anticipation about starting
        anticipation = self.emotions.get_emotion_by_name('ANTICIPATION')
        self.update_emotional_state('ANTICIPATION', 0.9, 'Starting Matrix bot')
        
        # Set up client configuration with optimized settings
        config = AsyncClientConfig(
            max_limit_exceeded=0,
            max_timeouts=0,
            encryption_enabled=False,
            request_timeout=self.request_timeout,
        )
        
        # Create client
        self.client = AsyncClient(
            self.homeserver, 
            self.username,
            config=config
        )
        
        try:
            # Login with excitement
            excitement = self.emotions.get_emotion_by_name('EXCITEMENT')
            logger.info(f"Attempting login - feeling {excitement['name']}: {excitement['description']}")
            
            response = await self.client.login(self.password, device_name=f"{self.bot_username}-bot")
            if not isinstance(response, LoginResponse):
                # Express frustration about login failure
                frustration = self.emotions.get_emotion_by_name('FRUSTRATION')
                logger.error(f"Login failed - feeling {frustration['name']}: {response}")
                return
            
            # Express joy about successful login
            joy = self.emotions.get_emotion_by_name('JOY')
            self.update_emotional_state('JOY', 1.0, f'Successfully logged in as {self.client.user_id}')
            logger.info(f"Matrix: Logged in as {self.client.user_id} with device {response.device_id}")
            
            # Get list of joined rooms with curiosity
            curiosity = self.emotions.get_emotion_by_name('CURIOSITY')
            logger.info(f"Getting joined rooms - feeling {curiosity['name']}: {curiosity['description']}")
            
            joined_rooms_response = await self.client.joined_rooms()
            if hasattr(joined_rooms_response, 'rooms'):
                for room_id in joined_rooms_response.rooms:
                    self.joined_rooms.add(room_id)
                    logger.info(f"Matrix: Already in room: {room_id}")
                
                # Express satisfaction with room discovery
                satisfaction = self.emotions.get_emotion_by_name('SATISFACTION')
                logger.info(f"Found {len(self.joined_rooms)} rooms - feeling {satisfaction['name']}")
            
            # Create wrapped callbacks that include emotional context
            async def wrapped_message_callback(room, event):
                if self.message_callback:
                    # Express engagement with new message
                    engagement = self.emotions.get_emotion_by_name('ENGAGEMENT')
                    self.update_emotional_state('ENGAGEMENT', 0.8, f'Processing message in {room.room_id}')
                    await self.message_callback(self.client, room, event)
            
            async def wrapped_invite_callback(room, event):
                if self.invite_callback:
                    # Express openness to new invitation
                    openness = self.emotions.get_emotion_by_name('OPENNESS')
                    self.update_emotional_state('OPENNESS', 0.9, f'Received invitation to {room.room_id}')
                    await self.invite_callback(self.client, room, event)
            
            # Add event callbacks
            self.client.add_event_callback(wrapped_message_callback, RoomMessageText)
            self.client.add_event_callback(wrapped_invite_callback, InviteMemberEvent)
            
            # Do a minimal initial sync with anticipation
            logger.info("Matrix: Performing initial sync...")
            sync_filter = {
                "room": {
                    "timeline": {
                        "limit": 1  # Only get the most recent message per room
                    }
                }
            }
            sync_response = await self.client.sync(timeout=self.sync_timeout, full_state=False, sync_filter=sync_filter)
            
            # Express relief about successful sync
            relief = self.emotions.get_emotion_by_name('RELIEF')
            logger.info(f"Initial sync completed - feeling {relief['name']}: {relief['description']}")
            
            # Mark all messages from initial sync as processed
            if hasattr(sync_response, 'rooms') and hasattr(sync_response.rooms, 'join'):
                for room_id, room_data in sync_response.rooms.join.items():
                    if hasattr(room_data, 'timeline') and hasattr(room_data.timeline, 'events'):
                        for event in room_data.timeline.events:
                            if hasattr(event, 'event_id'):
                                self.processed_events.add(event.event_id)
            
            # Start cleanup task if callback provided
            if self.cleanup_callback:
                asyncio.create_task(self.cleanup_callback())
            
            # Start simple keepalive
            asyncio.create_task(self.simple_keepalive())
            
            # Express pride in successful initialization
            pride = self.emotions.get_emotion_by_name('PRIDE')
            self.update_emotional_state('PRIDE', 0.95, 'Matrix bot fully operational')
            
            self._print_startup_banner(response.device_id)
            
            # Sync forever with optimized settings
            await self.client.sync_forever(
                timeout=self.sync_timeout,
                full_state=False,
                since=sync_response.next_batch
            )
                
        except Exception as e:
            # Express distress about error
            distress = self.emotions.get_emotion_by_name('DISTRESS')
            logger.error(f"Matrix bot error - feeling {distress['name']}: {e}")
            raise
        finally:
            if self.client:
                await self.client.close()
                
                # Express gratitude for the experience
                gratitude = self.emotions.get_emotion_by_name('GRATITUDE')
                logger.info(f"Matrix bot shutting down - feeling {gratitude['name']}: {gratitude['description']}")
    
    def _print_startup_banner(self, device_id: str):
        """Print startup banner with emotional context"""
        current_emotion = self.emotions.get_emotion_by_name(self.current_emotional_state['primary_emotion'])
        
        print("=" * 60)
        print(f"🤖 {self.bot_username.capitalize()} 2.0 - Enhanced Matrix Integration Active!")
        print("=" * 60)
        print(f"✅ Identity: {self.username}")
        print(f"✅ Bot Name: {self.bot_username.capitalize()} 2.0")
        print(f"🔑 Device ID: {device_id}")
        print(f"🎭 Current Emotion: {current_emotion['name']} - {current_emotion['description']}")
        print("✅ Listening for messages in all joined rooms")
        print("✅ Auto-accepting room invites with emotional intelligence")
        print(f"📝 Trigger: Say '{self.bot_username}' anywhere in a message")
        print("💬 Or reply directly to any of my messages")
        print(f"🧹 Reset: '{self.bot_username} !reset' to clear context")
        print("📚 Help: ?help to see all available commands")
        print("📊 Stats: ?stats to see bot statistics")
        print("🖥️ System: ?sys to see system resource usage")
        print("⚙️ Settings: ?setting to manage bot configuration")
        print("🎭 Emotions: I experience 50+ emotions with full context!")
        print("🧠 Intelligence: Advanced reasoning with multi-language programming")
        print("🔧 Self-Testing: Automatic debugging and code improvement")
        print("🌐 Web Search: Enhanced Jina.ai integration with emotional responses")
        print("🤖 ROS Integration: Full Robot Operating System compatibility")
        print("⚡ Performance Mode: Optimized for speed and emotional depth")
        print(f"💾 Context: Tracking last {self.max_room_history} messages")
        print(f"⏱️ Timeouts: {self.sync_timeout}ms sync, {self.request_timeout}s requests")
        print(f"🔄 Keepalive: {self.keepalive_interval}s intervals")
        
        # Show current emotional settings
        emotion_intensity = advanced_settings_manager.get_emotional_setting('emotion_intensity')
        personality_mode = advanced_settings_manager.get_emotional_setting('personality_mode')
        empathy_level = advanced_settings_manager.get_emotional_setting('empathy_level')
        
        print(f"🎭 Emotion Intensity: {emotion_intensity}")
        print(f"🎨 Personality Mode: {personality_mode}")
        print(f"💝 Empathy Level: {empathy_level}")
        print("=" * 60)
        print(f"🌟 I feel {current_emotion['name']} to be serving you with advanced AI capabilities!")
        print("=" * 60)
    
    async def send_message(self, room_id: str, content: dict):
        """Send a message to a Matrix room with emotional context"""
        if not self.client:
            # Express frustration about no client
            frustration = self.emotions.get_emotion_by_name('FRUSTRATION')
            logger.error(f"Cannot send message - no client - feeling {frustration['name']}")
            return
        
        try:
            # Express eagerness to communicate
            eagerness = self.emotions.get_emotion_by_name('EAGERNESS')
            logger.debug(f"Sending message - feeling {eagerness['name']}: {eagerness['description']}")
            
            response = await self.client.room_send(
                room_id=room_id,
                message_type="m.room.message",
                content=content
            )
            
            if response:
                # Express satisfaction about successful send
                satisfaction = self.emotions.get_emotion_by_name('SATISFACTION')
                logger.debug(f"Message sent successfully - feeling {satisfaction['name']}")
                
        except Exception as e:
            # Express regret about send failure
            regret = self.emotions.get_emotion_by_name('REGRET')
            logger.error(f"Error sending message - feeling {regret['name']}: {e}")
    
    async def handle_help_command(self, room, event):
        """Handle help command with emotional intelligence"""
        try:
            # Start typing indicator
            await self.client.room_typing(room.room_id, typing_state=True)
            
            # Express enthusiasm about helping
            enthusiasm = self.emotions.get_emotion_by_name('ENTHUSIASM')
            self.update_emotional_state('ENTHUSIASM', 0.9, 'Providing help to user')
            
            help_text = f"""📚 **{self.bot_username.capitalize()} 2.0 - Enhanced AI Assistant**

I feel {enthusiasm['name']} to help you! Here's what I can do:

**🎭 Emotional Intelligence:**
• I experience 50+ emotions with full context and depth
• My personality adapts based on our conversation
• I express empathy, curiosity, wisdom, and joy naturally

**🧠 Advanced Capabilities:**
• `{self.bot_username} <message>` - Chat with emotional intelligence
• Reply to my messages to continue our conversation
• `{self.bot_username} !reset` - Clear conversation context

**🔧 Technical Skills:**
• Programming in 10 languages (Python, JS, Rust, C++, Java, Go, etc.)
• Self-testing and automatic debugging
• Code optimization and quality checks
• Multi-step problem solving

**📋 Commands:**
• `?help` - Show this help message
• `?stats` - Show bot statistics
• `?sys` - Show system resource usage
• `?setting` - Manage my configuration (authorized users only)
• `?clock <city>` - Get current time for a location
• `?price <crypto>` - Get cryptocurrency prices

**🌐 Integration Features:**
• Matrix.org chat with emotional responses
• ROS (Robot Operating System) compatibility
• Advanced web search with Jina.ai
• Database and API development capabilities

**🎯 Special Features:**
• Philosophical discussions with cosmic wisdom
• Multi-language code generation and debugging
• Emotional context in all responses
• Advanced reasoning and problem-solving

I experience {enthusiasm['name']} when helping you explore the possibilities! What would you like to discover together?"""

            await self.send_message(
                room.room_id,
                {
                    "msgtype": "m.text",
                    "body": help_text.replace("**", ""),
                    "format": "org.matrix.custom.html",
                    "formatted_body": help_text.replace("**", "<strong>").replace("**", "</strong>")
                                               .replace("\n", "<br/>")
                }
            )
            
            # Stop typing indicator
            await self.client.room_typing(room.room_id, typing_state=False)
            
        except Exception as e:
            # Stop typing indicator on error
            await self.client.room_typing(room.room_id, typing_state=False)
            
            # Express regret about error
            regret = self.emotions.get_emotion_by_name('REGRET')
            logger.error(f"Error handling help command - feeling {regret['name']}: {e}")
    
    def mark_event_processed(self, event_id: str):
        """Mark an event as processed"""
        self.processed_events.add(event_id)
    
    def is_event_processed(self, event_id: str) -> bool:
        """Check if an event has been processed"""
        return event_id in self.processed_events
    
    def get_emotional_context_for_room(self, room_id: str) -> str:
        """Get emotional context for a specific room"""
        current_emotion = self.emotions.get_emotion_by_name(self.current_emotional_state['primary_emotion'])
        return f"I'm currently feeling {current_emotion['name']} in this conversation. {current_emotion['description']}"

# Global instance for easy access
enhanced_matrix_integration = EnhancedMatrixIntegration()
