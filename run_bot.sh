#!/bin/bash

# Ribit 2.0 - Bot Runner Script
# Automatically loads .env and runs the bot

echo "========================================"
echo "  Ribit 2.0 - Starting Bot"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "Please create a .env file with your Matrix credentials."
    echo "You can use the setup helper:"
    echo "  ./setup_credentials.sh"
    echo ""
    echo "Or create .env manually with:"
    echo "  MATRIX_HOMESERVER=https://matrix.envs.net"
    echo "  MATRIX_USER_ID=@rabit232:envs.net"
    echo "  MATRIX_ACCESS_TOKEN=your_token_here"
    echo ""
    exit 1
fi

# Load .env file
echo "Loading credentials from .env..."
set -a
source <(cat .env | grep -v '^#' | grep -v '^$')
set +a

# Check if required variables are set
if [ -z "$MATRIX_USER_ID" ] || [ -z "$MATRIX_ACCESS_TOKEN" ]; then
    echo "❌ Required credentials not found in .env"
    echo ""
    echo "Please make sure .env contains:"
    echo "  MATRIX_USER_ID=@rabit232:envs.net"
    echo "  MATRIX_ACCESS_TOKEN=your_token_here"
    echo ""
    exit 1
fi

echo "✓ Credentials loaded"
echo "  Homeserver: ${MATRIX_HOMESERVER:-https://matrix.envs.net}"
echo "  User ID: $MATRIX_USER_ID"
echo ""

# Choose bot type
echo "Which bot would you like to run?"
echo "1. Enhanced Autonomous Bot (recommended)"
echo "2. Secure E2EE Bot"
echo "3. Basic Matrix Bot"
echo ""
read -p "Choice [1]: " choice
choice=${choice:-1}

echo ""
echo "Starting bot..."
echo ""

case $choice in
    1)
        python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
        ;;
    2)
        python3 run_secure_ribit.py
        ;;
    3)
        python3 -m ribit_2_0.matrix_bot
        ;;
    *)
        echo "Invalid choice, starting Enhanced Autonomous Bot..."
        python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
        ;;
esac

