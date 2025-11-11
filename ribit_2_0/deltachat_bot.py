"""
DeltaChat Bot Integration for Ribit 2.0

Enables Ribit 2.0 to operate on DeltaChat platform with intelligent responses
and cross-platform message relay with Matrix.

Author: Manus AI
Date: November 2025
"""

import asyncio
import logging
import os
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import deltachat
    from deltachat import Chat
    from deltachat.events import EventType
    DELTACHAT_AVAILABLE = True
    logger.info("DeltaChat library detected and imported successfully")
except ImportError:
    DELTACHAT_AVAILABLE = False
    logger.warning("DeltaChat library not installed. Run: pip install deltabot")


class DeltaChatBotConfig:
    """Configuration for DeltaChat Bot."""

    def __init__(
        self,
        db_path: str = "deltachat.db",
        email: str = "",
        password: str = "",
        smtp_server: str = "",
        imap_server: str = "",
        display_name: str = "Ribit 2.0",
    ):
        self.db_path = db_path
        self.email = email or os.getenv("DELTACHAT_EMAIL", "")
        self.password = password or os.getenv("DELTACHAT_PASSWORD", "")
        self.smtp_server = smtp_server or os.getenv("DELTACHAT_SMTP", "")
        self.imap_server = imap_server or os.getenv("DELTACHAT_IMAP", "")
        self.display_name = display_name


class DeltaChatRibotBot:
    """DeltaChat Bot powered by Ribit 2.0 LLM."""

    def __init__(
        self,
        config: DeltaChatBotConfig,
        llm=None,
        enable_bridge: bool = True,
    ):
        self.config = config
        self.llm = llm
        self.enable_bridge = enable_bridge
        self.is_running = False
        self.chat = None
        self.conversation_context: Dict[int, List[str]] = {}
        self.message_handlers: Dict[str, Callable] = {}
        self.bridge_relay: Optional[BridgeRelay] = None

        logger.info(f"DeltaChat Bot initialized for {config.email}")

    async def initialize(self):
        """Initialize DeltaChat bot."""
        if not DELTACHAT_AVAILABLE:
            logger.error("DeltaChat not available!")
            return False

        try:
            self.chat = Chat(self.config.db_path)

            if not self.chat.is_configured():
                await self._configure_account()
            else:
                logger.info(f"Using existing account: {self.chat.get_config('addr')}")

            logger.info("✅ DeltaChat Bot initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize DeltaChat Bot: {e}")
            return False

    async def _configure_account(self):
        """Configure DeltaChat account."""
        try:
            if not self.config.email or not self.config.password:
                logger.error("Email and password required for configuration")
                raise ValueError("Missing credentials")

            logger.info(f"Configuring DeltaChat account: {self.config.email}")

            self.chat.set_config("addr", self.config.email)
            self.chat.set_config("mail_pw", self.config.password)
            self.chat.set_config("displayname", self.config.display_name)

            if self.config.smtp_server:
                self.chat.set_config("send_server", self.config.smtp_server)
            if self.config.imap_server:
                self.chat.set_config("recv_server", self.config.imap_server)

            logger.info("✅ DeltaChat account configured successfully")

        except Exception as e:
            logger.error(f"Account configuration failed: {e}")
            raise

    async def start(self):
        """Start the DeltaChat bot."""
        if not DELTACHAT_AVAILABLE:
            logger.warning("Running DeltaChat Bot in mock mode")
            await self._run_mock_mode()
            return

        try:
            if not await self.initialize():
                return

            self.is_running = True

            logger.info("🤖 DeltaChat Bot starting...")

            self.chat.on_new_message(self._handle_message)

            self._display_startup_info()

            await self._run_event_loop()

        except Exception as e:
            logger.error(f"DeltaChat Bot error: {e}")
        finally:
            self.shutdown()

    def _handle_message(self, message):
        """Handle incoming DeltaChat message."""
        try:
            if message.is_system_message():
                logger.debug(f"System message: {message.text}")
                return

            sender = message.get_sender_contact()
            chat = message.chat

            logger.info(f"📨 Message from {sender.email} in {chat.get_name()}: {message.text}")

            response = asyncio.run(
                self._process_message(
                    message.text, sender.email, chat.id, sender.display_name
                )
            )

            if response:
                chat.send_text(response)
                logger.debug(f"Response sent to {chat.get_name()}")

        except Exception as e:
            logger.error(f"Error handling message: {e}")

    async def _process_message(
        self, text: str, sender_email: str, chat_id: int, sender_name: str
    ) -> Optional[str]:
        """Process message and generate response."""
        try:
            # --- 1. Handle 'post note' command for cross-platform relay ---
            if self.enable_bridge and self.bridge_relay and text.lower().startswith("post note"):
                note_content = text[len("post note"):].strip()
                if note_content:
                    # Relay the message to the other platform via the bridge
                    relay_status = await self.bridge_relay.handle_post_note(
                        sender_name, "DeltaChat", note_content
                    )
                    return f"✅ Post Note relayed. {relay_status}"
                else:
                    return "❌ Post Note command requires a message. Usage: 'post note <message>'"

            # --- 2. Normal LLM processing ---
            context = self.conversation_context.get(chat_id, [])
            self._add_to_context(chat_id, f"User ({sender_name}): {text}")

            if self.llm:
                # Use Megabite's specific method
                if hasattr(self.llm, 'generate_response'):
                    response = self.llm.generate_response(text, context)
                # Fallback to Ribit's method
                elif hasattr(self.llm, 'get_decision'):
                    response = self.llm.get_decision(text)
                else:
                    response = f"LLM Error: Unknown response method."
            else:
                response = f"Echo: {text}"

            self._add_to_context(chat_id, f"Bot: {response}")

            return response

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return f"Error: {str(e)}"

    def _add_to_context(self, chat_id: int, message: str):
        """Add message to conversation context."""
        if chat_id not in self.conversation_context:
            self.conversation_context[chat_id] = []

        self.conversation_context[chat_id].append(message)

        if len(self.conversation_context[chat_id]) > 20:
            self.conversation_context[chat_id] = self.conversation_context[chat_id][-20:]

    async def _run_event_loop(self):
        """Run the DeltaChat event loop."""
        try:
            while self.is_running:
                self.chat.wait_for_incoming_message()
                await asyncio.sleep(0.1)

        except KeyboardInterrupt:
            logger.info("DeltaChat Bot interrupted")
        except Exception as e:
            logger.error(f"Event loop error: {e}")

    async def _run_mock_mode(self):
        """Run in mock mode when DeltaChat is not available."""
        print("🤖 DeltaChat Bot - Mock Mode")
        print("=" * 50)
        print("✅ Ribit 2.0: Ready")
        print("⚠️  DeltaChat: Running in mock mode")
        print("=" * 50)

        while True:
            try:
                user_input = input("\nSimulate DeltaChat message (or 'quit'): ")
                if user_input.lower() == "quit":
                    break

                if self.llm:
                    if hasattr(self.llm, 'generate_response'):
                        response = self.llm.generate_response(user_input, [])
                    elif hasattr(self.llm, 'get_decision'):
                        response = self.llm.get_decision(user_input)
                    else:
                        response = f"LLM Error: Unknown response method."
                else:
                    response = f"Mock response: {user_input}"

                print(f"🤖 Ribit: {response}")

            except KeyboardInterrupt:
                break

        print("👋 Mock mode ended")

    def set_bridge_relay(self, bridge_relay):
        """Set the bridge relay for cross-platform messaging."""
        self.bridge_relay = bridge_relay
        logger.info("Bridge relay configured for DeltaChat Bot")

    def send_message(self, chat_id_or_email: str, message: str):
        """Send a message to a DeltaChat chat or contact."""
        try:
            if not DELTACHAT_AVAILABLE or not self.chat:
                logger.warning("DeltaChat not available")
                return False

            if isinstance(chat_id_or_email, int):
                chat = self.chat.get_chat(chat_id_or_email)
            else:
                chat = self.chat.create_chat_by_contact(
                    self.chat.create_contact(chat_id_or_email)
                )

            if chat:
                chat.send_text(message)
                logger.debug(f"Message sent: {message[:50]}...")
                return True

            return False

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    def shutdown(self):
        """Shutdown the DeltaChat bot."""
        try:
            self.is_running = False
            if self.chat:
                self.chat.close()
            logger.info("DeltaChat Bot shutdown complete")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

    def _display_startup_info(self):
        """Display startup information."""
        print("=" * 60)
        print("🤖 DeltaChat Bot - ACTIVE!")
        print("=" * 60)
        print(f"✅ Account: {self.config.email}")
        print(f"✅ Display Name: {self.config.display_name}")
        print(f"✅ Bridge Enabled: {self.enable_bridge}")
        if self.llm:
            print(f"✅ LLM: {self.llm.name}")
            print(f"✅ LLM Type: {self.llm.__class__.__name__}")
            
            # Megabite Status Check
            if self.llm.__class__.__name__ == "MegabiteLLM":
                from .megabite_llm import MegabiteLLM
                megabite_status = MegabiteLLM.check_status()
                print(f"✅ Megabite Core: {megabite_status['status_message']}")
        print("")
        print("🚀 Ready to receive messages!")
        print("=" * 60)


async def main():
    """Main function to run the DeltaChat Bot."""
    config = DeltaChatBotConfig(
        email=os.getenv("DELTACHAT_EMAIL", ""),
        password=os.getenv("DELTACHAT_PASSWORD", ""),
    )

    try:
        from .megabite_llm import MegabiteLLM
        llm = MegabiteLLM()
        logger.info("Using MegabiteLLM for DeltaChat Bot.")
    except Exception as e:
        logger.warning(f"Could not initialize MegabiteLLM: {e}. Falling back to MockRibit20LLM.")
        try:
            from .mock_llm_wrapper import MockRibit20LLM
            llm = MockRibit20LLM()
        except Exception as e2:
            logger.error(f"Could not initialize any LLM: {e2}")
            llm = None

    bot = DeltaChatRibotBot(config, llm=llm)
    await bot.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
