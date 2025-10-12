#!/bin/bash

# Ribit 2.0 - Fix Missing Modules Script
# This script downloads any missing modules from GitHub

set -e

echo "========================================"
echo "  Ribit 2.0 - Fix Missing Modules"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# GitHub raw URL base
GITHUB_RAW="https://raw.githubusercontent.com/rabit232/ribit.2.0/master/ribit_2_0"

# List of critical modules
declare -A MODULES=(
    ["enhanced_mock_llm.py"]="Enhanced MockLLM (8 parameters)"
    ["advanced_mock_llm.py"]="Advanced MockLLM (20+ parameters)"
    ["dual_llm_pipeline.py"]="Dual LLM Pipeline (NEW!)"
    ["message_history_learner.py"]="Message History Learner"
    ["web_scraping_wikipedia.py"]="Web Scraping & Wikipedia"
    ["image_generation.py"]="Image Generation"
)

DOWNLOADED=0
SKIPPED=0
FAILED=0

echo "Checking for missing modules..."
echo ""

for module in "${!MODULES[@]}"; do
    description="${MODULES[$module]}"
    filepath="ribit_2_0/$module"
    
    if [ -f "$filepath" ]; then
        echo -e "${GREEN}✓${NC} $description (already present)"
        SKIPPED=$((SKIPPED + 1))
    else
        echo -e "${YELLOW}⚠${NC} $description (missing, downloading...)"
        
        # Download from GitHub
        if wget -q "$GITHUB_RAW/$module" -O "$filepath"; then
            echo -e "${GREEN}✓${NC} Downloaded $module"
            DOWNLOADED=$((DOWNLOADED + 1))
        else
            echo -e "${RED}✗${NC} Failed to download $module"
            FAILED=$((FAILED + 1))
        fi
    fi
done

echo ""
echo "========================================"
echo "Summary:"
echo "  Downloaded: $DOWNLOADED"
echo "  Already present: $SKIPPED"
echo "  Failed: $FAILED"
echo "========================================"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All modules are now present!${NC}"
    echo ""
    echo "Running verification..."
    python3 verify_modules.py
else
    echo -e "${RED}✗ Some modules failed to download${NC}"
    echo "Please check your internet connection and try again"
    echo ""
    echo "Or try manual git pull:"
    echo "  git pull origin master"
    exit 1
fi

