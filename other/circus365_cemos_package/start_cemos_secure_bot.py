#!/usr/bin/env python3
"""
🎪 CEMOS Secure Matrix Bot Startup Script

Specifically configured for circus365/cemos project integration
with Ribit 2.0 E2EE and Matrix capabilities.

Usage:
    python start_cemos_secure_bot.py [--config CONFIG_FILE] [--debug]

Author: Manus AI (for circus365/cemos)
Date: September 27, 2024
"""

import os
import sys
import asyncio
import logging
import argparse
from pathlib import Path
from typing import Optional

# Add current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from integrated_secure_matrix_bot import IntegratedSecureMatrixBot
    from matrix_e2ee_protocol import MatrixE2EEProtocol
    from enhanced_e2ee_integration import EnhancedE2EEIntegration
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure all E2EE modules are in the same directory as this script.")
    sys.exit(1)

# Configure logging
def setup_logging(debug: bool = False, log_file: Optional[str] = None):
    """Setup logging configuration for CEMOS"""
    level = logging.DEBUG if debug else logging.INFO
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Setup file handler if specified
    handlers = [console_handler]
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        handlers=handlers,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Set specific logger levels
    logging.getLogger('matrix_e2ee_protocol').setLevel(level)
    logging.getLogger('integrated_secure_matrix_bot').setLevel(level)

class CEMOSSecureBot:
    """
    CEMOS-specific secure Matrix bot with E2EE integration
    """
    
    def __init__(self, config_file: str = ".env"):
        self.config_file = config_file
        self.bot = None
        self.logger = logging.getLogger(__name__)
        
        # Load environment configuration
        self.load_config()
        
        # Validate CEMOS configuration
        self.validate_cemos_config()
    
    def load_config(self):
        """Load configuration from environment file"""
        if os.path.exists(self.config_file):
            # Load environment variables from file
            with open(self.config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            
            self.logger.info(f"✅ Loaded configuration from {self.config_file}")
        else:
            self.logger.warning(f"⚠️  Configuration file {self.config_file} not found")
            self.logger.info("Using environment variables or defaults")
    
    def validate_cemos_config(self):
        """Validate CEMOS-specific configuration"""
        required_vars = [
            'MATRIX_HOMESERVER',
            'MATRIX_USER_ID', 
            'MATRIX_ACCESS_TOKEN',
            'MATRIX_ROOM_ID'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            self.logger.error(f"❌ Missing required environment variables: {missing_vars}")
            self.logger.error("Please configure your .env file with CEMOS Matrix settings")
            sys.exit(1)
        
        # Check CEMOS-specific settings
        if os.getenv('CEMOS_PROJECT_MODE', '').lower() != 'true':
            self.logger.warning("⚠️  CEMOS_PROJECT_MODE not enabled")
        
        self.logger.info("✅ CEMOS configuration validated")
    
    async def start(self):
        """Start the CEMOS secure bot"""
        try:
            self.logger.info("🎪 Starting CEMOS Secure Matrix Bot...")
            
            # Initialize the integrated secure bot
            self.bot = IntegratedSecureMatrixBot()
            
            # Configure CEMOS-specific settings
            await self.configure_cemos_features()
            
            # Start the bot
            self.logger.info("🚀 CEMOS bot starting...")
            await self.bot.start()
            
        except KeyboardInterrupt:
            self.logger.info("🛑 CEMOS bot stopped by user")
        except Exception as e:
            self.logger.error(f"❌ CEMOS bot error: {e}")
            raise
        finally:
            await self.cleanup()
    
    async def configure_cemos_features(self):
        """Configure CEMOS-specific features"""
        self.logger.info("⚙️  Configuring CEMOS features...")
        
        # Set project identification
        if hasattr(self.bot, 'set_project_mode'):
            self.bot.set_project_mode("CEMOS")
        
        # Configure E2EE level
        e2ee_level = os.getenv('E2EE_DEFAULT_LEVEL', 'enhanced')
        if hasattr(self.bot, 'set_encryption_level'):
            self.bot.set_encryption_level(e2ee_level)
        
        # Configure authorized users
        authorized_users = os.getenv('AUTHORIZED_USERS', '').split(',')
        authorized_users = [user.strip() for user in authorized_users if user.strip()]
        if authorized_users and hasattr(self.bot, 'set_authorized_users'):
            self.bot.set_authorized_users(authorized_users)
            self.logger.info(f"✅ Configured {len(authorized_users)} authorized users")
        
        # Configure CEMOS-specific commands
        await self.setup_cemos_commands()
        
        self.logger.info("✅ CEMOS features configured")
    
    async def setup_cemos_commands(self):
        """Setup CEMOS-specific commands"""
        cemos_commands = {
            "!cemos status": "Check CEMOS system status",
            "!cemos security": "Security audit and status",
            "!cemos encrypt": "Encrypt CEMOS data",
            "!cemos decrypt": "Decrypt CEMOS data",
            "!cemos backup": "Secure backup operations",
            "!cemos analyze": "Analyze CEMOS data",
            "!cemos report": "Generate CEMOS reports",
            "!cemos emergency": "Emergency operations"
        }
        
        if hasattr(self.bot, 'register_custom_commands'):
            self.bot.register_custom_commands(cemos_commands)
            self.logger.info(f"✅ Registered {len(cemos_commands)} CEMOS commands")
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.bot and hasattr(self.bot, 'close'):
            await self.bot.close()
        self.logger.info("🧹 CEMOS bot cleanup completed")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="CEMOS Secure Matrix Bot with E2EE",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_cemos_secure_bot.py
  python start_cemos_secure_bot.py --config .env.cemos
  python start_cemos_secure_bot.py --debug --config .env.production
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        default='.env',
        help='Configuration file path (default: .env)'
    )
    
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '--log-file', '-l',
        help='Log file path (optional)'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_file = args.log_file or os.getenv('LOG_FILE')
    setup_logging(debug=args.debug, log_file=log_file)
    
    logger = logging.getLogger(__name__)
    
    # Print startup banner
    print("🎪" + "="*58 + "🎪")
    print("🎪  CEMOS Secure Matrix Bot with E2EE Integration  🎪")
    print("🎪  Powered by Ribit 2.0 AI Consciousness           🎪") 
    print("🎪  circus365/cemos project                         🎪")
    print("🎪" + "="*58 + "🎪")
    print()
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8+ required")
        sys.exit(1)
    
    # Check configuration file
    if not os.path.exists(args.config):
        logger.warning(f"⚠️  Configuration file {args.config} not found")
        logger.info("Create .env file from .env.cemos.example template")
    
    # Start CEMOS bot
    try:
        cemos_bot = CEMOSSecureBot(config_file=args.config)
        asyncio.run(cemos_bot.start())
    except KeyboardInterrupt:
        logger.info("🛑 CEMOS bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Failed to start CEMOS bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
