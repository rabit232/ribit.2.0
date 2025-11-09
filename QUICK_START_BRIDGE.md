# Quick Start: DeltaChat-Matrix Bridge

**Get the bridge running in 5 minutes!**

## Prerequisites

- Python 3.8+
- Matrix account (create at matrix.org)
- Email account (for DeltaChat bot)
- Supabase account (optional but recommended)

## 1. Install Dependencies

```bash
cd ribit.2.0
pip install -r requirements.txt
```

## 2. Set Up Configuration

```bash
cp .env.example .env
```

Edit `.env` and fill in:

```bash
# Required: Matrix
MATRIX_HOMESERVER=https://envs.net
MATRIX_USERNAME=@yourbot:envs.net
MATRIX_PASSWORD=your_password

# Required: DeltaChat Email
DELTACHAT_EMAIL=your-email@gmail.com
DELTACHAT_PASSWORD=your-app-password

# Optional but recommended: Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-key
```

## 3. Start the Bridge

```bash
python run_deltachat_matrix_bridge.py
```

You should see:
```
🌉 DeltaChat-Matrix Bridge - Ribit 2.0
✅ All modules imported successfully
✅ Supabase client initialized
✅ Matrix Bot initialized
✅ DeltaChat Bot initialized
✅ Bridge initialization complete
```

## 4. Map Your First Room (Optional)

Create `setup_room.py`:

```python
import asyncio
from ribit_2_0.bridge_controller import BridgeController
from supabase import create_client

async def setup():
    supabase = create_client(
        "your-supabase-url",
        "your-anon-key"
    )

    config = {
        "name": "test-bridge",
        "matrix_homeserver": "https://envs.net",
        "matrix_username": "@bot:envs.net",
        "deltachat_email": "bot@gmail.com"
    }

    controller = BridgeController(supabase, config)
    await controller.initialize()

    # Map your room
    await controller.map_room(
        matrix_room_id="!your-room-id:envs.net",
        matrix_room_name="Test Room",
        deltachat_group_id=12345,
        deltachat_group_name="Test Group"
    )

    print("✅ Room mapped!")

asyncio.run(setup())
```

```bash
python setup_room.py
```

## 5. Test Message Relay

1. **Send message in Matrix room**
   - Type a message in your Matrix room
   - Bot should respond with Ribit's reply
   - Check your DeltaChat group - message should appear there!

2. **Send message in DeltaChat group**
   - Send a message to the bot in DeltaChat
   - Message should appear in Matrix room
   - Users see the platform badge!

## Message Format

**DeltaChat → Matrix:**
```
📱 **[DELTACHAT] your-email:**
Your message here

_To reply on DeltaChat: Reply to the bot's email_
```

**Matrix → DeltaChat:**
```
💻 **[MATRIX] username:**
Your message here

_To reply on Matrix: Use this room_
```

## Troubleshooting

### "Missing required environment variables"
→ Edit `.env` and fill in MATRIX_USERNAME, MATRIX_PASSWORD, DELTACHAT_EMAIL, DELTACHAT_PASSWORD

### "Matrix bot not connecting"
→ Check that your Matrix homeserver URL is correct
→ Verify username and password
→ Ensure bot account exists on the server

### "DeltaChat not connecting"
→ For Gmail: Use app-specific password, not account password
→ Check IMAP/SMTP settings in .env

### "Bridge not relaying messages"
→ Ensure room mapping is set up
→ Check that both bots are connected
→ Review logs with: `export LOG_LEVEL=DEBUG`

## Commands

While bridge is running, use these commands in Matrix:

```
ribit.2.0 ?help              # Show help
ribit.2.0 ?bridge-status     # Check bridge status
ribit.2.0 hello              # Chat with Ribit
```

## Next Steps

- Read **DELTACHAT_BRIDGE_GUIDE.md** for advanced setup
- Read **BRIDGE_IMPLEMENTATION_SUMMARY.md** for technical details
- Set up multiple room mappings for different conversations
- Configure Supabase for message history persistence

## That's It! 🌉

Your bridge is now running. Messages will automatically relay between Matrix and DeltaChat!

For issues, see DELTACHAT_BRIDGE_GUIDE.md Troubleshooting section or check the logs.
