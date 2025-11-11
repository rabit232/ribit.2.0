# Manual Download and Copy Guide

This guide provides step-by-step instructions for manually downloading and copying all dependencies to the `packages/` folder.

---

## 📋 Overview

You'll need to:
1. Download 63 Python packages (~43 MB)
2. Optionally download ROS packages (~2-4 GB)
3. Copy everything to the `packages/` folder
4. Run the offline installer

---

## 🌐 Method 1: Download Using Web Browser

### Step 1: Create Packages Folder

```bash
mkdir -p ~/ribit.2.0/packages
cd ~/ribit.2.0/packages
```

---

### Step 2: Download Each Package from PyPI

Visit each package page and download the `.whl` file:

#### Matrix Protocol (4 packages)

1. **matrix-nio**
   - URL: https://pypi.org/project/matrix-nio/#files
   - Download: `matrix_nio-0.25.2-py3-none-any.whl`

2. **python-olm**
   - URL: https://pypi.org/project/python-olm/#files
   - Download: Latest `.whl` file

3. **unpaddedbase64**
   - URL: https://pypi.org/project/unpaddedbase64/#files
   - Download: `Unpaddedbase64-*-py3-none-any.whl`

4. **pycryptodome**
   - URL: https://pypi.org/project/pycryptodome/#files
   - Download: `pycryptodome-*-cp311-cp311-manylinux_*_x86_64.whl`

---

#### DeltaChat (3 packages)

5. **deltachat**
   - URL: https://pypi.org/project/deltachat/#files
   - Download: Latest `.whl` file

6. **imap-tools**
   - URL: https://pypi.org/project/imap-tools/#files
   - Download: `imap_tools-*-py3-none-any.whl`

7. **peewee**
   - URL: https://pypi.org/project/peewee/#files
   - Download: `peewee-*-py3-none-any.whl`

---

#### Async HTTP (8 packages)

8. **aiohttp**
   - URL: https://pypi.org/project/aiohttp/#files
   - Download: `aiohttp-*-cp311-cp311-manylinux_*_x86_64.whl`

9. **aiofiles**
   - URL: https://pypi.org/project/aiofiles/#files
   - Download: `aiofiles-*-py3-none-any.whl`

10. **aiohappyeyeballs**
    - URL: https://pypi.org/project/aiohappyeyeballs/#files
    - Download: Latest `.whl` file

11. **aiohttp-socks**
    - URL: https://pypi.org/project/aiohttp-socks/#files
    - Download: Latest `.whl` file

12. **aiosignal**
    - URL: https://pypi.org/project/aiosignal/#files
    - Download: `aiosignal-*-py3-none-any.whl`

13. **frozenlist**
    - URL: https://pypi.org/project/frozenlist/#files
    - Download: `frozenlist-*-cp311-cp311-manylinux_*_x86_64.whl`

14. **multidict**
    - URL: https://pypi.org/project/multidict/#files
    - Download: `multidict-*-cp311-cp311-manylinux_*_x86_64.whl`

15. **yarl**
    - URL: https://pypi.org/project/yarl/#files
    - Download: `yarl-*-cp311-cp311-manylinux_*_x86_64.whl`

---

#### HTTP & Web (10 packages)

16. **requests**
    - URL: https://pypi.org/project/requests/#files
    - Download: `requests-*-py3-none-any.whl`

17. **beautifulsoup4**
    - URL: https://pypi.org/project/beautifulsoup4/#files
    - Download: `beautifulsoup4-*-py3-none-any.whl`

18. **lxml**
    - URL: https://pypi.org/project/lxml/#files
    - Download: `lxml-*-cp311-cp311-manylinux_*_x86_64.whl`

19. **httpx**
    - URL: https://pypi.org/project/httpx/#files
    - Download: `httpx-*-py3-none-any.whl`

20. **httpcore**
    - URL: https://pypi.org/project/httpcore/#files
    - Download: `httpcore-*-py3-none-any.whl`

21. **h11**
    - URL: https://pypi.org/project/h11/#files
    - Download: `h11-*-py3-none-any.whl`

22. **h2**
    - URL: https://pypi.org/project/h2/#files
    - Download: `h2-*-py3-none-any.whl`

23. **hpack**
    - URL: https://pypi.org/project/hpack/#files
    - Download: `hpack-*-py3-none-any.whl`

24. **hyperframe**
    - URL: https://pypi.org/project/hyperframe/#files
    - Download: `hyperframe-*-py3-none-any.whl`

25. **soupsieve**
    - URL: https://pypi.org/project/soupsieve/#files
    - Download: `soupsieve-*-py3-none-any.whl`

---

#### Continue for all 63 packages...

**Full list**: See `DOWNLOAD_LINKS.md` for complete package URLs.

---

## 💻 Method 2: Download Using Command Line (wget)

### Quick Download Script

```bash
#!/bin/bash
# Download all packages using wget

cd ~/ribit.2.0/packages

# Matrix Protocol
wget https://files.pythonhosted.org/packages/.../matrix_nio-0.25.2-py3-none-any.whl
wget https://files.pythonhosted.org/packages/.../python_olm-*.whl
# ... (add all 63 packages)

echo "Download complete!"
```

---

### Automated Download with pip

**Easiest method**:

```bash
cd ~/ribit.2.0
pip3 download -d packages/ -r requirements-offline.txt
```

This automatically downloads all 63 packages and their dependencies.

---

## 📁 Method 3: Copy from Another System

### Using USB Drive

#### On Source System (with internet):

```bash
# 1. Download packages
cd ~/ribit.2.0
./download_dependencies.sh

# 2. Create tarball
tar -czf ribit-packages.tar.gz packages/

# 3. Copy to USB
cp ribit-packages.tar.gz /media/usb/
```

#### On Target System (offline):

```bash
# 1. Copy from USB
cp /media/usb/ribit-packages.tar.gz ~/

# 2. Extract
tar -xzf ribit-packages.tar.gz

# 3. Move to ribit.2.0 folder
mv packages/ ~/ribit.2.0/
```

---

### Using SCP (Network Transfer)

```bash
# From source to target
scp -r ~/ribit.2.0/packages/ user@target-ip:~/ribit.2.0/

# Or compress first for faster transfer
tar -czf packages.tar.gz packages/
scp packages.tar.gz user@target-ip:~/
```

---

### Using Network Share (SMB/CIFS)

```bash
# On source system
cp -r ~/ribit.2.0/packages/ /mnt/network-share/

# On target system
sudo mount -t cifs //server/share /mnt/share
cp -r /mnt/share/packages/ ~/ribit.2.0/
```

---

## 📦 Method 4: Download ROS Packages

### ROS 1 Noetic

```bash
# Create ROS packages folder
mkdir -p ~/ros-noetic-packages
cd ~/ros-noetic-packages

# Download ROS Noetic Desktop Full
apt-get download ros-noetic-desktop-full

# Download all dependencies
apt-cache depends ros-noetic-desktop-full | \
  grep "Depends:" | \
  cut -d: -f2 | \
  xargs apt-get download

# Create tarball
cd ..
tar -czf ros-noetic-offline.tar.gz ros-noetic-packages/
```

---

### ROS 2 Humble

```bash
# Create ROS 2 packages folder
mkdir -p ~/ros2-humble-packages
cd ~/ros2-humble-packages

# Download ROS 2 Humble Desktop
apt-get download ros-humble-desktop

# Download all dependencies
apt-cache depends ros-humble-desktop | \
  grep "Depends:" | \
  cut -d: -f2 | \
  xargs apt-get download

# Create tarball
cd ..
tar -czf ros2-humble-offline.tar.gz ros2-humble-packages/
```

---

## ✅ Verification

After downloading/copying, verify the packages:

```bash
# Check package count
cd ~/ribit.2.0/packages
ls -1 *.whl | wc -l
# Should show: 63

# Check total size
du -sh .
# Should show: ~43M

# List all packages
ls -lh *.whl
```

---

## 📋 Checklist

Before proceeding to installation, ensure:

- [ ] `packages/` folder exists in `~/ribit.2.0/`
- [ ] 63 `.whl` files are present
- [ ] Total size is approximately 43 MB
- [ ] All filenames end with `.whl`
- [ ] No corrupted downloads (check file sizes)

---

## 🔄 Copy Methods Comparison

| Method | Speed | Difficulty | Requirements |
|:-------|:------|:-----------|:-------------|
| **USB Drive** | Medium | Easy | USB drive |
| **SCP** | Fast | Medium | Network, SSH |
| **Network Share** | Fast | Medium | SMB/CIFS share |
| **wget** | Slow | Easy | Internet |
| **pip download** | Slow | Easiest | Internet, pip |

---

## 🐛 Troubleshooting

### "No such file or directory"

**Solution**: Create the packages folder first:
```bash
mkdir -p ~/ribit.2.0/packages
```

---

### "Permission denied"

**Solution**: Check folder permissions:
```bash
chmod 755 ~/ribit.2.0/packages
```

---

### "Disk space full"

**Solution**: Check available space:
```bash
df -h ~/ribit.2.0
# Need at least 100 MB free
```

---

### "File corrupted"

**Solution**: Re-download the package:
```bash
rm packages/PACKAGE_NAME.whl
wget -P packages/ https://pypi.org/...
```

---

## 📊 File Structure

After copying, your structure should look like:

```
ribit.2.0/
├── packages/
│   ├── aiofiles-*.whl
│   ├── aiohttp-*.whl
│   ├── beautifulsoup4-*.whl
│   ├── deltachat-*.whl
│   ├── matrix_nio-*.whl
│   ├── Pillow-*.whl
│   ├── requests-*.whl
│   ├── ... (57 more .whl files)
│   └── MANIFEST.txt
├── download_dependencies.sh
├── install_offline.sh
├── requirements-offline.txt
└── OFFLINE_INSTALLATION.md
```

---

## 🚀 Next Steps

After copying all packages:

1. **Verify packages**:
   ```bash
   ls -1 packages/*.whl | wc -l
   ```

2. **Run offline installer**:
   ```bash
   ./install_offline.sh
   ```

3. **Choose installation method** (option 3 recommended)

4. **Set up credentials**:
   ```bash
   python3 setup_credentials.py
   ```

5. **Run Ribit 2.0**:
   ```bash
   python3 -m ribit_2_0.matrix_bot
   ```

---

## 📝 Notes

- **Bandwidth**: Downloading all packages requires ~50 MB download
- **Time**: Manual download takes 15-30 minutes
- **Automated**: Use `./download_dependencies.sh` for fastest method
- **Compression**: Tarball reduces size to ~20 MB
- **Platform**: Download packages matching your target platform

---

**See Also**:
- `DOWNLOAD_LINKS.md` - Direct links to all packages
- `ROS_INSTALLATION.md` - ROS installation guide
- `OFFLINE_INSTALLATION.md` - Complete offline installation guide

**Last Updated**: November 11, 2025
