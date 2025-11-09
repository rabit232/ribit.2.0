# DeltaChat-Matrix Bridge Functionality Guide

## Overview

The Ribit 2.0 project includes a **fully functional bidirectional bridge** between DeltaChat and Matrix platforms. This allows users on DeltaChat to communicate seamlessly with users on Matrix, and vice versa.

## Architecture

The bridge consists of three main components:

### 1. DeltaChat Bot (`ribit_2_0/deltachat_bot.py`)
- Connects to DeltaChat platform via email/IMAP/SMTP
- Handles incoming messages from DeltaChat users
- Sends messages to DeltaChat groups
- Powered by Ribit 2.0 LLM for intelligent responses

### 2. Matrix Bot (`ribit_2_0/matrix_bot.py`)
- Connects to Matrix homeserver
- Handles incoming messages from Matrix rooms
- Sends messages to Matrix rooms
- Powered by Ribit 2.0 LLM for intelligent responses

### 3. Bridge Controller (`ribit_2_0/bridge_controller.py`)
- Manages message relay between platforms
- Maintains user and room mappings
- Handles message deduplication
- Stores message history in Supabase

### 4. Bridge Integration (`ribit_2_0/deltachat_matrix_bridge.py`)
- Unified bridge coordinator
- Routes messages between platforms
- Manages relay queue
- Provides statistics and monitoring

## How It Works

### Message Flow

```
DeltaChat User → DeltaChat Bot → Bridge Controller → Matrix Bot → Matrix User
                                      ↓
                                  Supabase DB
                                  (History & Mapping)
```

And in reverse:

```
Matrix User → Matrix Bot → Bridge Controller → DeltaChat Bot → DeltaChat User
                               ↓
                           Supabase DB
                           (History & Mapping)
```

### Key Features

#### 1. Bidirectional Message Relay
- Messages from DeltaChat are automatically sent to mapped Matrix rooms
- Messages from Matrix are automatically sent to mapped DeltaChat groups
- Each message includes platform badge and sender information

#### 2. User Mapping
- Maps DeltaChat email addresses to Matrix user IDs
- Maintains consistent identity across platforms
- Cached for performance

#### 3. Room Mapping
- Associates DeltaChat groups with Matrix rooms
- Supports many-to-many relationships
- Configurable via Supabase database

#### 4. Message Deduplication
- Prevents duplicate messages from being relayed
- Uses hash-based detection
- Maintains recent message cache

#### 5. Message Formatting
```
📱 **[DELTACHAT] Alice:**
Hello from DeltaChat!

_To reply on DeltaChat: Reply to the bot's email_
```

```
💻 **[MATRIX] Bob:**
Hello from Matrix!

_To reply on Matrix: Use this room_
```

#### 6. Persistent Storage (Supabase)
The bridge uses Supabase for:
- Bridge configuration
- User mappings
- Room mappings
- Message history
- Bridge state and statistics

## Database Schema

The bridge requires these Supabase tables (created via migration):

### `bridge_config`
- `id` - UUID, primary key
- `bridge_name` - Text, unique bridge identifier
- `matrix_homeserver` - Text
- `matrix_username` - Text
- `deltachat_email` - Text
- `enabled` - Boolean
- `config_data` - JSONB
- `created_at` - Timestamp

### `bridge_state`
- `id` - UUID, primary key
- `bridge_id` - UUID, references bridge_config
- `matrix_connected` - Boolean
- `deltachat_connected` - Boolean
- `status` - Text
- `status_message` - Text
- `updated_at` - Timestamp

### `user_mappings`
- `id` - UUID, primary key
- `bridge_id` - UUID, references bridge_config
- `matrix_user_id` - Text
- `matrix_display_name` - Text
- `deltachat_email` - Text
- `created_at` - Timestamp

### `room_mappings`
- `id` - UUID, primary key
- `bridge_id` - UUID, references bridge_config
- `matrix_room_id` - Text
- `matrix_room_name` - Text
- `deltachat_group_id` - Integer
- `deltachat_group_name` - Text
- `bidirectional` - Boolean
- `created_at` - Timestamp

### `bridge_messages`
- `message_id` - UUID, primary key
- `bridge_id` - UUID, references bridge_config
- `source_platform` - Text (deltachat/matrix)
- `target_platform` - Text (deltachat/matrix)
- `sender_id` - Text
- `sender_name` - Text
- `message_text` - Text
- `source_room_id` - Text
- `target_room_id` - Text
- `relay_status` - Text (pending/sent/failed/deduped)
- `relay_error` - Text
- `created_at` - Timestamp
- `relayed_at` - Timestamp

## Setup Instructions

### 1. Install Dependencies

```bash
pip install matrix-nio deltachat supabase-py
```

### 2. Configure Environment Variables

Create a `.env` file:

```bash
# Matrix Configuration
MATRIX_HOMESERVER=https://matrix.example.com
MATRIX_USERNAME=@ribit:matrix.example.com
MATRIX_PASSWORD=your_matrix_password

# DeltaChat Configuration
DELTACHAT_EMAIL=ribit@example.com
DELTACHAT_PASSWORD=your_deltachat_password
DELTACHAT_SMTP=smtp.example.com
DELTACHAT_IMAP=imap.example.com

# Supabase Configuration (for persistence)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
```

### 3. Set Up Supabase Database

Run the migration to create the required tables:

```bash
# Migration already created in supabase/migrations/
# Apply it via Supabase dashboard or CLI
```

### 4. Run the Bridge

```bash
python run_deltachat_matrix_bridge.py
```

## Usage Examples

### Running the Bridge

```bash
# Full bridge with both platforms
python run_deltachat_matrix_bridge.py

# Matrix bot only
python run_matrix_bot.py

# DeltaChat bot only
# (implement run_deltachat_bot.py if needed)
```

### Testing the Bridge

1. **Send from DeltaChat to Matrix:**
   - Send a message in a DeltaChat group
   - The message should appear in the mapped Matrix room
   - Format: `📱 **[DELTACHAT] YourName:** Message text`

2. **Send from Matrix to DeltaChat:**
   - Send a message in a Matrix room
   - The message should appear in the mapped DeltaChat group
   - Format: `💻 **[MATRIX] YourName:** Message text`

3. **Check Statistics:**
   ```python
   stats = await bridge.get_stats()
   print(stats)
   # Shows: total_messages, relayed_messages, failed_messages, etc.
   ```

### Mapping Rooms

Use the Bridge Controller to map rooms:

```python
from ribit_2_0.bridge_controller import BridgeController

# Map a Matrix room to a DeltaChat group
await bridge_controller.map_room(
    matrix_room_id="!abc123:matrix.org",
    matrix_room_name="General Chat",
    deltachat_group_id=12345,
    deltachat_group_name="Team Discussion"
)
```

### Mapping Users

```python
# Map a Matrix user to a DeltaChat email
await bridge_controller.map_matrix_user(
    matrix_user_id="@alice:matrix.org",
    display_name="Alice",
    deltachat_email="alice@example.com"
)
```

## Bridge Features in Detail

### Intelligent Message Detection

Both bots use Ribit 2.0's intelligent detection:
- Questions are automatically answered
- Direct mentions trigger responses
- Group greetings are ignored
- Context-aware conversations

### Error Handling

- **Connection Loss:** Auto-reconnect with exponential backoff
- **Failed Messages:** Marked as failed with error details in database
- **Missing Mappings:** Logged and messages are queued
- **Deduplication:** Hash-based to prevent message loops

### Performance Optimizations

- **Caching:** User and room mappings cached in memory
- **Async Processing:** All I/O operations are async
- **Queue Management:** Relay queue prevents blocking
- **Batch Operations:** Messages processed efficiently

### Monitoring & Statistics

The bridge provides comprehensive statistics:

```python
stats = await bridge.get_stats()
# Returns:
{
    "bridge_running": true,
    "matrix_available": true,
    "deltachat_available": true,
    "supabase_available": true,
    "total_messages": 1234,
    "relayed_messages": 1200,
    "failed_messages": 5,
    "user_mappings": 50,
    "room_mappings": 10,
    "timestamp": "2025-11-09T12:00:00"
}
```

## Troubleshooting

### Bridge Not Starting

1. Check environment variables are set
2. Verify Supabase credentials
3. Confirm Matrix and DeltaChat credentials
4. Check logs for detailed error messages

### Messages Not Relaying

1. Verify room mappings exist in database
2. Check both bots are connected
3. Review bridge_state table for connection status
4. Look for errors in bridge_messages table

### Duplicate Messages

- The bridge has built-in deduplication
- Check if messages are being marked as "deduped" in logs
- Recent message hashes are cached to prevent loops

### Performance Issues

1. Enable Supabase for persistent state
2. Increase cache sizes if needed
3. Check network latency to both platforms
4. Review database query performance

## Advanced Configuration

### Custom Message Formatting

Modify the `BridgeMessage.get_formatted_message()` method to customize:
- Platform badges
- Sender name format
- Instructions text
- Additional metadata

### Room Mapping Strategies

1. **One-to-One:** Single Matrix room ↔ Single DeltaChat group
2. **One-to-Many:** One Matrix room ↔ Multiple DeltaChat groups
3. **Many-to-One:** Multiple Matrix rooms ↔ Single DeltaChat group
4. **Many-to-Many:** Complex mapping with routing rules

### Security Considerations

- Use environment variables for credentials
- Enable RLS (Row Level Security) in Supabase
- Restrict bridge to authorized users only
- Monitor message logs for abuse
- Implement rate limiting if needed

## Future Enhancements

Potential improvements:
- Media file relay (images, videos)
- Reaction sync between platforms
- Thread support
- Typing indicators
- Read receipts
- End-to-end encryption bridge
- Administrative commands
- Web dashboard for management

## Summary

The DeltaChat-Matrix bridge is **fully implemented and functional**. It provides:

✅ **Bidirectional message relay**
✅ **User and room mapping**
✅ **Message deduplication**
✅ **Persistent storage with Supabase**
✅ **Intelligent message formatting**
✅ **Error handling and recovery**
✅ **Statistics and monitoring**
✅ **Easy configuration via environment variables**

The bridge integrates seamlessly with both platforms and allows users to communicate across DeltaChat and Matrix as if they were on the same platform.
