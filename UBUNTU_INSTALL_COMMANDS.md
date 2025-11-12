# Ribit 2.0 - Ubuntu Installation Commands

**Complete step-by-step commands for Ubuntu to fix missing modules and install everything.**

---

## 🚨 Quick Fix for Missing Modules

If you're seeing missing modules, your local repository is out of date. Here's how to fix it:

### Option 1: Pull Latest Changes (Recommended)

```bash
# Navigate to ribit directory
cd ~/ribit.2.0

# Pull latest changes from GitHub
git pull origin master

# Verify all modules are now present
python3 verify_modules.py
```

### Option 2: Fresh Install (If pull doesn't work)

```bash
# Backup your .env file if you have one
cp ~/ribit.2.0/.env ~/ribit_env_backup.txt 2>/dev/null || true

# Remove old directory
cd ~
rm -rf ribit.2.0

# Clone fresh copy
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0

# Restore .env if you had one
cp ~/ribit_env_backup.txt .env 2>/dev/null || true

# Run installation
chmod +x install.sh
./install.sh
```

---

## 📦 Complete Fresh Installation (Ubuntu 20.04/22.04)

### Step 1: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Python 3.8+ (if not installed)

```bash
# Check Python version
python3 --version

# If Python < 3.8, install Python 3.10
sudo apt install -y python3.10 python3.10-dev python3-pip
```

### Step 3: Install System Dependencies

```bash
sudo apt install -y \
    python3-dev \
    build-essential \
    git \
    libolm-dev \
    libmagic1 \
    pkg-config \
    libssl-dev \
    libffi-dev
```

### Step 4: Clone Repository

```bash
cd ~
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0
```

### Step 5: Install Python Dependencies

```bash
# Upgrade pip first
pip3 install --upgrade pip

# Install all dependencies
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

### Step 6: Create Directories

```bash
mkdir -p generated_images logs
```

### Step 7: Verify Installation

```bash
python3 verify_modules.py
```

**Expected output:**
```
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

Results: 14 passed, 0 failed
✅ ALL MODULES VERIFIED!
```

### Step 8: Run Tests

```bash
# Test basic features
python3 test_fixes.py

# Test learning features
python3 test_learning_features.py

# Test advanced LLM
python3 test_advanced_llm.py

# Test dual LLM pipeline
python3 test_dual_pipeline.py

# Test emoji features
python3 test_emoji_features.py
```

### Step 9: Configure Credentials

```bash
# Create .env file
nano .env
```

**Add this content:**
```bash
# Matrix Configuration
MATRIX_HOMESERVER=https://matrix.envs.net
MATRIX_USER_ID=@rabit232:envs.net
MATRIX_ACCESS_TOKEN=your_token_here

# Optional
MATRIX_DEVICE_ID=RIBIT_DEVICE
JINA_API_KEY=your_jina_key
OPENAI_API_KEY=your_openai_key
STABILITY_API_KEY=your_stability_key
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

### Step 10: Run Ribit

```bash
# Make scripts executable
chmod +x run_bot.sh setup_credentials.sh

# Run the bot
./run_bot.sh
```

---

## 🔧 Fix Specific Missing Modules

If individual modules are missing after git pull, you can download them directly:

### Fix Enhanced MockLLM

```bash
cd ~/ribit.2.0
wget https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0/enhanced_mock_llm.py -O ribit_2_0/enhanced_mock_llm.py
```

### Fix Advanced MockLLM

```bash
cd ~/ribit.2.0
wget https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0/advanced_mock_llm.py -O ribit_2_0/advanced_mock_llm.py
```

### Fix Dual LLM Pipeline

```bash
cd ~/ribit.2.0
wget https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0/dual_llm_pipeline.py -O ribit_2_0/dual_llm_pipeline.py
```

### Fix Message History Learner

```bash
cd ~/ribit.2.0
wget https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0/message_history_learner.py -O ribit_2_0/message_history_learner.py
```

### Fix Web Scraping & Wikipedia

```bash
cd ~/ribit.2.0
wget https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0/web_scraping_wikipedia.py -O ribit_2_0/web_scraping_wikipedia.py
```

### Fix Image Generation

```bash
cd ~/ribit.2.0
wget https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0/image_generation.py -O ribit_2_0/image_generation.py
```

### Download All Missing Modules at Once

```bash
cd ~/ribit.2.0

# Download all missing modules
wget https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0/enhanced_mock_llm.py -O ribit_2_0/enhanced_mock_llm.py
wget https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0/advanced_mock_llm.py -O ribit_2_0/advanced_mock_llm.py
wget https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0/dual_llm_pipeline.py -O ribit_2_0/dual_llm_pipeline.py
wget https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0/message_history_learner.py -O ribit_2_0/message_history_learner.py
wget https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0/web_scraping_wikipedia.py -O ribit_2_0/web_scraping_wikipedia.py
wget https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0/image_generation.py -O ribit_2_0/image_generation.py

# Verify
python3 verify_modules.py
```

---

## 🐛 Troubleshooting Common Issues

### Issue: "git pull" says "Already up to date" but modules missing

**Solution:**
```bash
cd ~/ribit.2.0

# Force fetch all changes
git fetch --all

# Reset to latest
git reset --hard origin/master

# Verify
python3 verify_modules.py
```

### Issue: "Permission denied" errors

**Solution:**
```bash
# Make scripts executable
chmod +x ~/ribit.2.0/*.sh

# Or for specific script
chmod +x ~/ribit.2.0/install.sh
chmod +x ~/ribit.2.0/run_bot.sh
```

### Issue: "pip3: command not found"

**Solution:**
```bash
sudo apt update
sudo apt install -y python3-pip
```

### Issue: "libolm not found" during matrix-nio installation

**Solution:**
```bash
# Install libolm development package
sudo apt install -y libolm-dev

# Reinstall matrix-nio
pip3 install --force-reinstall 'matrix-nio[e2e]'
```

### Issue: Import errors for specific modules

**Solution:**
```bash
# Reinstall all Python dependencies
pip3 install -r ~/ribit.2.0/requirements.txt --force-reinstall
```

### Issue: "No module named 'ribit_2_0'"

**Solution:**
```bash
# Make sure you're in the ribit.2.0 directory
cd ~/ribit.2.0

# Then run commands
python3 verify_modules.py
```

### Issue: Tests fail

**Solution:**
```bash
cd ~/ribit.2.0

# Check Python version (must be 3.8+)
python3 --version

# Reinstall dependencies
pip3 install -r requirements.txt --force-reinstall

# Run tests individually to see which fails
python3 test_fixes.py
python3 test_learning_features.py
python3 test_advanced_llm.py
python3 test_dual_pipeline.py
```

---

## ✅ Verification Checklist

After installation, verify everything works:

```bash
cd ~/ribit.2.0

# 1. Check all modules present
python3 verify_modules.py
# Should show: 14 passed, 0 failed

# 2. Check Python packages
pip3 list | grep -E "(matrix-nio|aiohttp|beautifulsoup4|wikipedia)"
# Should show all packages installed

# 3. Check system dependencies
dpkg -l | grep -E "(libolm-dev|libmagic1|build-essential)"
# Should show all installed

# 4. Run a quick test
python3 -c "from ribit_2_0.dual_llm_pipeline import DualLLMPipeline; print('✓ Dual LLM works!')"
# Should print: ✓ Dual LLM works!

# 5. Check file permissions
ls -la *.sh
# Should show executable permissions (x)
```

---

## 🚀 Quick Start After Installation

```bash
cd ~/ribit.2.0

# Option 1: Use setup script
./setup_credentials.sh
./run_bot.sh

# Option 2: Manual
nano .env  # Add your credentials
python3 -m ribit_2_0.enhanced_autonomous_matrix_bot

# Option 3: Test dual LLM
python3 test_dual_llm_programming.py
```

---

## 📊 Expected File Structure

After successful installation, you should have:

```
~/ribit.2.0/
├── ribit_2_0/
│   ├── mock_llm_wrapper.py          ✓ Basic MockLLM
│   ├── enhanced_mock_llm.py         ✓ Enhanced MockLLM
│   ├── advanced_mock_llm.py         ✓ Advanced MockLLM
│   ├── dual_llm_pipeline.py         ✓ Dual LLM Pipeline
│   ├── emoji_expression.py          ✓ Emoji support
│   ├── message_history_learner.py   ✓ History learning
│   ├── philosophical_reasoning.py   ✓ Philosophy
│   ├── conversational_mode.py       ✓ Conversation
│   ├── autonomous_matrix.py         ✓ Autonomous
│   ├── task_autonomy.py             ✓ Task selection
│   ├── web_scraping_wikipedia.py    ✓ Web scraping
│   └── image_generation.py          ✓ Images
├── install.sh                       ✓ Installer
├── run_bot.sh                       ✓ Run script
├── verify_modules.py                ✓ Verification
├── test_dual_pipeline.py            ✓ Tests
└── .env                             ✓ Your credentials
```

---

## 💡 Pro Tips

### Tip 1: Keep Repository Updated

```bash
# Add this to your cron for daily updates
cd ~/ribit.2.0 && git pull origin master
```

### Tip 2: Backup Your Configuration

```bash
# Backup .env file
cp ~/ribit.2.0/.env ~/ribit_backup_$(date +%Y%m%d).env
```

### Tip 3: Use Virtual Environment (Optional)

```bash
# Create virtual environment
python3 -m venv ~/ribit_venv

# Activate it
source ~/ribit_venv/bin/activate

# Install dependencies
cd ~/ribit.2.0
pip install -r requirements.txt

# Run ribit
python -m ribit_2_0.enhanced_autonomous_matrix_bot
```

### Tip 4: Run as System Service

```bash
# Create systemd service
sudo nano /etc/systemd/system/ribit.service
```

**Add:**
```ini
[Unit]
Description=Ribit 2.0 Matrix Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/ribit.2.0
ExecStart=/usr/bin/python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ribit
sudo systemctl start ribit
sudo systemctl status ribit
```

---

## 📞 Getting Help

If you still have issues:

1. **Check logs:**
   ```bash
   cd ~/ribit.2.0
   ls -la logs/
   cat logs/ribit.log
   ```

2. **Run verification:**
   ```bash
   python3 verify_modules.py
   ```

3. **Check GitHub issues:**
   https://github.com/rabit232/ribit.2.0/issues

4. **Fresh install:**
   ```bash
   cd ~
   rm -rf ribit.2.0
   git clone https://github.com/rabit232/ribit.2.0.git
   cd ribit.2.0
   ./install.sh
   ```

---

**All commands tested on Ubuntu 20.04 and 22.04!** ✅

**Repository:** https://github.com/rabit232/ribit.2.0

