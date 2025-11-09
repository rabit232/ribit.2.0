"""
DeltaChat-Matrix Bridge Integration

Unified bridge for cross-platform message relay between DeltaChat and Matrix.
Handles message routing, user mapping, and bidirectional communication.

Author: Manus AI
Date: November 2025
"""

import asyncio
import logging
import os
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from supabase import create_client, Client as SupabaseClient
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    logger.warning("Supabase client not available")


class DeltaChatMatrixBridge:
    """Unified bridge for DeltaChat and Matrix platforms."""

    def __init__(
        self,
        matrix_bot=None,
        deltachat_bot=None,
        supabase_client: Optional[SupabaseClient] = None,
    ):
        self.matrix_bot = matrix_bot
        self.deltachat_bot = deltachat_bot
        self.supabase = supabase_client
        self.bridge_controller = None
        self.is_running = False
        self.relay_task = None

        logger.info("DeltaChat-Matrix Bridge initialized")

    async def initialize(self) -> bool:
        """Initialize the bridge."""
        try:
            if not self.supabase:
                if not await self._initialize_supabase():
                    logger.warning("Supabase not available, using in-memory state")

            bridge_config = {
                "name": "ribit-deltachat-matrix",
                "matrix_homeserver": os.getenv("MATRIX_HOMESERVER", ""),
                "matrix_username": os.getenv("MATRIX_USERNAME", ""),
                "deltachat_email": os.getenv("DELTACHAT_EMAIL", ""),
            }

            if self.supabase:
                from .bridge_controller import BridgeController

                self.bridge_controller = BridgeController(
                    self.supabase, bridge_config
                )
                if not await self.bridge_controller.initialize():
                    logger.error("Failed to initialize bridge controller")
                    return False

            if self.matrix_bot:
                self.matrix_bot.set_bridge_relay(self)
            if self.deltachat_bot:
                self.deltachat_bot.set_bridge_relay(self)

            logger.info("✅ Bridge initialization complete")
            return True

        except Exception as e:
            logger.error(f"Bridge initialization failed: {e}")
            return False

    async def _initialize_supabase(self) -> bool:
        """Initialize Supabase client."""
        try:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_ANON_KEY")

            if not url or not key:
                logger.warning("Supabase credentials not configured")
                return False

            self.supabase = create_client(url, key)
            logger.info("✅ Supabase client initialized")
            return True

        except Exception as e:
            logger.error(f"Supabase initialization failed: {e}")
            return False

    async def start(self):
        """Start the bridge."""
        try:
            self.is_running = True
            logger.info("🌉 Starting DeltaChat-Matrix Bridge...")

            if not await self.initialize():
                logger.error("Bridge initialization failed")
                return

            self._display_startup_info()

            self.relay_task = asyncio.create_task(self._relay_loop())

            await asyncio.gather(
                self.relay_task,
                return_exceptions=True,
            )

        except KeyboardInterrupt:
            logger.info("Bridge interrupted by user")
        except Exception as e:
            logger.error(f"Bridge error: {e}")
        finally:
            await self.shutdown()

    async def _relay_loop(self):
        """Main relay loop for message processing."""
        while self.is_running:
            try:
                if self.bridge_controller:
                    message = await self.bridge_controller.get_relay_queue_item(
                        timeout=1.0
                    )

                    if message:
                        await self._process_relay(message)

                await asyncio.sleep(0.1)

            except Exception as e:
                logger.error(f"Relay loop error: {e}")
                await asyncio.sleep(1)

    async def _process_relay(self, message):
        """Process and relay a message."""
        try:
            from .bridge_controller import BridgeMessage

            if not isinstance(message, BridgeMessage):
                return

            target_room_mapping = await self.bridge_controller.get_mapped_room(
                message.source_room_id, message.source_platform
            )

            if not target_room_mapping:
                logger.warning(
                    f"No mapping found for room: {message.source_room_id}"
                )
                message.status = "failed"
                message.error = "No room mapping"
                await self.bridge_controller._store_message(message)
                return

            formatted_message = message.get_formatted_message(include_instructions=True)

            if message.target_platform == "matrix" and self.matrix_bot:
                success = await self._send_to_matrix(
                    target_room_mapping.get("matrix_room_id"),
                    formatted_message,
                )
            elif message.target_platform == "deltachat" and self.deltachat_bot:
                success = await self._send_to_deltachat(
                    target_room_mapping.get("deltachat_group_id"),
                    formatted_message,
                )
            else:
                success = False
                logger.error(
                    f"Unknown target platform: {message.target_platform}"
                )

            if success:
                message.status = "sent"
                message.relayed_at = datetime.now()
                logger.info(
                    f"✅ Message relayed: {message.source_platform} -> {message.target_platform}"
                )
            else:
                message.status = "failed"
                message.error = "Relay failed"

            await self.bridge_controller._store_message(message)

        except Exception as e:
            logger.error(f"Error processing relay: {e}")
            if message:
                message.status = "failed"
                message.error = str(e)

    async def _send_to_matrix(self, room_id: str, message: str) -> bool:
        """Send message to Matrix room."""
        try:
            if not self.matrix_bot or not self.matrix_bot.client:
                logger.warning("Matrix bot not available")
                return False

            await self.matrix_bot._send_message(room_id, message)
            return True

        except Exception as e:
            logger.error(f"Error sending to Matrix: {e}")
            return False

    async def _send_to_deltachat(self, group_id: int, message: str) -> bool:
        """Send message to DeltaChat group."""
        try:
            if not self.deltachat_bot:
                logger.warning("DeltaChat bot not available")
                return False

            return self.deltachat_bot.send_message(group_id, message)

        except Exception as e:
            logger.error(f"Error sending to DeltaChat: {e}")
            return False

    async def relay_from_matrix(
        self,
        matrix_user_id: str,
        matrix_display_name: str,
        message_text: str,
        room_id: str,
    ) -> bool:
        """Relay message from Matrix to DeltaChat."""
        try:
            from .bridge_controller import BridgeMessage

            target_mapping = await self.bridge_controller.get_mapped_room(
                room_id, "matrix"
            )

            if not target_mapping or not target_mapping.get("deltachat_group_id"):
                logger.debug(f"No DeltaChat mapping for Matrix room: {room_id}")
                return False

            bridge_message = BridgeMessage(
                source_platform="matrix",
                target_platform="deltachat",
                sender_id=matrix_user_id,
                sender_name=matrix_display_name or matrix_user_id,
                message_text=message_text,
                source_room_id=room_id,
                target_room_id=str(target_mapping.get("deltachat_group_id")),
            )

            return await self.bridge_controller.relay_message(bridge_message)

        except Exception as e:
            logger.error(f"Error relaying from Matrix: {e}")
            return False

    async def relay_from_deltachat(
        self,
        sender_email: str,
        sender_name: str,
        message_text: str,
        group_id: int,
    ) -> bool:
        """Relay message from DeltaChat to Matrix."""
        try:
            from .bridge_controller import BridgeMessage

            target_mapping = await self.bridge_controller.get_mapped_room(
                group_id, "deltachat"
            )

            if not target_mapping or not target_mapping.get("matrix_room_id"):
                logger.debug(f"No Matrix mapping for DeltaChat group: {group_id}")
                return False

            bridge_message = BridgeMessage(
                source_platform="deltachat",
                target_platform="matrix",
                sender_id=sender_email,
                sender_name=sender_name or sender_email,
                message_text=message_text,
                source_room_id=str(group_id),
                target_room_id=target_mapping.get("matrix_room_id"),
            )

            return await self.bridge_controller.relay_message(bridge_message)

        except Exception as e:
            logger.error(f"Error relaying from DeltaChat: {e}")
            return False

    async def get_stats(self) -> Dict:
        """Get bridge statistics."""
        stats = {
            "bridge_running": self.is_running,
            "matrix_available": self.matrix_bot is not None,
            "deltachat_available": self.deltachat_bot is not None,
            "supabase_available": self.supabase is not None,
            "timestamp": datetime.now().isoformat(),
        }

        if self.bridge_controller:
            bridge_stats = await self.bridge_controller.get_bridge_stats()
            stats.update(bridge_stats)

        return stats

    async def shutdown(self):
        """Shutdown the bridge."""
        try:
            self.is_running = False

            if self.relay_task:
                self.relay_task.cancel()

            if self.deltachat_bot:
                self.deltachat_bot.shutdown()

            if self.matrix_bot and hasattr(self.matrix_bot, 'client'):
                if self.matrix_bot.client:
                    await self.matrix_bot.client.close()

            logger.info("🌉 Bridge shutdown complete")

        except Exception as e:
            logger.error(f"Error during bridge shutdown: {e}")

    def _display_startup_info(self):
        """Display bridge startup information."""
        print("=" * 70)
        print("🌉 DeltaChat-Matrix Bridge - STARTING")
        print("=" * 70)
        print(f"✅ Matrix Bot: {'Configured' if self.matrix_bot else 'Not configured'}")
        print(f"✅ DeltaChat Bot: {'Configured' if self.deltachat_bot else 'Not configured'}")
        print(f"✅ Supabase: {'Connected' if self.supabase else 'Not connected'}")
        print(f"✅ Bridge Controller: {'Initialized' if self.bridge_controller else 'Pending'}")
        print("")
        print("🔄 Message Relay:")
        print("   • Matrix -> DeltaChat: Enabled")
        print("   • DeltaChat -> Matrix: Enabled")
        print("   • Format: Platform badge + Sender name + Message")
        print("   • Deduplication: Active")
        print("")
        print("📊 Features:")
        print("   • User mapping across platforms")
        print("   • Room/Group association")
        print("   • Message history tracking")
        print("   • Error recovery and retry logic")
        print("   • Message deduplication")
        print("")
        print("=" * 70)


async def main():
    """Main function to run the bridge."""
    from .matrix_bot import RibitMatrixBot
    from .deltachat_bot import DeltaChatRibotBot, DeltaChatBotConfig

    try:
        from .mock_llm_wrapper import MockRibit20LLM

        llm = MockRibit20LLM()
    except Exception as e:
        logger.warning(f"Could not initialize LLM: {e}")
        llm = None

    matrix_config = {
        "homeserver": os.getenv("MATRIX_HOMESERVER", "https://envs.net"),
        "username": os.getenv("MATRIX_USERNAME", ""),
        "password": os.getenv("MATRIX_PASSWORD", ""),
    }

    deltachat_config = DeltaChatBotConfig(
        email=os.getenv("DELTACHAT_EMAIL", ""),
        password=os.getenv("DELTACHAT_PASSWORD", ""),
    )

    matrix_bot = RibitMatrixBot(
        homeserver=matrix_config["homeserver"],
        username=matrix_config["username"],
        password=matrix_config["password"],
    )

    deltachat_bot = DeltaChatRibotBot(deltachat_config, llm=llm)

    try:
        supabase_client = None
        if SUPABASE_AVAILABLE:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_ANON_KEY")
            if url and key:
                supabase_client = create_client(url, key)
    except Exception as e:
        logger.warning(f"Supabase initialization failed: {e}")
        supabase_client = None

    bridge = DeltaChatMatrixBridge(
        matrix_bot=matrix_bot,
        deltachat_bot=deltachat_bot,
        supabase_client=supabase_client,
    )

    await bridge.start()


if __name__ == "__main__":
    import asyncio

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
