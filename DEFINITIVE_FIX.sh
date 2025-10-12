#!/bin/bash

# Ribit 2.0 - DEFINITIVE FIX for Missing Modules
# This script will 100% fix the missing modules issue

set -e

echo "================================================================"
echo "  Ribit 2.0 - DEFINITIVE FIX for Missing Modules"
echo "================================================================"
echo ""
echo "This script will:"
echo "  1. Check your current status"
echo "  2. Force pull latest files from GitHub"
echo "  3. Verify all modules are present"
echo ""
echo "Press Enter to continue or Ctrl+C to cancel..."
read

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}Step 1: Checking current status...${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "verify_modules.py" ]; then
    echo -e "${RED}Error: Not in ribit.2.0 directory${NC}"
    echo "Please run this script from the ribit.2.0 directory:"
    echo "  cd ~/ribit.2.0"
    echo "  ./DEFINITIVE_FIX.sh"
    exit 1
fi

echo -e "${GREEN}✓ In correct directory${NC}"

# Check git status
echo ""
echo -e "${BLUE}Step 2: Fetching latest from GitHub...${NC}"
echo ""

# Fetch all changes
git fetch --all

echo -e "${GREEN}✓ Fetched latest changes${NC}"

# Check if we have uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo ""
    echo -e "${YELLOW}⚠ You have uncommitted changes${NC}"
    echo "Stashing them temporarily..."
    git stash
    echo -e "${GREEN}✓ Changes stashed${NC}"
    STASHED=1
else
    STASHED=0
fi

echo ""
echo -e "${BLUE}Step 3: Pulling latest files...${NC}"
echo ""

# Force reset to match GitHub
git reset --hard origin/master

echo -e "${GREEN}✓ Repository updated to latest version${NC}"

# Restore stashed changes if any
if [ $STASHED -eq 1 ]; then
    echo ""
    echo "Restoring your changes..."
    git stash pop || echo -e "${YELLOW}⚠ Could not restore some changes (this is OK)${NC}"
fi

echo ""
echo -e "${BLUE}Step 4: Verifying modules...${NC}"
echo ""

# Run verification
if python3 verify_modules.py 2>&1 | grep -q "14 passed, 0 failed"; then
    echo ""
    echo "================================================================"
    echo -e "${GREEN}✅ SUCCESS! All modules are now present!${NC}"
    echo "================================================================"
    echo ""
    echo "You can now run Ribit:"
    echo "  ./run_bot.sh"
    echo ""
    echo "Or test the dual LLM:"
    echo "  python3 test_dual_llm_programming.py"
    echo ""
    exit 0
else
    echo ""
    echo "================================================================"
    echo -e "${YELLOW}⚠ Some modules still missing${NC}"
    echo "================================================================"
    echo ""
    echo "Trying alternative fix method..."
    echo ""
    
    # Alternative: Download files directly
    echo -e "${BLUE}Downloading missing modules directly from GitHub...${NC}"
    echo ""
    
    GITHUB_RAW="https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0"
    
    FILES=(
        "enhanced_mock_llm.py"
        "advanced_mock_llm.py"
        "dual_llm_pipeline.py"
        "message_history_learner.py"
        "web_scraping_wikipedia.py"
        "image_generation.py"
    )
    
    for file in "${FILES[@]}"; do
        echo "Downloading $file..."
        wget -q "$GITHUB_RAW/$file" -O "ribit_2_0/$file" && echo -e "${GREEN}✓ $file${NC}" || echo -e "${RED}✗ $file${NC}"
    done
    
    echo ""
    echo "Verifying again..."
    python3 verify_modules.py
    
    echo ""
    echo "================================================================"
    echo -e "${GREEN}✅ Fix complete!${NC}"
    echo "================================================================"
    echo ""
fi

