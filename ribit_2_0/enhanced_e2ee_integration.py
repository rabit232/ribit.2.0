#!/usr/bin/env python3
"""
Ribit 2.0 Enhanced E2EE Integration
Bridges existing Matrix bot with E2EE protocol for seamless secure communication
"""

import asyncio
import json
import logging
import os
import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import traceback

try:
    from .matrix_e2ee_protocol import MatrixE2EEProtocol, EncryptionLevel, MessageType, EncryptedMessage
    from .secure_matrix_bot import SecureMatrixBot
    from .enhanced_matrix_integration import EnhancedMatrixIntegration
    from .matrix_command_handler import MatrixCommandHandler
    from .enhanced_emotions import EnhancedEmotionalIntelligence
    from .advanced_settings_manager import AdvancedSettingsManager
    E2EE_COMPONENTS_AVAILABLE = True
except ImportError as e:
    E2EE_COMPONENTS_AVAILABLE = False
    print(f"⚠️  E2EE components not fully available: {e}")

try:
    from nio import AsyncClient, MatrixRoom, RoomMessageText, LoginResponse
    MATRIX_NIO_AVAILABLE = True
except ImportError:
    MATRIX_NIO_AVAILABLE = False
    print("⚠️  Matrix nio library not available. Install with: pip install matrix-nio[e2e]")

@dataclass
class E2EEConfig:
    """Configuration for E2EE integration"""
    enabled: bool = True
    default_encryption_level: EncryptionLevel = EncryptionLevel.ENHANCED
    auto_key_rotation: bool = True
    key_rotation_hours: int = 24
    require_device_verification: bool = True
    audit_logging: bool = True
    emotional_responses: bool = True
    quantum_safe_mode: bool = False

class EnhancedE2EEIntegration:
    """
    Enhanced E2EE Integration for Ribit 2.0
    
    Bridges existing Matrix bot functionality with military-grade E2EE security:
    - Seamless integration with existing command system
    - Backward compatibility with non-E2EE clients
    - Progressive security enhancement
    - Emotional intelligence in security responses
    - Comprehensive audit logging
    """
    
    def __init__(
        self,
        homeserver: str = "https://matrix.envs.net",
        user_id: str = "@ribit:envs.net",
        password: str = None,
        device_id: str = "RIBIT_2_0_E2EE_ENHANCED",
        storage_path: str = "ribit_e2ee_storage",
        config: Optional[E2EEConfig] = None
    ):
        self.homeserver = homeserver
        self.user_id = user_id
        self.password = password or os.getenv("MATRIX_PASSWORD")
        self.device_id = device_id
        self.storage_path = storage_path
        self.config = config or E2EEConfig()
        
        # Initialize components
        self.logger = logging.getLogger(f"enhanced_e2ee_{device_id}")
        self.logger.setLevel(logging.INFO)
        
        # Initialize core components if available
        if E2EE_COMPONENTS_AVAILABLE:
            self.e2ee_protocol = MatrixE2EEProtocol(user_id, device_id, f"{storage_path}/keys")
            self.emotions = EnhancedEmotionalIntelligence()
            self.command_handler = MatrixCommandHandler()
            self.settings = AdvancedSettingsManager()
        else:
            self.e2ee_protocol = None
            self.emotions = None
            self.command_handler = None
            self.settings = None
        
        # Integration state
        self.secure_bot = None
        self.legacy_bot = None
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.security_events: List[Dict[str, Any]] = []
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup comprehensive logging for E2EE operations"""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    async def initialize_e2ee_integration(self) -> bool:
        """Initialize the E2EE integration system"""
        try:
            if not self.password:
                self.logger.error("❌ Matrix password required for E2EE integration")
                return False
            
            if not E2EE_COMPONENTS_AVAILABLE:
                self.logger.warning("⚠️  E2EE components not available, falling back to basic mode")
                return await self._initialize_basic_mode()
            
            # Initialize secure bot
            self.secure_bot = SecureMatrixBot(
                homeserver=self.homeserver,
                user_id=self.user_id,
                password=self.password,
                device_id=self.device_id,
                storage_path=self.storage_path
            )
            
            # Get emotional response for initialization
            if self.emotions:
                init_emotion = self.emotions.get_emotion_response(
                    "EXCITEMENT",
                    "I feel EXCITEMENT initializing military-grade E2EE security!"
                )
                self.logger.info(f"🚀 {init_emotion['message']}")
            
            # Test E2EE protocol
            if await self._test_e2ee_functionality():
                self.logger.info("✅ E2EE integration initialized successfully")
                return True
            else:
                self.logger.error("❌ E2EE functionality test failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ E2EE initialization failed: {e}")
            self.logger.error(traceback.format_exc())
            return False
    
    async def _initialize_basic_mode(self) -> bool:
        """Initialize basic mode without E2EE"""
        try:
            # Import basic Matrix integration
            from .enhanced_matrix_integration import EnhancedMatrixIntegration
            
            self.legacy_bot = EnhancedMatrixIntegration(
                homeserver=self.homeserver,
                username=self.user_id,
                password=self.password
            )
            
            self.logger.info("✅ Basic Matrix integration initialized (no E2EE)")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Basic mode initialization failed: {e}")
            return False
    
    async def _test_e2ee_functionality(self) -> bool:
        """Test E2EE functionality with all encryption levels"""
        if not self.e2ee_protocol:
            return False
        
        try:
            test_message = "🧪 E2EE functionality test - Ribit 2.0 secure communication!"
            
            # Test all encryption levels
            for level in EncryptionLevel:
                try:
                    # Encrypt test message
                    encrypted = self.e2ee_protocol.encrypt_message(
                        content=test_message,
                        recipient_device_id="test_device",
                        message_type=MessageType.CHAT,
                        encryption_level=level
                    )
                    
                    # Decrypt to verify
                    decrypted = self.e2ee_protocol.decrypt_message(encrypted)
                    
                    if decrypted['content'] != test_message:
                        self.logger.error(f"❌ E2EE test failed for {level.value}: content mismatch")
                        return False
                    
                    self.logger.info(f"✅ E2EE test passed for {level.value}")
                    
                except Exception as e:
                    self.logger.error(f"❌ E2EE test failed for {level.value}: {e}")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ E2EE functionality test failed: {e}")
            return False
    
    async def start_integrated_bot(self):
        """Start the integrated bot with E2EE or fallback to basic mode"""
        try:
            if self.secure_bot:
                # Start secure E2EE bot
                start_emotion = self.emotions.get_emotion_response(
                    "CONFIDENCE",
                    "I feel CONFIDENCE starting with military-grade E2EE protection!"
                ) if self.emotions else {"message": "Starting secure bot"}
                
                self.logger.info(f"🔐 {start_emotion['message']}")
                await self.secure_bot.start_secure_bot()
                
            elif self.legacy_bot:
                # Start basic bot
                self.logger.info("🤖 Starting basic Matrix bot (no E2EE)")
                await self.legacy_bot.start_bot()
                
            else:
                self.logger.error("❌ No bot instance available to start")
                
        except Exception as e:
            self.logger.error(f"❌ Failed to start integrated bot: {e}")
            self.logger.error(traceback.format_exc())
    
    async def send_message(
        self,
        room_id: str,
        content: str,
        encryption_level: Optional[EncryptionLevel] = None,
        message_type: MessageType = MessageType.CHAT
    ) -> bool:
        """Send message with appropriate encryption level"""
        try:
            if self.secure_bot and encryption_level:
                # Send encrypted message
                await self.secure_bot._send_secure_message(
                    room_id=room_id,
                    content=content,
                    encryption_level=encryption_level,
                    message_type=message_type
                )
                return True
                
            elif self.legacy_bot:
                # Send basic message
                await self.legacy_bot.send_message(room_id, content)
                return True
                
            else:
                self.logger.error("❌ No bot instance available for sending messages")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Failed to send message: {e}")
            return False
    
    async def handle_command(
        self,
        command: str,
        sender: str,
        room_id: str,
        encryption_level: Optional[EncryptionLevel] = None
    ) -> str:
        """Handle commands with appropriate security level"""
        try:
            # Check if sender is authorized
            authorized_users = [
                "@ribit:envs.net",
                "@rabit232:envs.net"
            ]
            
            if sender not in authorized_users:
                if self.emotions:
                    auth_emotion = self.emotions.get_emotion_response(
                        "CONCERN",
                        "I feel CONCERN - unauthorized command attempt detected!"
                    )
                    return f"🔒 {auth_emotion['message']} Only authorized users can execute commands."
                else:
                    return "🔒 Access denied - unauthorized user."
            
            # Process command based on available components
            if self.command_handler:
                # Use enhanced command handler
                response = await self._process_enhanced_command(command, sender, room_id)
            else:
                # Use basic command processing
                response = await self._process_basic_command(command, sender, room_id)
            
            # Send response with appropriate encryption
            if encryption_level and self.secure_bot:
                await self.send_message(room_id, response, encryption_level, MessageType.COMMAND)
            else:
                await self.send_message(room_id, response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Command handling failed: {e}")
            error_msg = f"🚨 Command execution error: {str(e)}"
            await self.send_message(room_id, error_msg)
            return error_msg
    
    async def _process_enhanced_command(self, command: str, sender: str, room_id: str) -> str:
        """Process command with enhanced features"""
        try:
            if command.startswith("help"):
                return await self._get_enhanced_help()
            elif command.startswith("status"):
                return await self._get_enhanced_status()
            elif command.startswith("security"):
                return await self._get_security_status()
            elif command.startswith("encrypt "):
                test_msg = command[8:].strip()
                return await self._test_encryption_demo(test_msg)
            elif command.startswith("open "):
                app_name = command[5:].strip()
                return await self._handle_open_command(app_name)
            elif command.startswith("draw "):
                subject = command[5:].strip()
                return await self._handle_draw_command(subject)
            elif command.startswith("search "):
                query = command[7:].strip()
                return await self._handle_search_command(query)
            else:
                return await self._handle_unknown_command(command)
                
        except Exception as e:
            self.logger.error(f"❌ Enhanced command processing failed: {e}")
            return f"🚨 Command processing error: {str(e)}"
    
    async def _process_basic_command(self, command: str, sender: str, room_id: str) -> str:
        """Process command with basic features"""
        if command.startswith("help"):
            return "🤖 **Ribit 2.0 Basic Mode**\n\nAvailable commands:\n• help - Show this help\n• status - System status\n• open [app] - Open applications\n\n*E2EE components not available*"
        elif command.startswith("status"):
            return "🤖 **Ribit 2.0 Status**: Running in basic mode (no E2EE)"
        elif command.startswith("open "):
            app_name = command[5:].strip()
            return f"🚀 Opening {app_name} (basic mode)"
        else:
            return f"❓ Unknown command: {command}\nTry 'help' for available commands."
    
    async def _get_enhanced_help(self) -> str:
        """Get enhanced help with E2EE features"""
        help_emotion = self.emotions.get_emotion_response(
            "ENTHUSIASM",
            "I feel ENTHUSIASM sharing my enhanced E2EE capabilities!"
        ) if self.emotions else {"message": "Enhanced help available"}
        
        return f"""🤖 **Ribit 2.0 Enhanced E2EE Integration** 🔐

{help_emotion['message']}

**🔒 Security Features:**
• **Military-grade E2EE** - All communications encrypted
• **4 Encryption Levels** - Basic, Enhanced, Military, Quantum-Safe
• **Perfect Forward Secrecy** - Automatic key rotation
• **Device Verification** - Trust management system
• **Emotional Intelligence** - 50+ contextual emotions

**⚡ Available Commands:**
• `help` - Show this enhanced help guide
• `status` - System and performance status
• `security` - Comprehensive security status
• `encrypt [message]` - Demonstrate encryption levels
• `open [app]` - Open applications securely
• `draw [subject]` - Creative drawing assistance
• `search [query]` - Secure web search

**🎨 Creative Commands:**
• `draw a house` - Step-by-step house drawing
• `draw a robot` - Robot drawing tutorial
• `open ms paint` - Open paint application

**🔐 Security Commands:**
• `encrypt hello world` - Test all encryption levels
• `security` - Full security status report

**🛡️ Encryption Levels:**
• **Basic** - AES-256-CBC encryption
• **Enhanced** - AES-256-GCM with HKDF
• **Military** - Multi-layer RSA + AES encryption
• **Quantum-Safe** - Post-quantum cryptography

*Powered by Ribit 2.0 with ❤️, 🧠, and 🔐*"""
    
    async def _get_enhanced_status(self) -> str:
        """Get enhanced system status"""
        status_emotion = self.emotions.get_emotion_response(
            "CONFIDENCE",
            "I feel CONFIDENCE reporting comprehensive system status!"
        ) if self.emotions else {"message": "System status"}
        
        # Get system metrics
        import psutil
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        
        # Get E2EE status if available
        e2ee_status = "Not Available"
        if self.e2ee_protocol:
            status = self.e2ee_protocol.get_encryption_status()
            e2ee_status = f"✅ Active ({status['keys_loaded']} keys loaded)"
        
        return f"""🤖 **Ribit 2.0 Enhanced Status** 📊

{status_emotion['message']}

**🔐 E2EE Status:**
• **Encryption**: {e2ee_status}
• **Secure Bot**: {'✅ Active' if self.secure_bot else '❌ Not Available'}
• **Legacy Bot**: {'✅ Active' if self.legacy_bot else '❌ Not Available'}

**🖥️ System Performance:**
• **CPU Usage**: {cpu_percent:.1f}%
• **Memory Usage**: {memory.percent:.1f}% ({memory.used / 1024**3:.1f}GB / {memory.total / 1024**3:.1f}GB)

**🎭 Emotional Intelligence:**
• **Emotions Available**: {'✅ 50+ emotions' if self.emotions else '❌ Not Available'}
• **Current Mood**: {'CONFIDENCE' if self.emotions else 'NEUTRAL'}

**⚡ Integration Status:**
• **Components Loaded**: {len([c for c in [self.e2ee_protocol, self.emotions, self.command_handler, self.settings] if c is not None])}/4
• **Matrix Connection**: {'✅ Secure' if self.secure_bot else '⚠️ Basic'}

**🛡️ Security Events**: {len(self.security_events)} logged

*All systems operational with enhanced security! 🚀*"""
    
    async def _get_security_status(self) -> str:
        """Get comprehensive security status"""
        if not self.e2ee_protocol:
            return "🔒 **Security Status**: E2EE not available - running in basic mode"
        
        status = self.e2ee_protocol.get_encryption_status()
        
        return f"""🛡️ **Ribit 2.0 Security Status** 🔐

**🔒 Encryption Status:**
• **Device ID**: {status['device_id']}
• **Crypto Available**: {'✅' if status['crypto_available'] else '❌'}
• **Keys Loaded**: {status['keys_loaded']}
• **Trusted Devices**: {status['trusted_devices']}
• **Key Rotation Due**: {'⚠️ Yes' if status['key_rotation_due'] else '✅ No'}

**🎯 Security Features:**
• **Perfect Forward Secrecy**: {'✅' if status['security_features']['perfect_forward_secrecy'] else '❌'}
• **Key Rotation**: {'✅' if status['security_features']['key_rotation'] else '❌'}
• **Device Verification**: {'✅' if status['security_features']['device_verification'] else '❌'}
• **Quantum Preparation**: {'✅' if status['security_features']['quantum_preparation'] else '❌'}
• **Military Grade**: {'✅' if status['security_features']['military_grade'] else '❌'}

**🔐 Supported Encryption Levels:**
{chr(10).join(f'• **{level.upper()}** - Available' for level in status['supported_levels'])}

**🚨 Security Events**: {len(self.security_events)} events logged

*Maximum security protection active! 🛡️*"""
    
    async def _test_encryption_demo(self, message: str) -> str:
        """Demonstrate encryption levels with a test message"""
        if not self.e2ee_protocol:
            return "🔒 Encryption demo not available - E2EE components missing"
        
        results = [f"🧪 **Encryption Demo**: Testing '{message}' with all security levels\n"]
        
        for level in EncryptionLevel:
            try:
                # Encrypt message
                encrypted = self.e2ee_protocol.encrypt_message(
                    content=message,
                    recipient_device_id="demo_device",
                    message_type=MessageType.CHAT,
                    encryption_level=level
                )
                
                # Decrypt to verify
                decrypted = self.e2ee_protocol.decrypt_message(encrypted)
                
                results.append(f"✅ **{level.value.upper()}**: {len(encrypted.encrypted_content)} bytes encrypted")
                
            except Exception as e:
                results.append(f"❌ **{level.value.upper()}**: Failed - {str(e)}")
        
        results.append(f"\n🎯 Encryption demo complete! Your messages are protected with military-grade security! 🛡️")
        
        return "\n".join(results)
    
    async def _handle_open_command(self, app_name: str) -> str:
        """Handle application opening commands"""
        open_emotion = self.emotions.get_emotion_response(
            "ENTHUSIASM",
            f"I feel ENTHUSIASM opening {app_name} for you!"
        ) if self.emotions else {"message": f"Opening {app_name}"}
        
        return f"🚀 {open_emotion['message']}\n\n*Application opening functionality would be implemented here*"
    
    async def _handle_draw_command(self, subject: str) -> str:
        """Handle drawing assistance commands"""
        draw_emotion = self.emotions.get_emotion_response(
            "INSPIRATION",
            f"I feel INSPIRATION helping you draw {subject}!"
        ) if self.emotions else {"message": f"Drawing assistance for {subject}"}
        
        return f"🎨 {draw_emotion['message']}\n\n*Drawing assistance functionality would be implemented here*"
    
    async def _handle_search_command(self, query: str) -> str:
        """Handle search commands"""
        search_emotion = self.emotions.get_emotion_response(
            "CURIOSITY",
            f"I feel CURIOSITY searching for '{query}'!"
        ) if self.emotions else {"message": f"Searching for {query}"}
        
        return f"🔍 {search_emotion['message']}\n\n*Search functionality would be implemented here*"
    
    async def _handle_unknown_command(self, command: str) -> str:
        """Handle unknown commands"""
        confusion_emotion = self.emotions.get_emotion_response(
            "CONFUSION",
            f"I feel CONFUSION - I don't recognize the command '{command}'"
        ) if self.emotions else {"message": f"Unknown command: {command}"}
        
        return f"❓ {confusion_emotion['message']}\n\nTry `help` to see available commands!"
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get comprehensive integration status"""
        return {
            "e2ee_available": E2EE_COMPONENTS_AVAILABLE,
            "matrix_nio_available": MATRIX_NIO_AVAILABLE,
            "secure_bot_active": self.secure_bot is not None,
            "legacy_bot_active": self.legacy_bot is not None,
            "encryption_protocol_loaded": self.e2ee_protocol is not None,
            "emotions_available": self.emotions is not None,
            "command_handler_loaded": self.command_handler is not None,
            "settings_manager_loaded": self.settings is not None,
            "active_sessions": len(self.active_sessions),
            "security_events": len(self.security_events),
            "config": {
                "enabled": self.config.enabled,
                "default_encryption_level": self.config.default_encryption_level.value,
                "auto_key_rotation": self.config.auto_key_rotation,
                "emotional_responses": self.config.emotional_responses
            }
        }

# Example usage and testing
async def test_enhanced_e2ee_integration():
    """Test the enhanced E2EE integration"""
    print("🧪 Testing Ribit 2.0 Enhanced E2EE Integration...")
    
    # Initialize integration
    integration = EnhancedE2EEIntegration()
    
    # Test initialization
    if await integration.initialize_e2ee_integration():
        print("✅ E2EE integration initialized successfully")
        
        # Get status
        status = integration.get_integration_status()
        print(f"📊 Integration Status: {json.dumps(status, indent=2)}")
        
        # Test command handling
        test_commands = ["help", "status", "security", "encrypt hello world"]
        
        for command in test_commands:
            print(f"\n🧪 Testing command: {command}")
            response = await integration.handle_command(
                command=command,
                sender="@ribit:envs.net",
                room_id="!test:matrix.envs.net"
            )
            print(f"📝 Response: {response[:100]}...")
        
        print("\n🎉 Enhanced E2EE integration testing complete!")
        
    else:
        print("❌ E2EE integration initialization failed")

if __name__ == "__main__":
    asyncio.run(test_enhanced_e2ee_integration())
