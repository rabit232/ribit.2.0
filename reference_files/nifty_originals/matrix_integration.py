"""
Matrix integration for Chatbot
"""
import asyncio
import logging
import time
import os
from pathlib import Path
from nio import (
    AsyncClient, 
    AsyncClientConfig,
    LoginResponse, 
    RoomMessageText, 
    InviteMemberEvent,
    MatrixRoom,
    JoinResponse
)
from config.settings import (
    HOMESERVER, USERNAME, PASSWORD, BOT_USERNAME, ENABLE_MEME_GENERATION,
    ENABLE_PRICE_TRACKING, ENABLE_STOCK_MARKET, INTEGRATIONS, LLM_PROVIDER, OPENROUTER_MODEL,
    OLLAMA_MODEL, MAX_ROOM_HISTORY, MAX_CONTEXT_LOOKBACK, OLLAMA_KEEP_ALIVE,
    MATRIX_SYNC_TIMEOUT, MATRIX_REQUEST_TIMEOUT, MATRIX_KEEPALIVE_INTERVAL,
    MATRIX_FULL_SYNC_INTERVAL, OLLAMA_WARM_INTERVAL, ENABLE_WEB_SEARCH,
    LLM_TIMEOUT, SEARCH_TIMEOUT
)

logger = logging.getLogger(__name__)

# Global variables to store callbacks - will be imported later to avoid circular imports
message_callback = None
mark_event_processed = None
invite_callback = None
joined_rooms = None
cleanup_old_context = None
meme_generator = None
stats_tracker = None
stock_tracker = None
world_clock = None
price_tracker = None
settings_manager = None
system_monitor = None

def initialize_handlers():
    """Initialize handlers after module is loaded to avoid circular imports"""
    global message_callback, mark_event_processed, invite_callback, joined_rooms
    global cleanup_old_context, meme_generator, stats_tracker, stock_tracker, world_clock, price_tracker
    global settings_manager, system_monitor
    
    from modules.message_handler import message_callback as mc, mark_event_processed as mep
    from modules.invite_handler import invite_callback as ic, joined_rooms as jr
    from modules.cleanup import cleanup_old_context as coc
    from modules.meme_generator import meme_generator as mg
    from modules.stats_tracker import stats_tracker as st
    from modules.stock_tracker import stock_tracker as stk
    from modules.world_clock import world_clock as wc
    from modules.price_tracker import price_tracker as pt
    from modules.settings_manager import settings_manager as sm
    from modules.system_monitor import system_monitor as sysm
    
    message_callback = mc
    mark_event_processed = mep
    invite_callback = ic
    joined_rooms = jr
    cleanup_old_context = coc
    meme_generator = mg
    stats_tracker = st
    stock_tracker = stk
    world_clock = wc
    price_tracker = pt
    settings_manager = sm
    system_monitor = sysm

async def simple_keepalive(client):
    """Simple keepalive to maintain connection"""
    last_sync = time.time()
    last_warm = time.time()
    
    while True:
        try:
            await asyncio.sleep(MATRIX_KEEPALIVE_INTERVAL)
            current_time = time.time()
            
            # Simple sync to keep connection alive
            if current_time - last_sync > MATRIX_KEEPALIVE_INTERVAL:
                try:
                    await client.sync(timeout=MATRIX_SYNC_TIMEOUT, full_state=False)
                    last_sync = current_time
                except Exception as e:
                    logger.debug(f"Keepalive sync failed: {e}")
            
            # Warm Ollama model if needed
            if LLM_PROVIDER == "ollama" and current_time - last_warm > OLLAMA_WARM_INTERVAL:
                try:
                    from modules.llm import call_ollama_api
                    warm_messages = [
                        {"role": "user", "content": "hi"}
                    ]
                    await call_ollama_api(warm_messages, temperature=0.1)
                    last_warm = current_time
                except Exception as e:
                    logger.debug(f"Ollama warm-up failed: {e}")
                    
        except Exception as e:
            logger.error(f"Keepalive error: {e}")
            await asyncio.sleep(10)

async def run_matrix_bot():
    """Run the Matrix bot"""
    # Initialize handlers first
    initialize_handlers()
    
    # Check for required Matrix credentials
    if not all([HOMESERVER, USERNAME, PASSWORD]):
        logger.error("Matrix credentials not configured. Please set MATRIX_HOMESERVER, MATRIX_USERNAME, and MATRIX_PASSWORD in .env file")
        print("\n❌ ERROR: Matrix credentials missing!")
        print("Please configure the following in your .env file:")
        print("  - MATRIX_HOMESERVER")
        print("  - MATRIX_USERNAME")
        print("  - MATRIX_PASSWORD")
        return
    
    # Set up client configuration with optimized settings
    config = AsyncClientConfig(
        max_limit_exceeded=0,
        max_timeouts=0,
        encryption_enabled=False,
        request_timeout=MATRIX_REQUEST_TIMEOUT,
    )
    
    # Create client
    client = AsyncClient(
        HOMESERVER, 
        USERNAME,
        config=config
    )
    
    try:
        # Login
        response = await client.login(PASSWORD, device_name=f"{BOT_USERNAME}-bot")
        if not isinstance(response, LoginResponse):
            logger.error(f"Failed to login to Matrix: {response}")
            return
        
        logger.info(f"Matrix: Logged in as {client.user_id} with device {response.device_id}")
        
        # Get list of joined rooms
        logger.info("Matrix: Getting list of joined rooms...")
        joined_rooms_response = await client.joined_rooms()
        if hasattr(joined_rooms_response, 'rooms'):
            for room_id in joined_rooms_response.rooms:
                joined_rooms.add(room_id)
                stats_tracker.record_room_join(room_id)
                logger.info(f"Matrix: Already in room: {room_id}")
        
        # Create wrapped callbacks that include the client
        async def wrapped_message_callback(room, event):
            await message_callback(client, room, event)
        
        async def wrapped_invite_callback(room, event):
            await invite_callback(client, room, event)
        
        # Add event callbacks
        client.add_event_callback(wrapped_message_callback, RoomMessageText)
        client.add_event_callback(wrapped_invite_callback, InviteMemberEvent)
        
        # Do a minimal initial sync
        logger.info("Matrix: Performing initial sync...")
        sync_filter = {
            "room": {
                "timeline": {
                    "limit": 1  # Only get the most recent message per room
                }
            }
        }
        sync_response = await client.sync(timeout=MATRIX_SYNC_TIMEOUT, full_state=False, sync_filter=sync_filter)
        logger.info(f"Matrix: Initial sync completed. Next batch: {sync_response.next_batch}")
        
        # Mark all messages from initial sync as processed
        if hasattr(sync_response, 'rooms') and hasattr(sync_response.rooms, 'join'):
            for room_id, room_data in sync_response.rooms.join.items():
                if hasattr(room_data, 'timeline') and hasattr(room_data.timeline, 'events'):
                    for event in room_data.timeline.events:
                        if hasattr(event, 'event_id'):
                            mark_event_processed(event.event_id)
        
        # Start cleanup task
        asyncio.create_task(cleanup_old_context())
        
        # Start simple keepalive
        asyncio.create_task(simple_keepalive(client))
        
        print("=" * 50)
        print(f"🤖 {BOT_USERNAME.capitalize()} Bot - Matrix Integration Active!")
        print("=" * 50)
        print(f"✅ Identity: {USERNAME}")
        print(f"✅ Bot Name: {BOT_USERNAME.capitalize()}")
        print(f"🔑 Device ID: {response.device_id}")
        print("✅ Listening for messages in all joined rooms")
        print("✅ Auto-accepting room invites")
        print(f"📝 Trigger: Say '{BOT_USERNAME}' anywhere in a message")
        print("💬 Or reply directly to any of my messages")
        print(f"🧹 Reset: '{BOT_USERNAME} !reset' to clear context")
        print("📚 Help: ?help to see all available commands")
        print("📊 Stats: ?stats to see bot statistics")
        print("🖥️ System: ?sys to see system resource usage")
        print("🕐 Clock: ?clock <city/country> for world time")
        print("💰 Price: ?price <crypto> [currency] for crypto/fiat prices")
        print("📊 Stocks: ?stonks <ticker> for stock market data")
        print("⚙️ Settings: ?setting to manage bot configuration")
        if settings_manager.is_meme_enabled():
            print("🎨 Meme generation: ?meme <topic> to create memes")
        print("⚡ Performance Mode: Optimized for speed")
        print(f"💾 Context: Tracking last {MAX_ROOM_HISTORY} messages")
        print(f"⏱️ Timeouts: {LLM_TIMEOUT}s LLM, {SEARCH_TIMEOUT}s search")
        print(f"🔄 Sync: {MATRIX_SYNC_TIMEOUT}ms timeout, {MATRIX_KEEPALIVE_INTERVAL}s keepalive")
        if ENABLE_WEB_SEARCH:
            print("🔍 Web search: ENABLED")
        else:
            print("🔍 Web search: DISABLED (for faster responses)")
        print("=" * 50)
        
        # Sync forever with optimized settings
        await client.sync_forever(
            timeout=MATRIX_SYNC_TIMEOUT,
            full_state=False,
            since=sync_response.next_batch
        )
            
    except Exception as e:
        logger.error(f"Matrix bot error: {e}")
        raise
    finally:
        await client.close()

async def send_message(client, room_id: str, content: dict):
    """Send a message to a Matrix room"""
    try:
        response = await client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content=content
        )
        
        if response:
            logger.debug(f"Message sent to room {room_id}")
            
    except Exception as e:
        logger.error(f"Error sending message: {e}")

async def handle_help_command(client, room, event):
    """Handle help command for Matrix"""
    try:
        # Start typing indicator
        await client.room_typing(room.room_id, typing_state=True)
        
        stats_tracker.record_command_usage('?help')
        
        help_text = f"""📚 **{BOT_USERNAME.capitalize()} Bot - Available Commands**

**Chat:**
• `{BOT_USERNAME} <message>` - Chat with me
• Reply to my messages to continue conversation
• `{BOT_USERNAME} !reset` - Clear conversation context

**Commands:**
• `?help` - Show this help message
• `?stats` - Show bot statistics
• `?sys` - Show system resource usage
• `?setting` - Manage bot configuration
• `?clock <city>` - Get current time for a location
• `?price <crypto>` - Get cryptocurrency prices
• `?stonks <ticker>` - Get stock information"""
        
        if settings_manager.is_meme_enabled():
            help_text += "\n• `?meme <topic>` - Generate a meme"
        
        help_text += "\n\nNeed help? Just ask me anything!"

        await send_message(
            client,
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
        await client.room_typing(room.room_id, typing_state=False)
        
    except Exception as e:
        # Stop typing indicator on error
        await client.room_typing(room.room_id, typing_state=False)
        logger.error(f"Error handling help command: {e}")

async def handle_clock_command(client, room, event):
    """Handle world clock command for Matrix"""
    try:
        # Start typing indicator
        await client.room_typing(room.room_id, typing_state=True)
        
        stats_tracker.record_command_usage('?clock')
        
        parts = event.body.strip().split(maxsplit=1)
        location = parts[1] if len(parts) > 1 else ""
        
        response = await world_clock.handle_clock_command(location)
        
        await send_message(
            client,
            room.room_id,
            {
                "msgtype": "m.text",
                "body": response.replace("**", ""),
                "format": "org.matrix.custom.html",
                "formatted_body": response.replace("**", "<strong>").replace("**", "</strong>")
                                         .replace("\n", "<br/>")
            }
        )
        
        stats_tracker.record_message_sent(room.room_id)
        
        # Stop typing indicator
        await client.room_typing(room.room_id, typing_state=False)
        
    except Exception as e:
        # Stop typing indicator on error
        await client.room_typing(room.room_id, typing_state=False)
        logger.error(f"Error handling clock command: {e}")

async def handle_price_command(client, room, event):
    """Handle price command for Matrix"""
    try:
        # Start typing indicator
        await client.room_typing(room.room_id, typing_state=True)
        
        if not ENABLE_PRICE_TRACKING:
            await send_message(
                client,
                room.room_id,
                {
                    "msgtype": "m.text",
                    "body": "Price tracking is disabled."
                }
            )
            # Stop typing indicator
            await client.room_typing(room.room_id, typing_state=False)
            return
        
        stats_tracker.record_command_usage('?price')
        
        parts = event.body.strip().split(maxsplit=1)
        query = parts[1] if len(parts) > 1 else "XMR"
        
        response = await price_tracker.get_price_response(query)
        
        if not response:
            response = "Usage: ?price btc [usd]"
        
        await send_message(
            client,
            room.room_id,
            {
                "msgtype": "m.text",
                "body": response.replace("**", ""),
                "format": "org.matrix.custom.html",
                "formatted_body": response.replace("**", "<strong>").replace("**", "</strong>")
                                         .replace("\n", "<br/>")
            }
        )
        
        stats_tracker.record_message_sent(room.room_id)
        
        # Stop typing indicator
        await client.room_typing(room.room_id, typing_state=False)
        
    except Exception as e:
        # Stop typing indicator on error
        await client.room_typing(room.room_id, typing_state=False)
        logger.error(f"Error handling price command: {e}")

async def handle_meme_command(client, room, event):
    """Handle meme generation command for Matrix"""
    try:
        # Start typing indicator
        await client.room_typing(room.room_id, typing_state=True)
        
        if not settings_manager.is_meme_enabled():
            await send_message(
                client,
                room.room_id,
                {
                    "msgtype": "m.text",
                    "body": "Meme generation is disabled."
                }
            )
            # Stop typing indicator
            await client.room_typing(room.room_id, typing_state=False)
            return
        
        stats_tracker.record_command_usage('?meme')
        
        meme_input = event.body.replace('?meme', '!meme', 1)
        meme_url, caption = await meme_generator.handle_meme_command(meme_input)
        
        if meme_url:
            formatted_body = f"{caption}\n{meme_url}"
            
            await send_message(
                client,
                room.room_id,
                {
                    "msgtype": "m.text",
                    "body": formatted_body,
                    "format": "org.matrix.custom.html",
                    "formatted_body": f'<p>{caption}</p><p><a href="{meme_url}">{meme_url}</a></p>'
                }
            )
            
            stats_tracker.record_message_sent(room.room_id)
        else:
            await send_message(
                client,
                room.room_id,
                {
                    "msgtype": "m.text",
                    "body": caption or "Failed to generate meme"
                }
            )
        
        # Stop typing indicator
        await client.room_typing(room.room_id, typing_state=False)
            
    except Exception as e:
        # Stop typing indicator on error
        await client.room_typing(room.room_id, typing_state=False)
        logger.error(f"Error handling meme command: {e}")

async def handle_stonks_command(client, room, event):
    """Handle stock market command for Matrix"""
    try:
        # Start typing indicator
        await client.room_typing(room.room_id, typing_state=True)
        
        if not ENABLE_STOCK_MARKET:
            await send_message(
                client,
                room.room_id,
                {
                    "msgtype": "m.text",
                    "body": "Stock tracking is disabled."
                }
            )
            # Stop typing indicator
            await client.room_typing(room.room_id, typing_state=False)
            return
        
        stats_tracker.record_command_usage('?stonks')
        
        parts = event.body.strip().split()
        
        if len(parts) == 1:
            response = await stock_tracker.get_market_summary()
        else:
            ticker = parts[1]
            response = await stock_tracker.get_stock_info(ticker)
        
        await send_message(
            client,
            room.room_id,
            {
                "msgtype": "m.text",
                "body": response.replace("**", ""),
                "format": "org.matrix.custom.html",
                "formatted_body": response.replace("**", "<strong>").replace("**", "</strong>")
                                         .replace("\n", "<br/>")
            }
        )
        
        stats_tracker.record_message_sent(room.room_id)
        
        # Stop typing indicator
        await client.room_typing(room.room_id, typing_state=False)
        
    except Exception as e:
        # Stop typing indicator on error
        await client.room_typing(room.room_id, typing_state=False)
        logger.error(f"Error handling stonks command: {e}")

async def handle_setting_command(client, room, event):
    """Handle setting command for Matrix"""
    try:
        # Start typing indicator
        await client.room_typing(room.room_id, typing_state=True)
        
        stats_tracker.record_command_usage('?setting')
        
        parts = event.body.strip().split(maxsplit=1)
        args = parts[1].split() if len(parts) > 1 else []
        
        user_id = event.sender
        
        response = await settings_manager.handle_setting_command(args, user_id, 'matrix')
        
        await send_message(
            client,
            room.room_id,
            {
                "msgtype": "m.text",
                "body": response.replace("**", ""),
                "format": "org.matrix.custom.html",
                "formatted_body": response.replace("**", "<strong>").replace("**", "</strong>")
                                         .replace("\n", "<br/>")
            }
        )
        
        stats_tracker.record_message_sent(room.room_id)
        
        # Stop typing indicator
        await client.room_typing(room.room_id, typing_state=False)
        
    except Exception as e:
        # Stop typing indicator on error
        await client.room_typing(room.room_id, typing_state=False)
        logger.error(f"Error handling setting command: {e}")

async def handle_sys_command(client, room, event):
    """Handle system resource monitor command for Matrix"""
    try:
        # Start typing indicator
        await client.room_typing(room.room_id, typing_state=True)
        
        stats_tracker.record_command_usage('?sys')
        
        response = system_monitor.get_system_info()
        
        await send_message(
            client,
            room.room_id,
            {
                "msgtype": "m.text",
                "body": response.replace("**", ""),
                "format": "org.matrix.custom.html",
                "formatted_body": response.replace("**", "<strong>").replace("**", "</strong>")
                                         .replace("\n", "<br/>")
            }
        )
        
        stats_tracker.record_message_sent(room.room_id)
        
        # Stop typing indicator
        await client.room_typing(room.room_id, typing_state=False)
        
    except Exception as e:
        # Stop typing indicator on error
        await client.room_typing(room.room_id, typing_state=False)
        logger.error(f"Error handling sys command: {e}")

async def handle_stats_command(client, room, event):
    """Handle stats command for Matrix"""
    try:
        # Start typing indicator
        await client.room_typing(room.room_id, typing_state=True)
        
        stats_tracker.record_command_usage('?stats')
        
        uptime = stats_tracker.get_uptime()
        daily_stats = stats_tracker.get_daily_stats()
        
        stats_text = f"""📊 **{BOT_USERNAME.capitalize()} Bot Statistics**

**🕐 Uptime:** {uptime}

**📈 Activity (Last 24 Hours):**
• Messages Received: {daily_stats['messages_received']}
• Messages Sent: {daily_stats['messages_sent']}
• Active Rooms: {daily_stats['active_rooms']}/{daily_stats['total_rooms']}

**🔌 Configuration:**
• LLM Provider: {LLM_PROVIDER.upper()}
• Context Size: {MAX_ROOM_HISTORY} messages
• Web Search: {'Enabled' if ENABLE_WEB_SEARCH else 'Disabled'}
• Price Tracking: {'Enabled' if ENABLE_PRICE_TRACKING else 'Disabled'}"""

        await send_message(
            client,
            room.room_id,
            {
                "msgtype": "m.text",
                "body": stats_text.replace("**", ""),
                "format": "org.matrix.custom.html",
                "formatted_body": stats_text.replace("**", "<strong>").replace("**", "</strong>")
                                           .replace("\n", "<br/>")
            }
        )
        
        stats_tracker.record_message_sent(room.room_id)
        
        # Stop typing indicator
        await client.room_typing(room.room_id, typing_state=False)
        
    except Exception as e:
        # Stop typing indicator on error
        await client.room_typing(room.room_id, typing_state=False)
        logger.error(f"Error handling stats command: {e}")
