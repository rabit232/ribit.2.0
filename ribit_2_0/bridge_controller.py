"""
Matrix-DeltaChat Bridge Controller

Manages cross-platform message routing, user mapping, and room associations
between Matrix and DeltaChat platforms.

Author: Manus AI
Date: November 2025
"""

import logging
import asyncio
import uuid
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)


class BridgeMessage:
    """Represents a message being relayed across platforms."""

    def __init__(
        self,
        source_platform: str,
        target_platform: str,
        sender_id: str,
        sender_name: str,
        message_text: str,
        source_room_id: str,
        target_room_id: str,
    ):
        self.message_id = str(uuid.uuid4())
        self.source_platform = source_platform
        self.target_platform = target_platform
        self.sender_id = sender_id
        self.sender_name = sender_name
        self.message_text = message_text
        self.source_room_id = source_room_id
        self.target_room_id = target_room_id
        self.created_at = datetime.now()
        self.status = "pending"
        self.error = None

    def get_formatted_message(self, include_instructions: bool = True) -> str:
        """Format message with sender platform and instructions."""
        platform_emoji = "📱" if self.source_platform == "deltachat" else "💻"
        formatted = f"{platform_emoji} **[{self.source_platform.upper()}] {self.sender_name}:**\n{self.message_text}"

        if include_instructions:
            if self.source_platform == "deltachat":
                formatted += (
                    "\n\n_To reply on DeltaChat: Reply to the bot's email_"
                )
            else:
                formatted += "\n\n_To reply on Matrix: Use this room_"

        return formatted

    def get_dedup_hash(self) -> str:
        """Get hash for deduplication check."""
        content = f"{self.sender_id}{self.message_text}{self.source_platform}"
        return hashlib.md5(content.encode()).hexdigest()


class BridgeController:
    """Controls message relay and user mapping between platforms."""

    def __init__(self, supabase_client, bridge_config: Dict):
        self.supabase = supabase_client
        self.bridge_config = bridge_config
        self.bridge_id = None
        self.user_mapping_cache: Dict[str, Dict] = {}
        self.room_mapping_cache: Dict[str, Dict] = {}
        self.processed_messages: set = set()
        self.relay_queue: asyncio.Queue = asyncio.Queue()

        logger.info("Bridge Controller initialized")

    async def initialize(self) -> bool:
        """Initialize bridge in Supabase."""
        try:
            config_data = {
                "matrix_homeserver": self.bridge_config.get("matrix_homeserver", ""),
                "matrix_username": self.bridge_config.get("matrix_username", ""),
                "deltachat_email": self.bridge_config.get("deltachat_email", ""),
                "created_at": datetime.now().isoformat(),
            }

            response = self.supabase.table("bridge_config").insert(
                {
                    "bridge_name": self.bridge_config.get("name", "ribit-bridge"),
                    "matrix_homeserver": config_data["matrix_homeserver"],
                    "matrix_username": config_data["matrix_username"],
                    "deltachat_email": config_data["deltachat_email"],
                    "enabled": True,
                    "config_data": config_data,
                }
            ).execute()

            if response.data:
                self.bridge_id = response.data[0]["id"]
                logger.info(f"✅ Bridge initialized with ID: {self.bridge_id}")

                await self._initialize_bridge_state()
                return True

        except Exception as e:
            logger.error(f"Failed to initialize bridge: {e}")

        return False

    async def _initialize_bridge_state(self):
        """Initialize bridge state table."""
        try:
            self.supabase.table("bridge_state").insert(
                {
                    "bridge_id": self.bridge_id,
                    "matrix_connected": False,
                    "deltachat_connected": False,
                    "status": "initializing",
                    "status_message": "Bridge initializing...",
                }
            ).execute()
        except Exception as e:
            logger.error(f"Failed to initialize bridge state: {e}")

    async def map_matrix_user(
        self, matrix_user_id: str, display_name: str, deltachat_email: str
    ) -> Optional[str]:
        """Create or retrieve user mapping."""
        try:
            mapping_id = str(uuid.uuid4())

            response = self.supabase.table("user_mappings").insert(
                {
                    "id": mapping_id,
                    "matrix_user_id": matrix_user_id,
                    "matrix_display_name": display_name,
                    "deltachat_email": deltachat_email,
                    "bridge_id": self.bridge_id,
                }
            ).execute()

            if response.data:
                self.user_mapping_cache[matrix_user_id] = response.data[0]
                logger.info(f"✅ User mapped: {matrix_user_id} -> {deltachat_email}")
                return mapping_id

        except Exception as e:
            logger.debug(f"User mapping error (may already exist): {e}")

        return await self._get_user_mapping(matrix_user_id)

    async def _get_user_mapping(self, matrix_user_id: str) -> Optional[str]:
        """Get existing user mapping."""
        try:
            if matrix_user_id in self.user_mapping_cache:
                return self.user_mapping_cache[matrix_user_id].get("id")

            response = (
                self.supabase.table("user_mappings")
                .select("*")
                .eq("matrix_user_id", matrix_user_id)
                .eq("bridge_id", self.bridge_id)
                .execute()
            )

            if response.data:
                self.user_mapping_cache[matrix_user_id] = response.data[0]
                return response.data[0]["id"]

        except Exception as e:
            logger.error(f"Error getting user mapping: {e}")

        return None

    async def map_room(
        self,
        matrix_room_id: str,
        matrix_room_name: str,
        deltachat_group_id: int,
        deltachat_group_name: str,
    ) -> Optional[str]:
        """Create room mapping between platforms."""
        try:
            mapping_id = str(uuid.uuid4())

            response = self.supabase.table("room_mappings").insert(
                {
                    "id": mapping_id,
                    "matrix_room_id": matrix_room_id,
                    "matrix_room_name": matrix_room_name,
                    "deltachat_group_id": deltachat_group_id,
                    "deltachat_group_name": deltachat_group_name,
                    "bridge_id": self.bridge_id,
                    "bidirectional": True,
                }
            ).execute()

            if response.data:
                self.room_mapping_cache[matrix_room_id] = response.data[0]
                logger.info(
                    f"✅ Room mapped: {matrix_room_id} -> {deltachat_group_id}"
                )
                return mapping_id

        except Exception as e:
            logger.error(f"Error mapping room: {e}")

        return None

    async def get_mapped_room(
        self, room_id: str, source_platform: str
    ) -> Optional[Dict]:
        """Get mapped room for target platform."""
        try:
            if room_id in self.room_mapping_cache:
                return self.room_mapping_cache[room_id]

            if source_platform == "matrix":
                response = (
                    self.supabase.table("room_mappings")
                    .select("*")
                    .eq("matrix_room_id", room_id)
                    .eq("bridge_id", self.bridge_id)
                    .execute()
                )
            else:
                response = (
                    self.supabase.table("room_mappings")
                    .select("*")
                    .eq("deltachat_group_id", room_id)
                    .eq("bridge_id", self.bridge_id)
                    .execute()
                )

            if response.data:
                mapping = response.data[0]
                self.room_mapping_cache[room_id] = mapping
                return mapping

        except Exception as e:
            logger.error(f"Error getting room mapping: {e}")

        return None

    async def relay_message(self, bridge_message: BridgeMessage) -> bool:
        """Relay message to target platform."""
        try:
            dedup_hash = bridge_message.get_dedup_hash()

            if dedup_hash in self.processed_messages:
                logger.debug(f"Duplicate message filtered: {dedup_hash}")
                bridge_message.status = "deduped"
                return await self._store_message(bridge_message)

            self.processed_messages.add(dedup_hash)

            if len(self.processed_messages) > 10000:
                self.processed_messages = set(list(self.processed_messages)[-5000:])

            await self.relay_queue.put(bridge_message)
            return await self._store_message(bridge_message)

        except Exception as e:
            logger.error(f"Error relaying message: {e}")
            bridge_message.status = "failed"
            bridge_message.error = str(e)
            await self._store_message(bridge_message)
            return False

    async def _store_message(self, bridge_message: BridgeMessage) -> bool:
        """Store message in database."""
        try:
            self.supabase.table("bridge_messages").insert(
                {
                    "message_id": bridge_message.message_id,
                    "source_platform": bridge_message.source_platform,
                    "target_platform": bridge_message.target_platform,
                    "sender_id": bridge_message.sender_id,
                    "sender_name": bridge_message.sender_name,
                    "message_text": bridge_message.message_text,
                    "source_room_id": bridge_message.source_room_id,
                    "target_room_id": bridge_message.target_room_id,
                    "relay_status": bridge_message.status,
                    "relay_error": bridge_message.error,
                    "bridge_id": self.bridge_id,
                }
            ).execute()

            return True

        except Exception as e:
            logger.error(f"Error storing message: {e}")
            return False

    async def update_bridge_state(
        self,
        matrix_connected: bool = None,
        deltachat_connected: bool = None,
        status: str = None,
        status_message: str = None,
    ) -> bool:
        """Update bridge state in database."""
        try:
            update_data = {"updated_at": datetime.now().isoformat()}

            if matrix_connected is not None:
                update_data["matrix_connected"] = matrix_connected
            if deltachat_connected is not None:
                update_data["deltachat_connected"] = deltachat_connected
            if status:
                update_data["status"] = status
            if status_message:
                update_data["status_message"] = status_message

            self.supabase.table("bridge_state").update(update_data).eq(
                "bridge_id", self.bridge_id
            ).execute()

            return True

        except Exception as e:
            logger.error(f"Error updating bridge state: {e}")
            return False

    async def get_bridge_stats(self) -> Dict:
        """Get bridge statistics."""
        try:
            messages = (
                self.supabase.table("bridge_messages")
                .select("count", count="exact")
                .eq("bridge_id", self.bridge_id)
                .execute()
            )

            relayed = (
                self.supabase.table("bridge_messages")
                .select("count", count="exact")
                .eq("bridge_id", self.bridge_id)
                .eq("relay_status", "sent")
                .execute()
            )

            failed = (
                self.supabase.table("bridge_messages")
                .select("count", count="exact")
                .eq("bridge_id", self.bridge_id)
                .eq("relay_status", "failed")
                .execute()
            )

            return {
                "total_messages": messages.count or 0,
                "relayed_messages": relayed.count or 0,
                "failed_messages": failed.count or 0,
                "user_mappings": len(self.user_mapping_cache),
                "room_mappings": len(self.room_mapping_cache),
            }

        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}

    async def cleanup_old_messages(self, days: int = 30) -> int:
        """Clean up old messages from database."""
        try:
            from datetime import timedelta

            cutoff_date = (
                datetime.now() - timedelta(days=days)
            ).isoformat()

            response = (
                self.supabase.table("bridge_messages")
                .delete()
                .lt("created_at", cutoff_date)
                .eq("bridge_id", self.bridge_id)
                .execute()
            )

            count = len(response.data) if response.data else 0
            logger.info(f"Cleaned up {count} old messages")
            return count

        except Exception as e:
            logger.error(f"Error cleaning up messages: {e}")
            return 0

    async def get_relay_queue_item(self, timeout: float = 1.0) -> Optional[BridgeMessage]:
        """Get next message from relay queue."""
        try:
            return await asyncio.wait_for(self.relay_queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None
        except Exception as e:
            logger.error(f"Error getting relay queue item: {e}")
            return None
