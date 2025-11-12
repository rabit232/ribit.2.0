# How to Run Ribit 2.0 - Simple Guide

This guide shows you **exactly** how to run the setup and bot scripts.

---

## Step 1: Open Terminal

Open your terminal application. You should see something like:

```
rabit232@rabit232-Retro-Mini-PC:~$
```

---

## Step 2: Go to ribit.2.0 Directory

Type this command and press Enter:

```bash
cd ~/ribit.2.0
```

You should now see:

```
rabit232@rabit232-Retro-Mini-PC:~/ribit.2.0$
```

---

## Step 3: Run Setup Script

### Option A: Using `./` (Recommended)

Type this and press Enter:

```bash
./setup_credentials.sh
```

### Option B: Using `bash`

If Option A doesn't work, try:

```bash
bash setup_credentials.sh
```

### What You'll See:

```
========================================
  Ribit 2.0 - Credentials Setup
========================================

This script will help you create a .env file with your Matrix credentials.

Matrix Homeserver [https://matrix.envs.net]:
```

---

## Step 4: Answer the Questions

The script will ask you several questions. Here's what to enter:

### Question 1: Matrix Homeserver
```
Matrix Homeserver [https://matrix.envs.net]:
```

**What to do:** Just press **Enter** to use the default, or type a different homeserver.

### Question 2: Matrix User ID
```
Matrix User ID [@rabit232:envs.net]:
```

**What to do:** Just press **Enter** to use the default, or type your user ID.

### Question 3: Matrix Access Token
```
To get your access token:
1. Go to https://app.element.io
2. Log in with your Matrix account
3. Settings → Help & About → Access Token

Matrix Access Token:
```

**What to do:** 
1. Open https://app.element.io in your browser
2. Log in
3. Click your profile picture (top left)
4. Click **Settings**
5. Click **Help & About**
6. Scroll down and click **Access Token**
7. Copy the token
8. Paste it here and press Enter

### Question 4: Device ID (Optional)
```
Matrix Device ID (optional, press Enter to skip):
```

**What to do:** Just press **Enter** to skip.

### Questions 5-7: API Keys (Optional)
```
Optional API keys (press Enter to skip):
Jina API Key (for web search):
OpenAI API Key (for DALL-E):
Stability API Key (for Stable Diffusion):
```

**What to do:** Press **Enter** for each one to skip (unless you have these API keys).

### Success Message:
```
✅ .env file created successfully!

To use these credentials, run:
  source .env
  export $(cat .env | xargs)
  python3 -m ribit_2_0.enhanced_autonomous_matrix_bot

Or use the run script:
  ./run_bot.sh
```

---

## Step 5: Run the Bot

Now that credentials are set up, run the bot:

### Option A: Using `./` (Recommended)

```bash
./run_bot.sh
```

### Option B: Using `bash`

If Option A doesn't work:

```bash
bash run_bot.sh
```

### What You'll See:

```
========================================
  Ribit 2.0 - Starting Bot
========================================

Loading credentials from .env...
✓ Credentials loaded
  Homeserver: https://matrix.envs.net
  User ID: @rabit232:envs.net

Which bot would you like to run?
1. Enhanced Autonomous Bot (recommended)
2. Secure E2EE Bot
3. Basic Matrix Bot

Choice [1]:
```

**What to do:** Type **1** and press Enter (or just press Enter for default).

### Bot Starting:

```
Starting bot...

INFO:__main__:Ribit 2.0 Enhanced Autonomous Matrix Bot
INFO:__main__:Connecting to https://matrix.envs.net
INFO:__main__:Logged in as @rabit232:envs.net
INFO:__main__:Listening for messages...
```

**Success!** The bot is now running! 🎉

---

## Troubleshooting

### Problem: "Permission denied"

**Error:**
```
bash: ./setup_credentials.sh: Permission denied
```

**Solution:**

Make the script executable:

```bash
chmod +x setup_credentials.sh
chmod +x run_bot.sh
```

Then try again:

```bash
./setup_credentials.sh
```

### Problem: "No such file or directory"

**Error:**
```
bash: ./setup_credentials.sh: No such file or directory
```

**Solution:**

Make sure you're in the right directory:

```bash
cd ~/ribit.2.0
ls -la *.sh
```

You should see:
```
-rwxr-xr-x 1 rabit232 rabit232 2500 Oct 11 20:58 setup_credentials.sh
-rwxr-xr-x 1 rabit232 rabit232 1900 Oct 11 20:58 run_bot.sh
```

If you don't see these files, you may need to pull the latest changes:

```bash
git pull origin master
```

### Problem: Script doesn't work with `./`

**Solution:**

Use `bash` instead:

```bash
bash setup_credentials.sh
bash run_bot.sh
```

### Problem: "MATRIX_USER_ID and MATRIX_ACCESS_TOKEN must be set"

**Solution:**

The `.env` file wasn't loaded. Use the run script:

```bash
./run_bot.sh
```

Or load manually:

```bash
export $(cat .env | grep -v '^#' | xargs)
python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
```

---

## Quick Reference Card

### Complete Setup (First Time)

```bash
# 1. Go to directory
cd ~/ribit.2.0

# 2. Make scripts executable (if needed)
chmod +x setup_credentials.sh run_bot.sh

# 3. Run setup
./setup_credentials.sh

# 4. Run bot
./run_bot.sh
```

### Running Bot (After Setup)

```bash
# Go to directory
cd ~/ribit.2.0

# Run bot
./run_bot.sh
```

### Stopping the Bot

Press **Ctrl + C** in the terminal where the bot is running.

---

## Alternative: Manual Method

If the scripts don't work, you can do it manually:

### 1. Create .env file

```bash
cd ~/ribit.2.0
nano .env
```

### 2. Add credentials

Type this (replace with your actual token):

```
MATRIX_HOMESERVER=https://matrix.envs.net
MATRIX_USER_ID=@rabit232:envs.net
MATRIX_ACCESS_TOKEN=your_actual_token_here
```

Press **Ctrl + X**, then **Y**, then **Enter** to save.

### 3. Load credentials

```bash
export $(cat .env | grep -v '^#' | xargs)
```

### 4. Run bot

```bash
python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
```

---

## Video Tutorial (Text Version)

### Part 1: Setup (First Time Only)

```
Terminal Commands:
┌─────────────────────────────────────────────────┐
│ $ cd ~/ribit.2.0                                │
│ $ ./setup_credentials.sh                        │
│                                                 │
│ [Answer the questions]                          │
│                                                 │
│ Matrix Homeserver: [press Enter]               │
│ Matrix User ID: [press Enter]                  │
│ Matrix Access Token: [paste token, press Enter]│
│ Device ID: [press Enter]                        │
│ API keys: [press Enter for each]               │
│                                                 │
│ ✅ .env file created successfully!             │
└─────────────────────────────────────────────────┘
```

### Part 2: Running Bot (Every Time)

```
Terminal Commands:
┌─────────────────────────────────────────────────┐
│ $ cd ~/ribit.2.0                                │
│ $ ./run_bot.sh                                  │
│                                                 │
│ Which bot would you like to run?               │
│ 1. Enhanced Autonomous Bot (recommended)        │
│ 2. Secure E2EE Bot                              │
│ 3. Basic Matrix Bot                             │
│                                                 │
│ Choice [1]: 1                                   │
│                                                 │
│ Starting bot...                                 │
│ ✓ Bot is running!                               │
└─────────────────────────────────────────────────┘
```

---

## Summary

**To run the scripts:**

1. Open terminal
2. `cd ~/ribit.2.0`
3. `./setup_credentials.sh` (first time only)
4. `./run_bot.sh` (every time)

**That's it!** 🚀

---

## Need More Help?

- **Full installation guide**: See `INSTALL.md`
- **Credentials guide**: See `CREDENTIALS_SETUP.md`
- **Quick start**: See `QUICK_START.md`
- **GitHub issues**: https://github.com/rabit232/ribit.2.0/issues

---

**Happy chatting with Ribit! 🤖✨**

