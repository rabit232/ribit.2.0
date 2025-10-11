#!/bin/bash
# Ribit 2.0 Environment Fix Script
# This script will help you fix the Matrix connection issues

echo "🔧 Ribit 2.0 Fix Script"
echo "======================="
echo ""

# Check if we're in the right directory
if [ ! -f "run_matrix_bot.py" ]; then
    echo "❌ Error: Not in ribit.2.0 directory"
    echo "Please run: cd ~/ribit.2.0"
    exit 1
fi

echo "✅ Found ribit.2.0 directory"
echo ""

# Pull latest changes
echo "📥 Pulling latest changes from GitHub..."
git pull origin master
echo ""

# Check if knowledge base exists
if [ -f "ribit_matrix_knowledge.txt" ]; then
    echo "✅ Knowledge base file found"
else
    echo "❌ Knowledge base file missing"
    echo "Creating from repository..."
    git checkout master -- ribit_matrix_knowledge.txt
fi
echo ""

# Check .env file
if [ -f ".env" ]; then
    echo "📄 Current .env configuration:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    grep "MATRIX_" .env | grep -v "PASSWORD"
    echo "MATRIX_PASSWORD: [HIDDEN]"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Check for wrong username format
    if grep -q "@.*\.matrix\.envs\.net" .env; then
        echo "❌ ISSUE FOUND: Wrong username format!"
        echo ""
        echo "Your .env has: @ribit.matrix.envs.net"
        echo "Should be:     @ribit:envs.net"
        echo ""
        echo "Matrix usernames use COLON (:) not PERIOD (.)"
        echo ""
    fi
    
    # Check homeserver
    if grep -q "MATRIX_HOMESERVER=https://matrix.envs.net" .env; then
        echo "❌ ISSUE FOUND: Wrong homeserver URL!"
        echo ""
        echo "Your .env has: https://matrix.envs.net"
        echo "Should be:     https://envs.net"
        echo ""
    fi
    
else
    echo "❌ No .env file found!"
    echo "Creating from example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
fi

echo ""
echo "🔧 FIXES NEEDED:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Edit your .env file:"
echo "   nano .env"
echo ""
echo "2. Change these lines:"
echo ""
echo "   MATRIX_HOMESERVER=https://envs.net"
echo "   MATRIX_USERNAME=@ribit:envs.net"
echo "   MATRIX_PASSWORD=your_actual_password"
echo ""
echo "   ⚠️  IMPORTANT: Use COLON (:) not period (.) in username!"
echo "   ⚠️  Format: @username:homeserver.domain"
echo ""
echo "3. Save and exit (Ctrl+X, Y, Enter)"
echo ""
echo "4. Restart the bot:"
echo "   python3 run_matrix_bot.py"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Would you like to edit .env now? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    nano .env
    echo ""
    echo "✅ Configuration updated!"
    echo ""
    echo "🚀 Ready to start? Run:"
    echo "   python3 run_matrix_bot.py"
else
    echo ""
    echo "⏭️  Skipped editing. Remember to fix .env manually!"
fi

echo ""
echo "📚 For more help, see: ribit-matrix-connection-fix.md"

