# Fix Missing Packages - Quick Guide

## Problem

You see an error like:
```
✗ Web Scraping & Wikipedia: ✗ Import error: No module named 'wikipediaapi'
```

Or:
```
ModuleNotFoundError: No module named 'wikipediaapi'
ModuleNotFoundError: No module named 'nio'
ModuleNotFoundError: No module named 'aiohttp'
```

## Solution

### Quick Fix (One Command)

```bash
cd ~/ribit.2.0
./fix_missing_packages.sh
```

This will:
1. ✅ Check all required Python packages
2. ✅ Install any missing packages
3. ✅ Verify all modules work
4. ✅ Show you the results

---

## Manual Fix

If the script doesn't work, install packages manually:

### Install All Packages

```bash
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

### Or Install from requirements.txt

```bash
cd ~/ribit.2.0
pip3 install -r requirements.txt
```

### Install Specific Missing Package

If only one package is missing:

```bash
# For wikipediaapi
pip3 install wikipedia-api

# For matrix-nio
pip3 install 'matrix-nio[e2e]'

# For aiohttp
pip3 install aiohttp

# For beautifulsoup4
pip3 install beautifulsoup4

# For lxml
pip3 install lxml

# For Pillow
pip3 install Pillow

# For python-magic
pip3 install python-magic

# For aiofiles
pip3 install aiofiles
```

---

## Verify Installation

After installing packages:

```bash
cd ~/ribit.2.0
python3 verify_modules.py
```

You should see:
```
✓ Web Scraping & Wikipedia
...
Results: 14 passed, 0 failed
✅ ALL MODULES VERIFIED!
```

---

## Common Issues

### Issue: pip3 not found

**Solution:**
```bash
sudo apt update
sudo apt install -y python3-pip
```

### Issue: Permission denied

**Solution:**
```bash
pip3 install --user wikipedia-api
```

Or with sudo:
```bash
sudo pip3 install wikipedia-api
```

### Issue: Package installs but import still fails

**Solution:**
```bash
# Check Python version
python3 --version

# Check where pip installs packages
pip3 show wikipediaapi

# Make sure you're using the right Python
which python3

# Try force reinstall
pip3 install --force-reinstall wikipedia-api
```

### Issue: Multiple Python versions

**Solution:**
```bash
# Use python3.11 specifically (or your version)
python3.11 -m pip install wikipedia-api

# Then use that Python to run Ribit
python3.11 -m ribit_2_0.enhanced_autonomous_matrix_bot
```

---

## What Packages Are Required?

| Package | Purpose | Import Name |
|---------|---------|-------------|
| matrix-nio[e2e] | Matrix client with encryption | nio |
| aiohttp | Async HTTP requests | aiohttp |
| requests | HTTP requests | requests |
| beautifulsoup4 | HTML parsing | bs4 |
| lxml | XML/HTML parser | lxml |
| wikipedia-api | Wikipedia integration | wikipediaapi |
| Pillow | Image processing | PIL |
| python-magic | File type detection | magic |
| aiofiles | Async file operations | aiofiles |

---

## After Fixing

Once all packages are installed:

```bash
cd ~/ribit.2.0
python3 verify_modules.py
```

Should show:
```
Results: 14 passed, 0 failed
✅ ALL MODULES VERIFIED!
```

Then you can run Ribit:
```bash
./run_bot.sh
```

---

## Prevention

To avoid this issue in the future:

### 1. Use Virtual Environment

```bash
cd ~/ribit.2.0
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Always Install from requirements.txt

```bash
cd ~/ribit.2.0
pip3 install -r requirements.txt
```

### 3. Use the Install Script

```bash
cd ~/ribit.2.0
./install.sh
```

This automatically installs all dependencies.

---

## Quick Reference

**Fix missing packages:**
```bash
./fix_missing_packages.sh
```

**Install all packages:**
```bash
pip3 install -r requirements.txt
```

**Verify installation:**
```bash
python3 verify_modules.py
```

**Run Ribit:**
```bash
./run_bot.sh
```

---

**Repository:** https://github.com/rabit232/ribit.2.0

