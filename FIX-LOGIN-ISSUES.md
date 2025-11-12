# 🚨 FIX: Matrix Login Issues

## Your Current Error

```
ERROR: M_FORBIDDEN Invalid username or password
```

This error appears even though your username looks correct (`@ribit:envs.net`). The issue is that your **homeserver URL is still wrong**.

---

## The Problem

Looking at your output:

```
✅ MATRIX_HOMESERVER: https://matrix.envs.net  ← WRONG!
✅ MATRIX_USERNAME: @ribit:envs.net            ← CORRECT!
```

**The homeserver URL still has "matrix." in it!**

---

## The Solution

### **Step 1: Edit Your .env File**

```bash
cd ~/ribit.2.0
nano .env
```

### **Step 2: Find and Change This Line**

**Find:**
```env
MATRIX_HOMESERVER=https://matrix.envs.net
```

**Change to:**
```env
MATRIX_HOMESERVER=https://envs.net
```

**Remove the "matrix." part!**

### **Step 3: Verify Your Password**

While you're editing, also make sure your password is correct:

```env
MATRIX_PASSWORD=your_actual_bot_password
```

**NOT** the placeholder `your_password_here`!

### **Step 4: Save and Restart**

```bash
# Save the file (Ctrl+X, Y, Enter)

# Validate your configuration
python3 validate-env.py

# If validation passes, start the bot
python3 run_matrix_bot.py
```

---

## Complete Correct Configuration

Your `.env` file should look like this:

```env
# Matrix Server Settings
MATRIX_HOMESERVER=https://envs.net
MATRIX_USERNAME=@ribit:envs.net
MATRIX_PASSWORD=YourActualPassword123

# Optional: Authorized Users
AUTHORIZED_USERS=@rabit232:envs.net,@rabit232:envs.net

# Optional: Bot Configuration
BOT_NAME=ribit.2.0
SYNC_TIMEOUT=30000
REQUEST_TIMEOUT=10000
KEEPALIVE_INTERVAL=60

# Optional: Feature Toggles
ENABLE_SYSTEM_COMMANDS=true
ENABLE_TERMINATOR_MODE=true
```

---

## Why This Matters

Matrix homeserver URLs should be the **base domain** only:

| Homeserver | Correct URL | Wrong URL |
|------------|-------------|-----------|
| envs.net | `https://envs.net` | ~~`https://matrix.envs.net`~~ |
| matrix.org | `https://matrix.org` | ~~`https://matrix.org`~~ |
| matrix.envs.net | `https://envs.net` | *(this one actually uses matrix. prefix)* |

**For envs.net specifically:** The correct URL is `https://envs.net` **without** the "matrix." prefix.

---

## Validation Tool

Use the validator to check your configuration:

```bash
cd ~/ribit.2.0
python3 validate-env.py
```

This will:
- ✅ Check your homeserver URL
- ✅ Check your username format
- ✅ Check your password
- ✅ Identify any issues
- ✅ Tell you exactly what to fix

---

## Expected Output After Fix

```
🤖 Ribit 2.0 Matrix Bot Launcher
==================================================
✅ Found .env file, loading configuration...
✅ MATRIX_HOMESERVER: https://envs.net          ← Fixed!
✅ MATRIX_USERNAME: @ribit:envs.net
✅ MATRIX_PASSWORD: **********

🚀 Starting Ribit 2.0 Matrix Bot...
📡 Homeserver: https://envs.net                 ← Fixed!
👤 Username: @ribit:envs.net
🔐 Authorized users: 2

INFO:ribit_2_0.matrix_bot:✅ Logged in successfully  ← Success!
INFO:ribit_2_0.matrix_bot:🔄 Starting sync loop...
```

---

## If You Still Get "Invalid Password"

After fixing the homeserver URL, if you still get the error:

### **Option 1: Reset Your Bot Password**

1. Go to https://envs.net
2. Log in with your bot account
3. Go to Settings → Security
4. Change password
5. Update `.env` with new password

### **Option 2: Create a New Bot Account**

1. Go to https://envs.net
2. Register a new account (e.g., `ribit2`)
3. Remember the password!
4. Update `.env`:
   ```env
   MATRIX_USERNAME=@ribit2:envs.net
   MATRIX_PASSWORD=NewPassword123
   ```

### **Option 3: Verify Account Exists**

Make sure your bot account actually exists on envs.net:

1. Try logging in manually at https://envs.net
2. Use username: `ribit` (without @ or :envs.net)
3. Use your password
4. If login fails, the account doesn't exist or password is wrong

---

## Quick Reference

### **Correct Format:**
```env
MATRIX_HOMESERVER=https://envs.net
MATRIX_USERNAME=@ribit:envs.net
MATRIX_PASSWORD=ActualPassword
```

### **Wrong Format:**
```env
MATRIX_HOMESERVER=https://matrix.envs.net     ← Remove "matrix."!
MATRIX_USERNAME=@ribit.matrix.envs.net        ← Use colon, not periods!
MATRIX_PASSWORD=your_password_here            ← Use actual password!
```

---

## Tools to Help You

### **1. Configuration Validator**
```bash
python3 validate-env.py
```
Checks your `.env` and tells you exactly what's wrong.

### **2. Configuration Template**
```bash
cp .env.template .env
nano .env
```
Start with a clean template with instructions.

### **3. Interactive Fix Script**
```bash
./fix-ribit-env.sh
```
Guides you through fixing common issues.

---

## Summary

**The ONE change you need:**

```diff
- MATRIX_HOMESERVER=https://matrix.envs.net
+ MATRIX_HOMESERVER=https://envs.net
```

**Remove "matrix." from the homeserver URL!**

And make sure your password is correct (not the placeholder).

---

**That's it!** Make this one change and Ribit should connect successfully! 🤖✨
