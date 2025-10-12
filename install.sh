#!/bin/bash

# Ribit 2.0 - Automated Installation Script
# This script installs all dependencies and sets up Ribit 2.0

set -e  # Exit on error

echo "========================================"
echo "  Ribit 2.0 - Installation Script"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}✗ This script is designed for Linux systems${NC}"
    echo "  Please install manually following INSTALL.md"
    exit 1
fi

echo -e "${GREEN}✓ Running on Linux${NC}"

# Check Python version
echo ""
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo -e "${RED}✗ Python 3.8+ required (found $PYTHON_VERSION)${NC}"
    echo "  Please install Python 3.8 or higher"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Check if pip is installed
echo ""
echo "Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}⚠ pip3 not found, installing...${NC}"
    sudo apt update
    sudo apt install -y python3-pip
fi

echo -e "${GREEN}✓ pip3 available${NC}"

# Install system dependencies
echo ""
echo "Installing system dependencies..."
echo -e "${YELLOW}This may require sudo password${NC}"

sudo apt update

PACKAGES=(
    python3-dev
    build-essential
    git
    libolm-dev
    libmagic1
)

for package in "${PACKAGES[@]}"; do
    if dpkg -l | grep -q "^ii  $package "; then
        echo -e "${GREEN}✓ $package already installed${NC}"
    else
        echo "Installing $package..."
        sudo apt install -y $package
    fi
done

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip3 install --upgrade pip --quiet

# Install Python packages
echo ""
echo "Installing Python dependencies..."
echo "This may take a few minutes..."

PYTHON_PACKAGES=(
    "matrix-nio[e2e]"
    "aiohttp"
    "requests"
    "beautifulsoup4"
    "lxml"
    "wikipedia-api"
    "Pillow"
    "python-magic"
    "aiofiles"
    "asyncio"
)

for package in "${PYTHON_PACKAGES[@]}"; do
    echo "Installing $package..."
    pip3 install "$package" --quiet
done

echo -e "${GREEN}✓ All Python packages installed${NC}"

# Create directories
echo ""
echo "Creating directories..."
mkdir -p generated_images
mkdir -p logs
echo -e "${GREEN}✓ Directories created${NC}"

# Run tests
echo ""
echo "Running tests..."
if python3 test_fixes.py > /dev/null 2>&1; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${YELLOW}⚠ Some tests failed (this is OK if optional features aren't configured)${NC}"
fi

# Check for .env file
echo ""
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ .env file found${NC}"
else
    echo -e "${YELLOW}⚠ No .env file found${NC}"
    echo "  Creating template .env file..."
    cat > .env << 'EOF'
# Matrix Configuration
MATRIX_HOMESERVER=https://anarchists.space
MATRIX_USER_ID=@rabit233:anarchists.space
MATRIX_ACCESS_TOKEN=your_token_here

# Optional: Web Search
JINA_API_KEY=your_jina_key_here

# Optional: Image Generation
OPENAI_API_KEY=your_openai_key_here
STABILITY_API_KEY=your_stability_key_here
EOF
    echo -e "${GREEN}✓ Template .env created${NC}"
    echo -e "${YELLOW}  Please edit .env with your credentials${NC}"
fi

# Installation complete
echo ""
echo "========================================"
echo -e "${GREEN}  Installation Complete! 🚀${NC}"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Matrix credentials"
echo "   nano .env"
echo ""
echo "2. Get your Matrix access token:"
echo "   - Log in to https://app.element.io"
echo "   - Settings → Help & About → Access Token"
echo ""
echo "3. Run the Matrix bot:"
echo "   python3 -m ribit_2_0.enhanced_autonomous_matrix_bot"
echo ""
echo "4. Or run the secure E2EE bot:"
echo "   python3 run_secure_ribit.py"
echo ""
echo "For more information, see INSTALL.md"
echo ""
echo -e "${GREEN}Happy chatting with Ribit! 🤖✨${NC}"
echo ""

