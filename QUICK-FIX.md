# 🚨 QUICK FIX for Matrix Connection Issues

## Your Current Errors

```
❌ MATRIX_USERNAME: @ribit.matrix.envs.net  (WRONG FORMAT!)
❌ ERROR: M_FORBIDDEN Invalid username or password
❌ Knowledge not found for key: identity
```

---

## 🔧 3-Step Fix

### **Step 1: Edit .env File**

```bash
cd ~/ribit.2.0
nano .env
```

### **Step 2: Fix These 3 Lines**

**Change FROM:**
```env
MATRIX_HOMESERVER=https://matrix.envs.net
MATRIX_USERNAME=@ribit.matrix.envs.net
MATRIX_PASSWORD=your_password_here
```

**Change TO:**
```env
MATRIX_HOMESERVER=https://envs.net
MATRIX_USERNAME=@ribit:envs.net
MATRIX_PASSWORD=your_actual_password
```

**⚠️ CRITICAL:** Use **COLON** (`:`) not **PERIOD** (`.`) in username!

### **Step 3: Pull Knowledge Base & Restart**

```bash
git pull origin master
python3 run_matrix_bot.py
```

---

## 🎯 The Key Fixes

| Issue | Wrong | Correct |
|-------|-------|---------|
| **Username Format** | `@ribit.matrix.envs.net` | `@ribit:envs.net` |
| **Homeserver URL** | `https://matrix.envs.net` | `https://envs.net` |
| **Password** | Must be your actual bot password | Not "your_password_here" |

---

## 📋 Quick Check

After editing `.env`, verify:

```bash
cat .env | grep MATRIX_
```

Should show:
```
MATRIX_HOMESERVER=https://envs.net
MATRIX_USERNAME=@ribit:envs.net
MATRIX_PASSWORD=[your actual password]
```

---

## ✅ Expected Success Output

```
✅ Logged in successfully
🔄 Starting sync loop...
INFO:ribit_2_0.knowledge_base:Retrieved knowledge: [identity]
INFO:ribit_2_0.knowledge_base:Retrieved knowledge: [purpose]
```

---

## 🆘 Still Having Issues?

### **Issue: "Invalid username or password"**

**Possible causes:**
1. Password is wrong
2. Username format is still wrong (check for periods!)
3. Bot account doesn't exist on the homeserver

**Solution:**
- Verify bot account exists at https://envs.net
- Double-check password (no typos)
- Ensure username uses colon: `@ribit:envs.net`

### **Issue: "Knowledge not found"**

**Solution:**
```bash
cd ~/ribit.2.0
git pull origin master
ls -la ribit_matrix_knowledge.txt  # Should exist
```

---

## 🤖 Matrix Username Format Rules

```
@username:homeserver.domain
 │    │   │         │
 │    │   │         └─ Domain (.net, .org, .com)
 │    │   └─────────── Homeserver name
 │    └───────────────── COLON (not period!)
 └────────────────────── @ symbol
```

**✅ Correct Examples:**
- `@ribit:envs.net`
- `@alice:matrix.org`
- `@bob:matrix.envs.net`

**❌ Wrong Examples:**
- `@ribit.matrix.envs.net` (periods instead of colon)
- `ribit:envs.net` (missing @)
- `@ribit@envs.net` (@ instead of colon)

---

## 🚀 One-Line Fix Command

```bash
cd ~/ribit.2.0 && nano .env
```

Then change the 3 lines shown above, save (Ctrl+X, Y, Enter), and run:

```bash
git pull && python3 run_matrix_bot.py
```

---

## 📞 Need More Help?

See full documentation:
- `ribit-matrix-connection-fix.md` - Detailed troubleshooting
- `ribit-troubleshooting-and-commands.md` - Commands guide
- `ribit-2-0-ubuntu-install-guide.md` - Installation guide

---

**Remember:** The most common mistake is using **periods** instead of **colon** in the username!

```
❌ @ribit.matrix.envs.net
✅ @ribit:envs.net
```

**Welcome, human.** Fix these three things and Ribit will connect! 🤖✨

