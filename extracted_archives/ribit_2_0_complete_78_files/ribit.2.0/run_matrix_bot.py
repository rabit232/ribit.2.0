#!/usr/bin/env python3
"""
Ribit 2.0 Matrix Bot Launcher

Easy launcher script for the Ribit 2.0 Matrix bot with configuration
and deployment options.

Author: Manus AI
Date: September 21, 2025
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the ribit_2_0 package to the path
sys.path.insert(0, str(Path(__file__).parent))

def setup_environment():
    """Set up environment variables and configuration."""
    
    print("🤖 Ribit 2.0 Matrix Bot Launcher")
    print("=" * 50)
    
    # Check for environment file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Found .env file, loading configuration...")
        load_env_file(env_file)
    else:
        print("⚠️  No .env file found, using environment variables...")
    
    # Check required environment variables
    required_vars = {
        "MATRIX_HOMESERVER": "https://envs.net",
        "MATRIX_USERNAME": "@ribit.2.0:envs.net", 
        "MATRIX_PASSWORD": ""
    }
    
    missing_vars = []
    for var, default in required_vars.items():
        value = os.getenv(var, default)
        if not value and var == "MATRIX_PASSWORD":
            missing_vars.append(var)
        elif not value:
            os.environ[var] = default
            print(f"🔧 Set {var} to default: {default}")
        else:
            print(f"✅ {var}: {'*' * len(value) if 'PASSWORD' in var else value}")
    
    if missing_vars:
        print("\n❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   • {var}")
        print("\nPlease set these variables or create a .env file:")
        print("Example .env file:")
        print("MATRIX_HOMESERVER=https://envs.net")
        print("MATRIX_USERNAME=@ribit.2.0:envs.net")
        print("MATRIX_PASSWORD=your_password_here")
        return False
    
    return True

def load_env_file(env_file: Path):
    """Load environment variables from .env file."""
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip('"\'')
                    os.environ[key] = value
    except Exception as e:
        print(f"⚠️  Error loading .env file: {e}")

def check_dependencies():
    """Check if required dependencies are installed."""
    print("\n🔍 Checking dependencies...")
    
    dependencies = {
        "matrix-nio": "Matrix client library",
        "psutil": "System monitoring (optional)"
    }
    
    missing_deps = []
    for dep, description in dependencies.items():
        try:
            if dep == "matrix-nio":
                import nio
                print(f"✅ {dep}: {description}")
            elif dep == "psutil":
                import psutil
                print(f"✅ {dep}: {description}")
        except ImportError:
            if dep == "matrix-nio":
                missing_deps.append(dep)
                print(f"❌ {dep}: {description} - REQUIRED")
            else:
                print(f"⚠️  {dep}: {description} - Optional")
    
    if missing_deps:
        print(f"\n❌ Missing required dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install matrix-nio")
        print("For full functionality: pip install matrix-nio psutil")
        return False
    
    return True

def create_sample_env():
    """Create a sample .env file."""
    env_content = """# Ribit 2.0 Matrix Bot Configuration

# Matrix server settings
MATRIX_HOMESERVER=https://envs.net
MATRIX_USERNAME=@ribit.2.0:envs.net
MATRIX_PASSWORD=your_password_here

# Optional: Authorized users (comma-separated)
AUTHORIZED_USERS=@rabit232:envs.net,@rabit232:envs.net

# Optional: Bot configuration
BOT_NAME=ribit.2.0
SYNC_TIMEOUT=30000
REQUEST_TIMEOUT=10000
KEEPALIVE_INTERVAL=60

# Optional: Enable/disable features
ENABLE_SYSTEM_COMMANDS=true
ENABLE_TERMINATOR_MODE=true
"""
    
    try:
        with open(".env.example", "w") as f:
            f.write(env_content)
        print("✅ Created .env.example file")
        print("Copy to .env and edit with your credentials:")
        print("cp .env.example .env")
    except Exception as e:
        print(f"❌ Error creating .env.example: {e}")

async def run_bot():
    """Run the Ribit Matrix Bot."""
    try:
        from ribit_2_0.matrix_bot import RibitMatrixBot
        
        # Get configuration
        homeserver = os.getenv("MATRIX_HOMESERVER")
        username = os.getenv("MATRIX_USERNAME") 
        password = os.getenv("MATRIX_PASSWORD")
        
        # Parse authorized users
        auth_users_str = os.getenv("AUTHORIZED_USERS", 
                                  "@rabit232:envs.net,@rabit232:envs.net")
        authorized_users = set(user.strip() for user in auth_users_str.split(","))
        
        print(f"\n🚀 Starting Ribit 2.0 Matrix Bot...")
        print(f"📡 Homeserver: {homeserver}")
        print(f"👤 Username: {username}")
        print(f"🔐 Authorized users: {len(authorized_users)}")
        
        # Create and start bot
        bot = RibitMatrixBot(homeserver, username, password, authorized_users)
        await bot.start()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure ribit_2_0 package is properly installed")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main launcher function."""
    print("🤖 Ribit 2.0 Matrix Bot Launcher")
    print("=" * 50)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--create-env":
            create_sample_env()
            return
        elif sys.argv[1] == "--help":
            print_help()
            return
        elif sys.argv[1] == "--check":
            setup_environment()
            check_dependencies()
            return
    
    # Setup and validation
    if not setup_environment():
        print("\n💡 Tip: Use --create-env to create a sample configuration file")
        return
    
    if not check_dependencies():
        return
    
    print("\n🎯 All checks passed! Starting bot...")
    
    # Run the bot
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\n\n👋 Ribit 2.0 Matrix Bot shutting down gracefully...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

def print_help():
    """Print help information."""
    print("""
Ribit 2.0 Matrix Bot Launcher

Usage:
    python run_matrix_bot.py [options]

Options:
    --help        Show this help message
    --create-env  Create a sample .env configuration file
    --check       Check configuration and dependencies without starting

Environment Variables:
    MATRIX_HOMESERVER    Matrix server URL (default: https://envs.net)
    MATRIX_USERNAME      Bot username (default: @ribit.2.0:envs.net)
    MATRIX_PASSWORD      Bot password (required)
    AUTHORIZED_USERS     Comma-separated list of authorized user IDs
    
Configuration File:
    Create a .env file in the same directory with your configuration.
    Use --create-env to generate a sample file.

Examples:
    # Start the bot
    python run_matrix_bot.py
    
    # Create sample configuration
    python run_matrix_bot.py --create-env
    
    # Check configuration
    python run_matrix_bot.py --check

For more information, see the documentation in the repository.
""")

if __name__ == "__main__":
    main()
