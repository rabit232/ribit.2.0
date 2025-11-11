# ROS Installation Guide for Ribit 2.0

This guide explains how to install ROS 1 (Noetic) and ROS 2 (Humble) for use with Ribit 2.0.

---

## 🤖 Do You Need ROS?

**ROS is OPTIONAL** for Ribit 2.0. You only need it if you want to:
- Control robots or robotic systems
- Use ROS topics, services, or actions
- Integrate with ROS-based hardware

**If you don't need robotics features**, skip ROS installation and use the standard offline installation instead.

---

## 📋 ROS Versions

| ROS Version | Ubuntu Version | Python Version | Status |
|:------------|:---------------|:---------------|:-------|
| **ROS 1 Noetic** | Ubuntu 20.04 | Python 3.8 | LTS until 2025 |
| **ROS 2 Humble** | Ubuntu 22.04 | Python 3.10+ | LTS until 2027 |

---

## 🔧 ROS 1 (Noetic) Installation

### Prerequisites

- **OS**: Ubuntu 20.04 (Focal Fossa)
- **Python**: 3.8
- **Disk Space**: ~2-4 GB

---

### Method 1: Online Installation (Recommended)

```bash
# 1. Set up sources.list
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

# 2. Set up keys
sudo apt install curl -y
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

# 3. Update package index
sudo apt update

# 4. Install ROS Noetic Desktop Full (recommended)
sudo apt install ros-noetic-desktop-full -y

# 5. Environment setup
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc

# 6. Install dependencies for building packages
sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential -y

# 7. Initialize rosdep
sudo rosdep init
rosdep update
```

---

### Method 2: Offline Installation

#### Step 1: Download Packages (On System WITH Internet)

```bash
# Create download directory
mkdir -p ros-noetic-packages
cd ros-noetic-packages

# Download ROS Noetic Desktop Full and all dependencies
apt-get download ros-noetic-desktop-full

# Download dependencies
apt-cache depends ros-noetic-desktop-full | grep "Depends:" | cut -d: -f2 | xargs apt-get download

# Create tarball
cd ..
tar -czf ros-noetic-offline.tar.gz ros-noetic-packages/
```

#### Step 2: Install Offline (On System WITHOUT Internet)

```bash
# Extract packages
tar -xzf ros-noetic-offline.tar.gz
cd ros-noetic-packages/

# Install all .deb files
sudo dpkg -i *.deb

# Fix any dependency issues
sudo apt-get install -f

# Environment setup
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

### Method 3: Download from Mirror

If the main server is slow, use a mirror:

```bash
# Tsinghua Mirror (China)
sudo sh -c 'echo "deb https://mirrors.tuna.tsinghua.edu.cn/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

# KAIST Mirror (South Korea)
sudo sh -c 'echo "deb http://mirror.kakao.com/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

# Then follow Method 1 steps 2-7
```

---

### Verify ROS 1 Installation

```bash
# Check ROS version
rosversion -d
# Should output: noetic

# Check Python version
python3 --version
# Should output: Python 3.8.x

# Test ROS core
roscore &
# Should start ROS master

# Kill roscore
killall roscore
```

---

## 🚀 ROS 2 (Humble) Installation

### Prerequisites

- **OS**: Ubuntu 22.04 (Jammy Jellyfish)
- **Python**: 3.10+
- **Disk Space**: ~2-4 GB

---

### Method 1: Online Installation (Recommended)

```bash
# 1. Set locale
sudo apt update && sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# 2. Setup sources
sudo apt install software-properties-common -y
sudo add-apt-repository universe

# 3. Add ROS 2 GPG key
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# 4. Add repository to sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 5. Update package index
sudo apt update

# 6. Install ROS 2 Humble Desktop (recommended)
sudo apt install ros-humble-desktop -y

# 7. Install development tools
sudo apt install ros-dev-tools -y

# 8. Environment setup
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

### Method 2: Offline Installation

#### Step 1: Download Packages (On System WITH Internet)

```bash
# Create download directory
mkdir -p ros2-humble-packages
cd ros2-humble-packages

# Download ROS 2 Humble Desktop and all dependencies
apt-get download ros-humble-desktop

# Download dependencies recursively
apt-cache depends ros-humble-desktop | grep "Depends:" | cut -d: -f2 | xargs apt-get download

# Create tarball
cd ..
tar -czf ros2-humble-offline.tar.gz ros2-humble-packages/
```

#### Step 2: Install Offline (On System WITHOUT Internet)

```bash
# Extract packages
tar -xzf ros2-humble-offline.tar.gz
cd ros2-humble-packages/

# Install all .deb files
sudo dpkg -i *.deb

# Fix any dependency issues
sudo apt-get install -f

# Environment setup
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

### Method 3: Download from Mirror

```bash
# Tsinghua Mirror (China)
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Then follow Method 1 steps 5-8
```

---

### Verify ROS 2 Installation

```bash
# Check ROS 2 version
ros2 --version
# Should output: ros2 cli version: humble

# Check Python version
python3 --version
# Should output: Python 3.10.x or higher

# Test ROS 2
ros2 run demo_nodes_cpp talker &
ros2 run demo_nodes_cpp listener

# Should see messages being published and received

# Kill demo nodes
killall talker listener
```

---

## 🔗 Manual Download Links

### ROS 1 Noetic Packages

**Base URL**: http://packages.ros.org/ros/ubuntu/pool/main/r/

**Key Packages to Download**:

1. **ros-noetic-desktop-full**  
   http://packages.ros.org/ros/ubuntu/pool/main/r/ros-noetic-desktop-full/

2. **ros-noetic-ros-base**  
   http://packages.ros.org/ros/ubuntu/pool/main/r/ros-noetic-ros-base/

3. **ros-noetic-rospy**  
   http://packages.ros.org/ros/ubuntu/pool/main/r/ros-noetic-rospy/

4. **ros-noetic-roscpp**  
   http://packages.ros.org/ros/ubuntu/pool/main/r/ros-noetic-roscpp/

5. **ros-noetic-roslaunch**  
   http://packages.ros.org/ros/ubuntu/pool/main/r/ros-noetic-roslaunch/

**Download all .deb files** from each package directory.

---

### ROS 2 Humble Packages

**Base URL**: http://packages.ros.org/ros2/ubuntu/pool/main/r/

**Key Packages to Download**:

1. **ros-humble-desktop**  
   http://packages.ros.org/ros2/ubuntu/pool/main/r/ros-humble-desktop/

2. **ros-humble-ros-base**  
   http://packages.ros.org/ros2/ubuntu/pool/main/r/ros-humble-ros-base/

3. **ros-humble-rclpy**  
   http://packages.ros.org/ros2/ubuntu/pool/main/r/ros-humble-rclpy/

4. **ros-humble-rclcpp**  
   http://packages.ros.org/ros2/ubuntu/pool/main/r/ros-humble-rclcpp/

**Download all .deb files** from each package directory.

---

## 📦 How to Copy ROS Packages

### From USB Drive

```bash
# On system with internet (download)
mkdir -p /media/usb/ros-packages
cd /media/usb/ros-packages
apt-get download ros-noetic-desktop-full  # or ros-humble-desktop

# On offline system (install)
cd /media/usb/ros-packages
sudo dpkg -i *.deb
sudo apt-get install -f
```

---

### From Network Share

```bash
# Mount network share
sudo mount -t cifs //server/share /mnt/share

# Copy packages
cp /mnt/share/ros-packages/*.deb ~/ros-packages/

# Install
cd ~/ros-packages
sudo dpkg -i *.deb
sudo apt-get install -f
```

---

## 🔧 Integration with Ribit 2.0

After installing ROS, integrate with Ribit 2.0:

### For ROS 1 (Noetic)

```bash
# Install Python ROS bindings
pip3 install rospy --break-system-packages

# Or use system package
sudo apt install python3-rospy
```

### For ROS 2 (Humble)

```bash
# Install Python ROS 2 bindings
pip3 install rclpy --break-system-packages

# Or use system package
sudo apt install python3-rclpy
```

---

## 📊 Package Sizes

| Package | Size (Compressed) | Size (Installed) |
|:--------|:------------------|:-----------------|
| **ROS 1 Noetic Desktop Full** | ~600 MB | ~2.5 GB |
| **ROS 1 Noetic ROS Base** | ~200 MB | ~800 MB |
| **ROS 2 Humble Desktop** | ~700 MB | ~3 GB |
| **ROS 2 Humble ROS Base** | ~250 MB | ~1 GB |

---

## 🌐 Download Mirrors

| Mirror | Location | ROS 1 URL | ROS 2 URL |
|:-------|:---------|:----------|:----------|
| **OSRF (Official)** | USA | http://packages.ros.org/ros/ubuntu | http://packages.ros.org/ros2/ubuntu |
| **Tsinghua** | China | https://mirrors.tuna.tsinghua.edu.cn/ros/ubuntu | https://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu |
| **KAIST** | South Korea | http://mirror.kakao.com/ros/ubuntu | http://mirror.kakao.com/ros2/ubuntu |
| **USTC** | China | http://mirrors.ustc.edu.cn/ros/ubuntu | http://mirrors.ustc.edu.cn/ros2/ubuntu |

---

## 🐛 Troubleshooting

### "Unable to locate package ros-noetic-desktop-full"

**Solution**: Check your Ubuntu version:
```bash
lsb_release -a
```
ROS Noetic requires Ubuntu 20.04.

---

### "rosdep: command not found"

**Solution**: Install rosdep:
```bash
sudo apt install python3-rosdep
sudo rosdep init
rosdep update
```

---

### "source: not found"

**Solution**: Make sure you're using bash:
```bash
echo $SHELL
# Should output: /bin/bash

# If not, switch to bash
chsh -s /bin/bash
```

---

### Dependencies fail to install

**Solution**: Install system dependencies first:
```bash
# For ROS 1
sudo apt install build-essential python3-dev python3-pip

# For ROS 2
sudo apt install build-essential python3-dev python3-pip python3-colcon-common-extensions
```

---

## ✅ Verification Checklist

After installation, verify:

- [ ] ROS version command works (`rosversion -d` or `ros2 --version`)
- [ ] Environment is sourced (check `$ROS_DISTRO`)
- [ ] Python bindings work (`import rospy` or `import rclpy`)
- [ ] Demo nodes run successfully
- [ ] Ribit 2.0 can import ROS modules

---

## 📝 Notes

- **ROS 1 vs ROS 2**: They are **not compatible**. Choose one based on your needs.
- **Python Version**: ROS 1 uses Python 3.8, ROS 2 uses Python 3.10+
- **Disk Space**: Reserve at least 5 GB for ROS + dependencies
- **Build Time**: First-time setup takes 10-30 minutes
- **Updates**: ROS packages are updated regularly; check for updates periodically

---

**Official Documentation**:
- ROS 1 Noetic: http://wiki.ros.org/noetic/Installation
- ROS 2 Humble: https://docs.ros.org/en/humble/Installation.html

**Last Updated**: November 11, 2025
