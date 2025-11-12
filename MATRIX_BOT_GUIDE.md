# Ribit 2.0 Matrix Bot Integration Guide

## Overview

The Ribit 2.0 Matrix Bot brings the sophisticated AI capabilities of the MockRibit20LLM emulator to Matrix.org chat rooms. This integration provides intelligent automation, conversation capabilities, and secure command execution with user authentication.

## Features

### Core Capabilities

**Intelligent Conversation**
- Natural language processing using MockRibit20LLM
- Context-aware responses with conversation history
- Elegant, wise, and knowledgeable personality
- Multi-step reasoning and task execution

**Matrix Integration**
- Full Matrix.org protocol support using matrix-nio
- Auto-joining room invitations
- Real-time message processing
- Typing indicators and rich message formatting

**Security & Authentication**
- User-based command restrictions
- Authorized user whitelist for system commands
- "Terminator mode" for unauthorized access attempts
- Secure credential management

**Command System**
- `?help` - Display available commands
- `?sys` - System status (authorized users only)
- `?status` - Bot status and capabilities
- `?command <action>` - Execute automation tasks (authorized users only)
- `!reset` - Clear conversation context

### Advanced Features

**Robot Control Integration**
- GUI automation through Controller class
- Mouse and keyboard control
- Application launching and management
- Coordinate-based actions

**System Monitoring**
- CPU, memory, and disk usage reporting
- Room and connection status
- Performance metrics and diagnostics

**Conversation Management**
- Per-room conversation contexts
- Automatic context cleanup
- Message history tracking
- Context reset functionality

## Installation

### Prerequisites

**Required Dependencies:**
```bash
pip install matrix-nio>=0.20.0
pip install aiofiles>=0.8.0
pip install asyncio-throttle>=1.0.2
```

**Optional Dependencies:**
```bash
pip install psutil>=5.9.0  # For system monitoring
```

**Complete Installation:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install Matrix-specific dependencies only
pip install matrix-nio aiofiles asyncio-throttle psutil
```

### Configuration

**Environment Variables:**
```bash
export MATRIX_HOMESERVER="https://matrix.envs.net"
export MATRIX_USERNAME="@ribit.2.0:envs.net"
export MATRIX_PASSWORD="your_password_here"
export AUTHORIZED_USERS="@rabit232:envs.net,@rabit232:envs.net"
```

**Configuration File (.env):**
```env
# Matrix server settings
MATRIX_HOMESERVER=https://matrix.envs.net
MATRIX_USERNAME=@ribit.2.0:envs.net
MATRIX_PASSWORD=your_password_here

# Authorized users (comma-separated)
AUTHORIZED_USERS=@rabit232:envs.net,@rabit232:envs.net

# Optional: Bot configuration
BOT_NAME=ribit.2.0
SYNC_TIMEOUT=30000
REQUEST_TIMEOUT=10000
KEEPALIVE_INTERVAL=60
```

## Usage

### Quick Start

**Using the Launcher:**
```bash
# Create sample configuration
python run_matrix_bot.py --create-env

# Edit .env file with your credentials
cp .env.example .env
# Edit .env with your Matrix credentials

# Check configuration
python run_matrix_bot.py --check

# Start the bot
python run_matrix_bot.py
```

**Direct Execution:**
```bash
# Set environment variables
export MATRIX_PASSWORD="your_password"

# Run the bot
python -m ribit_2_0.matrix_bot
```

### Interacting with the Bot

**Basic Conversation:**
```
User: ribit.2.0 hello there
Bot: Greetings! I am Ribit 2.0, an elegant AI agent. How may I assist you today?

User: tell me about robotics
Bot: Ah, robotics! The magnificent fusion of intelligence and mechanism...
```

**Commands:**
```
User: ?help
Bot: 📚 Ribit 2.0 Commands
     Chat: ribit.2.0 <message> - Chat with me
     ...

User: ?status
Bot: 🤖 Ribit 2.0 Status
     Core Status: Operational ✅
     ...
```

**Authorized Commands:**
```
User: ?sys
Bot: 🖥️ System Status
     CPU: 15%
     Memory: 45% (4GB / 8GB)
     ...

User: ?command open ms paint and draw a house
Bot: 🎨 Executed: open ms paint and draw a house
     📋 Result: Application launched
     🧠 AI Decision: run_command('mspaint.exe')...
```

### Security Features

**User Authentication:**
- Only users in `AUTHORIZED_USERS` can execute system commands
- Unauthorized attempts trigger "terminator mode" responses
- Progressive warning system for repeated unauthorized access

**Terminator Mode Example:**
```
Unauthorized User: ?sys
Bot: 🚫 I can't do this silly thing! Only authorized users can execute system commands.

Unauthorized User: ?sys
Bot: 🤖 Action terminated! You've tried again. Would you like to enable terminator mode? (Just kidding! 😄)

Unauthorized User: ?sys
Bot: 🤖💀 TERMINATOR MODE ACTIVATED! Just kidding! I'm still the same elegant, wise Ribit...
```

## Architecture

### Core Components

**RibitMatrixBot Class:**
- Main bot controller and Matrix client wrapper
- Event handling and message processing
- User authentication and command routing

**MockRibit20LLM Integration:**
- AI decision making and response generation
- Personality expression and conversation management
- Knowledge storage and retrieval

**Controller Integration:**
- GUI automation and system control
- Mouse, keyboard, and application management
- Coordinate-based action execution

### Message Flow

1. **Message Reception:** Matrix client receives room messages
2. **Filtering:** Check if message is directed at bot
3. **Authentication:** Verify user permissions for commands
4. **Processing:** Route to appropriate handler (chat/command)
5. **AI Processing:** MockRibit20LLM generates response
6. **Execution:** Execute any required actions via Controller
7. **Response:** Send formatted response to Matrix room

### State Management

**Conversation Context:**
- Per-room conversation history
- Automatic context cleanup
- Configurable history limits

**Bot State:**
- Joined rooms tracking
- Processed events deduplication
- User warning counters

## Deployment

### Production Deployment

**Systemd Service (Linux):**
```ini
[Unit]
Description=Ribit 2.0 Matrix Bot
After=network.target

[Service]
Type=simple
User=ribit
WorkingDirectory=/opt/ribit2.0
Environment=MATRIX_PASSWORD=your_password
ExecStart=/usr/bin/python3 run_matrix_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Docker Deployment:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV MATRIX_HOMESERVER=https://matrix.envs.net
ENV MATRIX_USERNAME=@ribit.2.0:envs.net

CMD ["python", "run_matrix_bot.py"]
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  ribit-matrix-bot:
    build: .
    environment:
      - MATRIX_HOMESERVER=https://matrix.envs.net
      - MATRIX_USERNAME=@ribit.2.0:envs.net
      - MATRIX_PASSWORD=${MATRIX_PASSWORD}
      - AUTHORIZED_USERS=@rabit232:envs.net,@rabit232:envs.net
    restart: unless-stopped
    volumes:
      - ./data:/app/data
```

### Monitoring and Logging

**Log Configuration:**
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ribit_matrix_bot.log'),
        logging.StreamHandler()
    ]
)
```

**Health Monitoring:**
- System resource monitoring via `?sys` command
- Bot status reporting via `?status` command
- Connection keepalive and automatic reconnection
- Error logging and exception handling

## Troubleshooting

### Common Issues

**Authentication Errors:**
```
Error: Failed to login to Matrix
Solution: Check MATRIX_PASSWORD and user credentials
```

**Import Errors:**
```
Error: No module named 'nio'
Solution: pip install matrix-nio
```

**Connection Issues:**
```
Error: Sync timeout
Solution: Check network connectivity and homeserver status
```

### Debug Mode

**Enable Debug Logging:**
```python
import logging
logging.getLogger('ribit_2_0.matrix_bot').setLevel(logging.DEBUG)
logging.getLogger('nio').setLevel(logging.DEBUG)
```

**Mock Mode Testing:**
```bash
# Test without Matrix libraries
python -c "
from ribit_2_0.matrix_bot import RibitMatrixBot
import asyncio
bot = RibitMatrixBot('', '', '')
asyncio.run(bot._run_mock_mode())
"
```

### Performance Optimization

**Configuration Tuning:**
```env
# Faster sync intervals
SYNC_TIMEOUT=15000
REQUEST_TIMEOUT=5000
KEEPALIVE_INTERVAL=30

# Reduced context size
MAX_CONTEXT_MESSAGES=10
```

**Resource Management:**
- Monitor memory usage with `?sys` command
- Adjust conversation context limits
- Use connection pooling for high-traffic deployments

## Integration Examples

### Custom Command Integration

```python
async def _handle_custom_command(self, command: str, sender: str, room_id: str) -> str:
    """Handle custom application-specific commands."""
    if command.startswith('?robot '):
        action = command[7:]  # Remove '?robot '
        
        # Use LLM to process robot action
        decision = self.llm.get_decision(f"Robot action: {action}")
        
        # Execute via controller
        result = self.controller.execute_robot_action(action)
        
        return f"🤖 Robot Action: {action}\n📋 Result: {result}\n🧠 AI: {decision}"
```

### Multi-Platform Integration

```python
# Extend for multiple chat platforms
class MultiPlatformRibitBot:
    def __init__(self):
        self.matrix_bot = RibitMatrixBot(...)
        self.discord_bot = RibitDiscordBot(...)
        self.telegram_bot = RibitTelegramBot(...)
    
    async def start_all(self):
        await asyncio.gather(
            self.matrix_bot.start(),
            self.discord_bot.start(),
            self.telegram_bot.start()
        )
```

## Future Enhancements

### Planned Features

**Enhanced AI Capabilities:**
- Photo understanding and analysis
- Voice message processing
- Multi-modal interaction support

**Advanced Automation:**
- Scheduled task execution
- Workflow automation
- Integration with external APIs

**Security Improvements:**
- End-to-end encryption support
- Advanced authentication methods
- Audit logging and compliance

**Performance Optimizations:**
- Connection pooling
- Message batching
- Caching and optimization

### Contributing

**Development Setup:**
```bash
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0
pip install -e .
pip install -r requirements.txt
```

**Testing:**
```bash
pytest tests/test_matrix_bot.py
python run_matrix_bot.py --check
```

**Code Style:**
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Include comprehensive docstrings
- Add unit tests for new features

## Support

**Documentation:**
- [Main README](README.md)
- [MockRibit20LLM Documentation](MOCK_LLM_EMULATOR.md)
- [ROS Integration Guide](ROS_INTEGRATION_GUIDE.md)

**Community:**
- GitHub Issues: Report bugs and request features
- Matrix Room: Join the development discussion
- Examples: Check the `examples/` directory

**Contact:**
- GitHub: [@rabit232](https://github.com/rabit232)
- Matrix: @rabit232:envs.net

---

**Ribit 2.0 Matrix Bot - Bringing elegant AI to Matrix.org!** 🤖✨
