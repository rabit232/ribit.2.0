# Ribit 2.0 - Credentials Setup Guide

Quick guide to set up Matrix credentials and run Ribit 2.0.

---

## Quick Setup (Recommended)

### Option 1: Interactive Setup Script

```bash
./setup_credentials.sh
```

This script will:
- Ask for your Matrix homeserver
- Ask for your Matrix user ID
- Ask for your access token
- Optionally ask for API keys
- Create a `.env` file with your credentials

### Option 2: Manual .env File

Create a file named `.env` in the `ribit.2.0` directory:

```bash
nano .env
```

Add your credentials:

```bash
# Matrix Configuration (Required)
MATRIX_HOMESERVER=https://matrix.envs.net
MATRIX_USER_ID=@rabit232:envs.net
MATRIX_ACCESS_TOKEN=your_access_token_here

# Optional: Device ID
MATRIX_DEVICE_ID=your_device_id

# Optional: Web Search
JINA_API_KEY=your_jina_key

# Optional: Image Generation
OPENAI_API_KEY=your_openai_key
STABILITY_API_KEY=your_stability_key
```

---

## Getting Your Access Token

### Method 1: Using Element Web (Easiest)

1. Go to https://app.element.io
2. Log in with your Matrix account
3. Click your profile picture (top left)
4. Click **Settings**
5. Click **Help & About**
6. Scroll down to **Advanced**
7. Click **Access Token** to reveal it
8. Copy the token

### Method 2: Using curl

```bash
curl -X POST https://matrix.envs.net/_matrix/client/r0/login \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "m.login.password",
    "user": "rabit233",
    "password": "YOUR_PASSWORD"
  }'
```

The response will contain your `access_token`:

```json
{
  "user_id": "@rabit232:envs.net",
  "access_token": "syt_...",
  "device_id": "ABCDEFGH"
}
```

Copy the `access_token` value.

---

## Running the Bot

### Option 1: Using run_bot.sh (Easiest)

```bash
./run_bot.sh
```

This script will:
- Load credentials from `.env`
- Ask which bot to run
- Start the bot

### Option 2: Manual with Environment Variables

**Load .env file:**

```bash
export $(cat .env | grep -v '^#' | xargs)
```

**Run the bot:**

```bash
# Enhanced Autonomous Bot (recommended)
python3 -m ribit_2_0.enhanced_autonomous_matrix_bot

# Or Secure E2EE Bot
python3 run_secure_ribit.py

# Or Basic Matrix Bot
python3 -m ribit_2_0.matrix_bot
```

### Option 3: Direct Export

```bash
export MATRIX_HOMESERVER="https://matrix.envs.net"
export MATRIX_USER_ID="@rabit232:envs.net"
export MATRIX_ACCESS_TOKEN="your_token_here"

python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
```

---

## Troubleshooting

### Error: "MATRIX_USER_ID and MATRIX_ACCESS_TOKEN must be set"

**Solution:**

1. Make sure you have a `.env` file with your credentials
2. Load the `.env` file before running:
   ```bash
   export $(cat .env | grep -v '^#' | xargs)
   ```
3. Or use the `run_bot.sh` script which does this automatically

### Error: "MATRIX_PASSWORD environment variable required"

This error appears when using `run_secure_ribit.py` which requires a password instead of an access token.

**Solution:**

Either:

1. **Use the enhanced autonomous bot instead** (recommended):
   ```bash
   python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
   ```

2. **Or set MATRIX_PASSWORD**:
   ```bash
   export MATRIX_PASSWORD="your_matrix_password"
   python3 run_secure_ribit.py
   ```

### ROS Warning: "No ROS installation detected"

This is **harmless**. Ribit will use a mock ROS interface.

If you want to use real ROS:

```bash
# For Ubuntu 22.04
sudo apt install ros-humble-desktop
source /opt/ros/humble/setup.bash
```

But this is **optional** - Ribit works fine without ROS.

### Cannot connect to homeserver

**Check homeserver is accessible:**

```bash
curl https://matrix.envs.net/_matrix/client/versions
```

**Try a different homeserver:**

```bash
export MATRIX_HOMESERVER="https://matrix.org"
```

### Invalid access token

Your access token may have expired. Get a new one:

1. Log out and log back in to Element
2. Get a new access token
3. Update your `.env` file

---

## Account Recommendations

### Recommended Account

- **Homeserver**: https://matrix.envs.net
- **Username**: rabit233
- **User ID**: @rabit232:envs.net

### Alternative Homeservers

If matrix.envs.net is down, you can use:

- https://matrix.org (official homeserver)
- https://envs.net
- https://tchncs.de
- Any other Matrix homeserver

Just update `MATRIX_HOMESERVER` in your `.env` file.

---

## Security Notes

### Protecting Your Access Token

**Important:** Your access token is like a password. Keep it secret!

- ✅ Store in `.env` file (not tracked by git)
- ✅ Never share your access token
- ✅ Never commit `.env` to git
- ✅ Use file permissions: `chmod 600 .env`

**The `.env` file is already in `.gitignore`** so it won't be accidentally committed.

### Revoking Access

If your access token is compromised:

1. Log in to Element
2. Settings → Security & Privacy → Sessions
3. Find the session with your token
4. Click "Sign out"
5. Get a new access token

---

## Quick Reference

### Setup Credentials
```bash
./setup_credentials.sh
```

### Run Bot
```bash
./run_bot.sh
```

### Check Credentials
```bash
cat .env
```

### Test Connection
```bash
export $(cat .env | grep -v '^#' | xargs)
python3 -c "import os; print(f'User: {os.getenv(\"MATRIX_USER_ID\")}')"
```

---

## Example .env File

```bash
# Matrix Configuration
MATRIX_HOMESERVER=https://matrix.envs.net
MATRIX_USER_ID=@rabit232:envs.net
MATRIX_ACCESS_TOKEN=syt_cmFiaXQyMzM_VGhpc0lzQW5FeGFtcGxlVG9rZW4_1234567890

# Optional: Device ID
MATRIX_DEVICE_ID=RIBITDEVICE

# Optional: Web Search (get from https://jina.ai)
JINA_API_KEY=jina_1234567890abcdef

# Optional: Image Generation (get from https://platform.openai.com)
OPENAI_API_KEY=sk-1234567890abcdef

# Optional: Stability AI (get from https://stability.ai)
STABILITY_API_KEY=sk-1234567890abcdef
```

---

## Next Steps

After setting up credentials:

1. **Test the bot**: `./run_bot.sh`
2. **Join a room**: Invite Ribit to a Matrix room
3. **Test commands**: Try `?help`, `?status`, `?tasks`
4. **Explore features**: Check AUTONOMOUS_FEATURES.md

---

## Support

**Need help?**

- Read INSTALL.md for full installation guide
- Check QUICK_START.md for quick start
- Open an issue: https://github.com/rabit232/ribit.2.0/issues

---

**Ready to chat with Ribit! 🤖✨**

