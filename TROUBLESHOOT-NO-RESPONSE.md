# 🔍 Troubleshooting: Bot Not Responding

## Your Situation

✅ **Bot is running** - You see the startup banner  
✅ **Bot is connected** - No connection errors  
❌ **Bot doesn't respond** - No replies to messages or mentions

---

## Important Notice: You're Running as YOUR Account!

Looking at your output:

```
👤 Username: @rabit232:envs.net
```

**This is YOUR personal account, not a bot account!**

### **The Problem:**

When you run Ribit using your personal account (@rabit233), the bot:
- Will skip messages from @rabit233 (because it thinks they're its own messages)
- Won't respond to your messages in rooms
- Will only respond to messages from OTHER users

### **The Solution:**

You need to create a **separate bot account** and run Ribit with that account.

---

## How to Fix: Create a Bot Account

### **Step 1: Register a New Bot Account**

1. Go to https://matrix.envs.net (or your homeserver)
2. Click "Create Account" or "Register"
3. Choose a bot username, e.g.:
   - `ribit`
   - `ribit2`
   - `ribit-bot`
4. Set a password and remember it!
5. Complete registration

### **Step 2: Update Your .env File**

```bash
cd ~/ribit.2.0
nano .env
```

**Change:**
```env
MATRIX_USERNAME=@rabit232:envs.net
MATRIX_PASSWORD=your_personal_password
```

**To:**
```env
MATRIX_USERNAME=@ribit:matrix.envs.net
MATRIX_PASSWORD=your_bot_password
```

### **Step 3: Update Authorized Users**

Make sure YOUR account is in the authorized users list:

```env
AUTHORIZED_USERS=@rabit232:envs.net,@rabit232:envs.net
```

**Note:** Remove any empty entries (the blank line you have)

### **Step 4: Restart the Bot**

```bash
python3 run_matrix_bot.py
```

### **Step 5: Invite the Bot to Your Room**

1. In your Matrix client, go to the room
2. Click "Invite"
3. Enter: `@ribit:matrix.envs.net` (your bot's username)
4. The bot should auto-join and send a welcome message

### **Step 6: Test**

Send a message in the room:
```
ribit.2.0 hello
```

The bot should now respond!

---

## Alternative: Test with Another User

If you want to keep running as @rabit233 for testing:

1. Ask someone else to join the room
2. Have THEM send: `ribit.2.0 hello`
3. The bot will respond to them (but not to you)

**Why?** Because the bot thinks @rabit233 is itself and ignores those messages.

---

## Message Triggering Rules

The bot responds when messages contain:

✅ **Triggers that work:**
- `ribit.2.0` (exact bot name)
- `ribit` (keyword)
- `?help` (command)
- `!reset` (reset command)

✅ **Examples that work:**
```
ribit.2.0 hello
Hey ribit, how are you?
ribit what's the weather?
?help
!reset
```

❌ **Examples that DON'T work:**
```
hello (no trigger word)
how are you? (no trigger word)
@ribit.2.0 (Matrix mention - bot looks for text, not mentions)
```

---

## Checking if Bot Sees Messages

### **Method 1: Check Terminal Output**

When someone sends a message, you should see in the terminal:

```
INFO:ribit_2_0.matrix_bot:Processing message from @username:server.com
```

If you DON'T see this, the bot isn't receiving messages.

### **Method 2: Enable Debug Logging**

Edit `run_matrix_bot.py` and change:

```python
logging.basicConfig(level=logging.INFO)
```

To:

```python
logging.basicConfig(level=logging.DEBUG)
```

Restart the bot and you'll see detailed message processing.

---

## Common Issues

### **Issue 1: Bot Running as Your Account**

**Symptom:** Bot doesn't respond to YOUR messages  
**Cause:** Bot skips messages from its own user ID  
**Solution:** Create a separate bot account

### **Issue 2: Bot Not in Room**

**Symptom:** No responses from anyone  
**Cause:** Bot hasn't joined the room  
**Solution:** Check "Joined Rooms: 0" in startup - invite bot to room

### **Issue 3: Wrong Trigger Word**

**Symptom:** Bot ignores messages  
**Cause:** Messages don't contain trigger words  
**Solution:** Include "ribit.2.0" or "ribit" in messages

### **Issue 4: Matrix Mentions Not Working**

**Symptom:** @ribit.2.0 doesn't trigger bot  
**Cause:** Bot looks for text, not Matrix mention events  
**Solution:** Type "ribit.2.0" as text, not as a mention

### **Issue 5: Empty Authorized User**

**Symptom:** Authorization issues  
**Cause:** Empty string in authorized users list  
**Solution:** Fix the authorized users line:

```env
# Wrong (has empty entry)
AUTHORIZED_USERS=@rabit232:envs.net,,@rabit232:envs.net

# Correct
AUTHORIZED_USERS=@rabit232:envs.net,@rabit232:envs.net
```

---

## Testing Checklist

- [ ] Bot is running (no errors in terminal)
- [ ] Bot is using a SEPARATE account (not your personal account)
- [ ] Bot has joined the room (check "Joined Rooms" count)
- [ ] Messages include trigger word ("ribit.2.0" or "ribit")
- [ ] Messages are from a DIFFERENT user than the bot account
- [ ] No errors in terminal when message is sent
- [ ] Terminal shows "Processing message from..." when triggered

---

## Quick Test Script

Run this to test if message triggering logic works:

```bash
cd ~/ribit.2.0
python3 test-message-trigger.py
```

This will show you which messages would trigger the bot.

---

## Recommended Configuration

### **Correct .env for Bot Account:**

```env
# Bot account (separate from your personal account)
MATRIX_HOMESERVER=https://matrix.envs.net
MATRIX_USERNAME=@ribit:matrix.envs.net
MATRIX_PASSWORD=bot_account_password

# Your personal account is authorized to use commands
AUTHORIZED_USERS=@rabit232:envs.net,@rabit232:envs.net

# Bot configuration
BOT_NAME=ribit.2.0
SYNC_TIMEOUT=30000
REQUEST_TIMEOUT=10000
KEEPALIVE_INTERVAL=60
```

---

## Debug Commands

### **Check Bot Status**

While bot is running, send (from another account):

```
?status
```

Should show bot capabilities and status.

### **Check System Status** (if authorized)

```
?sys
```

Shows system resources.

### **Get Help**

```
?help
```

Shows available commands.

---

## Summary

**Main Issue:** You're running the bot as your personal account (@rabit233)

**Solution:**
1. Create a new bot account (e.g., @ribit:matrix.envs.net)
2. Update .env with bot account credentials
3. Keep your personal account in AUTHORIZED_USERS
4. Restart bot
5. Invite bot to room
6. Test from your personal account: "ribit.2.0 hello"

**The bot will now respond to YOUR messages because you're messaging from @rabit233 to @ribit!**

---

## Still Not Working?

If the bot still doesn't respond after creating a separate bot account:

1. **Check terminal for errors** when you send a message
2. **Enable debug logging** (see above)
3. **Verify bot is in the room** - Check "Joined Rooms" count
4. **Try the test script** - `python3 test-message-trigger.py`
5. **Check message format** - Must include "ribit.2.0" or "ribit"

---

**Welcome, human.** Create that bot account and Ribit will respond! 🤖✨

