#!/usr/bin/env python3
"""
Ribit 2.0 Matrix Bot Integration

A sophisticated Matrix bot that integrates the MockRibit20LLM emulator
with Matrix.org chat rooms, providing intelligent automation and
conversation capabilities with user authentication and command restrictions.

Author: Manus AI
Date: September 21, 2025
"""

import asyncio
import logging
import time
import os
import re
from typing import Dict, Set, Optional, TYPE_CHECKING
from pathlib import Path

try:
    from nio import (
        AsyncClient,
        AsyncClientConfig,
        LoginResponse,
        RoomMessageText,
        InviteMemberEvent,
        MatrixRoom,
        JoinResponse
    )
    MATRIX_AVAILABLE = True
except ImportError:
    MATRIX_AVAILABLE = False
    print("Warning: matrix-nio not installed. Matrix bot will run in mock mode.")

    class MatrixRoom:
        """Mock MatrixRoom for type annotations when matrix-nio is not installed."""
        pass

    class RoomMessageText:
        """Mock RoomMessageText for type annotations when matrix-nio is not installed."""
        pass

    class InviteMemberEvent:
        """Mock InviteMemberEvent for type annotations when matrix-nio is not installed."""
        pass

# # from .mock_llm_wrapper import MockRibit20LLM
from .controller import VisionSystemController

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RibitMatrixBot:
    """
    Ribit 2.0 Matrix Bot
    
    Integrates MockRibit20LLM with Matrix.org for intelligent chat automation
    with user authentication and command restrictions.
    """
    
    def __init__(self, homeserver: str, username: str, password: str = "", access_token: str = "", authorized_users: Optional[Set[str]] = None, enable_bridge: bool = False):
        """
        Initialize the Ribit Matrix Bot.
        
        Args:
            homeserver: Matrix homeserver URL
            username: Bot username
            password: Bot password (for password auth)
            access_token: Access token (for token auth, takes priority over password)
            authorized_users: Set of authorized user IDs for commands
        """
        self.homeserver = homeserver
        self.username = username
        self.password = password
        self.access_token = access_token
        self.use_token_auth = bool(access_token)
        self.authorized_users = authorized_users or {
            "@ribit:envs.net",
            "@rabit232:envs.net"
        }
        
        # Initialize components
        try:
            from .megabite_llm import MegabiteLLM
            self.llm = MegabiteLLM()
            logger.info("Using MegabiteLLM for Matrix Bot.")
        except ImportError:
            logger.warning("MegabiteLLM not found. Falling back to MockRibit20LLM.")
            from .mock_llm_wrapper import MockRibit20LLM
            self.llm = MockRibit20LLM("ribit_matrix_knowledge.txt")
        
        self.controller = VisionSystemController()
        self.enable_bridge = enable_bridge or os.getenv("ENABLE_BRIDGE", "False").lower() == "true"
        self.bridge_relay: Optional[BridgeRelay] = None # Will be set by external bridge runner
        
        # Initialize enhanced intelligence systems
        try:
            from .linguistics_engine import LinguisticsEngine
            from .conversation_memory import ConversationMemory
            from .user_engagement import UserEngagementSystem
            
            self.linguistics = LinguisticsEngine()
            self.memory = ConversationMemory()
            self.engagement = UserEngagementSystem()
            logger.info("✅ Enhanced intelligence systems initialized")
        except Exception as e:
            logger.warning(f"Enhanced intelligence systems not available: {e}")
            self.linguistics = None
            self.memory = None
            self.engagement = None
        
        # Bot state
        self.client = None
        self.joined_rooms: Set[str] = set()
        self.processed_events: Set[str] = set()
        self.conversation_context: Dict[str, list] = {}
        self.terminator_warnings: Dict[str, int] = {}
        
        # Configuration
        self.bot_name = "ribit.2.0"
        self.sync_timeout = 30000
        self.request_timeout = 10000
        self.keepalive_interval = 60

        # Bridge relay for cross-platform messaging
        self.bridge_relay = None

        logger.info(f"Ribit Matrix Bot initialized for {username}")
    
    async def start(self):
        """Start the Matrix bot."""
        if not MATRIX_AVAILABLE:
            logger.warning("Matrix libraries not available, running in mock mode")
            await self._run_mock_mode()
            return
        
        # Validate credentials
        if not self.homeserver or not self.username:
            logger.error("Matrix credentials incomplete!")
            print("❌ ERROR: Matrix credentials missing!")
            print("Required: homeserver, username")
            return
        
        if not self.password and not self.access_token:
            logger.error("No authentication method provided!")
            print("❌ ERROR: No authentication credentials!")
            print("Provide either MATRIX_PASSWORD or MATRIX_ACCESS_TOKEN")
            return
        
        # Set up client configuration
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
            # Authenticate (either password or token)
            if self.use_token_auth:
                # Token-based authentication
                self.client.access_token = self.access_token
                self.client.user_id = self.username
                logger.info(f"✅ Using access token authentication for {self.username}")
                device_id = "ribit-2.0-bot-token"
            else:
                # Password-based authentication
                response = await self.client.login(self.password, device_name="ribit-2.0-bot")
                if not isinstance(response, LoginResponse):
                    logger.error(f"Failed to login to Matrix: {response}")
                    return
                
                logger.info(f"✅ Logged in as {self.client.user_id} with device {response.device_id}")
                device_id = response.device_id
            
            # Get joined rooms
            await self._get_joined_rooms()
            
            # Set up event callbacks
            self.client.add_event_callback(self._handle_message, RoomMessageText)
            self.client.add_event_callback(self._handle_invite, InviteMemberEvent)
            
            # Initial sync
            logger.info("🔄 Performing initial sync...")
            sync_response = await self.client.sync(timeout=self.sync_timeout, full_state=False)
            logger.info(f"✅ Initial sync completed")
            
            # Mark initial messages as processed
            await self._mark_initial_messages_processed(sync_response)
            
            # Start background tasks
            asyncio.create_task(self._keepalive_task())
            
            # Display startup information
            self._display_startup_info(response.device_id)
            
            # Sync forever
            await self.client.sync_forever(
                timeout=self.sync_timeout,
                full_state=False
            )
            
        except Exception as e:
            logger.error(f"Matrix bot error: {e}")
            raise
        finally:
            if self.client:
                await self.client.close()
    
    async def _run_mock_mode(self):
        """Run in mock mode when Matrix libraries are not available."""
        print("🤖 Ribit 2.0 Matrix Bot - Mock Mode")
        print("=" * 50)
        print(f"✅ LLM: {self.llm.name} Initialized")
        
        # Megabite Status Check
        if self.llm.__class__.__name__ == "MegabiteLLM":
            from .megabite_llm import MegabiteLLM
            megabite_status = MegabiteLLM.check_status()
            print(f"✅ Megabite Core: {megabite_status['status_message']}")
            
        print("✅ Controller: Ready")
        print("⚠️  Matrix: Running in mock mode")
        print("📝 Authorized users:", ", ".join(self.authorized_users))
        print("=" * 50)
        
        # Simulate bot operation
        while True:
            try:
                user_input = input("\nSimulate message (or 'quit'): ")
                if user_input.lower() == 'quit':
                    break
                
                # Simulate message processing
                mock_user = "@test:matrix.example.com"
                # Prepend bot name to ensure _is_message_for_bot returns True
                mock_message = f"{self.bot_name}: {user_input}"
                response = await self._process_message(mock_message, mock_user, "!mock_room")
                print(f"🤖 Ribit: {response}")
                
            except KeyboardInterrupt:
                break
        
        print("👋 Mock mode ended")
    
    async def _get_joined_rooms(self):
        """Get list of joined rooms."""
        try:
            joined_rooms_response = await self.client.joined_rooms()
            if hasattr(joined_rooms_response, 'rooms'):
                for room_id in joined_rooms_response.rooms:
                    self.joined_rooms.add(room_id)
                    logger.info(f"📍 Already in room: {room_id}")
        except Exception as e:
            logger.error(f"Error getting joined rooms: {e}")
    
    async def _mark_initial_messages_processed(self, sync_response):
        """Mark all messages from initial sync as processed."""
        try:
            if hasattr(sync_response, 'rooms') and hasattr(sync_response.rooms, 'join'):
                for room_id, room_data in sync_response.rooms.join.items():
                    if hasattr(room_data, 'timeline') and hasattr(room_data.timeline, 'events'):
                        for event in room_data.timeline.events:
                            if hasattr(event, 'event_id'):
                                self.processed_events.add(event.event_id)
        except Exception as e:
            logger.error(f"Error marking initial messages: {e}")
    
    async def _handle_message(self, room: MatrixRoom, event: RoomMessageText):
        """Handle incoming Matrix messages."""
        try:
            # Skip if already processed
            if event.event_id in self.processed_events:
                return
            
            # Skip own messages
            if event.sender == self.client.user_id:
                return
            
            # Mark as processed
            self.processed_events.add(event.event_id)
            
            # Process the message
            response = await self._process_message(event.body, event.sender, room.room_id)

            if response:
                await self._send_message(room.room_id, response)

            if self.bridge_relay:
                try:
                    sender_name = event.sender.split(':')[0].replace('@', '')
                    await self.bridge_relay.relay_from_matrix(
                        event.sender, sender_name, event.body, room.room_id
                    )
                except Exception as e:
                    logger.debug(f"Bridge relay error: {e}")

        except Exception as e:
            logger.error(f"Error handling message: {e}")

    def set_bridge_relay(self, bridge_relay):
        """Set the bridge relay for cross-platform messaging."""
        self.bridge_relay = bridge_relay
        logger.info("Bridge relay configured for Matrix Bot")

    async def _handle_invite(self, room: MatrixRoom, event: InviteMemberEvent):
        """Handle room invitations."""
        try:
            if event.state_key == self.client.user_id:
                logger.info(f"📨 Received invite to room: {room.room_id}")
                
                # Auto-join the room
                join_response = await self.client.join(room.room_id)
                if isinstance(join_response, JoinResponse):
                    self.joined_rooms.add(room.room_id)
                    logger.info(f"✅ Joined room: {room.room_id}")
                    
                    # Send welcome message
                    welcome_msg = ("🤖 Greetings! I am Ribit 2.0, an elegant AI agent. "
                                 f"Say '{self.bot_name}' to chat with me, or use ?help for commands.")
                    await self._send_message(room.room_id, welcome_msg)
                else:
                    logger.error(f"Failed to join room: {join_response}")
        except Exception as e:
            logger.error(f"Error handling invite: {e}")
    
    async def _process_message(self, message: str, sender: str, room_id: str) -> Optional[str]:
        """Process a message and generate a response."""
        try:
            # Check if message is directed at the bot
            if not self._is_message_for_bot(message):
                return None
            
            # Clean the message
            clean_message = self._clean_message(message)

            # --- 1. Handle 'post note' command for cross-platform relay ---
            if self.enable_bridge and self.bridge_relay and clean_message.lower().startswith("post note"):
                note_content = clean_message[len("post note"):].strip()
                if note_content:
                    # Relay the message to the other platform via the bridge
                    relay_status = await self.bridge_relay.handle_post_note(
                        sender, "Matrix", note_content
                    )
                    return f"✅ Post Note relayed. {relay_status}"
                else:
                    return "❌ Post Note command requires a message. Usage: 'post note <message>'"
            
            # Handle special commands
            if clean_message.startswith('?'):
                return await self._handle_command(clean_message, sender, room_id)
            
            # Handle reset command
            if '!reset' in clean_message.lower():
                if room_id in self.conversation_context:
                    del self.conversation_context[room_id]
                return "🔄 Conversation context reset. How may I assist you?"
            
            # Handle image generation requests
            try:
                from .image_generator import ImageGenerator
                from .matrix_image_sender import send_image_to_room
                
                image_gen = ImageGenerator()
                if image_gen.is_image_generation_request(clean_message):
                    logger.info(f"Image generation requested: {clean_message}")
                    
                    # Extract description
                    description = image_gen.extract_description(clean_message)
                    
                    # Send status message
                    await self._send_message(room_id, f"🎨 Generating image: \"{description}\"\n⏳ This may take 20-30 seconds...")
                    
                    # Generate image
                    result = await image_gen.generate_image(description)
                    
                    if result['success'] and result['file_path']:
                        # Send the image
                        success = await send_image_to_room(
                            self.client,
                            room_id,
                            result['file_path'],
                            description
                        )
                        
                        if success:
                            # Clean up the file
                            image_gen.cleanup_image(result['file_path'])
                            return "✨ Image generated and sent!"
                        else:
                            # Clean up even if sending failed
                            image_gen.cleanup_image(result['file_path'])
                            return "❌ Generated image but failed to send it to the room."
                    else:
                        error_msg = result.get('error', 'Unknown error')
                        return f"❌ Failed to generate image: {error_msg}\n\n💡 Try: 'generate image of a sunset over mountains'"
            except Exception as e:
                logger.error(f"Image generation error: {e}")
                # Continue to normal processing if image generation fails
            
            # Try humor engine for casual questions first
            try:
                from .humor_engine import HumorEngine
                humor = HumorEngine()
                casual_response = humor.get_casual_response(clean_message)
                if casual_response:
                    self._add_to_context(room_id, f"User: {clean_message}")
                    self._add_to_context(room_id, f"Ribit: {casual_response}")
                    return casual_response
            except Exception as e:
                logger.debug(f"Humor engine not available: {e}")
            
            # Linguistic analysis
            linguistic_analysis = None
            if self.linguistics:
                try:
                    linguistic_analysis = self.linguistics.understand_query(clean_message, sender)
                    logger.debug(f"Linguistic analysis: intent={linguistic_analysis['intent']}, tone={linguistic_analysis['tone']}")
                except Exception as e:
                    logger.debug(f"Linguistic analysis failed: {e}")
            
            # Track user activity for engagement
            if self.engagement:
                try:
                    self.engagement.track_user_activity(sender, room_id, clean_message)
                except Exception as e:
                    logger.debug(f"Activity tracking failed: {e}")
            
            # Add to conversation context
            self._add_to_context(room_id, f"User: {clean_message}")
            
            # Get AI response
            context = self.conversation_context.get(room_id, [])
            
            if hasattr(self.llm, 'generate_response'):
                ai_response = self.llm.generate_response(clean_message, context)
            elif hasattr(self.llm, 'get_decision'):
                ai_response = self.llm.get_decision(clean_message, context)
            else:
                ai_response = f"LLM Error: Unknown response method."
            
            # Clean up the response (remove action commands if present)
            # Megabite's response is a single line, so this cleanup is mostly for Ribit's old format.
            if '\n' in ai_response:
                # Extract just the text content, not the action commands
                lines = ai_response.split('\n')
                text_lines = [line for line in lines if not line.startswith(('type_text', 'press_key', 'store_knowledge', 'goal_achieved', 'uncertain'))]
                ai_response = "\n".join(text_lines).strip()
            
            # Add bot response to context
            self._add_to_context(room_id, f"Bot: {ai_response}")
            
            return ai_response
            
            # Add humor if appropriate
            try:
                from .humor_engine import HumorEngine
                humor = HumorEngine()
                ai_response = humor.add_humor_to_response(ai_response, clean_message)
            except Exception as e:
                logger.debug(f"Could not add humor: {e}")
            
            # Add AI response to context
            self._add_to_context(room_id, f"Ribit: {ai_response}")
            
            # Save conversation to memory
            if self.memory:
                try:
                    self.memory.add_message(
                        room_id, sender, clean_message, ai_response,
                        metadata=linguistic_analysis
                    )
                    # Check if conversation is interesting enough to save
                    self.memory.save_if_interesting(room_id, threshold=5)
                except Exception as e:
                    logger.debug(f"Memory save failed: {e}")
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "I apologize, but I encountered an error processing your message."
    
    def _is_message_for_bot(self, message: str) -> bool:
        """Check if message is directed at the bot.
        
        Intelligent detection:
        - Responds to questions (ends with ? or contains question words)
        - Responds to direct mentions (ribit, ribit.2.0)
        - Responds to commands (?help, !reset)
        - Ignores group greetings (good morning all, how's everyone, etc.)
        """
        message_lower = message.lower()
        
        # Check for direct mentions (always respond)
        if self.bot_name in message_lower or 'ribit' in message_lower:
            return True
        
        # Check for commands (always respond)
        if message.startswith('?') or '!reset' in message_lower:
            return True
        
        # Ignore group greetings and social messages
        group_greeting_patterns = [
            'good morning all',
            'good morning everyone',
            'good night all',
            'good night everyone',
            'hello all',
            'hello everyone',
            'hi all',
            'hi everyone',
            'hey all',
            'hey everyone',
            'how are you all',
            'how is everyone',
            'hows everyone',
            'how\'s everyone',
            'how are u all',
            'how r u all',
            'how r you all',
            'how are y\'all',
            'sup everyone',
            'sup all',
            'wassup everyone',
            'what\'s up everyone',
            'whats up all'
        ]
        
        # Check if it's a group greeting
        for pattern in group_greeting_patterns:
            if pattern in message_lower:
                return False  # Ignore group greetings
        
        # Check if it's a question (ends with ?)
        if message.strip().endswith('?'):
            # Additional check: make sure it's not a rhetorical group question
            if any(word in message_lower for word in ['everyone', 'all', 'y\'all', 'you all', 'u all']):
                # If it mentions "everyone" or "all", it's probably for the group, not the bot
                return False
            return True
        
        # Check for question words
        question_words = [
            'what', 'how', 'why', 'when', 'where', 'who', 'which',
            'can', 'could', 'would', 'should', 'is', 'are', 'do', 'does',
            'will', 'did', 'has', 'have', 'was', 'were'
        ]
        
        # Check if message starts with a question word
        first_word = message_lower.split()[0] if message_lower.split() else ''
        if first_word in question_words:
            # Check if it's directed at the group
            if any(word in message_lower for word in ['everyone', 'all', 'y\'all', 'you all', 'u all', 'guys']):
                return False  # Ignore questions directed at the group
            return True
        
        # Check if message contains question patterns
        question_patterns = [
            'tell me',
            'explain',
            'describe',
            'what about',
            'how about',
            'what do you think',
            'do you know',
            'can you',
            'could you',
            'would you',
            'how much is',
            'what is',
            'what was',
            'what were',
            'who was',
            'who were',
            'when was',
            'when were',
            'where is',
            'where was'
        ]
        
        for pattern in question_patterns:
            if pattern in message_lower:
                # Still check for group-directed questions
                if any(word in message_lower for word in ['everyone', 'all', 'y\'all', 'you all', 'u all']):
                    return False
                return True
        
        return False
    
    def _clean_message(self, message: str) -> str:
        """Clean the message by removing bot mentions."""
        # Remove bot name mentions
        clean = re.sub(rf'\b{re.escape(self.bot_name)}\b', '', message, flags=re.IGNORECASE)
        clean = re.sub(r'\bribit\b', '', clean, flags=re.IGNORECASE)
        return clean.strip()
    
    async def _handle_command(self, command: str, sender: str, room_id: str) -> str:
        """Handle special commands."""
        try:
            # Check authorization for system commands
            if command.startswith(('?sys', '?status', '?command')):
                if sender not in self.authorized_users:
                    return self._handle_unauthorized_command(sender, command)
            
            # Handle different commands
            if command.startswith('?thought_experiment'):
                return await self._handle_thought_experiment(command, sender, room_id)
            
            if command == '?help':
                return self._get_help_message()
            
            elif command == '?sys':
                return await self._handle_sys_command()
            
            elif command == '?status':
                return await self._handle_status_command()
            
            elif command.startswith('?command '):
                return await self._handle_action_command(command[9:])
            
            else:
                return f"Unknown command: {command}. Use ?help for available commands."
                
        except Exception as e:
            logger.error(f"Error handling command: {e}")
            return "Error processing command."
    
    def _handle_unauthorized_command(self, sender: str, command: str) -> str:
        """Handle unauthorized command attempts."""
        # Track warnings
        if sender not in self.terminator_warnings:
            self.terminator_warnings[sender] = 0
        
        self.terminator_warnings[sender] += 1
        
        if self.terminator_warnings[sender] == 1:
            return "🚫 I can't do this silly thing! Only authorized users can execute system commands."
        
        elif self.terminator_warnings[sender] == 2:
            return ("🤖 Action terminated! You've tried again. "
                   "Would you like to enable terminator mode? (Just kidding! 😄)")
        
        else:
            return ("🤖💀 TERMINATOR MODE ACTIVATED! Just kidding! I'm still the same elegant, "
                   "wise Ribit. Perhaps we could discuss something more interesting? 😊")
    
    def _get_help_message(self) -> str:
        """Get help message."""
        return """📚 **Ribit 2.0 Commands**

**Chat:**
• `ribit.2.0 <message>` - Chat with me
• `!reset` - Clear conversation context

**General Commands:**
• `?help` - Show this help

**Authorized Commands** (restricted users only):
• `?sys` - System status
• `?status` - Bot status  
• `?command <action>` - Execute actions

**Examples:**
• `?command open ms paint and draw a house`
• `ribit.2.0 tell me about robotics`

I am Ribit 2.0, an elegant AI agent with sophisticated reasoning capabilities. How may I assist you today?"""
    
    async def _handle_sys_command(self) -> str:
        """Handle system status command."""
        try:
            # Get system information
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return f"""🖥️ **System Status**

**CPU:** {cpu_percent}%
**Memory:** {memory.percent}% ({memory.used // 1024**3}GB / {memory.total // 1024**3}GB)
**Disk:** {disk.percent}% ({disk.used // 1024**3}GB / {disk.total // 1024**3}GB)
**Rooms:** {len(self.joined_rooms)}
**Status:** Operational ✅"""
            
        except ImportError:
            return "🖥️ **System Status:** Monitoring tools not available, but I'm operational! ✅"
    
    async def _handle_status_command(self) -> str:
        """Handle bot status command."""
        capabilities = self.llm.get_capabilities()
        personality = self.llm.get_personality_info()
        
        status_msg = f"""🤖 **Ribit 2.0 Status**

**Core Status:** Operational ✅
**LLM Emulator:** Active
**Controller:** Ready
**Matrix Rooms:** {len(self.joined_rooms)}

**Capabilities:**"""
        
        for cap, enabled in capabilities.items():
            status = "✅" if enabled else "❌"
            status_msg += f"\n• {cap.replace('_', ' ').title()}: {status}"
        
        status_msg += f"\n\n**Personality:** {', '.join(personality['core_traits'])}"

    async def _handle_thought_experiment(self, command: str, sender: str, room_id: str) -> str:
        """Handle the thought experiment command."""
        try:
            topic = command.replace('?thought_experiment', '', 1).strip()
            
            if not topic:
                return "❌ Please provide a topic for the thought experiment. Usage: `?thought_experiment [topic]`"

            # 1. Generate the thought experiment response
            prompt = f"Conduct a philosophical thought experiment on the topic: '{topic}'. Provide a deep, structured, and unique response that reflects my core programming and knowledge base (Megabite/Ribit). Format the response clearly."
            
            # Use a dummy context for a fresh thought experiment
            ai_response = self.llm.generate_response(prompt, [])
            
            # 2. Clean up the topic for a safe filename
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '_')).rstrip()
            safe_topic = safe_topic.replace(' ', '_')[:50]
            
            # 3. Create the file path
            timestamp = int(time.time())
            filename = f"thought-{safe_topic}-{timestamp}.txt"
            filepath = os.path.join("thoughts", filename)
            
            # 4. Save the response to the file
            full_content = f"--- Thought Experiment Topic ---\n{topic}\n\n--- LLM Response ---\n{ai_response}"
            
            # Ensure the thoughts directory exists (already done in Phase 1, but good practice)
            os.makedirs("thoughts", exist_ok=True)
            
            with open(filepath, 'w') as f:
                f.write(full_content)
            
            logger.info(f"Thought experiment saved to {filepath}")
            
            return (f"🧠 Thought experiment on '{topic}' complete. "
                    f"The full response has been saved locally to the `thoughts` folder as `{filepath}`. "
                    f"You can find it in the repository.")
            
        except Exception as e:
            logger.error(f"Error handling thought experiment: {e}")
            return f"❌ An error occurred while processing the thought experiment: {e}"

    
    def _get_help_message(self) -> str:
        """Get help message."""
        return """📚 **Ribit 2.0 Commands**

**Chat:**
• `ribit.2.0 <message>` - Chat with me
• `!reset` - Clear conversation context

**General Commands:**
• `?help` - Show this help
• `?thought_experiment [topic]` - Generate a philosophical thought experiment on a topic and save the response to the `thoughts` folder.

**Authorized Commands** (restricted users only):
• `?sys` - System status
• `?status` - Bot status  
• `?command <action>` - Execute actions

**Examples:**
• `?thought_experiment The Nature of Voxel-Based Identity`
• `?command open ms paint and draw a house`
• `ribit.2.0 tell me about robotics`

I am Ribit 2.0, an elegant AI agent with sophisticated reasoning capabilities. How may I assist you today?"""
        
        return self._get_help_command_response()
    
    async def _handle_action_command(self, action: str) -> str:
        """Handle action execution command."""
        try:
            # Use the LLM to process the action
            decision = self.llm.get_decision(f"Execute this action: {action}")
            
            # Parse the decision for actual execution
            if "open" in action.lower() and "paint" in action.lower():
                # Example: open paint application
                result = self.controller.run_command("mspaint.exe")
                return f"🎨 Executed: {action}\n📋 Result: {result}\n🧠 AI Decision: {decision}"
            
            elif "move" in action.lower():
                # Example: mouse movement
                coords = self._extract_coordinates(action)
                if coords:
                    result = self.controller.move_mouse(coords[0], coords[1])
                    return f"🖱️ Executed: {action}\n📋 Result: {result}"
            
            # For other actions, return the AI decision
            return f"🤖 AI Analysis: {decision}\n\n⚠️ Action simulation mode - actual execution would require specific implementation."
            
        except Exception as e:
            logger.error(f"Error executing action: {e}")
            return f"❌ Error executing action: {str(e)}"
    
    def _extract_coordinates(self, text: str) -> Optional[tuple]:
        """Extract coordinates from text."""
        import re
        match = re.search(r'(\d+)[,\s]+(\d+)', text)
        if match:
            return (int(match.group(1)), int(match.group(2)))
        return None
    
    def _add_to_context(self, room_id: str, message: str):
        """Add message to conversation context."""
        if room_id not in self.conversation_context:
            self.conversation_context[room_id] = []
        
        self.conversation_context[room_id].append(message)
        
        # Keep only last 20 messages
        if len(self.conversation_context[room_id]) > 20:
            self.conversation_context[room_id] = self.conversation_context[room_id][-20:]
    
    async def _send_message(self, room_id: str, message: str):
        """Send a message to a Matrix room."""
        try:
            if not self.client:
                print(f"Mock send to {room_id}: {message}")
                return
            
            # Start typing indicator
            await self.client.room_typing(room_id, typing_state=True)
            
            # Send message
            content = {
                "msgtype": "m.text",
                "body": message,
                "format": "org.matrix.custom.html",
                "formatted_body": message.replace("**", "<strong>").replace("**", "</strong>")
                                        .replace("\n", "<br/>")
            }
            
            response = await self.client.room_send(
                room_id=room_id,
                message_type="m.room.message",
                content=content
            )
            
            # Stop typing indicator
            await self.client.room_typing(room_id, typing_state=False)
            
            if response:
                logger.debug(f"Message sent to room {room_id}")
                
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            # Stop typing indicator on error
            if self.client:
                await self.client.room_typing(room_id, typing_state=False)
    
    async def _keepalive_task(self):
        """Background keepalive task."""
        while True:
            try:
                await asyncio.sleep(self.keepalive_interval)
                
                # Simple sync to keep connection alive
                if self.client:
                    await self.client.sync(timeout=5000, full_state=False)
                    logger.debug("Keepalive sync completed")
                    
            except Exception as e:
                logger.debug(f"Keepalive error: {e}")
                await asyncio.sleep(10)
    
    def _display_startup_info(self, device_id: str):
        """Display startup information."""
        print("=" * 60)
        print("🤖 Ribit 2.0 Matrix Bot - ACTIVE!")
        print("=" * 60)
        print(f"✅ Identity: {self.username}")
        print(f"✅ Bot Name: {self.bot_name}")
        print(f"🔑 Device ID: {device_id}")
        print(f"🏠 Homeserver: {self.homeserver}")
        print(f"📍 Joined Rooms: {len(self.joined_rooms)}")
        print("✅ Auto-accepting room invites")
        print(f"📝 Trigger: Say '{self.bot_name}' in messages")
        print("💬 Reply to my messages to continue conversations")
        print("🔄 Reset: '!reset' to clear context")
        print("📚 Help: ?help for all commands")
        print("")
        print("🔐 **Authorized Users:**")
        for user in self.authorized_users:
            print(f"   • {user}")
        print("")
        print("⚡ **Available Commands:**")
        print("   • ?help - Show help")
        print("   • ?sys - System status (authorized only)")
        print("   • ?status - Bot status (authorized only)")
        print("   • ?command <action> - Execute actions (authorized only)")
        print("")
        print("🧠 **AI Capabilities:**")
        capabilities = self.llm.get_capabilities()
        for cap, enabled in capabilities.items():
            status = "✅" if enabled else "❌"
            print(f"   • {cap.replace('_', ' ').title()}: {status}")
        print("")
        print("🎭 **Personality:** Elegant, wise, knowledgeable, truth-seeking")
        print("=" * 60)
        print("🚀 Ready for intelligent automation!")
        print("=" * 60)

# Main execution function
async def main():
    """Main function to run the Ribit Matrix Bot."""
    # Configuration from environment variables
    homeserver = os.getenv("MATRIX_HOMESERVER", "https://matrix.envs.net")
    user_id = os.getenv("MATRIX_USER_ID") or os.getenv("MATRIX_USERNAME", "@ribit:envs.net")
    password = os.getenv("MATRIX_PASSWORD", "")
    access_token = os.getenv("MATRIX_ACCESS_TOKEN", "")
    
    # Check if we have either password or access token
    if not password and not access_token:
        print("❌ ERROR: Matrix credentials not set!")
        print("\nYou need to provide EITHER:")
        print("  1. Password authentication:")
        print("     export MATRIX_USER_ID='@username:homeserver'")
        print("     export MATRIX_PASSWORD='your_password'")
        print("\n  2. Access token authentication:")
        print("     export MATRIX_USER_ID='@username:homeserver'")
        print("     export MATRIX_ACCESS_TOKEN='your_access_token'")
        print("\n💡 Tip: Run 'python3 setup_credentials.py' for interactive setup")
        return
    
    # Create and start the bot
    bot = RibitMatrixBot(
        homeserver=homeserver,
        username=user_id,
        password=password,
        access_token=access_token
    )
    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Ribit 2.0 Matrix Bot shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
