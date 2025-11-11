import logging
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .deltachat_bot import DeltaChatRibotBot
    from .matrix_bot import RibitMatrixBot

class BridgeRelay:
    """
    Mock Bridge Relay for cross-platform message passing between DeltaChat and Matrix.
    In a real scenario, this would manage the connection and message queues.
    """
    def __init__(self, deltachat_bot: 'DeltaChatRibotBot' = None, matrix_bot: 'RibitMatrixBot' = None):
        self.deltachat_bot = deltachat_bot
        self.matrix_bot = matrix_bot
        logger.info("BridgeRelay initialized in MOCK mode.")

    def set_bots(self, deltachat_bot: 'DeltaChatRibotBot', matrix_bot: 'RibitMatrixBot'):
        self.deltachat_bot = deltachat_bot
        self.matrix_bot = matrix_bot
        logger.info("BridgeRelay bots set.")

    async def relay_from_deltachat(self, sender_email: str, sender_name: str, message: str, chat_id: int):
        """Relay a message from DeltaChat to Matrix."""
        logger.info(f"Relaying from DeltaChat to Matrix: {sender_name}: {message}")
        if self.matrix_bot:
            # In a real scenario, this would send to a specific Matrix room
            # For mock purposes, we'll simulate the message being received by the Matrix bot
            # and check for the 'post note' command.
            await self.matrix_bot.receive_relayed_message(sender_name, "DeltaChat", message)

    async def relay_from_matrix(self, sender_name: str, message: str, room_id: str):
        """Relay a message from Matrix to DeltaChat."""
        logger.info(f"Relaying from Matrix to DeltaChat: {sender_name}: {message}")
        if self.deltachat_bot:
            # In a real scenario, this would send to a specific DeltaChat contact/chat
            # For mock purposes, we'll simulate the message being received by the DeltaChat bot
            # and check for the 'post note' command.
            await self.deltachat_bot.receive_relayed_message(sender_name, "Matrix", message)

    async def handle_post_note(self, sender_name: str, platform: str, message: str):
        """Handles the 'post note' command and relays it to the other platform."""
        target_platform = "Matrix" if platform == "DeltaChat" else "DeltaChat"
        
        # 1. Format the relayed message
        relayed_message = (
            f"[Post Note] User {sender_name} from {platform}: {message} | "
            f"To respond, use 'post note <response message>'"
        )

        # 2. Relay the message
        if target_platform == "Matrix" and self.matrix_bot:
            # In a real bridge, this would send to the designated bridge room
            # For mock, we'll just log it and return the message for the bot to display
            logger.info(f"BRIDGE: Relaying Post Note to Matrix: {relayed_message}")
            # In a real scenario, the Matrix bot would have a method to send this message
            # await self.matrix_bot.send_message_to_bridge_room(relayed_message)
            return f"Post Note relayed to Matrix: {relayed_message}"
        
        elif target_platform == "DeltaChat" and self.deltachat_bot:
            # In a real bridge, this would send to the designated bridge contact/chat
            logger.info(f"BRIDGE: Relaying Post Note to DeltaChat: {relayed_message}")
            # In a real scenario, the DeltaChat bot would have a method to send this message
            # await self.deltachat_bot.send_message_to_bridge_chat(relayed_message)
            return f"Post Note relayed to DeltaChat: {relayed_message}"
        
        return f"Error: Could not relay Post Note to {target_platform}."
