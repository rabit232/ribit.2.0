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

# Check for required modules
echo ""
echo "Checking for Ribit modules..."
MODULE_CHECK_PASSED=0
MODULE_CHECK_TOTAL=0

REQUIRED_MODULES=(
    "ribit_2_0/mock_llm_wrapper.py:MockRibit20LLM (Basic)"
    "ribit_2_0/enhanced_mock_llm.py:EnhancedMockLLM"
    "ribit_2_0/advanced_mock_llm.py:AdvancedMockLLM"
    "ribit_2_0/dual_llm_pipeline.py:DualLLMPipeline (NEW!)"
    "ribit_2_0/emoji_expression.py:EmojiExpression"
    "ribit_2_0/message_history_learner.py:MessageHistoryLearner"
    "ribit_2_0/philosophical_reasoning.py:PhilosophicalReasoning"
    "ribit_2_0/conversational_mode.py:ConversationalMode"
    "ribit_2_0/autonomous_matrix.py:AutonomousMatrix"
    "ribit_2_0/task_autonomy.py:TaskAutonomy"
)

for module_info in "${REQUIRED_MODULES[@]}"; do
    module_path="${module_info%%:*}"
    module_name="${module_info##*:}"
    
    if [ -f "$module_path" ]; then
        echo -e "${GREEN}✓ $module_name${NC}"
        MODULE_CHECK_PASSED=$((MODULE_CHECK_PASSED + 1))
    else
        echo -e "${RED}✗ $module_name (missing: $module_path)${NC}"
    fi
    MODULE_CHECK_TOTAL=$((MODULE_CHECK_TOTAL + 1))
done

if [ $MODULE_CHECK_PASSED -eq $MODULE_CHECK_TOTAL ]; then
    echo -e "${GREEN}✓ All $MODULE_CHECK_PASSED/$MODULE_CHECK_TOTAL modules found${NC}"
else
    echo -e "${YELLOW}⚠ $MODULE_CHECK_PASSED/$MODULE_CHECK_TOTAL modules found${NC}"
fi

# Run tests
echo ""
echo "Running tests..."
TEST_PASSED=0
TEST_TOTAL=0

# Test 1: test_fixes.py
if [ -f "test_fixes.py" ]; then
    echo "Running test_fixes.py..."
    if python3 test_fixes.py > /dev/null 2>&1; then
        echo -e "${GREEN}✓ test_fixes.py passed${NC}"
        TEST_PASSED=$((TEST_PASSED + 1))
    else
        echo -e "${YELLOW}⚠ test_fixes.py failed${NC}"
    fi
    TEST_TOTAL=$((TEST_TOTAL + 1))
fi

# Test 2: test_learning_features.py
if [ -f "test_learning_features.py" ]; then
    echo "Running test_learning_features.py..."
    if python3 test_learning_features.py > /dev/null 2>&1; then
        echo -e "${GREEN}✓ test_learning_features.py passed${NC}"
        TEST_PASSED=$((TEST_PASSED + 1))
    else
        echo -e "${YELLOW}⚠ test_learning_features.py failed${NC}"
    fi
    TEST_TOTAL=$((TEST_TOTAL + 1))
fi

# Test 3: test_advanced_llm.py
if [ -f "test_advanced_llm.py" ]; then
    echo "Running test_advanced_llm.py..."
    if python3 test_advanced_llm.py > /dev/null 2>&1; then
        echo -e "${GREEN}✓ test_advanced_llm.py passed${NC}"
        TEST_PASSED=$((TEST_PASSED + 1))
    else
        echo -e "${YELLOW}⚠ test_advanced_llm.py failed${NC}"
    fi
    TEST_TOTAL=$((TEST_TOTAL + 1))
fi

# Test 4: test_dual_pipeline.py (NEW!)
if [ -f "test_dual_pipeline.py" ]; then
    echo "Running test_dual_pipeline.py (Dual LLM)..."
    if timeout 90 python3 test_dual_pipeline.py > /dev/null 2>&1; then
        echo -e "${GREEN}✓ test_dual_pipeline.py passed (Dual LLM working!)${NC}"
        TEST_PASSED=$((TEST_PASSED + 1))
    else
        echo -e "${YELLOW}⚠ test_dual_pipeline.py failed${NC}"
    fi
    TEST_TOTAL=$((TEST_TOTAL + 1))
fi

if [ $TEST_TOTAL -eq 0 ]; then
    echo -e "${YELLOW}⚠ No test files found (this is OK)${NC}"
elif [ $TEST_PASSED -eq $TEST_TOTAL ]; then
    echo -e "${GREEN}✓ All $TEST_PASSED/$TEST_TOTAL tests passed${NC}"
else
    echo -e "${YELLOW}⚠ $TEST_PASSED/$TEST_TOTAL tests passed${NC}"
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
MATRIX_HOMESERVER=https://matrix.envs.net
MATRIX_USER_ID=@rabit232:envs.net
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

