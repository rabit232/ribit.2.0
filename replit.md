# Ribit 2.0 - Replit Project Documentation

## Overview

**Ribit 2.0** is an enhanced AI agent with production-ready LLM emulator for GUI automation and robotic control. This project has been imported from GitHub and configured to run in the Replit environment.

### Project Type
- **Language**: Python 3.11
- **Type**: Console Application / Library
- **Purpose**: AI agent for automation, robotics, and intelligent conversation

## Current State (November 20, 2025)

### Setup Complete
✅ Python 3.11 installed  
✅ All dependencies installed from requirements.txt  
✅ Interactive demo workflow configured and running  
✅ Project structure preserved from GitHub import  
✅ Matrix bot controls added to CLI demo (November 20, 2025)  

### Available Features
- **Mock LLM Emulator**: Production-ready AI decision-making without external LLM services
- **Knowledge Management**: Persistent learning and knowledge retrieval
- **Personality System**: Elegant, wise AI with sophisticated conversation capabilities
- **Task Execution**: Automation capabilities (GUI automation when in supported environment)
- **Multi-step Reasoning**: Complex task breakdown and execution
- **ROS Integration**: Robot Operating System compatibility (optional)
- **Matrix Bot**: Decentralized chat automation (optional, requires configuration)

## Running the Project

### Main Demo (Currently Running)
The interactive demo is configured as the primary workflow:
```bash
python demo.py
```

This provides an interactive menu to:
1. Meet Ribit 2.0 (introduction)
2. View capabilities
3. Learn about personality
4. Ask questions
5. Teach knowledge
6. Recall knowledge
7. Demonstrate task execution
8. View conversation history

**Matrix Word Library:**
9. View Learned Words - Show words from Matrix history (CLI access to word library)

**Matrix Bot Controls:**
10. Start Matrix Bot - Launch the bot
11. Stop Matrix Bot - Stop the bot
12. Restart Matrix Bot - Restart the bot
13. Bot Status - Check bot status and config
14. Learn Words from Rooms - Scan Matrix rooms and learn new words

### NEW: Offline Features Demo
Test all the new offline capabilities:
```bash
python ribit_2_0/ribit_offline_features_demo.py
```

This demonstrates:
- Image analysis without external APIs
- Message history tracking and search
- Smart natural language queries
- Word learning from conversations

### Other Examples
```bash
# Basic usage example
python examples/basic_usage.py

# Multi-step tasks
python examples/multi_step_tasks.py
```

### Using as a Library
```python
from ribit_2_0.mock_llm_wrapper import MockRibit20LLM

# Initialize the AI agent
llm = MockRibit20LLM()

# Get decisions
response = llm.get_decision("Introduce yourself")

# Check capabilities
capabilities = llm.get_capabilities()

# View personality
personality = llm.get_personality_info()
```

## Project Structure

```
ribit.2.0/
├── ribit_2_0/              # Main package
│   ├── agent.py            # Core agent implementation
│   ├── mock_llm_wrapper.py # Enhanced LLM emulator
│   ├── knowledge_base.py   # Persistent knowledge storage
│   ├── controller.py       # GUI automation controller
│   ├── ros_controller.py   # ROS integration (optional)
│   └── ...                 # Additional modules
├── examples/               # Usage examples
├── demo.py                 # Interactive demo (current workflow)
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
└── README.md              # Full documentation
```

## Dependencies

### Core Dependencies (Installed)
- matrix-nio[e2e] - Matrix protocol support
- aiohttp - Async HTTP client
- requests - HTTP library
- beautifulsoup4 - Web scraping
- lxml - XML/HTML parser
- wikipedia-api - Wikipedia access
- Pillow - Image processing
- python-magic - File type detection
- aiofiles - Async file operations
- supabase - Database integration

### Optional Dependencies (Not Installed)
- pyautogui - GUI automation (requires X11/display)
- pynput - Keyboard/mouse control
- rclpy - ROS 2 support
- rospy - ROS 1 support

## Known Limitations in Replit Environment

1. **GUI Automation**: Limited due to no X11 display server (falls back to mock controller)
2. **ROS**: Not installed by default (can be added if needed)
3. **Interactive Input**: Demo requires interactive console input

## Configuration Notes

### Workflow
- **Name**: "Ribit 2.0 Demo"
- **Command**: `python demo.py`
- **Type**: Console application (interactive)
- **Output**: Console only

### Knowledge Storage
- Knowledge is stored in flat files (knowledge.txt, knowledge.json)
- Conversation history maintained in memory during session
- Persistent across restarts via file storage

### Matrix Bot Configuration
To use the Matrix bot features from the demo CLI, configure these environment variables:

**Required Environment Variables:**
- `MATRIX_HOMESERVER` - Your Matrix server URL (e.g., `https://matrix.envs.net`)
- `MATRIX_USERNAME` - Your bot's Matrix ID (e.g., `@ribit.2.0:envs.net`)

**Required Secrets (add via Replit Secrets tab):**
- `MATRIX_PASSWORD` - Your Matrix account password, OR
- `MATRIX_ACCESS_TOKEN` - Your Matrix access token

**How to Add Secrets:**
1. Click on the "Tools" icon in the left sidebar
2. Select "Secrets"
3. Add `MATRIX_PASSWORD` or `MATRIX_ACCESS_TOKEN`
4. Paste your credential value
5. Click "Add secret"

Once configured, use the demo menu options 10-13 to control the bot!

## User Preferences

*To be added as preferences are discovered*

## Recent Changes

### November 20, 2025 - Enhanced Conversation & Image Analysis
- 🤖 **Improved Natural Conversation Detection**
  - Bot now responds to more natural questions: "tell me", "explain", "what is"
  - Responds to "hey bot", "hey ai", direct address patterns
  - Detects question intent better (what/who/when/where/how)
  - Still ignores group greetings ("good morning everyone")
  - More responsive and helpful in natural conversations

- 📸 **Fixed Image Analysis Issues**
  - Better error handling for corrupted or unsupported images
  - Automatic image format conversion (PNG → RGB)
  - Validates image dimensions before processing
  - Detailed error messages with supported formats
  - More robust PIL image handling
  - Added logging for debugging image issues
  - Shows image dimensions and focal points

### November 20, 2025 - Enhanced Word Library & Admin Configuration
- ✅ **Enhanced ?words Command**
  - Now accepts parameter: `?words 200` or `?words 120`
  - Default increased from 20 to 120 words
  - Maximum cap at 500 words
  - Shows total learned words from 3-month history
  - Example usage: `?words` (120), `?words 200` (200 words)

- 🔐 **Admin User Configuration**
  - @rabit232:envs.net configured as primary admin user
  - Full command privileges: ?sys, ?status, ?command
  - Clearly documented in code and help messages
  
- 📚 **New Database Method**
  - Added `get_word_library()` to MatrixHistoryTracker
  - Efficient database queries with configurable limits
  - Returns word frequency, first/last seen timestamps

- 🔧 **Environment Variable Loading**
  - demo.py now loads .env file automatically
  - Matrix credentials persist across workflow restarts
  - Simplified bot configuration for users

### November 20, 2025 - Matrix Bot CLI Controls
- ✅ **Interactive Bot Management**
  - Start/Stop/Restart Matrix bot from demo CLI
  - Real-time bot status monitoring (CPU, memory, uptime)
  - Graceful shutdown on all exit paths (normal, Ctrl+C, errors)
  - Production-ready subprocess management

- 🔧 **Technical Improvements**
  - Added psutil for process monitoring
  - Fixed subprocess deadlock risk (redirected I/O to DEVNULL)
  - Implemented cleanup handlers for all exit scenarios
  - Architect-reviewed and approved implementation

- 📚 **Documentation**
  - Added Matrix bot configuration guide to replit.md
  - Documented environment variable setup
  - Added instructions for Replit Secrets

### November 18, 2025 - Complete Offline Features Integration
- ✅ **Offline Image Analysis Module**
  - Color detection and dominant color extraction
  - Shape and edge recognition
  - Text region detection (basic OCR-like functionality)
  - Composition analysis and focal point detection
  - Human/nature/sky scene classification
  - No external APIs required - fully offline!
  - **Fixed:** RGB overflow warnings and orientation detection

- ✅ **Matrix Message History Tracker**
  - 90-day message retention with automatic cleanup
  - Smart search with natural language queries
  - Word learning system (automatic vocabulary extraction)
  - Topic and user mention tracking
  - Searchable SQLite database
  - **Fixed:** SQL syntax errors in table creation

- ✅ **Matrix Bot Integration**
  - Automatic image analysis for uploaded images
  - Real-time message history tracking
  - New commands: `?search`, `?history`, `?words`
  - Seamless integration with existing bot features
  - Defensive error handling and graceful degradation

- ✅ **Smart Search Capabilities**
  - Query examples: "did alice mention python last week?"
  - Time-based filtering (today, yesterday, last week, etc.)
  - User and topic correlation
  - Question detection

- 📚 Documentation
  - OFFLINE_FEATURES_GUIDE.md - Detailed feature guide
  - MATRIX_BOT_OFFLINE_INTEGRATION.md - Complete integration docs
  - Updated help command with new features

- 🎯 Testing
  - Demo script: ribit_offline_features_demo.py
  - All features tested and working
  - Architect review passed

### November 18, 2025 - Initial Replit Setup
- Imported GitHub repository
- Installed Python 3.11 and all dependencies
- Created interactive demo.py for easy exploration
- Configured workflow for console execution
- Verified core functionality working correctly
- LLM emulator initializes successfully with knowledge base

## Architecture Decisions

### Why Interactive Demo?
The project is a console-based AI agent library, not a web application. An interactive demo provides the best way to explore Ribit's capabilities in the Replit environment without requiring complex GUI or web frontend setup.

### Mock Mode by Default
Since Replit doesn't have an X11 display server, the project runs in "mock mode" for GUI automation features. This still demonstrates the AI decision-making, knowledge management, and conversation capabilities.

### Knowledge Base
Uses file-based storage (knowledge.txt) for simplicity and portability. Can be upgraded to database storage (SQLite, PostgreSQL) if needed for production use.

## Future Enhancements

Potential improvements for this Replit deployment:
- Add web interface for easier interaction (Flask/FastAPI)
- Configure Matrix bot for remote interaction
- Set up Supabase integration for persistent storage
- Add automated testing workflows
- Deploy as a chatbot service

## Documentation Links

Full documentation available in the repository:
- [README.md](README.md) - Complete project overview
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Comprehensive technical summary
- [ENHANCED_LLM_EMULATOR.md](ENHANCED_LLM_EMULATOR.md) - LLM emulator details
- [ROS_INTEGRATION_GUIDE.md](ROS_INTEGRATION_GUIDE.md) - Robot OS integration
- [MATRIX_BOT_GUIDE.md](MATRIX_BOT_GUIDE.md) - Matrix chat bot setup
- [API_REFERENCE.md](API_REFERENCE.md) - API documentation

## Support

For issues or questions:
- Check the comprehensive documentation in the repository
- Review examples/ directory for usage patterns
- See GitHub issues: https://github.com/rabit232/ribit.2.0/issues
