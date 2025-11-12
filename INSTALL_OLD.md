# Ribit 2.0 - Installation Instructions

Complete guide to install and run Ribit 2.0 with all features including web scraping, Wikipedia search, image generation, autonomous Matrix bot, and more.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Install (Ubuntu/Debian)](#quick-install-ubuntudebian)
3. [Manual Installation](#manual-installation)
4. [Matrix Bot Setup](#matrix-bot-setup)
5. [Optional Features](#optional-features)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements:
- **OS**: Ubuntu 20.04+, Debian 11+, or similar Linux distribution
- **Python**: 3.8 or higher (3.11 recommended)
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB for installation
- **Internet**: Required for Matrix bot and web features

### Recommended:
- Ubuntu 22.04 LTS
- Python 3.11
- 4GB RAM
- Stable internet connection

---

## Quick Install (Ubuntu/Debian)

### One-Command Installation:

```bash
# Clone repository
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0

# Run installation script
chmod +x install.sh
./install.sh
```

**The installation script will:**
1. Check Python version
2. Install system dependencies
3. Install Python packages
4. Set up configuration
5. Run tests

---

## Manual Installation

### Step 1: Clone Repository

```bash
# Clone from GitHub
git clone https://github.com/rabit232/ribit.2.0.git

# Navigate to directory
cd ribit.2.0
```

### Step 2: Install System Dependencies

```bash
# Update package list
sudo apt update

# Install required system packages
sudo apt install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    libolm-dev \
    libmagic1
```

**Package Explanations:**
- `python3` - Python interpreter
- `python3-pip` - Python package manager
- `python3-dev` - Python development headers
- `build-essential` - Compilation tools
- `git` - Version control
- `libolm-dev` - End-to-end encryption library
- `libmagic1` - File type detection

### Step 3: Install Python Dependencies

```bash
# Upgrade pip
pip3 install --upgrade pip

# Install all required packages
pip3 install -r requirements.txt
```

**If `requirements.txt` is missing, install manually:**

```bash
pip3 install \
    matrix-nio[e2e] \
    aiohttp \
    requests \
    beautifulsoup4 \
    lxml \
    wikipedia-api \
    Pillow \
    python-magic \
    aiofiles \
    asyncio
```

### Step 4: Verify Installation

```bash
# Run test script
python3 test_fixes.py
```

**Expected output:**
```
✓ Wikipedia search working
✓ Web scraping successful
✓ Image generation working
✓ MockLLM initialized with 150 response samples
✓ Response diversity: GOOD
```

---

## Matrix Bot Setup

### Step 1: Get Matrix Account

**Option A: Use Existing Account**
- Use your existing Matrix account credentials

**Option B: Create New Account**
1. Go to https://matrix.envs.net (or any Matrix homeserver)
2. Register a new account
3. Note your username and password

**Recommended Account:**
- Username: `@rabit232:envs.net`
- Homeserver: `https://matrix.envs.net`

### Step 2: Get Access Token

**Method 1: Using Element Web**
1. Log in to https://app.element.io
2. Click your profile (top left)
3. Settings → Help & About
4. Scroll down to "Advanced"
5. Click "Access Token"
6. Copy the token

**Method 2: Using curl**
```bash
curl -X POST \
  https://matrix.envs.net/_matrix/client/r0/login \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "m.login.password",
    "user": "rabit233",
    "password": "YOUR_PASSWORD"
  }'
```

Copy the `access_token` from the response.

### Step 3: Configure Environment Variables

**Create `.env` file:**
```bash
nano .env
```

**Add configuration:**
```bash
# Matrix Configuration
MATRIX_HOMESERVER=https://matrix.envs.net
MATRIX_USER_ID=@rabit232:envs.net
MATRIX_ACCESS_TOKEN=your_access_token_here

# Optional: Web Search
JINA_API_KEY=your_jina_key_here

# Optional: Image Generation
OPENAI_API_KEY=your_openai_key_here
STABILITY_API_KEY=your_stability_key_here
```

**Or export directly:**
```bash
export MATRIX_HOMESERVER="https://matrix.envs.net"
export MATRIX_USER_ID="@rabit232:envs.net"
export MATRIX_ACCESS_TOKEN="your_token_here"
```

### Step 4: Run Matrix Bot

**Basic Matrix Bot:**
```bash
python3 -m ribit_2_0.matrix_bot
```

**Enhanced Autonomous Bot (Recommended):**
```bash
python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
```

**Secure E2EE Bot:**
```bash
python3 run_secure_ribit.py
```

**Expected output:**
```
Ribit 2.0 Matrix Bot Starting...
✓ Connected to https://matrix.envs.net
✓ Logged in as @rabit232:envs.net
✓ Autonomous features enabled
✓ Emoji support active
✓ Listening for messages...
```

---

## Optional Features

### 1. Web Search (Jina AI)

**Get API Key:**
1. Go to https://jina.ai
2. Sign up for free account
3. Get API key from dashboard

**Configure:**
```bash
export JINA_API_KEY="your_jina_key"
```

### 2. Image Generation (DALL-E)

**Get API Key:**
1. Go to https://platform.openai.com
2. Create account and add payment method
3. Get API key from API keys section

**Configure:**
```bash
export OPENAI_API_KEY="your_openai_key"
```

**Usage:**
```python
from ribit_2_0.image_generation import get_image_generation

img_gen = get_image_generation()
path = img_gen.generate_with_dalle("A robot in a garden")
```

### 3. Image Generation (Stability AI)

**Get API Key:**
1. Go to https://stability.ai
2. Create account
3. Get API key from dashboard

**Configure:**
```bash
export STABILITY_API_KEY="your_stability_key"
```

### 4. ROS Integration (Robotics)

**Install ROS:**
```bash
# For Ubuntu 22.04 (ROS 2 Humble)
sudo apt install ros-humble-desktop

# Source ROS
source /opt/ros/humble/setup.bash
```

**Configure:**
```bash
export ROS_VERSION=2
export ROS_DISTRO=humble
```

---

## Verification

### Test All Features

**Run comprehensive test:**
```bash
python3 test_fixes.py
```

**Test individual features:**

```python
# Test Wikipedia
from ribit_2_0.web_scraping_wikipedia import get_web_scraping_wikipedia
wsw = get_web_scraping_wikipedia()
results = wsw.search_wikipedia("Python programming")
print(results)

# Test Image Generation
from ribit_2_0.image_generation import get_image_generation
img_gen = get_image_generation()
path = img_gen.generate_image_placeholder("Test", 400, 300)
print(f"Image: {path}")

# Test MockLLM
from ribit_2_0.mock_llm_wrapper import MockRibit20LLM
llm = MockRibit20LLM()
response = llm.get_decision("What is quantum physics?")
print(response)
```

### Check Matrix Connection

```bash
# Test Matrix connection
python3 -c "
from ribit_2_0.matrix_bot import MatrixBot
import os
bot = MatrixBot(
    os.getenv('MATRIX_HOMESERVER'),
    os.getenv('MATRIX_USER_ID'),
    os.getenv('MATRIX_ACCESS_TOKEN')
)
print('✓ Matrix connection successful!')
"
```

---

## Troubleshooting

### Common Issues

#### 1. Python Version Error

**Error:** `Python 3.8+ required`

**Solution:**
```bash
# Check version
python3 --version

# Install Python 3.11
sudo apt install python3.11 python3.11-dev

# Use Python 3.11
python3.11 -m pip install -r requirements.txt
```

#### 2. libolm Not Found

**Error:** `Could not find libolm`

**Solution:**
```bash
sudo apt update
sudo apt install libolm-dev
pip3 install --force-reinstall matrix-nio[e2e]
```

#### 3. Matrix Connection Failed

**Error:** `Failed to connect to Matrix homeserver`

**Solution:**
```bash
# Check homeserver is accessible
curl https://matrix.envs.net/_matrix/client/versions

# Verify credentials
echo $MATRIX_USER_ID
echo $MATRIX_HOMESERVER

# Test with different homeserver
export MATRIX_HOMESERVER="https://matrix.org"
```

#### 4. Wikipedia 403 Error

**Error:** `403 Forbidden for Wikipedia API`

**Solution:**
Wikipedia API requires a proper User-Agent. This is already configured in the code, but if issues persist:

```python
# The module automatically sets:
User-Agent: Ribit2.0Bot/1.0 (https://github.com/rabit232/ribit.2.0)
```

Use the wikipediaapi method instead:
```python
wsw.get_wikipedia_summary("Topic")  # Works better
```

#### 5. Image Generation Fails

**Error:** `PIL/Pillow not installed`

**Solution:**
```bash
pip3 install Pillow
```

#### 6. Import Errors

**Error:** `ModuleNotFoundError: No module named 'ribit_2_0'`

**Solution:**
```bash
# Make sure you're in the ribit.2.0 directory
cd /path/to/ribit.2.0

# Install in development mode
pip3 install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/ribit.2.0"
```

#### 7. Permission Denied

**Error:** `Permission denied` when running scripts

**Solution:**
```bash
# Make scripts executable
chmod +x install.sh
chmod +x run_*.py

# Or run with python3
python3 run_secure_ribit.py
```

---

## Running as a Service

### Create systemd service

**Create service file:**
```bash
sudo nano /etc/systemd/system/ribit.service
```

**Add configuration:**
```ini
[Unit]
Description=Ribit 2.0 Matrix Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/ribit.2.0
Environment="MATRIX_HOMESERVER=https://matrix.envs.net"
Environment="MATRIX_USER_ID=@rabit232:envs.net"
Environment="MATRIX_ACCESS_TOKEN=your_token_here"
ExecStart=/usr/bin/python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable ribit.service

# Start service
sudo systemctl start ribit.service

# Check status
sudo systemctl status ribit.service

# View logs
sudo journalctl -u ribit.service -f
```

---

## Quick Reference

### Start Matrix Bot
```bash
python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
```

### Run Tests
```bash
python3 test_fixes.py
```

### Update Ribit
```bash
cd ribit.2.0
git pull origin master
pip3 install -r requirements.txt
```

### Check Logs
```bash
# If running as service
sudo journalctl -u ribit.service -f

# If running in terminal
# Logs are printed to stdout
```

---

## Next Steps

After installation:

1. **Join Matrix Rooms**: Invite Ribit to your Matrix rooms
2. **Test Commands**: Try `?help`, `?status`, `?tasks`
3. **Configure Settings**: Customize behavior in settings
4. **Explore Features**: Try autonomous responses, emoji reactions
5. **Read Documentation**: Check other `.md` files for advanced features

---

## Support

**Issues?** Open an issue on GitHub:
https://github.com/rabit232/ribit.2.0/issues

**Documentation:**
- `README.md` - Overview
- `AUTONOMOUS_FEATURES.md` - Autonomous capabilities
- `EMOJI_FEATURES.md` - Emoji support
- `FIXES_SUMMARY.md` - Recent fixes
- `QUICK_START.md` - Quick start guide

---

## License

Ribit 2.0 is open source. See `LICENSE` file for details.

---

**Installation complete! Ribit 2.0 is ready to use! 🚀🤖✨**

