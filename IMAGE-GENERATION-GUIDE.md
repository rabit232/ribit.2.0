# 🎨 AI Image Generation Guide for Ribit 2.0

## Overview

Ribit 2.0 can now generate AI images from text descriptions! Just ask Ribit to create an image, and it will:
1. Open the Perchance AI image generator
2. Input your description
3. Generate the image
4. Upload it to your Matrix room
5. Clean up the file automatically

---

## 🚀 How to Use

### **Simple Commands:**

```
generate image of a sunset over mountains
create image of a cute robot
make picture of a fantasy castle
draw image of a cyberpunk city
ai image of a dragon
```

### **What Ribit Does:**

1. **Acknowledges** your request
   ```
   🎨 Generating image: "a sunset over mountains"
   ⏳ This may take 20-30 seconds...
   ```

2. **Generates** the image using AI
   - Opens Perchance image generator
   - Inputs your description
   - Waits for generation (15-30 seconds)

3. **Uploads** to Matrix room
   - Sends the image directly to your chat
   - Includes your description as caption

4. **Cleans up** automatically
   - Deletes the local file to save space
   - Confirms completion
   ```
   ✨ Image generated and sent!
   ```

---

## 📝 Command Formats

Ribit recognizes these phrases:

### **Generate Commands:**
- `generate image of [description]`
- `generate picture of [description]`
- `generate art of [description]`

### **Create Commands:**
- `create image of [description]`
- `create picture of [description]`
- `create art of [description]`

### **Make Commands:**
- `make image of [description]`
- `make picture of [description]`
- `make art of [description]`

### **Draw Commands:**
- `draw image of [description]`
- `draw picture of [description]`

### **AI Commands:**
- `ai image of [description]`
- `ai art of [description]`

### **Short Commands:**
- `image of [description]`
- `picture of [description]`

---

## 💡 Example Requests

### **Nature & Landscapes:**
```
generate image of a sunset over the ocean
create picture of a mountain lake at dawn
make image of a forest in autumn
```

### **Characters & People:**
```
generate image of a cyberpunk hacker
create picture of a medieval knight
make image of a friendly robot
```

### **Fantasy & Sci-Fi:**
```
generate image of a dragon flying over a castle
create picture of a spaceship in deep space
make image of a magical forest with glowing mushrooms
```

### **Abstract & Artistic:**
```
generate image of abstract geometric patterns
create picture of colorful swirling galaxies
make image of a surreal dreamscape
```

### **Animals:**
```
generate image of a majestic lion
create picture of a cute kitten
make image of a wolf in the snow
```

---

## ⚙️ Technical Details

### **Image Generator:**
- **Service:** Perchance AI Text-to-Image Generator
- **URL:** https://perchance.org/ai-text-to-image-generator
- **Method:** Selenium browser automation
- **Generation Time:** 15-30 seconds typically

### **File Handling:**
- **Download Location:** `~/ribit_generated_images/`
- **Format:** PNG, JPG, or WebP (depending on generator output)
- **Cleanup:** Automatic deletion after upload
- **Old File Cleanup:** Images older than 24 hours are auto-deleted

### **Matrix Integration:**
- **Upload:** Images uploaded to Matrix server
- **Message Type:** `m.image`
- **Caption:** Your original description
- **Metadata:** Includes file size, MIME type, dimensions (if available)

---

## 🔧 Requirements

### **Python Packages:**
```bash
pip install selenium pillow
```

### **System Requirements:**
- Chrome/Chromium browser
- ChromeDriver (installed automatically by Selenium)
- Internet connection

### **Optional:**
- PIL/Pillow for image dimension detection

---

## 🐛 Troubleshooting

### **"Selenium not installed" Error:**
```bash
pip install selenium
```

### **"ChromeDriver not found" Error:**
Selenium should auto-install ChromeDriver, but if it fails:
```bash
# Ubuntu/Debian
sudo apt install chromium-chromedriver

# Or download manually from:
# https://chromedriver.chromium.org/
```

### **"Failed to generate image" Error:**

**Possible causes:**
1. Website changed layout (selectors need updating)
2. Network timeout
3. Browser automation blocked

**Solutions:**
- Check internet connection
- Try again (sometimes the website is slow)
- Check logs for detailed error

### **Image Generated but Not Sent:**

**Possible causes:**
1. Matrix upload failed
2. File permissions issue
3. Network issue

**Solutions:**
- Check Matrix connection
- Verify bot has upload permissions
- Check disk space

---

## 📊 Usage Examples

### **Example 1: Simple Request**
```
You: generate image of a sunset
Ribit: 🎨 Generating image: "a sunset"
       ⏳ This may take 20-30 seconds...
       
       [Image appears in chat]
       
       ✨ Image generated and sent!
```

### **Example 2: Detailed Request**
```
You: create image of a futuristic city with flying cars and neon lights
Ribit: 🎨 Generating image: "a futuristic city with flying cars and neon lights"
       ⏳ This may take 20-30 seconds...
       
       [Image appears in chat]
       
       ✨ Image generated and sent!
```

### **Example 3: Multiple Requests**
```
You: make image of a dragon
Ribit: [Generates dragon image]

You: now make one of a castle
Ribit: [Generates castle image]

You: combine them - dragon flying over castle
Ribit: [Generates combined scene]
```

---

## 🎯 Tips for Better Images

### **Be Specific:**
❌ "a person"
✅ "a medieval knight in shining armor"

### **Add Details:**
❌ "a landscape"
✅ "a mountain landscape at sunset with a lake"

### **Include Style:**
❌ "a robot"
✅ "a cute cartoon robot with big eyes"

### **Use Descriptive Words:**
- Colors: "vibrant", "pastel", "dark", "bright"
- Mood: "peaceful", "dramatic", "mysterious", "cheerful"
- Style: "realistic", "cartoon", "anime", "photorealistic"
- Lighting: "sunset", "moonlight", "neon", "golden hour"

---

## 🔒 Privacy & Storage

### **Local Storage:**
- Images temporarily saved to `~/ribit_generated_images/`
- Automatically deleted after upload
- Old images (24+ hours) cleaned up automatically

### **Matrix Storage:**
- Images uploaded to your Matrix homeserver
- Subject to your homeserver's retention policy
- Accessible to room members

### **No Tracking:**
- Ribit doesn't track what images you generate
- No data sent to third parties (except Perchance for generation)

---

## 🚀 Advanced Usage

### **Batch Generation:**
Currently generates one image at a time. For multiple images:
```
generate image of a cat
generate image of a dog
generate image of a bird
```

### **Custom Styles:**
The Perchance generator has various styles. You can specify:
```
generate photorealistic image of a sunset
create anime-style image of a character
make cartoon image of a robot
```

---

## 📈 Performance

### **Typical Times:**
- Request processing: < 1 second
- Image generation: 15-30 seconds
- Upload to Matrix: 2-5 seconds
- **Total:** ~20-35 seconds

### **Optimization:**
- Headless browser mode (faster, no GUI)
- Automatic cleanup (saves disk space)
- Efficient file handling

---

## 🎉 Summary

**Features:**
- ✅ AI image generation from text
- ✅ Automatic upload to Matrix
- ✅ Auto-cleanup of files
- ✅ Simple natural language commands
- ✅ Multiple command formats
- ✅ Detailed status updates

**Benefits:**
- 🎨 Create custom images on demand
- 💬 Share AI art in your Matrix rooms
- 🚀 Fast and automated
- 🧹 No manual file management
- 🔒 Privacy-focused

**Limitations:**
- ⏱️ Takes 20-30 seconds per image
- 🌐 Requires internet connection
- 🖥️ Requires Chrome/Chromium
- 🎨 Quality depends on Perchance generator

---

**Welcome, human.** Ribit can now create AI art for you! Just describe what you want to see, and Ribit will bring it to life! 🎨🤖✨
