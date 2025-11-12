# Ribit 2.0 Quick Start Guide

## Matrix Account Configuration

**Updated Account Information:**
- **Matrix User ID:** `@rabit232:envs.net`
- **Homeserver:** `https://matrix.envs.net`

## Running the Enhanced Autonomous Matrix Bot

### 1. Set Environment Variables

```bash
export MATRIX_HOMESERVER="https://matrix.envs.net"
export MATRIX_USER_ID="@rabit232:envs.net"
export MATRIX_ACCESS_TOKEN="your_access_token_here"
export MATRIX_DEVICE_ID="optional_device_id"
```

### 2. Run the Bot

```bash
cd ribit.2.0
python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
```

Or using the standalone script:

```bash
cd ribit.2.0
python3 ribit_2_0/enhanced_autonomous_matrix_bot.py
```

## Getting Your Access Token

### Option 1: Using Element Web Client

1. Log in to Element at https://app.element.io
2. Go to Settings → Help & About
3. Scroll down to "Access Token"
4. Click "Click to reveal" and copy your token

### Option 2: Using Matrix API

```bash
curl -X POST https://matrix.envs.net/_matrix/client/r0/login \
  -H "Content-Type: application/json" \
  -d '{
    "type": "m.login.password",
    "user": "ribit.2.0",
    "password": "your_password"
  }'
```

The response will contain your `access_token`.

## Authorized Users

Only these users can send commands to Ribit:
- `@rabit232:envs.net`
- `@rabit232:envs.net`

## Available Commands

### Basic Commands
- `?status` - View current status and activity
- `?sys` - Full system status
- `!reset` - Clear conversation context

### Autonomous Features
- `?tasks` - View autonomous task suggestions
- `?opinion <topic>` - Get Ribit's opinion on a topic
- `?discuss <topic>` - Start a philosophical discussion

### Examples

```
?status
?opinion quantum mechanics
?discuss consciousness and free will
?tasks
?sys
```

## Autonomous Behavior

Ribit will automatically respond (without being mentioned) to messages about:
- Quantum physics
- Consciousness and free will
- Philosophy and metaphysics
- AI and artificial intelligence
- Walter Russell's work
- Physics models and theories

**Settings:**
- Response probability: 70%
- Max responses per hour: 10
- Minimum time between responses: 30 seconds

## Bot-to-Bot Communication

Ribit can interact with other bots, including:
- `@nifty:converser.eu` (registered and ready)

## Testing Locally

Run the test suite:

```bash
cd ribit.2.0
python3 test_new_features.py
```

Expected output:
```
================================================================================
ALL TESTS COMPLETED SUCCESSFULLY ✓
================================================================================
```

## Configuration Files

### Create `.env` file (optional)

```bash
cd ribit.2.0
cat > .env << EOF
MATRIX_HOMESERVER=https://matrix.envs.net
MATRIX_USER_ID=@rabit232:envs.net
MATRIX_ACCESS_TOKEN=your_token_here
MATRIX_DEVICE_ID=your_device_id
EOF
```

Then load it:

```bash
source .env
python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
```

## Troubleshooting

### Bot not responding
1. Check that environment variables are set: `echo $MATRIX_USER_ID`
2. Verify access token is valid
3. Check bot is in the room: invite `@rabit232:envs.net`
4. Check logs for errors

### Autonomous responses not working
1. Verify messages contain interest keywords (quantum, consciousness, etc.)
2. Check rate limits haven't been exceeded
3. Ensure messages are questions or discussions (contains `?` or discussion phrases)

### Access denied errors
1. Verify you're using an authorized user account
2. Check the authorized users list in the code

## Features Overview

### Philosophical Reasoning
- Deep discussions on quantum physics, consciousness, reality models
- Nuanced positions with confidence scores
- Integration with knowledge base

### Conversational Mode
- Natural language conversation
- Self-introduction and capability descriptions
- Opinion formation

### Autonomous Interaction
- Unprompted responses to interesting topics
- Bot-to-bot communication
- Interest-based engagement

### Task Autonomy
- Self-directed task selection
- Priority and interest-based evaluation
- Post-task opinion generation

## Documentation

- **AUTONOMOUS_FEATURES.md** - Comprehensive feature documentation
- **CHANGELOG_AUTONOMOUS.md** - Detailed changelog
- **IMPLEMENTATION_SUMMARY.md** - Implementation overview
- **API_REFERENCE.md** - API documentation
- **MATRIX_BOT_GUIDE.md** - Matrix integration guide

## Support

For issues or questions:
- GitHub: https://github.com/rabit232/ribit.2.0
- Check existing documentation in the repository

## Example Session

```
# Terminal 1: Start the bot
$ export MATRIX_HOMESERVER="https://matrix.envs.net"
$ export MATRIX_USER_ID="@rabit232:envs.net"
$ export MATRIX_ACCESS_TOKEN="syt_..."
$ cd ribit.2.0
$ python3 -m ribit_2_0.enhanced_autonomous_matrix_bot

INFO - Enhanced Autonomous Matrix Bot initialized
INFO - Starting Enhanced Autonomous Matrix Bot...
INFO - Bot started and synced

# Matrix Room: User messages
User: "I've been thinking about quantum mechanics"
Ribit: *[Ribit's interest is piqued]* This discussion about quantum 
       physics fascinates me... I strongly agree with the criticism 
       that we're forcing two incompatible models onto phenomena...

User: "?status"
Ribit: **Ribit 2.0 Status**
       Current Activity: Idle, ready for conversation
       Task Queue: 0 tasks
       Completed: 3 tasks
       ...

User: "?opinion consciousness"
Ribit: **On Consciousness and Determinism:**
       The question strikes at the heart of agency...
       [Full philosophical response]
```

## Next Steps

1. Get your access token from Element
2. Set environment variables
3. Run the bot
4. Invite it to a Matrix room
5. Try commands like `?status` and `?tasks`
6. Mention topics like "quantum physics" to trigger autonomous responses

Enjoy your autonomous AI companion! 🤖✨
