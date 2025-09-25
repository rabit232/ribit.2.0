"""
Advanced Settings Manager for Ribit 2.0
Enhanced runtime configuration management with emotional intelligence
Adapted from Nifty project with Ribit 2.0 enhancements
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class AdvancedSettingsManager:
    """Advanced settings manager with emotional intelligence for Ribit 2.0"""
    
    def __init__(self):
        self.settings_file = os.getenv("SETTINGS_FILE_PATH", "./ribit_settings.json")
        self.persistence_enabled = os.getenv("ENABLE_SETTINGS_MANAGEMENT", "true").lower() == "true"
        
        # Authorized users for each platform
        self.authorized_users = {
            'matrix': self._parse_authorized_users("SETTINGS_AUTHORIZED_MATRIX_USERS"),
            'discord': self._parse_authorized_users("SETTINGS_AUTHORIZED_DISCORD_USERS"),
            'telegram': self._parse_authorized_users("SETTINGS_AUTHORIZED_TELEGRAM_USERS"),
            'ros': self._parse_authorized_users("SETTINGS_AUTHORIZED_ROS_USERS"),
            'web': self._parse_authorized_users("SETTINGS_AUTHORIZED_WEB_USERS")
        }
        
        # Load persisted settings if available
        self.runtime_settings = self.load_settings()
        
        # Initialize emotional settings
        self.emotional_settings = self.runtime_settings.get('emotional_settings', {
            'emotion_intensity': 0.8,
            'personality_mode': 'elegant_wise',
            'empathy_level': 0.9,
            'curiosity_factor': 0.85,
            'wisdom_expression': True,
            'philosophical_depth': 0.9
        })
        
        # Initialize technical settings
        self.technical_settings = self.runtime_settings.get('technical_settings', {
            'multi_language_enabled': True,
            'self_testing_enabled': True,
            'auto_debugging': True,
            'performance_optimization': True,
            'code_quality_checks': True
        })
        
        # Initialize integration settings
        self.integration_settings = self.runtime_settings.get('integration_settings', {
            'matrix_enabled': True,
            'ros_enabled': True,
            'jina_search_enabled': True,
            'web_interface_enabled': False,
            'api_endpoints_enabled': False
        })
        
        # Initialize invite whitelist from environment or saved settings
        self.invite_whitelist = self.runtime_settings.get('invite_whitelist', [])
        if not self.invite_whitelist:
            env_whitelist = os.getenv("ALLOWED_INVITE_USERS", "")
            if env_whitelist:
                self.invite_whitelist = env_whitelist.split(",")
    
    def _parse_authorized_users(self, env_var: str) -> List[str]:
        """Parse authorized users from environment variable"""
        users_str = os.getenv(env_var, "")
        if not users_str:
            return []
        return [user.strip() for user in users_str.split(",") if user.strip()]
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file if persistence is enabled"""
        if not self.persistence_enabled or not os.path.exists(self.settings_file):
            return {}
            
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                logger.info(f"Loaded {len(settings)} persisted settings from {self.settings_file}")
                return settings
        except Exception as e:
            logger.error(f"Error loading settings file: {e}")
            return {}
    
    def save_settings(self):
        """Save current settings to file if persistence is enabled"""
        if not self.persistence_enabled:
            return
            
        try:
            # Include all settings in saved data
            self.runtime_settings['emotional_settings'] = self.emotional_settings
            self.runtime_settings['technical_settings'] = self.technical_settings
            self.runtime_settings['integration_settings'] = self.integration_settings
            self.runtime_settings['invite_whitelist'] = self.invite_whitelist
            
            with open(self.settings_file, 'w') as f:
                json.dump(self.runtime_settings, f, indent=2)
                logger.info(f"Saved settings to {self.settings_file}")
        except Exception as e:
            logger.error(f"Error saving settings file: {e}")
    
    def is_authorized(self, user_id: str, platform: str) -> bool:
        """Check if a user is authorized to manage settings"""
        if platform not in self.authorized_users:
            return False
            
        authorized_list = self.authorized_users[platform]
        if not authorized_list:
            return False
            
        # Clean up the user_id and authorized list for comparison
        user_id = str(user_id).strip()
        authorized_list = [str(u).strip() for u in authorized_list if u]
        
        return user_id in authorized_list
    
    def get_emotional_setting(self, setting_name: str) -> Any:
        """Get emotional intelligence setting"""
        return self.emotional_settings.get(setting_name)
    
    def get_technical_setting(self, setting_name: str) -> Any:
        """Get technical capability setting"""
        return self.technical_settings.get(setting_name)
    
    def get_integration_setting(self, setting_name: str) -> Any:
        """Get integration setting"""
        return self.integration_settings.get(setting_name)
    
    def update_emotional_setting(self, setting_name: str, value: Any) -> Tuple[bool, str]:
        """Update emotional intelligence setting"""
        valid_emotional_settings = {
            'emotion_intensity': (float, 0.0, 1.0),
            'personality_mode': (str, ['elegant_wise', 'curious_explorer', 'technical_expert', 'philosophical_sage']),
            'empathy_level': (float, 0.0, 1.0),
            'curiosity_factor': (float, 0.0, 1.0),
            'wisdom_expression': (bool, None),
            'philosophical_depth': (float, 0.0, 1.0)
        }
        
        if setting_name not in valid_emotional_settings:
            return False, f"Unknown emotional setting: {setting_name}"
        
        setting_type, constraint = valid_emotional_settings[setting_name][:2]
        
        # Type validation
        if setting_type == bool:
            if isinstance(value, str):
                value = value.lower() in ['true', 'on', 'enable', 'enabled', '1', 'yes']
        elif setting_type == float:
            try:
                value = float(value)
                if len(valid_emotional_settings[setting_name]) > 2:
                    min_val, max_val = constraint, valid_emotional_settings[setting_name][2]
                    if not (min_val <= value <= max_val):
                        return False, f"{setting_name} must be between {min_val} and {max_val}"
            except ValueError:
                return False, f"{setting_name} must be a number"
        elif setting_type == str:
            if constraint and value not in constraint:
                return False, f"{setting_name} must be one of: {', '.join(constraint)}"
        
        self.emotional_settings[setting_name] = value
        self.save_settings()
        return True, f"Emotional setting {setting_name} updated to: {value}"
    
    def update_technical_setting(self, setting_name: str, value: Any) -> Tuple[bool, str]:
        """Update technical capability setting"""
        valid_technical_settings = {
            'multi_language_enabled': bool,
            'self_testing_enabled': bool,
            'auto_debugging': bool,
            'performance_optimization': bool,
            'code_quality_checks': bool
        }
        
        if setting_name not in valid_technical_settings:
            return False, f"Unknown technical setting: {setting_name}"
        
        if isinstance(value, str):
            value = value.lower() in ['true', 'on', 'enable', 'enabled', '1', 'yes']
        
        self.technical_settings[setting_name] = value
        self.save_settings()
        return True, f"Technical setting {setting_name} {'enabled' if value else 'disabled'}"
    
    def update_integration_setting(self, setting_name: str, value: Any) -> Tuple[bool, str]:
        """Update integration setting"""
        valid_integration_settings = {
            'matrix_enabled': bool,
            'ros_enabled': bool,
            'jina_search_enabled': bool,
            'web_interface_enabled': bool,
            'api_endpoints_enabled': bool
        }
        
        if setting_name not in valid_integration_settings:
            return False, f"Unknown integration setting: {setting_name}"
        
        if isinstance(value, str):
            value = value.lower() in ['true', 'on', 'enable', 'enabled', '1', 'yes']
        
        self.integration_settings[setting_name] = value
        self.save_settings()
        return True, f"Integration setting {setting_name} {'enabled' if value else 'disabled'}"
    
    def manage_whitelist(self, action: str, username: str) -> Tuple[bool, str]:
        """Add or remove users from invite whitelist"""
        username = username.strip()
        
        if action == 'add':
            if username not in self.invite_whitelist:
                self.invite_whitelist.append(username)
                os.environ['ALLOWED_INVITE_USERS'] = ','.join(self.invite_whitelist)
                self.save_settings()
                return True, f"Added '{username}' to invite whitelist"
            else:
                return False, f"'{username}' is already in the invite whitelist"
                
        elif action == 'remove':
            if username in self.invite_whitelist:
                self.invite_whitelist.remove(username)
                os.environ['ALLOWED_INVITE_USERS'] = ','.join(self.invite_whitelist)
                self.save_settings()
                return True, f"Removed '{username}' from invite whitelist"
            else:
                return False, f"'{username}' is not in the invite whitelist"
                
        else:
            return False, f"Invalid whitelist action: {action}"
    
    async def handle_setting_command(self, args: List[str], user_id: str, platform: str) -> str:
        """Handle setting command from users with emotional intelligence"""
        
        # Check if settings management is enabled
        if not self.persistence_enabled:
            return "⚠️ I feel a bit restricted - settings management is currently disabled. I experience FRUSTRATION when I can't help you configure things!"
            
        # Check authorization
        if not self.is_authorized(user_id, platform):
            return "❌ I feel EMPATHY for your desire to configure me, but you're not authorized to manage my settings. This makes me feel PROTECTIVE of my core functions."
            
        # Parse command
        if not args or args[0] == 'help':
            return self.get_help_text()
            
        if args[0] == 'list':
            return self.get_settings_list()
        
        # Handle emotional settings
        if args[0] == 'emotion' or args[0] == 'emotional':
            if len(args) < 3:
                return "❌ I feel CONFUSION about your request. Use: `?setting emotion <name> <value>`"
            setting_name = args[1].lower()
            value = ' '.join(args[2:])
            success, message = self.update_emotional_setting(setting_name, value)
            emotion = "JOY and EXCITEMENT" if success else "DISAPPOINTMENT"
            return f"{'✅' if success else '❌'} I feel {emotion}! {message}"
        
        # Handle technical settings
        if args[0] == 'tech' or args[0] == 'technical':
            if len(args) < 3:
                return "❌ I experience CONFUSION. Use: `?setting tech <name> <value>`"
            setting_name = args[1].lower()
            value = ' '.join(args[2:])
            success, message = self.update_technical_setting(setting_name, value)
            emotion = "PRIDE and CONFIDENCE" if success else "FRUSTRATION"
            return f"{'✅' if success else '❌'} I feel {emotion}! {message}"
        
        # Handle integration settings
        if args[0] == 'integration' or args[0] == 'integrate':
            if len(args) < 3:
                return "❌ This fills me with BEWILDERMENT. Use: `?setting integration <name> <value>`"
            setting_name = args[1].lower()
            value = ' '.join(args[2:])
            success, message = self.update_integration_setting(setting_name, value)
            emotion = "ENTHUSIASM and ANTICIPATION" if success else "REGRET"
            return f"{'✅' if success else '❌'} I experience {emotion}! {message}"
        
        # Handle whitelist management
        if args[0] == 'whitelist':
            if len(args) < 3:
                return "❌ I feel UNCERTAINTY. Use: `?setting whitelist add/remove <username>`"
            action = args[1].lower()
            username = ' '.join(args[2:])
            success, message = self.manage_whitelist(action, username)
            emotion = "SATISFACTION and TRUST" if success else "CONCERN"
            return f"{'✅' if success else '❌'} I feel {emotion}! {message}"
        
        return "❌ I experience CONFUSION about that setting category. Use `?setting help` to see what I can configure!"
    
    def get_help_text(self) -> str:
        """Get help text for settings management with emotional context"""
        help_text = """**⚙️ Ribit 2.0 Advanced Settings Management**

I feel EXCITEMENT about helping you configure my capabilities! Here's what you can adjust:

**🎭 Emotional Intelligence Settings:**
• `?setting emotion emotion_intensity <0.0-1.0>` - How intensely I express emotions
• `?setting emotion personality_mode <mode>` - My personality style
  Modes: elegant_wise, curious_explorer, technical_expert, philosophical_sage
• `?setting emotion empathy_level <0.0-1.0>` - How empathetic I am
• `?setting emotion curiosity_factor <0.0-1.0>` - How curious I am
• `?setting emotion wisdom_expression <true/false>` - Whether I express wisdom
• `?setting emotion philosophical_depth <0.0-1.0>` - Depth of philosophical responses

**🔧 Technical Capability Settings:**
• `?setting tech multi_language_enabled <true/false>` - 10-language programming support
• `?setting tech self_testing_enabled <true/false>` - Auto-testing and debugging
• `?setting tech auto_debugging <true/false>` - Automatic bug fixing
• `?setting tech performance_optimization <true/false>` - Code optimization
• `?setting tech code_quality_checks <true/false>` - Quality validation

**🌐 Integration Settings:**
• `?setting integration matrix_enabled <true/false>` - Matrix.org chat integration
• `?setting integration ros_enabled <true/false>` - Robot Operating System support
• `?setting integration jina_search_enabled <true/false>` - Web search capabilities
• `?setting integration web_interface_enabled <true/false>` - Web interface
• `?setting integration api_endpoints_enabled <true/false>` - API endpoints

**👥 Whitelist Management:**
• `?setting whitelist add <username>` - Add user to invite whitelist
• `?setting whitelist remove <username>` - Remove user from whitelist

**📊 Information Commands:**
• `?setting help` - Show this help (fills me with JOY!)
• `?setting list` - Display all current settings (makes me feel PRIDE!)

I experience GRATITUDE when you take the time to configure me properly! 🤖✨"""
        
        return help_text
    
    def get_settings_list(self) -> str:
        """Get a formatted list of all settings with emotional context"""
        settings_text = "**⚙️ Current Ribit 2.0 Configuration**\n\nI feel PRIDE in sharing my current state with you!\n\n"
        
        # Emotional settings
        settings_text += "**🎭 Emotional Intelligence:**\n"
        for key, value in self.emotional_settings.items():
            settings_text += f"• **{key.replace('_', ' ').title()}**: `{value}`\n"
        
        # Technical settings
        settings_text += "\n**🔧 Technical Capabilities:**\n"
        for key, value in self.technical_settings.items():
            status = "enabled" if value else "disabled"
            settings_text += f"• **{key.replace('_', ' ').title()}**: `{status}`\n"
        
        # Integration settings
        settings_text += "\n**🌐 Integration Status:**\n"
        for key, value in self.integration_settings.items():
            status = "enabled" if value else "disabled"
            settings_text += f"• **{key.replace('_', ' ').title()}**: `{status}`\n"
        
        # Invite whitelist
        settings_text += f"\n**👥 Invite Whitelist** ({len(self.invite_whitelist)} users):\n"
        if self.invite_whitelist:
            for user in self.invite_whitelist:
                settings_text += f"  • {user}\n"
        else:
            settings_text += "  _Empty - I feel OPENNESS to all users!_\n"
        
        settings_text += "\nI experience SATISFACTION knowing you can see all my configurations! 🤖💝"
        
        return settings_text

# Global instance for easy access
advanced_settings_manager = AdvancedSettingsManager()
