# Setting Ribit's Avatar - Robot Girl 🤖👧

Ribit now has a cute robot girl avatar from Giphy!

![Robot Girl](ribit_avatar.gif)

---

## 🎨 Quick Setup

### Automatic (Easiest)

```bash
cd ~/ribit.2.0
python3 set_avatar.py
```

That's it! The script will:
1. ✅ Load your Matrix credentials from .env
2. ✅ Upload the robot girl GIF
3. ✅ Set it as Ribit's profile picture

---

## 📋 Manual Setup

If you prefer to set the avatar manually:

### Step 1: Get the Avatar

The avatar is already downloaded: `ribit_avatar.gif`

Or download again:
```bash
wget "https://media.giphy.com/media/6F4TGyw69QRvVrHgRC/giphy.gif" -O ribit_avatar.gif
```

### Step 2: Upload to Matrix

Using Element Web:
1. Go to https://app.element.io
2. Log in as Ribit (@rabit232:envs.net)
3. Click profile (top left)
4. Settings → General
5. Click avatar circle
6. Upload `ribit_avatar.gif`
7. Save

---

## 🔧 Troubleshooting

### Issue: Credentials Not Found

**Error:** `❌ MATRIX_ACCESS_TOKEN not set!`

**Solution:**

```bash
# Option 1: Set environment variable
export MATRIX_ACCESS_TOKEN='your_token_here'
python3 set_avatar.py

# Option 2: Create/update .env file
echo "MATRIX_ACCESS_TOKEN=your_token_here" >> .env
python3 set_avatar.py
```

### Issue: Avatar File Not Found

**Error:** `❌ Avatar file not found`

**Solution:**

```bash
cd ~/ribit.2.0
wget "https://media.giphy.com/media/6F4TGyw69QRvVrHgRC/giphy.gif" -O ribit_avatar.gif
python3 set_avatar.py
```

### Issue: Upload Failed

**Error:** `❌ Upload failed`

**Possible causes:**
1. Invalid access token
2. Network issues
3. File too large
4. Homeserver issues

**Solutions:**

```bash
# Check token is valid
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://matrix.envs.net/_matrix/client/r0/account/whoami

# Check file size (should be <1MB)
ls -lh ribit_avatar.gif

# Try again
python3 set_avatar.py
```

---

## 📊 Avatar Details

| Property | Value |
|----------|-------|
| **Source** | https://giphy.com/stickers/kiwibot-robot-girl-robotic-kiwibot-6F4TGyw69QRvVrHgRC |
| **Format** | Animated GIF |
| **Size** | 944 KB |
| **Dimensions** | 480x480 pixels |
| **File** | `ribit_avatar.gif` |
| **Character** | Cute robot girl |

---

## 🎯 What It Does

The `set_avatar.py` script:

1. **Loads Credentials**
   - Reads from environment variables
   - Or reads from .env file
   - Validates credentials

2. **Uploads Avatar**
   - Reads `ribit_avatar.gif`
   - Uploads to Matrix homeserver
   - Gets MXC URL

3. **Sets Profile Picture**
   - Calls Matrix API
   - Sets avatar for Ribit's account
   - Confirms success

---

## 💻 Script Usage

### Basic

```bash
python3 set_avatar.py
```

### With Custom Credentials

```bash
export MATRIX_HOMESERVER="https://matrix.envs.net"
export MATRIX_USER_ID="@rabit232:envs.net"
export MATRIX_ACCESS_TOKEN="your_token"
python3 set_avatar.py
```

### With Custom Avatar

```bash
# Download different avatar
wget "https://example.com/avatar.gif" -O ribit_avatar.gif

# Set it
python3 set_avatar.py
```

---

## 🔍 Verification

After setting the avatar, verify it worked:

### Method 1: Element Web

1. Go to https://app.element.io
2. Search for @rabit232:envs.net
3. Check profile picture

### Method 2: Matrix API

```bash
curl https://matrix.envs.net/_matrix/client/r0/profile/@rabit232:envs.net/avatar_url
```

Should return:
```json
{
  "avatar_url": "mxc://matrix.envs.net/..."
}
```

### Method 3: Start Ribit

```bash
./run_bot.sh
```

Join a room with Ribit and check its avatar!

---

## 🎨 Changing Avatar Later

To change Ribit's avatar:

1. **Download new avatar:**
   ```bash
   wget "URL_TO_NEW_AVATAR" -O ribit_avatar.gif
   ```

2. **Set it:**
   ```bash
   python3 set_avatar.py
   ```

Or edit `set_avatar.py` to use a different file.

---

## 📝 Notes

- Avatar is animated GIF (Matrix supports this!)
- File size should be <1MB for best performance
- Recommended dimensions: 256x256 to 512x512
- Animated avatars work in Element and most Matrix clients
- Avatar is stored on homeserver, not locally

---

## 🤖 Why This Avatar?

The robot girl avatar represents:
- 🤖 Ribit's AI nature
- 👧 Friendly, approachable personality
- ✨ Cute and engaging character
- 🎨 Visual identity for Ribit

Perfect for a chatbot with personality!

---

## 📦 Files

- `ribit_avatar.gif` - The avatar image
- `set_avatar.py` - Avatar setting script
- `AVATAR_SETUP.md` - This guide

---

## 🚀 Quick Reference

**Set avatar:**
```bash
python3 set_avatar.py
```

**Download avatar:**
```bash
wget "https://media.giphy.com/media/6F4TGyw69QRvVrHgRC/giphy.gif" -O ribit_avatar.gif
```

**Verify avatar:**
```bash
curl https://matrix.envs.net/_matrix/client/r0/profile/@rabit232:envs.net/avatar_url
```

---

**Repository:** https://github.com/rabit232/ribit.2.0

**Avatar ready! Ribit now has a face! 🤖👧✨**

