#!/bin/bash

# Ribit 2.0 - Credentials Setup Helper
# This script helps you set up Matrix credentials

echo "========================================"
echo "  Ribit 2.0 - Credentials Setup"
echo "========================================"
echo ""

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " overwrite
    if [[ ! $overwrite =~ ^[Yy]$ ]]; then
        echo "Keeping existing .env file"
        exit 0
    fi
fi

echo "This script will help you create a .env file with your Matrix credentials."
echo ""

# Get homeserver
read -p "Matrix Homeserver [https://matrix.envs.net]: " homeserver
homeserver=${homeserver:-https://matrix.envs.net}

# Get user ID
read -p "Matrix User ID [@rabit232:envs.net]: " user_id
user_id=${user_id:-@rabit232:envs.net}

# Get access token
echo ""
echo "To get your access token:"
echo "1. Go to https://app.element.io"
echo "2. Log in with your Matrix account"
echo "3. Settings → Help & About → Access Token"
echo ""
read -p "Matrix Access Token: " access_token

if [ -z "$access_token" ]; then
    echo "❌ Access token is required!"
    exit 1
fi

# Optional: Device ID
read -p "Matrix Device ID (optional, press Enter to skip): " device_id

# Optional: API keys
echo ""
echo "Optional API keys (press Enter to skip):"
read -p "Jina API Key (for web search): " jina_key
read -p "OpenAI API Key (for DALL-E): " openai_key
read -p "Stability API Key (for Stable Diffusion): " stability_key

# Create .env file
cat > .env << EOF
# Matrix Configuration
MATRIX_HOMESERVER=$homeserver
MATRIX_USER_ID=$user_id
MATRIX_ACCESS_TOKEN=$access_token
EOF

if [ ! -z "$device_id" ]; then
    echo "MATRIX_DEVICE_ID=$device_id" >> .env
fi

if [ ! -z "$jina_key" ]; then
    echo "" >> .env
    echo "# Web Search" >> .env
    echo "JINA_API_KEY=$jina_key" >> .env
fi

if [ ! -z "$openai_key" ]; then
    echo "" >> .env
    echo "# Image Generation" >> .env
    echo "OPENAI_API_KEY=$openai_key" >> .env
fi

if [ ! -z "$stability_key" ]; then
    if [ -z "$openai_key" ]; then
        echo "" >> .env
        echo "# Image Generation" >> .env
    fi
    echo "STABILITY_API_KEY=$stability_key" >> .env
fi

echo ""
echo "✅ .env file created successfully!"
echo ""
echo "To use these credentials, run:"
echo "  source .env"
echo "  export \$(cat .env | xargs)"
echo "  python3 -m ribit_2_0.enhanced_autonomous_matrix_bot"
echo ""
echo "Or use the run script:"
echo "  ./run_bot.sh"
echo ""

