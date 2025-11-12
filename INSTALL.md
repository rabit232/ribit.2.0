# Ribit 2.0 - Complete Installation Guide

**Version:** 2.0 (Latest)  
**Date:** October 2025  
**Status:** All 14 modules verified ✅

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation Methods](#installation-methods)
4. [Verification](#verification)
5. [Configuration](#configuration)
6. [Running Ribit](#running-ribit)
7. [Features & Commands](#features--commands)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Setup](#advanced-setup)

---

## 🚀 Quick Start

**For Ubuntu/Debian users (fastest method):**

```bash
# Clone repository
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0

# Run automated installer
chmod +x install.sh
./install.sh

# Configure credentials
./setup_credentials.sh

# Run Ribit
./run_bot.sh
```

**That's it!** 🎉

---

## 💻 System Requirements

### Minimum Requirements

- **OS:** Ubuntu 20.04+, Debian 10+, or compatible Linux
- **Python:** 3.7 or higher (3.8+ recommended)
- **RAM:** 512 MB minimum, 1 GB recommended
- **Disk:** 500 MB free space
- **Internet:** Required for Matrix connection

### Recommended

- **OS:** Ubuntu 22.04 LTS
- **Python:** 3.11
- **RAM:** 2 GB
- **Disk:** 1 GB free space

### Check Your System

```bash
# Check Python version
python3 --version

# Check available disk space
df -h ~

# Check RAM
free -h

# Check internet connection
ping -c 3 matrix.org
```

---

## 📦 Installation Methods

### Method 1: Automated Installation (Recommended) ⭐

**Best for:** Most users, quick setup

```bash
# 1. Clone repository
cd ~
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0

# 2. Run installer
chmod +x install.sh
./install.sh
```

The installer will:
- ✅ Check Python version
- ✅ Install system dependencies
- ✅ Install Python packages
- ✅ Create necessary directories
- ✅ Run verification tests
- ✅ Create configuration template

**Time:** ~5-10 minutes

---

### Method 2: Manual Installation

**Best for:** Advanced users, custom setups

#### Step 1: Install System Dependencies

```bash
sudo apt update
sudo apt install -y \
    python3-dev \
    build-essential \
    git \
    libolm-dev \
    libmagic1 \
    pkg-config \
    libssl-dev \
    libffi-dev \
    wget \
    curl
```

#### Step 2: Clone Repository

```bash
cd ~
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0
```

#### Step 3: Install Python Dependencies

```bash
pip3 install --upgrade pip

pip3 install \
    'matrix-nio[e2e]>=0.20.0' \
    'aiohttp>=3.8.0' \
    'requests>=2.28.0' \
    'beautifulsoup4>=4.11.0' \
    'lxml>=4.9.0' \
    'wikipedia-api>=0.5.8' \
    'Pillow>=9.0.0' \
    'python-magic>=0.4.27' \
    'aiofiles>=23.0.0'
```

#### Step 4: Create Directories

```bash
mkdir -p generated_images logs ribit_thoughts
```

#### Step 5: Verify Installation

```bash
python3 verify_modules.py
```

You should see: **14 passed, 0 failed** ✅

---

### Method 3: Virtual Environment (Recommended for Development)

**Best for:** Developers, isolated environment

```bash
# 1. Install virtualenv
pip3 install virtualenv

# 2. Clone repository
cd ~
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0

# 3. Create virtual environment
python3 -m venv venv

# 4. Activate virtual environment
source venv/bin/activate

# 5. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 6. Verify
python verify_modules.py
```

**To activate later:**

```bash
cd ~/ribit.2.0
source venv/bin/activate
```

---

## ✅ Verification

### Verify All Modules

```bash
cd ~/ribit.2.0
python3 verify_modules.py
```

**Expected output:**

```
======================================================================
Ribit 2.0 - Module Verification
======================================================================

Checking modules...

✓ Basic MockLLM
✓ Enhanced MockLLM (8 params)
✓ Advanced MockLLM (20+ params)
✓ Dual LLM Pipeline (NEW!) 🎮
✓ Emotional Module
✓ Intellectual Module
✓ Emoji Expression
✓ Message History Learner
✓ Philosophical Reasoning
✓ Conversational Mode
✓ Autonomous Matrix
✓ Task Autonomy
✓ Web Scraping & Wikipedia
✓ Image Generation

======================================================================
Results: 14 passed, 0 failed
======================================================================

✅ ALL MODULES VERIFIED!
```

### Run Tests

```bash
# Test all features
python3 test_fixes.py
python3 test_learning_features.py
python3 test_advanced_llm.py
python3 test_dual_pipeline.py
python3 test_emoji_features.py

# Test dual LLM
python3 test_dual_llm_programming.py
```

---

## ⚙️ Configuration

### Step 1: Get Matrix Credentials

#### Option A: Using Element Web (Easiest)

1. Go to https://app.element.io
2. Log in with your Matrix account
3. Click your profile (top left)
4. Settings → Help & About
5. Scroll to "Access Token"
6. Click to reveal and copy

#### Option B: Using curl

```bash
curl -X POST https://matrix.envs.net/_matrix/client/r0/login \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "m.login.password",
    "user": "rabit233",
    "password": "YOUR_PASSWORD"
  }'
```

Copy the `access_token` from the response.

### Step 2: Configure Ribit

#### Option A: Interactive Setup (Easiest)

```bash
cd ~/ribit.2.0
./setup_credentials.sh
```

Follow the prompts:
1. **Homeserver:** Press Enter (uses default: https://matrix.envs.net)
2. **User ID:** Press Enter (uses default: @rabit232:envs.net)
3. **Access Token:** Paste your token
4. **Device ID:** Press Enter (skip)
5. **API Keys:** Press Enter for each (skip optional features)

#### Option B: Manual Configuration

Create `.env` file:

```bash
cd ~/ribit.2.0
nano .env
```

Add this content:

```bash
# Matrix Configuration
MATRIX_HOMESERVER=https://matrix.envs.net
MATRIX_USER_ID=@rabit232:envs.net
MATRIX_ACCESS_TOKEN=your_access_token_here

# Optional: Device ID
MATRIX_DEVICE_ID=RIBIT_BOT

# Optional: Jina AI (for advanced web search)
JINA_API_KEY=your_jina_key_here

# Optional: DALL-E (for image generation)
OPENAI_API_KEY=your_openai_key_here

# Optional: Stability AI (for image generation)
STABILITY_API_KEY=your_stability_key_here
```

Save and exit (Ctrl+X, Y, Enter)

### Step 3: Verify Configuration

```bash
# Load credentials
export $(cat .env | grep -v '^#' | xargs)

# Check they're loaded
echo "User: $MATRIX_USER_ID"
echo "Homeserver: $MATRIX_HOMESERVER"
echo "Token: ${MATRIX_ACCESS_TOKEN:0:20}..."
```

---

## 🏃 Running Ribit

### Method 1: Run Script (Easiest)

```bash
cd ~/ribit.2.0
./run_bot.sh
```

Choose option:
1. **Enhanced Autonomous Bot** (recommended) - Full features
2. **Secure E2EE Bot** - End-to-end encryption support
3. **Basic Matrix Bot** - Simple bot

### Method 2: Direct Python

```bash
cd ~/ribit.2.0
python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
```

### Method 3: With Virtual Environment

```bash
cd ~/ribit.2.0
source venv/bin/activate
python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
```

### Expected Output

```
INFO:__main__:Ribit 2.0 Enhanced Autonomous Matrix Bot
INFO:__main__:Connecting to https://matrix.envs.net
INFO:__main__:Logged in as @rabit232:envs.net
INFO:__main__:Listening for messages...
INFO:__main__:Autonomous work loop started
```

**Ribit is now running!** 🎉

### Stop Ribit

Press **Ctrl+C** in the terminal.

---

## 🎯 Features & Commands

### Learning Commands

| Command | Description | Example |
|---------|-------------|---------|
| `?history` | Learn from room history | `?history` |
| `?history [limit]` | Learn from N messages | `?history 2000` |
| `?history [limit] [days]` | Learn from N messages, D days back | `?history 1000 60` |
| `?learn` | Alias for ?history | `?learn` |
| `?vocab` | Show learned vocabulary | `?vocab` |

### Information Commands

| Command | Description |
|---------|-------------|
| `?status` | Show bot status and engagement stats |
| `?sys` | Show system information |
| `?tasks` | Show autonomous task suggestions |
| `?llm` | Show LLM statistics and parameters |

### Interaction Commands

| Command | Description | Example |
|---------|-------------|---------|
| `?opinion <topic>` | Get Ribit's opinion | `?opinion quantum physics` |
| `?discuss <topic>` | Start philosophical discussion | `?discuss consciousness` |

### Example Usage

```
You: ?history 1000
Ribit: 📚 Starting to learn from message history...

[Ribit analyzes 1000 messages]

Ribit: ✅ Learning Complete!
       Processed: 1000 messages from 12 users
       Learned: 2,341 words, 1,156 phrases, 38 topics
       I'll now speak more fluently! 🤖✨

You: ?vocab
Ribit: 📚 My Learned Vocabulary
       Top Words: quantum, physics, algorithm, neural, network...
       Common Phrases: quantum physics, machine learning...

You: ?opinion quantum physics
Ribit: Quantum physics fascinates me! The way it challenges 
       our classical assumptions about reality is profound...

You: ?status
Ribit: 🤖 Ribit 2.0 Status
       Uptime: 2h 34m
       Messages processed: 156
       Autonomous responses: 23
       Tasks completed: 5
```

---

## 🔧 Troubleshooting

### Issue: Modules Not Found

**Error:** `✗ Enhanced MockLLM (8 params): File not found`

**Solution:**

```bash
cd ~/ribit.2.0
git pull origin master
python3 verify_modules.py
```

Or use the fix script:

```bash
cd ~/ribit.2.0
./DEFINITIVE_FIX.sh
```

---

### Issue: Type Subscript Error

**Error:** `'type' object is not subscriptable`

**Cause:** Python version incompatibility

**Solution:**

```bash
# Check Python version
python3 --version

# If Python 3.7 or 3.8, update the module
cd ~/ribit.2.0
git pull origin master
```

The latest version is compatible with Python 3.7+

---

### Issue: Matrix Connection Failed

**Error:** `Failed to connect to Matrix homeserver`

**Solutions:**

1. **Check credentials:**
   ```bash
   cat .env
   ```
   Verify MATRIX_USER_ID and MATRIX_ACCESS_TOKEN are correct

2. **Check homeserver:**
   ```bash
   curl -I https://matrix.envs.net
   ```
   Should return HTTP 200

3. **Test access token:**
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://matrix.envs.net/_matrix/client/r0/account/whoami
   ```

4. **Regenerate token:**
   - Log out and log back in to Element
   - Get new access token
   - Update .env file

---

### Issue: Import Errors

**Error:** `ModuleNotFoundError: No module named 'matrix'`

**Solution:**

```bash
# Reinstall dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Or install specific package
pip3 install 'matrix-nio[e2e]>=0.20.0'
```

---

### Issue: Permission Denied

**Error:** `Permission denied: './install.sh'`

**Solution:**

```bash
chmod +x install.sh setup_credentials.sh run_bot.sh
./install.sh
```

---

### Issue: libolm Not Found

**Error:** `libolm not found`

**Solution:**

```bash
sudo apt update
sudo apt install -y libolm-dev
pip3 install --force-reinstall 'matrix-nio[e2e]'
```

---

## 🎓 Advanced Setup

### Run as Systemd Service

Create service file:

```bash
sudo nano /etc/systemd/system/ribit.service
```

Add:

```ini
[Unit]
Description=Ribit 2.0 Matrix Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/ribit.2.0
Environment="MATRIX_HOMESERVER=https://matrix.envs.net"
Environment="MATRIX_USER_ID=@rabit232:envs.net"
Environment="MATRIX_ACCESS_TOKEN=YOUR_TOKEN"
ExecStart=/usr/bin/python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ribit
sudo systemctl start ribit

# Check status
sudo systemctl status ribit

# View logs
sudo journalctl -u ribit -f
```

---

### Auto-Update with Cron

```bash
# Edit crontab
crontab -e

# Add this line (runs every Sunday at 2 AM)
0 2 * * 0 cd ~/ribit.2.0 && git pull origin master && systemctl restart ribit
```

---

### Use Different LLM

Edit your bot startup:

```python
# In your custom script
from ribit_2_0.dual_llm_pipeline import DualLLMPipeline

# Use Dual LLM Pipeline (best quality)
llm = DualLLMPipeline(preset='quality')

# Or use Advanced MockLLM
from ribit_2_0.advanced_mock_llm import AdvancedMockLLM
llm = AdvancedMockLLM(
    temperature=0.8,
    repetition_penalty=1.5,
    sampling_strategy='nucleus'
)
```

---

### Configure Logging

Create `logging_config.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ribit.log'),
        logging.StreamHandler()
    ]
)
```

---

## 📚 What You Get

After installation, you have:

### 14 Verified Modules

✅ Basic MockLLM  
✅ Enhanced MockLLM (8 parameters)  
✅ Advanced MockLLM (20+ parameters)  
✅ Dual LLM Pipeline (4-stage processing)  
✅ Emotional Module  
✅ Intellectual Module  
✅ Emoji Expression  
✅ Message History Learner  
✅ Philosophical Reasoning  
✅ Conversational Mode  
✅ Autonomous Matrix Interaction  
✅ Task Autonomy  
✅ Web Scraping & Wikipedia  
✅ Image Generation  

### 4 LLM Options

1. **MockRibit20LLM** - Basic, fast
2. **EnhancedMockLLM** - 8 parameters, style adaptation
3. **AdvancedMockLLM** - 20+ parameters, full control
4. **DualLLMPipeline** - 4-stage processing (best quality)

### Key Features

✅ Learn from message history (`?history`)  
✅ Understand word context in sentences  
✅ Autonomous conversation  
✅ Self-selected tasks  
✅ Philosophical reasoning  
✅ Bot-to-bot communication  
✅ Emoji support  
✅ Web scraping  
✅ Wikipedia integration  
✅ Image generation  

---

## 🆘 Getting Help

### Documentation

- **Installation:** `INSTALL_NEW.md` (this file)
- **Quick Start:** `QUICK_START.md`
- **How to Run:** `HOW_TO_RUN.md`
- **Credentials:** `CREDENTIALS_SETUP.md`
- **Ubuntu Commands:** `UBUNTU_INSTALL_COMMANDS.md`
- **Fix Missing Modules:** `FIX_MISSING_MODULES_README.md`
- **Final Summary:** `FINAL_FIX_SUMMARY.md`

### Quick Fixes

- **Missing modules:** `./DEFINITIVE_FIX.sh`
- **Verify installation:** `python3 verify_modules.py`
- **Test features:** `python3 test_*.py`

### Repository

**GitHub:** https://github.com/rabit232/ribit.2.0

---

## ✅ Installation Checklist

- [ ] Python 3.7+ installed
- [ ] System dependencies installed
- [ ] Repository cloned
- [ ] Python packages installed
- [ ] Modules verified (14/14)
- [ ] Matrix credentials configured
- [ ] .env file created
- [ ] Tests passed
- [ ] Bot runs successfully
- [ ] Commands work in Matrix

---

## 🎉 You're Ready!

```bash
cd ~/ribit.2.0
./run_bot.sh
```

**Enjoy your fully autonomous AI bot!** 🤖✨

---

**Version:** 2.0  
**Last Updated:** October 2025  
**Status:** Production Ready ✅

