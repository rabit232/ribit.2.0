# Ribit 2.0 - Offline Installation Guide

This guide explains how to install Ribit 2.0 and all its dependencies on systems **without internet access**.

---

## 📦 What's Included

This offline installation package contains:

- **63 Python packages** (~50 MB total)
- All dependencies for Matrix, DeltaChat, HTTP, and image processing
- **Excludes ROS** (install from system packages if needed)

### Included Dependencies:

| Category | Packages |
|:---------|:---------|
| **Matrix Protocol** | matrix-nio[e2e], python-olm, unpaddedbase64, pycryptodome |
| **DeltaChat** | deltachat, imap-tools, peewee |
| **Async HTTP** | aiohttp, aiofiles, aiohappyeyeballs, aiohttp-socks |
| **HTTP & Web** | requests, beautifulsoup4, lxml, httpx, httpcore |
| **Wikipedia** | wikipedia-api |
| **Image Processing** | Pillow, python-magic |
| **Database** | supabase, postgrest, realtime, storage3, supabase-auth |
| **Cryptography** | cryptography, cffi, pycparser |
| **Utilities** | attrs, certifi, charset-normalizer, idna, urllib3, yarl |

---

## 🚀 Quick Start

### On a System WITH Internet (Download Phase)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rabit232/ribit.2.0.git
   cd ribit.2.0
   ```

2. **Download all dependencies**:
   ```bash
   ./download_dependencies.sh
   ```

   This will:
   - Download all 15 core packages + dependencies to `packages/` folder
   - Create a manifest file
   - Take ~2-5 minutes depending on internet speed

3. **Copy to offline system**:
   ```bash
   # Create a tarball
   tar -czf ribit-2.0-offline.tar.gz ribit.2.0/
   
   # Or just copy the whole folder
   cp -r ribit.2.0/ /path/to/usb/drive/
   ```

### On a System WITHOUT Internet (Installation Phase)

1. **Extract the package**:
   ```bash
   tar -xzf ribit-2.0-offline.tar.gz
   cd ribit.2.0/
   ```

2. **Install dependencies**:
   ```bash
   ./install_offline.sh
   ```

   Choose installation method:
   - **Option 1**: System-wide (requires sudo)
   - **Option 2**: User-only (--user flag)
   - **Option 3**: With --break-system-packages (recommended for Debian/Ubuntu)

3. **Set up credentials**:
   ```bash
   python3 setup_credentials.py
   ```

4. **Run the bot**:
   ```bash
   python3 -m ribit_2_0.matrix_bot
   ```

---

## 📋 Detailed Instructions

### Method 1: Standard Offline Installation (Recommended)

This method installs packages using pip from the local cache.

**Advantages**:
- Standard pip installation
- Packages are properly registered
- Easy to update or uninstall

**Steps**:
```bash
# 1. Ensure packages/ folder exists
ls packages/

# 2. Run the installation script
./install_offline.sh

# 3. Choose option 3 (--break-system-packages)
```

---

### Method 2: Vendored Dependencies (Alternative)

This method extracts packages to a `vendor/` folder for direct import.

**Advantages**:
- No pip installation needed
- Portable across systems
- Doesn't modify system Python

**Disadvantages**:
- Only works for pure Python packages
- Binary packages (like cryptography) won't work

**Steps**:
```bash
# 1. Set up vendor folder
python3 setup_vendor.py

# 2. Update ribit_2_0/__init__.py to use vendor
import sys
sys.path.insert(0, 'vendor')
```

---

## 🔧 Manual Installation

If the scripts don't work, you can install manually:

```bash
# Install all packages from local folder
pip3 install \
    --no-index \
    --find-links=packages/ \
    --requirement requirements-offline.txt \
    --break-system-packages
```

---

## 🐛 Troubleshooting

### Error: "packages/ directory not found"

**Solution**: Make sure you copied the entire `ribit.2.0/` folder including the `packages/` subdirectory.

```bash
# Check if packages exist
ls -la packages/
```

---

### Error: "pip3 not found"

**Solution**: Install Python 3 and pip first:

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install python3 python3-pip

# Fedora/RHEL
sudo dnf install python3 python3-pip
```

---

### Error: "externally-managed-environment"

**Solution**: Use one of these options:

1. **Use --break-system-packages** (recommended):
   ```bash
   ./install_offline.sh
   # Choose option 3
   ```

2. **Use --user flag**:
   ```bash
   ./install_offline.sh
   # Choose option 2
   ```

3. **Use a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip3 install --no-index --find-links=packages/ -r requirements-offline.txt
   ```

---

### Some packages fail to install

**Solution**: Check if you're missing system dependencies:

```bash
# For Pillow (image processing)
sudo apt install libjpeg-dev zlib1g-dev

# For cryptography
sudo apt install libssl-dev libffi-dev

# For lxml
sudo apt install libxml2-dev libxslt1-dev
```

---

## 📦 Package Manifest

To see all downloaded packages:

```bash
cat packages/MANIFEST.txt
```

This file contains:
- List of all 15 core packages + dependencies
- Download date
- Platform architecture
- Total package count

---

## 🔄 Updating Dependencies

If you need to update dependencies:

1. **On a system with internet**:
   ```bash
   # Remove old packages
   rm -rf packages/
   
   # Download fresh packages
   ./download_dependencies.sh
   ```

2. **Copy to offline system** and run `./install_offline.sh` again.

---

## 🚫 What's NOT Included

### ROS (Robot Operating System)

ROS is **excluded** because:
- ROS1 and ROS2 are **huge** (several GB)
- Better installed from system packages
- Platform-specific

**To install ROS** (if needed):

```bash
# ROS 1 (Noetic on Ubuntu 20.04)
sudo apt install ros-noetic-desktop-full

# ROS 2 (Humble on Ubuntu 22.04)
sudo apt install ros-humble-desktop
```

### GUI Automation (Optional)

`pyautogui` and `pynput` are commented out in `requirements-offline.txt` because they're optional.

**To include them**:
1. Uncomment in `requirements-offline.txt`
2. Run `./download_dependencies.sh` again

---

## 📊 File Structure

```
ribit.2.0/
├── packages/                    # Downloaded packages (~50 MB)
│   ├── matrix_nio-*.whl
│   ├── deltachat-*.whl
│   ├── aiohttp-*.whl
│   ├── ... (60 more packages)
│   └── MANIFEST.txt            # Package list
├── download_dependencies.sh     # Download script (run with internet)
├── install_offline.sh          # Install script (run offline)
├── setup_vendor.py             # Vendor setup (alternative method)
├── requirements-offline.txt    # Dependency list
└── OFFLINE_INSTALLATION.md     # This file
```

---

## ✅ Verification

After installation, verify everything works:

```bash
# Check if matrix-nio is installed
python3 -c "import nio; print('matrix-nio:', nio.__version__)"

# Check if deltachat is installed
python3 -c "import deltachat; print('deltachat:', deltachat.__version__)"

# Run the dependency checker
python3 check_ribit_dependencies.py
```

---

## 🆘 Support

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Run the dependency checker: `python3 check_ribit_dependencies.py`
3. Check the logs in `download.log` or `install.log`
4. Open an issue on GitHub with error details

---

## 📝 Notes

- **Platform**: Packages are downloaded for `x86_64` Linux
- **Python Version**: Requires Python 3.11+
- **Total Size**: ~~50 MB (compressed: ~20 MB)
- **Package Count**: 15 core packages + dependencies
- **Last Updated**: November 11, 2025

---

## 🎯 Summary

**For systems WITH internet**:
```bash
./download_dependencies.sh
```

**For systems WITHOUT internet**:
```bash
./install_offline.sh
```

That's it! Ribit 2.0 is now ready to run offline. 🚀
