# Ribit 2.0 - Complete Installation Guide

**Updated for all new features:** Message history learning, Advanced MockLLM, emoji support, autonomous capabilities, web scraping, and more!

---

## 📋 Table of Contents

1. [What's New](#whats-new)
2. [System Requirements](#system-requirements)
3. [Quick Install](#quick-install)
4. [Manual Installation](#manual-installation)
5. [Matrix Bot Setup](#matrix-bot-setup)
6. [Feature Configuration](#feature-configuration)
7. [Running Ribit](#running-ribit)
8. [Verification](#verification)
9. [Troubleshooting](#troubleshooting)

---

## 🆕 What's New

Ribit 2.0 now includes:

✅ **Message History Learning** - Learn from past conversations  
✅ **Advanced MockLLM** - 20+ parameters for complete control  
✅ **Enhanced MockLLM** - Temperature, penalties, style adaptation  
✅ **Emoji Support** - Natural emoji usage in conversations  
✅ **Autonomous Interaction** - Respond without being prompted  
✅ **Task Autonomy** - Self-select and complete tasks  
✅ **Philosophical Reasoning** - Deep discussions on complex topics  
✅ **Web Scraping** - Extract content from websites  
✅ **Wikipedia Integration** - Search and retrieve Wikipedia content  
✅ **Image Generation** - Generate placeholder images  
✅ **Bot-to-Bot Communication** - Talk to other Matrix bots  

---

## 💻 System Requirements

### Minimum Requirements:
- **OS**: Ubuntu 20.04+, Debian 11+, or similar Linux
- **Python**: 3.8+ (3.11 recommended)
- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 1GB for installation
- **Internet**: Required for Matrix and web features

### Recommended:
- Ubuntu 22.04 LTS
- Python 3.11
- 4GB RAM
- Stable internet connection

---

## 🚀 Quick Install

### One-Command Installation:

```bash
# Clone repository
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0

# Run installation script
chmod +x install.sh
./install.sh
```

**The script automatically:**
1. ✓ Checks Python version (3.8+ required)
2. ✓ Installs system dependencies
3. ✓ Installs Python packages
4. ✓ Creates configuration files
5. ✓ Runs verification tests

---

## 🔧 Manual Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0
```

### Step 2: Install System Dependencies

```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    libolm-dev \
    libmagic1
```

**What these packages do:**
- `python3` - Python interpreter
- `python3-pip` - Package manager
- `python3-dev` - Development headers
- `build-essential` - Compilation tools
- `git` - Version control
- `libolm-dev` - E2E encryption (for Matrix)
- `libmagic1` - File type detection

### Step 3: Install Python Dependencies

```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Install from requirements.txt
pip3 install -r requirements.txt
```

**Core packages installed:**
- `matrix-nio[e2e]>=0.20.0` - Matrix client with encryption
- `aiohttp>=3.8.0` - Async HTTP client
- `requests>=2.28.0` - HTTP library
- `beautifulsoup4>=4.11.0` - Web scraping
- `lxml>=4.9.0` - XML/HTML parser
- `wikipedia-api>=0.5.8` - Wikipedia integration
- `Pillow>=9.0.0` - Image processing
- `python-magic>=0.4.27` - File type detection
- `aiofiles>=23.0.0` - Async file operations

### Step 4: Verify Installation

```bash
# Run test suite
python3 test_learning_features.py
python3 test_advanced_llm.py
python3 test_fixes.py
```

All tests should pass! ✅

---

## 🤖 Matrix Bot Setup

### Step 1: Get Matrix Credentials

You need:
1. Matrix homeserver URL
2. Matrix user ID
3. Matrix access token

#### Option A: Using Element Web (Easiest)

1. Go to https://app.element.io
2. Log in with your Matrix account
3. Click your profile (top left)
4. Go to **Settings** → **Help & About**
5. Scroll to **Access Token**
6. Click to reveal and copy

#### Option B: Using curl

```bash
curl -X POST https://anarchists.space/_matrix/client/r0/login \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "m.login.password",
    "user": "rabit233",
    "password": "YOUR_PASSWORD"
  }'
```

Look for `"access_token"` in the response.

### Step 2: Configure Credentials

#### Option A: Interactive Setup (Recommended)

```bash
./setup_credentials.sh
```

Follow the prompts:
- Homeserver: Press Enter for default (`https://anarchists.space`)
- User ID: Press Enter for default (`@rabit233:anarchists.space`)
- Access Token: Paste your token
- Device ID: Press Enter to skip
- API Keys: Press Enter to skip (optional)

#### Option B: Manual Setup

Create `.env` file:

```bash
cat > .env << 'EOF'
# Matrix Configuration
MATRIX_HOMESERVER=https://anarchists.space
MATRIX_USER_ID=@rabit233:anarchists.space
MATRIX_ACCESS_TOKEN=your_access_token_here

# Optional: Device ID
MATRIX_DEVICE_ID=RIBIT_DEVICE

# Optional: API Keys (for advanced features)
JINA_API_KEY=your_jina_key
OPENAI_API_KEY=your_openai_key
STABILITY_API_KEY=your_stability_key
EOF
```

**Security Note:** `.env` is in `.gitignore` and won't be committed to git.

---

## ⚙️ Feature Configuration

### 1. Advanced MockLLM Parameters

Edit in code or configure programmatically:

```python
from ribit_2_0.advanced_mock_llm import AdvancedMockLLM

llm = AdvancedMockLLM(
    # Creativity
    temperature=0.7,          # 0.0-2.0 (higher = more creative)
    top_p=0.9,               # 0.0-1.0 (nucleus sampling)
    
    # Anti-repetition
    frequency_penalty=0.5,    # 0.0-2.0 (avoid word repetition)
    presence_penalty=0.3,     # 0.0-2.0 (topic diversity)
    repetition_penalty=1.2,   # 1.0-2.0 (n-gram penalty)
    no_repeat_ngram_size=3,   # N-gram size
    
    # Length control
    min_length=10,            # Minimum chars
    max_length=500,           # Maximum chars
    max_tokens=None,          # Max words (None = unlimited)
    length_penalty=1.0,       # 0.5-2.0 (prefer longer/shorter)
    
    # Sampling
    sampling_strategy='nucleus',  # greedy, top_k, nucleus, beam
    top_k=50,                # Top-K sampling
    num_beams=1,             # Beam search beams
    diversity_penalty=0.0,   # 0.0-1.0 (beam diversity)
    
    # Performance
    enable_caching=True,     # Cache responses
    cache_size=100,          # Max cached responses
    enable_monitoring=True,  # Track performance
    
    # Context
    context_window=2000,     # Max context length
    sliding_window=True,     # Sliding context
    
    # Learning
    learning_enabled=True,   # Enable history learning
    style_adaptation=True,   # Adapt to users
    
    # Error handling
    max_retries=3,           # Retries on error
    fallback_response=None   # Fallback message
)
```

### 2. Message History Learning

Configure learning behavior:

```python
from ribit_2_0.message_history_learner import MessageHistoryLearner

learner = MessageHistoryLearner(knowledge_base)

# Learn from room history
summary = await learner.scroll_and_learn(
    client=matrix_client,
    room_id="!room:matrix.org",
    limit=1000,      # Max messages to process
    days_back=30     # How far back to go
)
```

### 3. Emoji Expression

Configure emoji usage:

```python
from ribit_2_0.emoji_expression import EmojiExpression

emoji_expr = EmojiExpression()

# Adjust intensity
emoji_expr.set_intensity(0.7)  # 0.0-1.0

# Enable/disable
emoji_expr.enabled = True
```

### 4. Autonomous Interaction

Configure autonomous behavior:

```python
from ribit_2_0.autonomous_matrix import AutonomousMatrixInteraction

autonomous = AutonomousMatrixInteraction(
    conversational_mode=conv_mode,
    philosophical_reasoning=phil_reasoning,
    knowledge_base=kb
)

# Adjust engagement probability
autonomous.engagement_probability = 0.7  # 70% chance to respond
```

---

## 🏃 Running Ribit

### Method 1: Using Run Script (Recommended)

```bash
./run_bot.sh
```

Choose which bot to run:
1. **Enhanced Autonomous Bot** (recommended) - All features
2. Secure E2EE Bot - With encryption
3. Basic Matrix Bot - Simple version

### Method 2: Direct Python

```bash
# Load credentials
export $(cat .env | grep -v '^#' | xargs)

# Run enhanced autonomous bot
python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
```

### Method 3: With Custom Parameters

```bash
# Set environment variables
export MATRIX_HOMESERVER="https://anarchists.space"
export MATRIX_USER_ID="@rabit233:anarchists.space"
export MATRIX_ACCESS_TOKEN="your_token"

# Run
python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
```

---

## ✅ Verification

### 1. Test Installation

All test files are included in the repository. Run them to verify installation:

```bash
# Test learning features
python3 test_learning_features.py

# Test advanced LLM
python3 test_advanced_llm.py

# Test fixes and new features
python3 test_fixes.py

# Test emoji features
python3 test_emoji_features.py

# Test all new features
python3 test_new_features.py
```

Expected output for each test:
```
✅ ALL TESTS PASSED!
```

**Note:** If you get import errors, make sure you've installed dependencies:
```bash
pip3 install -r requirements.txt
```

### 2. Test Matrix Bot

After starting the bot:

1. **Invite bot to a room** or **join a room with the bot**

2. **Test basic commands:**
   ```
   ?status      # Check bot status
   ?sys         # System information
   ```

3. **Test new features:**
   ```
   ?learn       # Learn from message history
   ?vocab       # Show learned vocabulary
   ?llm         # Show LLM statistics
   ?tasks       # View autonomous tasks
   ?opinion quantum physics  # Get opinion
   ```

4. **Test autonomous features:**
   - Mention topics like "quantum physics", "consciousness", "AI"
   - Bot should respond autonomously (70% probability)

5. **Test emoji support:**
   - Bot should use emojis naturally in responses
   - Try: "What do you think about quantum physics? 🤔"

### 3. Verify Features

Check that all features work:

- ✅ Message history learning (`?learn`)
- ✅ Vocabulary display (`?vocab`)
- ✅ LLM statistics (`?llm`)
- ✅ Autonomous responses (mention interests)
- ✅ Emoji usage (natural in responses)
- ✅ Task autonomy (`?tasks`)
- ✅ Opinion formation (`?opinion <topic>`)
- ✅ Philosophical discussion (`?discuss <topic>`)

---

## 🔍 Troubleshooting

### Issue: "MATRIX_USER_ID and MATRIX_ACCESS_TOKEN must be set"

**Solution:**
```bash
# Run setup script
./setup_credentials.sh

# Or manually set environment variables
export MATRIX_HOMESERVER="https://anarchists.space"
export MATRIX_USER_ID="@rabit233:anarchists.space"
export MATRIX_ACCESS_TOKEN="your_token_here"
```

### Issue: "No module named 'matrix'"

**Solution:**
```bash
# Install matrix-nio
pip3 install matrix-nio[e2e]
```

### Issue: "libolm not found"

**Solution:**
```bash
# Install libolm development package
sudo apt install libolm-dev

# Reinstall matrix-nio
pip3 install --force-reinstall matrix-nio[e2e]
```

### Issue: Bot doesn't respond

**Checklist:**
1. ✓ Bot is running (check terminal)
2. ✓ Bot is in the room (invite it)
3. ✓ Credentials are correct (check `.env`)
4. ✓ Internet connection is stable
5. ✓ Try mentioning interests: "quantum physics", "AI", "consciousness"

### Issue: Import errors

**Solution:**
```bash
# Reinstall all dependencies
pip3 install -r requirements.txt --force-reinstall

# Or run install script
./install.sh
```

### Issue: Tests fail

**Solution:**
```bash
# Check Python version (must be 3.8+)
python3 --version

# Reinstall dependencies
pip3 install -r requirements.txt

# Run tests individually
python3 test_learning_features.py
python3 test_advanced_llm.py
```

### Issue: "No ROS installation detected"

**This is normal!** It's just a warning. ROS is optional. The bot will use mock ROS interface.

### Issue: Slow responses

**Solutions:**
1. Use greedy sampling for speed:
   ```python
   llm.set_advanced_parameters(sampling_strategy='greedy')
   ```

2. Enable caching:
   ```python
   llm.enable_caching = True
   llm.cache_size = 200
   ```

3. Reduce beam count:
   ```python
   llm.set_advanced_parameters(num_beams=1)
   ```

### Issue: Repetitive responses

**Solutions:**
1. Increase penalties:
   ```python
   llm.set_parameters(frequency_penalty=0.8)
   llm.set_advanced_parameters(repetition_penalty=1.8)
   ```

2. Learn from message history:
   ```
   ?learn 1000 30
   ```

---

## 📚 Additional Resources

### Documentation Files

- **README.md** - Project overview
- **INSTALL.md** - Original installation guide
- **QUICK_START.md** - Quick start guide
- **HOW_TO_RUN.md** - How to run the bot
- **LEARNING_FEATURES.md** - Message history learning
- **ADVANCED_LLM.md** - Advanced MockLLM parameters
- **EMOJI_FEATURES.md** - Emoji support
- **AUTONOMOUS_FEATURES.md** - Autonomous capabilities
- **FIXES_SUMMARY.md** - Recent fixes
- **CREDENTIALS_SETUP.md** - Credential setup guide

### Commands Reference

| Command | Description |
|---------|-------------|
| `?status` | Bot status and current activity |
| `?sys` | Full system status |
| `?learn [limit] [days]` | Learn from message history |
| `?vocab` | Show learned vocabulary |
| `?llm` | Show LLM statistics |
| `?tasks` | View autonomous task queue |
| `?opinion <topic>` | Get Ribit's opinion |
| `?discuss <topic>` | Start philosophical discussion |
| `!reset` | Reset bot state |

### New Features Guide

#### Message History Learning
```
?learn           # Learn from last 1000 messages
?learn 500 14    # Learn from 500 messages, 14 days back
?vocab           # See what was learned
```

#### Advanced LLM Control
```
?llm             # View current parameters
```

Then adjust in code:
```python
llm.set_parameters(temperature=1.2)
llm.set_advanced_parameters(repetition_penalty=1.8)
```

#### Autonomous Interaction

Just mention topics Ribit is interested in:
- "quantum physics"
- "consciousness"
- "AI and machine learning"
- "philosophy of science"

Ribit will respond autonomously!

---

## 🎯 Quick Start Summary

1. **Install:**
   ```bash
   git clone https://github.com/rabit232/ribit.2.0.git
   cd ribit.2.0
   ./install.sh
   ```

2. **Configure:**
   ```bash
   ./setup_credentials.sh
   ```

3. **Run:**
   ```bash
   ./run_bot.sh
   ```

4. **Test:**
   - Invite bot to Matrix room
   - Send: `?status`
   - Send: `?learn`
   - Mention: "quantum physics"

5. **Enjoy!** 🎉

---

## 🆘 Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Review documentation files
3. Check GitHub issues: https://github.com/rabit232/ribit.2.0/issues
4. Run diagnostics: `?llm` and `?sys` commands

---

## 🎉 You're Ready!

Ribit 2.0 is now installed with all features:

✅ Message history learning  
✅ Advanced MockLLM (20+ parameters)  
✅ Emoji support  
✅ Autonomous interaction  
✅ Task autonomy  
✅ Philosophical reasoning  
✅ Web scraping  
✅ Wikipedia integration  
✅ Image generation  
✅ Bot-to-bot communication  

**Start the bot and enjoy!** 🚀🤖✨

---

**Last Updated:** October 2025  
**Version:** 2.0 (with all new features)

