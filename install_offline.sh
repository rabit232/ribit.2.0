#!/bin/bash
# Ribit 2.0 - Offline Installation Script
# This script installs all dependencies from the packages/ folder without internet

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${CYAN}║                                                                   ║${RESET}"
echo -e "${CYAN}║  ${BOLD}Ribit 2.0 - Offline Installation${RESET}${CYAN}                              ║${RESET}"
echo -e "${CYAN}║                                                                   ║${RESET}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════╝${RESET}"
echo ""

# Check if packages directory exists
if [ ! -d "packages" ]; then
    echo -e "${RED}❌ Error: packages/ directory not found${RESET}"
    echo ""
    echo "Please ensure you have:"
    echo "  1. Run ./download_dependencies.sh on a system with internet"
    echo "  2. Copied the packages/ folder to this system"
    exit 1
fi

# Check if pip3 is available
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ Error: pip3 not found${RESET}"
    echo "Please install Python 3 and pip first"
    exit 1
fi

# Count packages
PACKAGE_COUNT=$(ls -1 packages/*.whl packages/*.tar.gz 2>/dev/null | wc -l)
echo -e "${YELLOW}📦 Found ${CYAN}$PACKAGE_COUNT${YELLOW} packages to install${RESET}"
echo ""

# Ask for confirmation
echo -e "${BOLD}Installation method:${RESET}"
echo "  1. System-wide (requires sudo)"
echo "  2. User-only (--user flag)"
echo "  3. With --break-system-packages (Debian/Ubuntu)"
echo ""
read -p "Choose installation method (1/2/3) [3]: " INSTALL_METHOD
INSTALL_METHOD=${INSTALL_METHOD:-3}

# Set installation flags
case $INSTALL_METHOD in
    1)
        INSTALL_FLAGS=""
        SUDO_CMD="sudo"
        echo -e "${YELLOW}⚠️  Installing system-wide (requires sudo)${RESET}"
        ;;
    2)
        INSTALL_FLAGS="--user"
        SUDO_CMD=""
        echo -e "${CYAN}Installing to user directory${RESET}"
        ;;
    3)
        INSTALL_FLAGS="--break-system-packages"
        SUDO_CMD=""
        echo -e "${CYAN}Installing with --break-system-packages${RESET}"
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${RESET}"
        exit 1
        ;;
esac

echo ""
echo -e "${CYAN}🚀 Installing dependencies from local packages...${RESET}"
echo ""

# Install from local packages
$SUDO_CMD pip3 install \
    --no-index \
    --find-links=packages/ \
    --requirement requirements-offline.txt \
    $INSTALL_FLAGS

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ All dependencies installed successfully!${RESET}"
    echo ""
    
    echo -e "${BOLD}📊 Installation Summary:${RESET}"
    echo -e "  Packages installed: ${CYAN}$PACKAGE_COUNT${RESET}"
    echo -e "  Installation method: ${CYAN}$([ -z \"$SUDO_CMD\" ] && echo \"User\" || echo \"System-wide\")${RESET}"
    echo ""
    
    echo -e "${GREEN}${BOLD}Next Steps:${RESET}"
    echo -e "  1. Set up your Matrix credentials:"
    echo -e "     ${CYAN}python3 setup_credentials.py${RESET}"
    echo ""
    echo -e "  2. Run the bot:"
    echo -e "     ${CYAN}python3 -m ribit_2_0.matrix_bot${RESET}"
    echo ""
    
else
    echo ""
    echo -e "${RED}❌ Error during installation${RESET}"
    echo "Please check the error messages above"
    exit 1
fi

echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${RESET}"
echo -e "${GREEN}${BOLD}✅ Offline Installation Complete!${RESET}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${RESET}"
