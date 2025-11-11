#!/bin/bash
# Ribit 2.0 - Download Dependencies for Offline Installation
# This script downloads all required Python packages to the packages/ folder

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
echo -e "${CYAN}║  ${BOLD}Ribit 2.0 - Dependency Downloader${RESET}${CYAN}                            ║${RESET}"
echo -e "${CYAN}║                                                                   ║${RESET}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════╝${RESET}"
echo ""

# Check if pip3 is available
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ Error: pip3 not found${RESET}"
    echo "Please install Python 3 and pip first"
    exit 1
fi

# Create packages directory
PACKAGES_DIR="packages"
echo -e "${YELLOW}📦 Creating packages directory...${RESET}"
mkdir -p "$PACKAGES_DIR"

# Download dependencies
echo -e "${CYAN}⬇️  Downloading dependencies from PyPI...${RESET}"
echo -e "${YELLOW}This may take a few minutes depending on your internet speed${RESET}"
echo ""

# Download all packages and their dependencies
pip3 download \
    --dest "$PACKAGES_DIR" \
    --requirement requirements-offline.txt \
    --progress-bar on

# Check if download was successful
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ All dependencies downloaded successfully!${RESET}"
    echo ""
    
    # Count downloaded packages
    PACKAGE_COUNT=$(ls -1 "$PACKAGES_DIR" | wc -l)
    TOTAL_SIZE=$(du -sh "$PACKAGES_DIR" | cut -f1)
    
    echo -e "${BOLD}📊 Download Summary:${RESET}"
    echo -e "  Packages downloaded: ${CYAN}$PACKAGE_COUNT${RESET}"
    echo -e "  Total size: ${CYAN}$TOTAL_SIZE${RESET}"
    echo -e "  Location: ${CYAN}$PACKAGES_DIR/${RESET}"
    echo ""
    
    echo -e "${GREEN}${BOLD}Next Steps:${RESET}"
    echo -e "  1. Copy the ${CYAN}packages/${RESET} folder to your offline system"
    echo -e "  2. Run ${CYAN}./install_offline.sh${RESET} on the offline system"
    echo ""
    
    # Create a manifest file
    echo -e "${YELLOW}📝 Creating package manifest...${RESET}"
    ls -1 "$PACKAGES_DIR" > "$PACKAGES_DIR/MANIFEST.txt"
    echo "Total packages: $PACKAGE_COUNT" >> "$PACKAGES_DIR/MANIFEST.txt"
    echo "Downloaded on: $(date)" >> "$PACKAGES_DIR/MANIFEST.txt"
    echo -e "${GREEN}✅ Manifest created: ${CYAN}$PACKAGES_DIR/MANIFEST.txt${RESET}"
    echo ""
    
else
    echo ""
    echo -e "${RED}❌ Error downloading dependencies${RESET}"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${RESET}"
echo -e "${GREEN}${BOLD}✅ Download Complete!${RESET}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${RESET}"
