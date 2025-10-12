#!/bin/bash

# Ribit 2.0 - Fix Missing Python Packages
# Installs any missing dependencies

set -e

echo "========================================"
echo "  Ribit 2.0 - Fix Missing Packages"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Checking for missing packages...${NC}"
echo ""

# Function to check and install package
check_and_install() {
    package=$1
    import_name=$2
    
    if python3 -c "import $import_name" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $package (already installed)"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $package (missing, installing...)"
        pip3 install "$package" -q
        if python3 -c "import $import_name" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} $package (installed successfully)"
            return 0
        else
            echo -e "${RED}✗${NC} $package (installation failed)"
            return 1
        fi
    fi
}

# Check all required packages
echo "Checking core packages:"
check_and_install "matrix-nio[e2e]" "nio"
check_and_install "aiohttp" "aiohttp"
check_and_install "requests" "requests"
check_and_install "beautifulsoup4" "bs4"
check_and_install "lxml" "lxml"
check_and_install "wikipedia-api" "wikipediaapi"
check_and_install "Pillow" "PIL"
check_and_install "python-magic" "magic"
check_and_install "aiofiles" "aiofiles"

echo ""
echo "========================================"
echo -e "${GREEN}Package check complete!${NC}"
echo "========================================"
echo ""

# Run verification
echo "Running module verification..."
echo ""
python3 verify_modules.py

echo ""
echo "========================================"
echo -e "${GREEN}✅ All done!${NC}"
echo "========================================"
echo ""
echo "If all modules passed, you can now run:"
echo "  ./run_bot.sh"
echo ""

