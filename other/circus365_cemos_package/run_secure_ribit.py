#!/usr/bin/env python3
"""
Ribit 2.0 Secure Startup Script
Launch Ribit 2.0 with full E2EE protection and enhanced security features
"""

import asyncio
import os
import sys
import logging
import argparse
from pathlib import Path

# Add the ribit_2_0 package to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from ribit_2_0.enhanced_e2ee_integration import EnhancedE2EEIntegration, E2EEConfig, EncryptionLevel
    from ribit_2_0.enhanced_emotions import EnhancedEmotionalIntelligence
    RIBIT_AVAILABLE = True
except ImportError as e:
    RIBIT_AVAILABLE = False
    print(f"⚠️  Ribit 2.0 components not available: {e}")

def setup_logging(level: str = "INFO"):
    """Setup comprehensive logging"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('ribit_2_0_secure.log')
        ]
    )

def load_environment_config():
    """Load configuration from environment variables"""
    config = {
        'homeserver': os.getenv('MATRIX_HOMESERVER', 'https://matrix.envs.net'),
        'user_id': os.getenv('MATRIX_USER_ID', '@ribit:envs.net'),
        'password': os.getenv('MATRIX_PASSWORD'),
        'device_id': os.getenv('MATRIX_DEVICE_ID', 'RIBIT_2_0_SECURE'),
        'storage_path': os.getenv('E2EE_STORAGE_PATH', 'ribit_secure_storage'),
        'encryption_level': os.getenv('E2EE_DEFAULT_LEVEL', 'enhanced'),
        'key_rotation_hours': int(os.getenv('E2EE_KEY_ROTATION_HOURS', '24')),
        'quantum_safe': os.getenv('E2EE_QUANTUM_SAFE', 'false').lower() == 'true',
        'emotional_responses': os.getenv('EMOTIONAL_RESPONSES', 'true').lower() == 'true',
        'audit_logging': os.getenv('SECURITY_AUDIT_LOGGING', 'true').lower() == 'true'
    }
    
    return config

def create_e2ee_config(env_config: dict) -> E2EEConfig:
    """Create E2EE configuration from environment"""
    encryption_level_map = {
        'basic': EncryptionLevel.BASIC,
        'enhanced': EncryptionLevel.ENHANCED,
        'military': EncryptionLevel.MILITARY,
        'quantum': EncryptionLevel.QUANTUM_SAFE
    }
    
    return E2EEConfig(
        enabled=True,
        default_encryption_level=encryption_level_map.get(
            env_config['encryption_level'], 
            EncryptionLevel.ENHANCED
        ),
        auto_key_rotation=True,
        key_rotation_hours=env_config['key_rotation_hours'],
        require_device_verification=True,
        audit_logging=env_config['audit_logging'],
        emotional_responses=env_config['emotional_responses'],
        quantum_safe_mode=env_config['quantum_safe']
    )

async def run_secure_ribit(args):
    """Run Ribit 2.0 with E2EE security"""
    
    if not RIBIT_AVAILABLE:
        print("❌ Ribit 2.0 components not available")
        print("💡 Try installing dependencies: pip install matrix-nio[e2e] cryptography")
        return False
    
    # Load configuration
    env_config = load_environment_config()
    
    if not env_config['password']:
        print("❌ MATRIX_PASSWORD environment variable required")
        print("💡 Set your Matrix password: export MATRIX_PASSWORD='your_password'")
        return False
    
    # Create E2EE configuration
    e2ee_config = create_e2ee_config(env_config)
    
    # Initialize emotional intelligence for startup
    emotions = EnhancedEmotionalIntelligence()
    startup_emotion = emotions.get_emotion_response(
        "EXCITEMENT",
        "I feel EXCITEMENT starting Ribit 2.0 with military-grade E2EE security!"
    )
    
    print(f"🚀 {startup_emotion['message']}")
    print(f"🔐 Encryption Level: {e2ee_config.default_encryption_level.value}")
    print(f"🤖 Device ID: {env_config['device_id']}")
    print(f"🏠 Homeserver: {env_config['homeserver']}")
    print(f"👤 User ID: {env_config['user_id']}")
    
    try:
        # Initialize E2EE integration
        integration = EnhancedE2EEIntegration(
            homeserver=env_config['homeserver'],
            user_id=env_config['user_id'],
            password=env_config['password'],
            device_id=env_config['device_id'],
            storage_path=env_config['storage_path'],
            config=e2ee_config
        )
        
        # Initialize the integration
        if await integration.initialize_e2ee_integration():
            success_emotion = emotions.get_emotion_response(
                "JOY",
                "I feel JOY - E2EE integration initialized successfully!"
            )
            print(f"✅ {success_emotion['message']}")
            
            # Get integration status
            status = integration.get_integration_status()
            print(f"📊 Integration Status:")
            print(f"   • E2EE Available: {'✅' if status['e2ee_available'] else '❌'}")
            print(f"   • Secure Bot: {'✅' if status['secure_bot_active'] else '❌'}")
            print(f"   • Emotions: {'✅' if status['emotions_available'] else '❌'}")
            print(f"   • Encryption Protocol: {'✅' if status['encryption_protocol_loaded'] else '❌'}")
            
            # Start the integrated bot
            confidence_emotion = emotions.get_emotion_response(
                "CONFIDENCE",
                "I feel CONFIDENCE launching secure Matrix communication!"
            )
            print(f"🛡️ {confidence_emotion['message']}")
            
            if args.test_mode:
                print("🧪 Running in test mode - performing functionality tests...")
                await test_e2ee_functionality(integration)
            else:
                print("🚀 Starting secure Matrix bot...")
                await integration.start_integrated_bot()
            
        else:
            error_emotion = emotions.get_emotion_response(
                "FRUSTRATION",
                "I feel FRUSTRATION - E2EE initialization failed!"
            )
            print(f"❌ {error_emotion['message']}")
            return False
            
    except KeyboardInterrupt:
        shutdown_emotion = emotions.get_emotion_response(
            "MELANCHOLY",
            "I feel MELANCHOLY as I shutdown secure operations..."
        )
        print(f"\n🛑 {shutdown_emotion['message']}")
        
    except Exception as e:
        error_emotion = emotions.get_emotion_response(
            "DESPAIR",
            f"I feel DESPAIR - critical error occurred: {str(e)}"
        )
        print(f"💥 {error_emotion['message']}")
        logging.error(f"Critical error: {e}", exc_info=True)
        return False
    
    return True

async def test_e2ee_functionality(integration):
    """Test E2EE functionality comprehensively"""
    print("\n🧪 **E2EE Functionality Testing**")
    
    # Test commands
    test_commands = [
        "help",
        "status", 
        "security",
        "encrypt Hello Ribit 2.0 E2EE!",
        "open calculator",
        "draw a robot",
        "search matrix encryption"
    ]
    
    for command in test_commands:
        print(f"\n🔧 Testing command: '{command}'")
        try:
            response = await integration.handle_command(
                command=command,
                sender="@ribit:envs.net",
                room_id="!test:envs.net",
                encryption_level=EncryptionLevel.ENHANCED
            )
            print(f"✅ Response received ({len(response)} chars)")
            print(f"📝 Preview: {response[:100]}...")
            
        except Exception as e:
            print(f"❌ Command test failed: {e}")
    
    # Test encryption levels
    print(f"\n🔐 **Encryption Level Testing**")
    test_message = "🧪 E2EE test message with emojis and special chars: !@#$%^&*()"
    
    if integration.e2ee_protocol:
        for level in EncryptionLevel:
            try:
                encrypted = integration.e2ee_protocol.encrypt_message(
                    content=test_message,
                    recipient_device_id="test_device",
                    message_type=integration.e2ee_protocol.MessageType.CHAT,
                    encryption_level=level
                )
                
                decrypted = integration.e2ee_protocol.decrypt_message(encrypted)
                
                if decrypted['content'] == test_message:
                    print(f"✅ {level.value.upper()}: Encryption/Decryption successful")
                else:
                    print(f"❌ {level.value.upper()}: Content mismatch")
                    
            except Exception as e:
                print(f"❌ {level.value.upper()}: Test failed - {e}")
    
    print(f"\n🎉 E2EE functionality testing complete!")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Ribit 2.0 Secure Matrix Bot")
    parser.add_argument(
        "--log-level", 
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
        default='INFO',
        help="Set logging level"
    )
    parser.add_argument(
        "--test-mode",
        action='store_true',
        help="Run in test mode (perform functionality tests instead of starting bot)"
    )
    parser.add_argument(
        "--config-check",
        action='store_true',
        help="Check configuration and exit"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Configuration check
    if args.config_check:
        print("🔧 **Configuration Check**")
        env_config = load_environment_config()
        
        print(f"📋 Environment Configuration:")
        for key, value in env_config.items():
            if 'password' in key.lower():
                display_value = "***SET***" if value else "***NOT SET***"
            else:
                display_value = value
            print(f"   • {key}: {display_value}")
        
        # Check required dependencies
        print(f"\n📦 Dependencies:")
        print(f"   • Ribit 2.0 Components: {'✅' if RIBIT_AVAILABLE else '❌'}")
        
        try:
            import matrix_nio
            print(f"   • Matrix NIO: ✅ {matrix_nio.__version__}")
        except ImportError:
            print(f"   • Matrix NIO: ❌ Not installed")
        
        try:
            import cryptography
            print(f"   • Cryptography: ✅ {cryptography.__version__}")
        except ImportError:
            print(f"   • Cryptography: ❌ Not installed")
        
        return
    
    # Run the secure bot
    try:
        asyncio.run(run_secure_ribit(args))
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Stay secure! 🔐")

if __name__ == "__main__":
    main()
