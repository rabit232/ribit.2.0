"""
Settings Manager for Chatbot
Handles runtime configuration changes for authorized users
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class SettingsManager:
    """Manages bot settings and configuration"""
    
    def __init__(self):
        self.settings_file = os.getenv("SETTINGS_FILE_PATH", "./settings.json")
        self.persistence_enabled = os.getenv("ENABLE_SETTINGS_MANAGEMENT", "true").lower() == "true"
        
        # Authorized users for each platform
        self.authorized_users = {
            'matrix': os.getenv("SETTINGS_AUTHORIZED_MATRIX_USERS", "").split(",") if os.getenv("SETTINGS_AUTHORIZED_MATRIX_USERS") else [],
            'discord': os.getenv("SETTINGS_AUTHORIZED_DISCORD_USERS", "").split(",") if os.getenv("SETTINGS_AUTHORIZED_DISCORD_USERS") else [],
            'telegram': os.getenv("SETTINGS_AUTHORIZED_TELEGRAM_USERS", "").split(",") if os.getenv("SETTINGS_AUTHORIZED_TELEGRAM_USERS") else []
        }
        
        # Load persisted settings if available
        self.runtime_settings = self.load_settings()
        
        # Initialize invite whitelist from environment or saved settings
        self.invite_whitelist = self.runtime_settings.get('invite_whitelist', [])
        if not self.invite_whitelist:
            env_whitelist = os.getenv("ALLOWED_INVITE_USERS", "")
            if env_whitelist:
                self.invite_whitelist = env_whitelist.split(",")
        
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
            # Include invite whitelist in saved settings
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
        
    def get_setting_value(self, setting_name: str) -> Any:
        """Get the current value of a setting"""
        # Check runtime settings first
        if setting_name in self.runtime_settings:
            return self.runtime_settings[setting_name]
            
        # Fall back to environment variable for specific settings
        env_mappings = {
            'main_llm': 'OPENROUTER_MODEL' if os.getenv('LLM_PROVIDER', 'openrouter').lower() == 'openrouter' else 'OLLAMA_MODEL',
            'fallback_llm': 'OPENROUTER_FALLBACK_MODEL',
            'auto_invite': 'ENABLE_AUTO_INVITE',
            'meme_generator': 'ENABLE_MEME_GENERATION',
            'web_search': 'ENABLE_WEB_SEARCH',
            # Note: price_tracking and stock_market removed from here - they use env vars directly
        }
        
        if setting_name in env_mappings:
            env_value = os.getenv(env_mappings[setting_name])
            if env_value is not None:
                if setting_name in ['auto_invite', 'meme_generator', 'web_search']:
                    return env_value.lower() == 'true'
                return env_value
                
        return None
    
    def is_meme_enabled(self) -> bool:
        """Check if meme generation is currently enabled"""
        # Check runtime settings first
        if 'meme_generator' in self.runtime_settings:
            return self.runtime_settings['meme_generator']
        
        # Fall back to environment variable
        return os.getenv('ENABLE_MEME_GENERATION', 'true').lower() == 'true'
    
    def is_web_search_enabled(self) -> bool:
        """Check if web search is currently enabled"""
        # Check runtime settings first
        if 'web_search' in self.runtime_settings:
            return self.runtime_settings['web_search']
        
        # Fall back to environment variable (default to true if not set)
        return os.getenv('ENABLE_WEB_SEARCH', 'true').lower() == 'true'
    
    def is_auto_invite_enabled(self) -> bool:
        """Check if auto invite is currently enabled"""
        # Check runtime settings first
        if 'auto_invite' in self.runtime_settings:
            return self.runtime_settings['auto_invite']
        
        # Fall back to environment variable
        return os.getenv('ENABLE_AUTO_INVITE', 'true').lower() == 'true'
    
    def is_price_tracking_enabled(self) -> bool:
        """Check if price tracking is currently enabled"""
        # Always use environment variable directly
        return os.getenv('ENABLE_PRICE_TRACKING', 'true').lower() == 'true'
    
    def is_stock_market_enabled(self) -> bool:
        """Check if stock market data is currently enabled"""
        # Always use environment variable directly
        return os.getenv('ENABLE_STOCK_MARKET', 'true').lower() == 'true'
        
    def update_setting(self, setting_name: str, value: Any) -> tuple[bool, str]:
        """Update a setting value"""
        
        # Handle main LLM model
        if setting_name == 'main_llm':
            self.runtime_settings['main_llm'] = value
            # Update appropriate environment variable based on provider
            if os.getenv('LLM_PROVIDER', 'openrouter').lower() == 'openrouter':
                os.environ['OPENROUTER_MODEL'] = str(value)
            else:
                os.environ['OLLAMA_MODEL'] = str(value)
            self.save_settings()
            return True, f"Main LLM model updated to: {value}"
            
        # Handle fallback LLM model
        elif setting_name == 'fallback_llm':
            self.runtime_settings['fallback_llm'] = value
            os.environ['OPENROUTER_FALLBACK_MODEL'] = str(value)
            self.save_settings()
            return True, f"Fallback LLM model updated to: {value}"
            
        # Handle auto invite toggle
        elif setting_name == 'auto_invite':
            if isinstance(value, str):
                value = value.lower() in ['true', 'on', 'enable', 'enabled', '1', 'yes']
            self.runtime_settings['auto_invite'] = value
            os.environ['ENABLE_AUTO_INVITE'] = 'true' if value else 'false'
            self.save_settings()
            return True, f"Auto invite {'enabled' if value else 'disabled'}"
            
        # Handle meme generator toggle
        elif setting_name == 'meme_generator':
            if isinstance(value, str):
                value = value.lower() in ['true', 'on', 'enable', 'enabled', '1', 'yes']
            self.runtime_settings['meme_generator'] = value
            os.environ['ENABLE_MEME_GENERATION'] = 'true' if value else 'false'
            self.save_settings()
            return True, f"Meme generator {'enabled' if value else 'disabled'}"
            
        # Handle web search toggle
        elif setting_name == 'web_search':
            if isinstance(value, str):
                value = value.lower() in ['true', 'on', 'enable', 'enabled', '1', 'yes']
            self.runtime_settings['web_search'] = value
            os.environ['ENABLE_WEB_SEARCH'] = 'true' if value else 'false'
            self.save_settings()
            return True, f"Web search {'enabled' if value else 'disabled'}"
            
        # Note: Removed price_tracking and stock_market from here - they use env vars directly
            
        else:
            return False, f"Unknown setting: {setting_name}"
            
    def manage_whitelist(self, action: str, username: str) -> tuple[bool, str]:
        """Add or remove users from invite whitelist"""
        username = username.strip()
        
        if action == 'add':
            if username not in self.invite_whitelist:
                self.invite_whitelist.append(username)
                # Update environment variable
                os.environ['ALLOWED_INVITE_USERS'] = ','.join(self.invite_whitelist)
                self.save_settings()
                return True, f"Added '{username}' to invite whitelist"
            else:
                return False, f"'{username}' is already in the invite whitelist"
                
        elif action == 'remove':
            if username in self.invite_whitelist:
                self.invite_whitelist.remove(username)
                # Update environment variable
                os.environ['ALLOWED_INVITE_USERS'] = ','.join(self.invite_whitelist)
                self.save_settings()
                return True, f"Removed '{username}' from invite whitelist"
            else:
                return False, f"'{username}' is not in the invite whitelist"
                
        else:
            return False, f"Invalid whitelist action: {action}"
            
    async def handle_setting_command(self, args: List[str], user_id: str, platform: str) -> str:
        """Handle setting command from users"""
        
        # Check if settings management is enabled
        if not self.persistence_enabled:
            return "⚠️ Settings management is currently disabled."
            
        # Check authorization
        if not self.is_authorized(user_id, platform):
            return "❌ You are not authorized to manage settings."
            
        # Parse command
        if not args or args[0] == 'help':
            return self.get_help_text()
            
        if args[0] == 'list':
            return self.get_settings_list()
            
        # Handle whitelist management
        if args[0] == 'whitelist':
            if len(args) < 3:
                return "❌ Invalid syntax. Use: `?setting whitelist add/remove <username>`"
            action = args[1].lower()
            username = ' '.join(args[2:])
            success, message = self.manage_whitelist(action, username)
            return f"✅ {message}" if success else f"❌ {message}"
            
        # Handle other settings
        if len(args) < 2:
            return "❌ Invalid syntax. Use: `?setting <name> <value>` or `?setting help`"
            
        setting_name = args[0].lower()
        value = ' '.join(args[1:])
        
        # Map user-friendly names to internal setting names
        setting_map = {
            'main_llm': 'main_llm',
            'main': 'main_llm',
            'llm': 'main_llm',
            'model': 'main_llm',
            'fallback_llm': 'fallback_llm',
            'fallback': 'fallback_llm',
            'auto_invite': 'auto_invite',
            'autoinvite': 'auto_invite',
            'invite': 'auto_invite',
            'meme': 'meme_generator',
            'memes': 'meme_generator',
            'meme_generator': 'meme_generator',
            'web': 'web_search',
            'search': 'web_search',
            'web_search': 'web_search',
            'websearch': 'web_search',
            # Note: Removed price and stock settings from here
        }
        
        # Check if user is trying to set price or stock settings
        if setting_name in ['price', 'prices', 'price_tracking', 'pricetracking', 'crypto',
                           'stock', 'stocks', 'stock_market', 'stockmarket', 'stock_tracking', 
                           'stocktracking', 'stonks']:
            return f"❌ {setting_name} is controlled by environment variables and cannot be changed at runtime. Please update your .env file and restart the bot."
        
        if setting_name not in setting_map:
            return f"❌ Unknown setting: {setting_name}. Use `?setting help` to see available settings."
            
        # Update the setting
        success, message = self.update_setting(setting_map[setting_name], value)
        
        if success:
            return f"✅ {message}"
        else:
            return f"❌ {message}"
            
    def get_help_text(self) -> str:
        """Get help text for settings management"""
        help_text = """**⚙️ Settings Management (Authorized Users Only)**

**Available Commands:**
• `?setting help` - Show this help message
• `?setting list` - Display current settings values
• `?setting <name> <value>` - Update a setting

**Configurable Settings:**

• **main_llm** (or: main, llm, model) - Change the main LLM model
  Example: `?setting main_llm gpt-4`
  
• **fallback_llm** (or: fallback) - Change the fallback LLM model
  Example: `?setting fallback_llm gpt-3.5-turbo`
  
• **auto_invite** (or: autoinvite, invite) - Toggle auto-accepting room invites
  Values: true/false, on/off, enable/disable
  Example: `?setting auto_invite false`
  
• **meme_generator** (or: meme, memes) - Toggle meme generation feature
  Values: true/false, on/off, enable/disable
  Example: `?setting meme on`
  
• **web_search** (or: web, search, websearch) - Toggle web search feature
  Values: true/false, on/off, enable/disable
  Example: `?setting web_search enable`

**Whitelist Management:**
• `?setting whitelist add <username>` - Add user to invite whitelist
• `?setting whitelist remove <username>` - Remove user from invite whitelist

Example: `?setting whitelist add @user:matrix.org`

**Note:** Price tracking and stock market features are controlled by environment variables and cannot be changed at runtime."""
        
        return help_text
        
    def get_settings_list(self) -> str:
        """Get a formatted list of all settings and their values"""
        settings_text = "**⚙️ Current Settings**\n\n"
        
        # Main LLM
        main_llm = self.get_setting_value('main_llm')
        provider = os.getenv('LLM_PROVIDER', 'openrouter')
        settings_text += f"• **Main LLM Model** ({provider}): `{main_llm if main_llm else 'not set'}`\n"
        
        # Fallback LLM
        fallback_llm = self.get_setting_value('fallback_llm')
        settings_text += f"• **Fallback LLM Model**: `{fallback_llm if fallback_llm else 'not set'}`\n"
        
        # Auto invite
        auto_invite = self.is_auto_invite_enabled()
        settings_text += f"• **Auto Invite**: `{'enabled' if auto_invite else 'disabled'}`\n"
        
        # Meme generator
        meme_gen = self.is_meme_enabled()
        settings_text += f"• **Meme Generator**: `{'enabled' if meme_gen else 'disabled'}`\n"
        
        # Web search
        web_search = self.is_web_search_enabled()
        settings_text += f"• **Web Search**: `{'enabled' if web_search else 'disabled'}`\n"
        
        # Price tracking (from env var)
        price_tracking = self.is_price_tracking_enabled()
        settings_text += f"• **Price Tracking**: `{'enabled' if price_tracking else 'disabled'}` (env var)\n"
        
        # Stock market (from env var)
        stock_market = self.is_stock_market_enabled()
        settings_text += f"• **Stock Market Data**: `{'enabled' if stock_market else 'disabled'}` (env var)\n"
        
        # Invite whitelist
        settings_text += f"\n**Invite Whitelist** ({len(self.invite_whitelist)} users):\n"
        if self.invite_whitelist:
            for user in self.invite_whitelist:
                settings_text += f"  • {user}\n"
        else:
            settings_text += "  _Empty - all users can invite the bot_\n"
                
        return settings_text

# Create singleton instance
settings_manager = SettingsManager()
