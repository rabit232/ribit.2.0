# DeltaChat-Matrix Bridge Guide

**Ribit 2.0 Cross-Platform Communication Bridge**

This guide explains how to set up and use the DeltaChat-Matrix bridge, enabling seamless communication between DeltaChat and Matrix users through Ribit 2.0.

## Overview

The DeltaChat-Matrix bridge allows:
- **Bidirectional messaging**: Messages flow between DeltaChat and Matrix in real-time
- **User mapping**: Automatic tracking of users across platforms
- **Room/Group association**: Linking DeltaChat groups with Matrix rooms
- **Message history**: Persistent storage of relayed messages in Supabase
- **Intelligent bot responses**: Ribit 2.0 LLM processes messages on both platforms
- **Cross-platform awareness**: Users see which platform messages originate from

## Installation

### Prerequisites

- Python 3.8 or higher
- Supabase account and project
- Matrix server account (create at matrix.org or self-hosted)
- DeltaChat account or email account for bot

### Step 1: Clone and Install

```bash
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0

pip install -r requirements.txt
```

### Step 2: Install DeltaChat Bot

```bash
pip install deltabot>=1.72.0
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-key-here

# Matrix Configuration
MATRIX_HOMESERVER=https://envs.net
MATRIX_USERNAME=@ribit.2.0:envs.net
MATRIX_PASSWORD=your-matrix-password

# DeltaChat Configuration
DELTACHAT_EMAIL=ribit2.0@example.com
DELTACHAT_PASSWORD=your-deltachat-password
DELTACHAT_SMTP=smtp.example.com
DELTACHAT_IMAP=imap.example.com

# Bridge Configuration
BRIDGE_NAME=ribit-deltachat-matrix
BRIDGE_ENABLED=true
```

## Setup Guide

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. In the SQL editor, the bridge tables will be created automatically when the bridge initializes
4. Get your `SUPABASE_URL` and `SUPABASE_ANON_KEY` from the project settings

### 2. Create Matrix Account

1. Visit [matrix.org](https://matrix.org) or your preferred Matrix server
2. Create a bot account (e.g., `@ribit.2.0:envs.net`)
3. Join or create a room for testing
4. Get the room ID from the room settings (format: `!roomid:server.com`)

### 3. Set Up DeltaChat Bot

```bash
# Initialize DeltaChat bot email
deltabot init ribit2.0@example.com your-password
```

### 4. Configure Bridge Room Mapping

The bridge needs to know which Matrix rooms should relay to which DeltaChat groups.

Create a script `configure_bridge.py`:

```python
import asyncio
from ribit_2_0.deltachat_matrix_bridge import DeltaChatMatrixBridge
from ribit_2_0.bridge_controller import BridgeController
from supabase import create_client

async def setup_mappings():
    url = "your-supabase-url"
    key = "your-anon-key"
    supabase = create_client(url, key)

    bridge_config = {
        "name": "ribit-bridge",
        "matrix_homeserver": "https://envs.net",
        "matrix_username": "@ribit.2.0:envs.net",
        "deltachat_email": "ribit2.0@example.com"
    }

    controller = BridgeController(supabase, bridge_config)
    await controller.initialize()

    # Map a room
    await controller.map_room(
        matrix_room_id="!room123:envs.net",
        matrix_room_name="Test Room",
        deltachat_group_id=12345,
        deltachat_group_name="Test Group"
    )

    print("✅ Room mapping created!")

asyncio.run(setup_mappings())
```

Run it:
```bash
python configure_bridge.py
```

## Running the Bridge

### Option 1: Start All Components Together

```bash
python -m ribit_2_0.deltachat_matrix_bridge
```

### Option 2: Start Components Separately

**Matrix Bot:**
```bash
python -m ribit_2_0.matrix_bot
```

**DeltaChat Bot:**
```bash
python -m ribit_2_0.deltachat_bot
```

**Bridge:**
```python
python -c "
import asyncio
from ribit_2_0.deltachat_matrix_bridge import main
asyncio.run(main())
"
```

### Option 3: Programmatic Control

```python
import asyncio
from ribit_2_0.deltachat_matrix_bridge import DeltaChatMatrixBridge
from ribit_2_0.matrix_bot import RibitMatrixBot
from ribit_2_0.deltachat_bot import DeltaChatRibotBot, DeltaChatBotConfig
from ribit_2_0.mock_llm_wrapper import MockRibit20LLM

async def main():
    llm = MockRibit20LLM()

    matrix_bot = RibitMatrixBot(
        homeserver="https://envs.net",
        username="@ribit.2.0:envs.net",
        password="your-password"
    )

    deltachat_config = DeltaChatBotConfig(
        email="ribit2.0@example.com",
        password="your-password"
    )

    deltachat_bot = DeltaChatRibotBot(deltachat_config, llm=llm)

    bridge = DeltaChatMatrixBridge(
        matrix_bot=matrix_bot,
        deltachat_bot=deltachat_bot
    )

    await bridge.start()

asyncio.run(main())
```

## Message Format

### Matrix → DeltaChat

```
📱 **[DELTACHAT] username:**
This is a message from a DeltaChat user

_To reply on DeltaChat: Reply to the bot's email_
```

### DeltaChat → Matrix

```
💻 **[MATRIX] username:**
This is a message from a Matrix user

_To reply on Matrix: Use this room_
```

## Commands

### Bridge Status

Get bridge statistics and status:

```
ribit.2.0 ?bridge-status
```

Response includes:
- Connection status of both platforms
- Message relay statistics
- Mapped rooms and users
- Error counts

### User Mapping

View or create user mappings:

```
ribit.2.0 ?map-user matrix-user@server.com deltachat@email.com
```

### Room Configuration

Manage room/group mappings:

```
ribit.2.0 ?list-rooms
ribit.2.0 ?map-room !roomid:server.com group-id
```

## Troubleshooting

### Bridge Not Relaying Messages

1. **Check room mappings:**
   ```python
   await bridge.bridge_controller.get_mapped_room("!roomid", "matrix")
   ```

2. **Verify platform connections:**
   ```python
   stats = await bridge.get_stats()
   print(stats)
   ```

3. **Check logs:**
   ```bash
   # Enable debug logging
   export LOG_LEVEL=DEBUG
   python -m ribit_2_0.deltachat_matrix_bridge
   ```

### DeltaChat Bot Not Connecting

1. **Verify credentials:**
   ```bash
   deltabot configure
   ```

2. **Check email account settings:**
   - IMAP enabled
   - SMTP configured
   - Less secure apps allowed (if using Gmail)

3. **Test DeltaChat independently:**
   ```bash
   python -m ribit_2_0.deltachat_bot
   ```

### Matrix Bot Not Connecting

1. **Verify homeserver URL:**
   ```python
   from nio import AsyncClient
   client = AsyncClient("https://envs.net", "@user:envs.net")
   # Should not raise errors
   ```

2. **Test login:**
   ```bash
   python -c "
   from nio import AsyncClient
   import asyncio
   async def test():
       client = AsyncClient('https://envs.net', '@ribit.2.0:envs.net')
       response = await client.login('password')
       print(response)
   asyncio.run(test())
   "
   ```

3. **Check room access:**
   Ensure bot account is in the room you're trying to relay from

### Supabase Connection Failed

1. **Verify credentials:**
   ```python
   from supabase import create_client
   client = create_client("url", "key")
   client.table("bridge_config").select("*").execute()
   ```

2. **Check network access:**
   ```bash
   curl https://your-project.supabase.co
   ```

## Database Schema

### bridge_config
- Stores bridge instance configuration
- One per bridge deployment
- Contains platform credentials (encrypted)

### user_mappings
- Maps Matrix users to DeltaChat contacts
- Indexed by matrix_user_id and deltachat_email
- Used for sender identification

### room_mappings
- Maps Matrix rooms to DeltaChat groups
- Bidirectional flag for relay direction
- Index on both matrix_room_id and deltachat_group_id

### bridge_messages
- Complete message relay history
- Status tracking: pending, sent, failed, deduped
- Deduplication hash for duplicate detection
- Message data in JSON for extensions

### bridge_state
- Real-time bridge status
- Connection state for each platform
- Error tracking and statistics
- Last heartbeat timestamp

## Performance Tuning

### Message Queue

Adjust relay queue processing:

```python
bridge.relay_queue.maxsize = 1000
```

### Database Cleanup

Automatically clean up old messages:

```python
await bridge.bridge_controller.cleanup_old_messages(days=30)
```

### Message Deduplication

Control deduplication window:

```python
# Only keep last 5000 message hashes
if len(bridge.bridge_controller.processed_messages) > 10000:
    bridge.bridge_controller.processed_messages = set(
        list(bridge.bridge_controller.processed_messages)[-5000:]
    )
```

## Advanced Features

### Custom Message Formatting

Extend `BridgeMessage` class:

```python
class CustomBridgeMessage(BridgeMessage):
    def get_formatted_message(self, include_instructions=True):
        # Custom formatting logic
        return formatted_msg
```

### Message Hooks

Add pre/post processing:

```python
async def before_relay(message):
    # Modify message before relay
    return message

async def after_relay(message, success):
    # Process relay result
    pass
```

### Platform-Specific Features

Use platform capabilities in messages:

```python
if message.target_platform == "matrix":
    # Use Matrix HTML formatting
    formatted = "<strong>bold</strong>"
elif message.target_platform == "deltachat":
    # Use DeltaChat markdown
    formatted = "**bold**"
```

## Security Considerations

1. **Credential Storage:**
   - Never commit `.env` to version control
   - Use environment variables or secrets manager
   - Rotate credentials regularly

2. **Message Privacy:**
   - Bridge messages stored in Supabase
   - Ensure Supabase backup encryption
   - Implement data retention policies

3. **Access Control:**
   - Use RLS policies for database access
   - Restrict bridge initialization to admins
   - Log all relay operations

4. **Rate Limiting:**
   - Implement per-user/room relay limits
   - Monitor for spam or abuse
   - Set queue size limits

## Monitoring

### Health Checks

```python
stats = await bridge.get_stats()
if stats['matrix_connected'] and stats['deltachat_connected']:
    print("✅ Bridge healthy")
else:
    print("❌ Platform connection lost")
```

### Metrics Collection

```python
from datetime import datetime

async def log_metrics():
    stats = await bridge.get_stats()
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] Relayed: {stats.get('relayed_messages', 0)}")
```

### Error Tracking

Monitor error rates and patterns:

```python
error_messages = supabase.table("bridge_messages")\
    .select("*")\
    .eq("relay_status", "failed")\
    .order("created_at", desc=True)\
    .limit(10)\
    .execute()
```

## Integration with Ribit 2.0

The bridge uses Ribit 2.0's MockRibit20LLM for intelligent responses:

1. **Message Processing:**
   - Each relayed message goes through LLM
   - Intelligent context understanding
   - Knowledge-aware responses

2. **Learning:**
   - Messages contribute to knowledge base
   - Platform-specific patterns learned
   - Improved response quality over time

3. **Personality:**
   - Maintains Ribit's elegant personality
   - Cross-platform communication style
   - Consistent voice across platforms

## Support and Contribution

- **GitHub:** https://github.com/rabit232/ribit.2.0
- **Issues:** Report bugs and request features
- **Discussions:** Join community conversations
- **Contributing:** Submit pull requests for improvements

---

**Ribit 2.0: Elegant Cross-Platform Intelligence** 🌉
