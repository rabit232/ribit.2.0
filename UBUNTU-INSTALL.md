# 🐧 Ribit 2.0 - Ubuntu Installation Guide

## Quick Install (5 Minutes)

### **Step 1: Install System Dependencies**
```bash
sudo apt update
sudo apt install -y python3 python3-pip git chromium-browser
```

### **Step 2: Clone Ribit 2.0**
```bash
cd ~
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0
```

### **Step 3: Install Python Packages**
```bash
pip3 install -r requirements.txt
```

### **Step 4: Configure Matrix Bot**
```bash
cp .env.example .env
nano .env
```

**Edit these lines:**
```env
MATRIX_HOMESERVER=https://your-homeserver.com
MATRIX_USERNAME=@yourbotname:your-homeserver.com
MATRIX_PASSWORD=your_bot_password
AUTHORIZED_USERS=@yourname:your-homeserver.com
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

### **Step 5: Run Ribit!**
```bash
python3 run_matrix_bot.py
```

---

## Complete Installation Guide

### **Prerequisites**

**Ubuntu Version:**
- Ubuntu 20.04 LTS or newer
- Ubuntu 22.04 LTS (recommended)
- Ubuntu 24.04 LTS

**Internet Connection:**
- Required for installation and image generation

---

## Detailed Steps

### **1. Update System**

```bash
sudo apt update
sudo apt upgrade -y
```

### **2. Install Required Packages**

```bash
# Python and Git
sudo apt install -y python3 python3-pip python3-venv git

# Chrome/Chromium for image generation
sudo apt install -y chromium-browser

# Optional: Build tools (if you get compilation errors)
sudo apt install -y build-essential python3-dev libffi-dev libssl-dev
```

### **3. Clone Repository**

```bash
cd ~
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0
```

### **4. Create Virtual Environment (Recommended)**

```bash
python3 -m venv ribit_env
source ribit_env/bin/activate
```

**Note:** You'll need to activate this every time:
```bash
cd ~/ribit.2.0
source ribit_env/bin/activate
```

### **5. Install Python Dependencies**

```bash
pip3 install -r requirements.txt
```

**This installs:**
- matrix-nio (Matrix chat)
- selenium (Image generation)
- pillow (Image processing)
- wikipedia-api (Knowledge)
- beautifulsoup4 (Web scraping)
- And more...

### **6. Create Matrix Bot Account**

**Option A: Use Existing Account**
- Use your personal Matrix account
- **Warning:** Bot will run as you!

**Option B: Create New Bot Account (Recommended)**

1. Go to your Matrix homeserver
2. Register new account
3. Username: `ribit` or `ribit-bot`
4. Remember the password!

### **7. Configure Environment**

```bash
cp .env.example .env
nano .env
```

**Required Settings:**

```env
# Matrix Connection
MATRIX_HOMESERVER=https://matrix.org
MATRIX_USERNAME=@ribit:matrix.org
MATRIX_PASSWORD=your_secure_password

# Authorized Users (who can use commands)
AUTHORIZED_USERS=@yourname:matrix.org,@friend:matrix.org

# Bot Name
BOT_NAME=ribit.2.0
```

**Optional Settings:**

```env
# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/ribit2.0.log

# Features
ENABLE_WEB_SEARCH=true
ENABLE_IMAGE_GENERATION=true
```

**Save:** `Ctrl+X`, `Y`, `Enter`

### **8. Test Configuration**

```bash
python3 validate-env.py
```

**Expected output:**
```
✅ MATRIX_HOMESERVER: https://matrix.org
✅ MATRIX_USERNAME: @ribit:matrix.org
✅ MATRIX_PASSWORD: **********
✅ Configuration valid!
```

### **9. Run Ribit**

```bash
python3 run_matrix_bot.py
```

**Expected output:**
```
🤖 Ribit 2.0 Matrix Bot Launcher
==================================================
✅ Found .env file, loading configuration...
✅ MATRIX_HOMESERVER: https://matrix.org
✅ MATRIX_USERNAME: @ribit:matrix.org

🚀 Starting Ribit 2.0 Matrix Bot...
✅ Logged in successfully
🔄 Starting sync loop...
```

### **10. Invite Bot to Room**

1. Open your Matrix client (Element, etc.)
2. Create or open a room
3. Invite the bot: `/invite @ribit:matrix.org`
4. Bot will auto-join

### **11. Test Bot**

Send in the room:
```
ribit.2.0 hello
```

**Expected response:**
```
Greetings! I am Ribit 2.0, an elegant AI agent...
```

---

## Features to Test

### **1. Basic Chat**
```
ribit.2.0 how are you?
```

### **2. Questions**
```
What is Python?
How much is 10 plus 10?
When was World War 2?
```

### **3. Programming Help**
```
How to create a loop in Python?
I got a syntax error
```

### **4. Image Generation**
```
generate image of a sunset over mountains
create picture of a cute robot
```

### **5. Commands**
```
?help
!reset
```

---

## Troubleshooting

### **Problem: "Module not found" errors**

**Solution:**
```bash
cd ~/ribit.2.0
source ribit_env/bin/activate  # If using venv
pip3 install -r requirements.txt
```

### **Problem: "Login failed" or "M_FORBIDDEN"**

**Check:**
1. Username format: `@username:homeserver.com` (use colon!)
2. Password is correct
3. Homeserver URL is correct (no `/matrix` at end)

**Fix:**
```bash
nano .env
# Fix MATRIX_USERNAME, MATRIX_PASSWORD, MATRIX_HOMESERVER
```

### **Problem: Bot doesn't respond**

**Check:**
1. Bot is running (terminal shows "Starting sync loop...")
2. Bot is in the room (invite it!)
3. Using trigger word: `ribit.2.0` or asking questions with `?`

**Test:**
```
ribit.2.0 are you there?
```

### **Problem: "Selenium not found" for image generation**

**Solution:**
```bash
pip3 install selenium
```

### **Problem: "ChromeDriver not found"**

**Solution:**
```bash
sudo apt install chromium-chromedriver
```

### **Problem: Bot crashes or stops**

**Check logs:**
```bash
cat logs/ribit2.0.log
```

**Restart:**
```bash
python3 run_matrix_bot.py
```

---

## Running as Service (Auto-Start)

### **Create systemd service:**

```bash
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
ExecStart=/home/your_username/ribit.2.0/ribit_env/bin/python3 run_matrix_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable ribit
sudo systemctl start ribit
```

**Check status:**
```bash
sudo systemctl status ribit
```

**View logs:**
```bash
sudo journalctl -u ribit -f
```

---

## Updating Ribit

### **Get Latest Version:**

```bash
cd ~/ribit.2.0
git pull origin master
pip3 install -r requirements.txt
```

### **Restart Bot:**

```bash
# If running manually:
# Press Ctrl+C to stop, then:
python3 run_matrix_bot.py

# If running as service:
sudo systemctl restart ribit
```

---

## Uninstalling

### **Stop Bot:**
```bash
# If running as service:
sudo systemctl stop ribit
sudo systemctl disable ribit
sudo rm /etc/systemd/system/ribit.service

# If running manually:
# Press Ctrl+C in terminal
```

### **Remove Files:**
```bash
cd ~
rm -rf ribit.2.0
rm -rf ribit_env  # If you used venv
```

---

## Quick Reference

### **Start Bot:**
```bash
cd ~/ribit.2.0
source ribit_env/bin/activate  # If using venv
python3 run_matrix_bot.py
```

### **Stop Bot:**
```
Press Ctrl+C
```

### **Update Bot:**
```bash
cd ~/ribit.2.0
git pull
pip3 install -r requirements.txt
```

### **View Logs:**
```bash
cat ~/ribit.2.0/logs/ribit2.0.log
```

### **Test Configuration:**
```bash
python3 validate-env.py
```

---

## Support

### **Check Documentation:**
- `README.md` - Overview
- `QUICK-FIX.md` - Common issues
- `IMAGE-GENERATION-GUIDE.md` - Image generation
- `PROGRAMMING-ASSISTANT-GUIDE.md` - Programming help
- `WEB-KNOWLEDGE-GUIDE.md` - Web search

### **Check Logs:**
```bash
cat logs/ribit2.0.log
```

### **GitHub Issues:**
https://github.com/rabit232/ribit.2.0/issues

---

## Summary

**Installation:**
```bash
# 1. Install dependencies
sudo apt install -y python3 python3-pip git chromium-browser

# 2. Clone repo
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0

# 3. Install packages
pip3 install -r requirements.txt

# 4. Configure
cp .env.example .env
nano .env  # Edit settings

# 5. Run
python3 run_matrix_bot.py
```

**That's it!** 🎉

---

**Welcome, human.** Ribit is ready to serve on Ubuntu! 🐧🤖✨
