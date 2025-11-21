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
        RoomMessageImage,
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
    
    class RoomMessageImage:
        """Mock RoomMessageImage for type annotations when matrix-nio is not installed."""
        pass

# # from .mock_llm_wrapper import MockRibit20LLM
from .controller import VisionSystemController
from .offline_image_analyzer import OfflineImageAnalyzer
from .matrix_history_tracker import MatrixHistoryTracker
from .image_provider import (
    ImageAnalysisProvider,
    OfflineImageProvider,
    WebAIImageProvider,
    FallbackImageProvider
)

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
        
        # Admin users with full command privileges (?sys, ?status, ?command)
        # @rabit232:envs.net is the primary admin user
        self.authorized_users = authorized_users or {
            "@ribit:envs.net",
            "@rabit232:envs.net"  # Primary admin user
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
        
        # Initialize offline features
        try:
            offline_analyzer = OfflineImageAnalyzer()
            offline_provider = OfflineImageProvider(offline_analyzer)
            
            providers = [offline_provider]
            
            webai_url = os.getenv("WEBAI_API_URL", "")
            webai_model = os.getenv("WEBAI_MODEL", "gemini-pro-vision")
            enable_webai_fallback = os.getenv("ENABLE_WEBAI_FALLBACK", "false").lower() == "true"
            
            if enable_webai_fallback and webai_url:
                webai_provider = WebAIImageProvider(
                    api_url=webai_url,
                    model=webai_model,
                    timeout=30
                )
                providers.append(webai_provider)
                logger.info(f"✅ WebAI fallback enabled: {webai_url} (model: {webai_model})")
            
            if len(providers) > 1:
                self.image_analyzer = FallbackImageProvider(providers)
                logger.info(f"✅ Image analysis with fallback: {' → '.join([p.get_name() for p in providers])}")
            else:
                self.image_analyzer = offline_provider
                logger.info("✅ Offline image analyzer initialized (no fallback)")
                
        except Exception as e:
            logger.warning(f"Failed to initialize image analyzer: {e}")
            self.image_analyzer = None
        
        try:
            db_path = os.getenv("MATRIX_HISTORY_DB", "matrix_message_history.db")
            self.history_tracker = MatrixHistoryTracker(db_path=db_path)
            logger.info("✅ Message history tracker initialized (90-day retention)")
        except Exception as e:
            logger.warning(f"Failed to initialize message history tracker: {e}")
            self.history_tracker = None
        
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
        
        # User preferences (per-user settings)
        self.user_personality: Dict[str, str] = {}  # user_id -> "ribit" or "megabite"
        self.user_model: Dict[str, str] = {}  # user_id -> model name
        
        # Default settings
        self.default_personality = "ribit"  # Technical assistant
        self.default_model = "offline"  # Offline analyzer
        
        # Available models
        self.available_models = {
            "offline": "Offline Image Analyzer (Private, No API)",
            "webai-gemini": "Google Gemini Pro Vision via WebAI",
            "webai-gpt4": "OpenAI GPT-4 Vision via WebAI",
            "webai-claude": "Anthropic Claude 3 Vision via WebAI",
            "webai-deepseek": "DeepSeek Vision via WebAI"
        }
        
        # Available personalities
        self.available_personalities = {
            "ribit": "Ribit - Technical AI Assistant (detailed, precise)",
            "megabite": "Megabite - Friendly Companion (casual, warm)"
        }
        
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
            logger.info("Matrix libraries not available, running in mock mode")
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
            
            # Add image upload handler if available
            if MATRIX_AVAILABLE:
                self.client.add_event_callback(self._handle_image, RoomMessageImage)
            
            # Initial sync with shorter timeout
            logger.info("🔄 Performing initial sync...")
            try:
                sync_response = await asyncio.wait_for(
                    self.client.sync(timeout=10000, full_state=False),
                    timeout=15.0
                )
                logger.info(f"✅ Initial sync completed")
                
                # Mark initial messages as processed
                await self._mark_initial_messages_processed(sync_response)
            except asyncio.TimeoutError:
                logger.warning("Initial sync timed out, continuing anyway...")
            except Exception as sync_error:
                logger.error(f"Initial sync failed: {sync_error}")
                # Continue anyway - bot can still function
            
            # Start background tasks
            asyncio.create_task(self._keepalive_task())
            
            # Display startup information
            self._display_startup_info(device_id)
            
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
            
            # Track message in history database
            if self.history_tracker:
                try:
                    sender_name = event.sender.split(':')[0].replace('@', '')
                    self.history_tracker.add_message(
                        room_id=room.room_id,
                        sender=event.sender,
                        sender_name=sender_name,
                        message_text=event.body
                    )
                except Exception as e:
                    logger.debug(f"Failed to track message in history: {e}")

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
    
    async def _handle_image(self, room: MatrixRoom, event: RoomMessageImage):
        """Handle incoming image uploads and analyze them."""
        try:
            # Skip if already processed
            if event.event_id in self.processed_events:
                return
            
            # Skip own messages
            if event.sender == self.client.user_id:
                return
            
            # Mark as processed
            self.processed_events.add(event.event_id)
            
            # Check if image analyzer is available
            if not self.image_analyzer:
                logger.warning("Image analyzer not available, skipping image analysis")
                return
            
            try:
                # Get image URL from event
                if hasattr(event, 'url'):
                    # Send initial response
                    await self._send_message(room.room_id, "🔍 Analyzing image... Please wait.")
                    
                    # Download image from Matrix server
                    download_response = await self.client.download(
                        server_name=event.url.split("/")[2],
                        media_id=event.url.split("/")[-1]
                    )
                    
                    if hasattr(download_response, 'body') and download_response.body:
                        # Save image temporarily
                        import tempfile
                        from PIL import Image
                        import io
                        
                        try:
                            # Convert bytes to image
                            image_data = io.BytesIO(download_response.body)
                            image = Image.open(image_data)
                            
                            # Convert to RGB if necessary (handle PNG, etc.)
                            if image.mode not in ('RGB', 'L'):
                                image = image.convert('RGB')
                            
                            # Verify image was loaded
                            if image.width == 0 or image.height == 0:
                                raise ValueError("Invalid image dimensions")
                            
                            logger.info(f"Image loaded: {image.width}x{image.height}, mode={image.mode}")
                            
                            # Get user's selected model
                            user_model = self.user_model.get(event.sender, self.default_model)
                            
                            # Create appropriate provider based on user's model preference
                            if user_model.startswith('webai-'):
                                # WebAI model requested
                                model_map = {
                                    'webai-gemini': 'gemini-pro-vision',
                                    'webai-gpt4': 'gpt-4-vision',
                                    'webai-claude': 'claude-3-opus',
                                    'webai-deepseek': 'deepseek-vision'
                                }
                                
                                webai_url = os.getenv("WEBAI_API_URL", "")
                                webai_model_name = model_map.get(user_model, 'gemini-pro-vision')
                                
                                if webai_url:
                                    from .image_provider import WebAIImageProvider
                                    provider = WebAIImageProvider(
                                        api_url=webai_url,
                                        model=webai_model_name,
                                        timeout=30
                                    )
                                    logger.info(f"Using WebAI model: {webai_model_name}")
                                else:
                                    # Fallback to offline if WebAI not configured
                                    provider = self.image_analyzer
                                    logger.warning(f"WebAI requested but not configured, using offline analyzer")
                            else:
                                # Offline model (default)
                                provider = self.image_analyzer
                                logger.info(f"Using offline image analyzer")
                            
                            # Analyze the image using selected provider (async)
                            analysis = await provider.analyze_image(image)
                            
                            if 'error' in analysis:
                                error_msg = analysis.get('error', 'Unknown error')
                                logger.error(f"Image analysis failed: {error_msg}")
                                await self._send_message(room.room_id, 
                                    f"❌ Could not analyze image: {error_msg}")
                                return
                            
                            description = analysis.get('description', 'Image uploaded successfully')
                            
                            # Simply send the rich description as-is
                            await self._send_message(room.room_id, description)
                            logger.info(f"✅ Image analysis completed successfully")
                            
                        except Exception as img_error:
                            import traceback
                            error_details = traceback.format_exc()
                            logger.error(f"Error processing image data: {type(img_error).__name__}: {img_error}")
                            logger.debug(f"Full traceback: {error_details}")
                            await self._send_message(room.room_id, 
                                "❌ Could not process image. The file may be corrupted or in an unsupported format. "
                                "Supported formats: JPEG, PNG, GIF, BMP, WebP")
                        
                    else:
                        logger.error("Download response has no body")
                        await self._send_message(room.room_id, "❌ Failed to download image data.")
                        
            except Exception as e:
                logger.error(f"Error in image handler: {e}", exc_info=True)
                await self._send_message(room.room_id, 
                    f"❌ Error analyzing image. Please try again or use a different image format.")
            
        except Exception as e:
            logger.error(f"Error handling image: {e}")

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
                    welcome_msg = "Hello! How can I help you?"
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
        - Responds to direct mentions (ribit, ribit.2.0, bot, ai)
        - Responds to commands (?help, !reset)
        - Responds to direct address patterns (hey bot, tell me, explain)
        - Ignores group greetings (good morning all, how's everyone, etc.)
        """
        message_lower = message.lower()
        
        # Check for direct mentions (always respond)
        bot_mentions = ['ribit', 'bot', 'ai', '@ribit', self.bot_name]
        if any(mention in message_lower for mention in bot_mentions):
            return True
        
        # Check for commands (always respond)
        if message.startswith('?') or '!reset' in message_lower:
            return True
        
        # Check for direct address patterns (always respond)
        direct_address = [
            'hey bot', 'hi bot', 'hello bot',
            'hey ai', 'hi ai', 'hello ai',
            'tell me', 'can you tell',
            'explain', 'describe',
            'what is', 'what are', 'what was',
            'who is', 'who are',
            'help me', 'show me',
            'do you know'
        ]
        if any(pattern in message_lower for pattern in direct_address):
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
                return self._get_help_message(sender)
            
            elif command.startswith('?model'):
                return await self._handle_model_command(command, sender)
            
            elif command.startswith('?personality'):
                return await self._handle_personality_command(command, sender)
            
            elif command == '?sys':
                return await self._handle_sys_command()
            
            elif command == '?status':
                return await self._handle_status_command(sender)
            
            elif command.startswith('?command '):
                return await self._handle_action_command(command[9:])
            
            elif command.startswith('?search '):
                return await self._handle_search_command(command[8:], room_id)
            
            elif command.startswith('?history'):
                return await self._handle_history_command(command, room_id)
            
            elif command.startswith('?words'):
                return await self._handle_words_command(command)
            
            elif command.startswith('?learn '):
                return await self._handle_learn_command(command[7:], sender, room_id)
            
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
    
    def _get_help_message(self, sender: str) -> str:
        """Get help message with current user settings."""
        current_model = self.user_model.get(sender, self.default_model)
        current_personality = self.user_personality.get(sender, self.default_personality)
        
        return f"""📚 **Ribit 2.0 Commands**

**Chat:**
• `ribit.2.0 <message>` - Chat with me
• `!reset` - Clear conversation context

**General Commands:**
• `?help` - Show this help
• `?status` - Show your current settings
• `?search <query>` - Search 3-month message history (natural language)
• `?history` - View message history statistics
• `?words [number]` - View learned words (default: 120, max: 500)
• `?learn <text>` - Teach me new knowledge and add to my vocabulary

**Image Analysis:**
• Upload any image - I'll analyze it automatically!
• `?model list` - Show available image analysis models
• `?model <name>` - Switch to different model (offline, webai-gemini, etc.)

**Personality:**
• `?personality list` - Show available personalities
• `?personality ribit` - Technical AI assistant mode
• `?personality megabite` - Friendly companion mode

**Authorized Commands** (admin users only):
• `?sys` - System status
• `?command <action>` - Execute actions

**Your Current Settings:**
• Model: **{current_model}**
• Personality: **{current_personality}**

**Examples:**
• `?model webai-gemini` - Use Gemini for image analysis
• `?personality megabite` - Switch to friendly mode
• `?words 200` - Show top 200 learned words
• `?search did alice mention python last week?`
• `?learn Python is a powerful programming language for AI`
• `?thought_experiment What if artificial intelligence became conscious?`

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
    
    async def _handle_status_command(self, sender: str) -> str:
        """Handle bot status command."""
        current_model = self.user_model.get(sender, self.default_model)
        current_personality = self.user_personality.get(sender, self.default_personality)
        model_desc = self.available_models.get(current_model, "Unknown")
        personality_desc = self.available_personalities.get(current_personality, "Unknown")
        
        try:
            capabilities = self.llm.get_capabilities()
            personality = self.llm.get_personality_info()
        except:
            capabilities = []
            personality = {}
        
        status_msg = f"""🤖 **Ribit 2.0 Status**

**Core Status:** Operational ✅
**LLM Emulator:** Active
**Controller:** Ready
**Matrix Rooms:** {len(self.joined_rooms)}

**Your Settings:**
• Image Model: **{current_model}**
  {model_desc}
• Personality: **{current_personality}**
  {personality_desc}

**Capabilities:**"""
        
        for cap, enabled in capabilities.items():
            status = "✅" if enabled else "❌"
            status_msg += f"\n• {cap.replace('_', ' ').title()}: {status}"
        
        status_msg += f"\n\n**Personality:** {', '.join(personality.get('core_traits', []))}" if personality else ""
        
        return status_msg
    
    async def _handle_model_command(self, command: str, sender: str) -> str:
        """Handle model switching command."""
        try:
            parts = command.split(maxsplit=1)
            
            if len(parts) == 1 or parts[1] == 'list':
                # Show available models
                models_list = "🎨 **Available Image Analysis Models:**\n\n"
                current_model = self.user_model.get(sender, self.default_model)
                
                for model_id, description in self.available_models.items():
                    marker = "✅" if model_id == current_model else "○"
                    models_list += f"{marker} `{model_id}`\n   {description}\n\n"
                
                models_list += f"**Current model:** {current_model}\n\n"
                models_list += "**Usage:** `?model <name>` (e.g., `?model webai-gemini`)"
                
                return models_list
            
            # Switch to specified model
            new_model = parts[1].lower().strip()
            
            if new_model not in self.available_models:
                return f"❌ Unknown model: {new_model}\n\nUse `?model list` to see available models."
            
            # Check if WebAI models are enabled
            if new_model.startswith('webai-'):
                enable_webai = os.getenv("ENABLE_WEBAI_FALLBACK", "false").lower() == "true"
                webai_url = os.getenv("WEBAI_API_URL", "")
                
                if not enable_webai or not webai_url:
                    return f"""❌ WebAI fallback is not enabled.

To use WebAI models, set these environment variables:
• `ENABLE_WEBAI_FALLBACK=true`
• `WEBAI_API_URL=<your-webai-server-url>`

Then restart the bot."""
            
            # Update user's model preference
            self.user_model[sender] = new_model
            
            return f"""✅ Image analysis model updated!

**New model:** {new_model}
**Description:** {self.available_models[new_model]}

Upload an image to test the new model!"""
            
        except Exception as e:
            logger.error(f"Error handling model command: {e}")
            return "❌ Error switching model. Please try again."
    
    async def _handle_personality_command(self, command: str, sender: str) -> str:
        """Handle personality switching command."""
        try:
            parts = command.split(maxsplit=1)
            
            if len(parts) == 1 or parts[1] == 'list':
                # Show available personalities
                personalities_list = "🎭 **Available Personalities:**\n\n"
                current_personality = self.user_personality.get(sender, self.default_personality)
                
                for personality_id, description in self.available_personalities.items():
                    marker = "✅" if personality_id == current_personality else "○"
                    personalities_list += f"{marker} `{personality_id}`\n   {description}\n\n"
                
                personalities_list += f"**Current personality:** {current_personality}\n\n"
                personalities_list += "**Usage:** `?personality <name>` (e.g., `?personality megabite`)"
                
                return personalities_list
            
            # Switch to specified personality
            new_personality = parts[1].lower().strip()
            
            if new_personality not in self.available_personalities:
                return f"❌ Unknown personality: {new_personality}\n\nUse `?personality list` to see available personalities."
            
            # Update user's personality preference
            self.user_personality[sender] = new_personality
            
            # Get personality-specific greeting
            if new_personality == "ribit":
                greeting = "I am now in Ribit mode - precise, technical, and detail-oriented. How may I assist you?"
            else:  # megabite
                greeting = "Hey there! 😊 I'm now in Megabite mode - friendly and casual. What's up?"
            
            return f"""✅ Personality updated!

**New personality:** {new_personality}
**Description:** {self.available_personalities[new_personality]}

{greeting}"""
            
        except Exception as e:
            logger.error(f"Error handling personality command: {e}")
            return "❌ Error switching personality. Please try again."

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
    
    async def _handle_learn_command(self, text: str, sender: str, room_id: str) -> str:
        """Handle learn command to teach the bot new knowledge."""
        try:
            if not text.strip():
                return "❌ Please provide text to learn from. Example: `?learn Python is a programming language`"
            
            # Learn from the text using word learning system
            if self.word_learner:
                self.word_learner.learn_from_message(text)
                stats = self.word_learner.get_statistics()
                
                # Update LLM knowledge base
                try:
                    concept = text.split('.')[0][:50] if '.' in text else text[:50]
                    self.llm.update_knowledge(concept, text[:200])
                except:
                    pass
                
                return f"""✅ **Knowledge Learned!**

📝 **Text:** {text[:100]}{'...' if len(text) > 100 else ''}

📊 **Learning Progress:**
• Vocabulary size: {stats.get('vocabulary_size', 0)} words
• Patterns learned: {stats.get('unique_patterns', 0)}
• Words tracked: {stats.get('word_pairs_known', 0)} pairs

🧠 I've added this to my knowledge base and will use it in future conversations!"""
            else:
                return "⚠️ Learning system not available, but I'll remember what you said!"
            
        except Exception as e:
            logger.error(f"Error handling learn command: {e}")
            return f"❌ Error learning from text: {str(e)}"
    
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
    
    async def _handle_search_command(self, query: str, room_id: str) -> str:
        """Handle message search command."""
        try:
            if not self.history_tracker:
                return "❌ Message history tracking is not enabled."
            
            if not query.strip():
                return "❌ Please provide a search query. Example: `?search did alice mention python`"
            
            # Search for messages
            results = self.history_tracker.search_messages(query, room_id=room_id, limit=5)
            
            if not results:
                return f"🔍 No messages found matching: \"{query}\""
            
            # Format results
            response_parts = [
                f"🔍 **Search Results** for: \"{query}\"",
                f"Found {len(results)} messages:\n"
            ]
            
            for msg in results:
                sender_name = msg.get('sender_name', msg.get('sender', 'Unknown'))
                timestamp = msg.get('timestamp', '')
                text = msg.get('message_text', '')
                
                # Truncate long messages
                if len(text) > 100:
                    text = text[:97] + "..."
                
                response_parts.append(f"• **{sender_name}** ({timestamp}): {text}")
            
            return "\n".join(response_parts)
            
        except Exception as e:
            logger.error(f"Error searching messages: {e}")
            return f"❌ Error searching messages: {str(e)}"
    
    async def _handle_history_command(self, command: str, room_id: str) -> str:
        """Handle message history command."""
        try:
            if not self.history_tracker:
                return "❌ Message history tracking is not enabled."
            
            # Get statistics
            stats = self.history_tracker.get_statistics(room_id=room_id)
            
            response_parts = [
                "📊 **Message History Statistics**\n",
                f"• Total Messages: {stats.get('total_messages', 0)}",
                f"• Unique Senders: {stats.get('unique_senders', 0)}",
                f"• Words Learned: {stats.get('words_learned', 0)}",
                f"• Retention Period: {stats.get('retention_days', 90)} days\n"
            ]
            
            # Top topics
            top_topics = stats.get('top_topics', [])
            if top_topics:
                response_parts.append("**Top Topics:**")
                for topic, count in top_topics[:5]:
                    response_parts.append(f"  • {topic}: {count} mentions")
            
            return "\n".join(response_parts)
            
        except Exception as e:
            logger.error(f"Error getting history: {e}")
            return f"❌ Error getting history: {str(e)}"
    
    async def _handle_words_command(self, command: str) -> str:
        """Handle word library command with optional limit parameter."""
        try:
            if not self.history_tracker:
                return "❌ Message history tracking is not enabled."
            
            # Parse limit parameter (e.g., "?words 200" or "?words 120")
            limit = 120  # Default to 120 words
            parts = command.strip().split()
            if len(parts) > 1:
                try:
                    limit = int(parts[1])
                    # Cap at reasonable maximum
                    limit = min(limit, 500)
                except ValueError:
                    return "❌ Invalid number. Usage: `?words` or `?words <number>` (e.g., `?words 200`)"
            
            # Get word library stats
            words = self.history_tracker.get_word_library(limit=limit)
            
            if not words:
                return "📚 No words have been learned yet from the past 3 months."
            
            # Get total word count
            stats = self.history_tracker.get_statistics()
            total_words = stats.get('words_learned', len(words))
            
            response_parts = [
                f"📚 **Word Library** (Top {len(words)} of {total_words} words from 3-month history)\n"
            ]
            
            for word_data in words:
                word = word_data.get('word', '')
                frequency = word_data.get('frequency', 0)
                response_parts.append(f"• {word}: {frequency} times")
            
            return "\n".join(response_parts)
            
        except Exception as e:
            logger.error(f"Error getting word library: {e}")
            return f"❌ Error getting word library: {str(e)}"
    
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
        try:
            capabilities = self.llm.get_capabilities() if hasattr(self.llm, 'get_capabilities') else {}
            for cap, enabled in capabilities.items():
                status = "✅" if enabled else "❌"
                print(f"   • {cap.replace('_', ' ').title()}: {status}")
            if not capabilities:
                print("   • LLM Ready ✅")
        except Exception as e:
            print(f"   • LLM Ready ✅")
        print("")
        print("🎭 **Personality:** Elegant, wise, knowledgeable, truth-seeking")
        print("=" * 60)
        print("🚀 Ready for intelligent automation!")
        print("=" * 60)

# Main execution function
async def main():
    """Main function to run the Ribit Matrix Bot."""
    # Load environment variables from .env file if it exists
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        logger.info(f"Loaded environment from {env_path}")
    
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
