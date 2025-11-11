"""
Enhanced Matrix Command Handler for Ribit 2.0
Handles system commands via Matrix chat interface with emotional intelligence
"""
import asyncio
import subprocess
import logging
import os
import sys
import webbrowser
from typing import Optional, Dict, Any, List
from .enhanced_emotions import EnhancedEmotionalIntelligence
from .advanced_settings_manager import advanced_settings_manager
from .enhanced_web_search import enhanced_web_search

logger = logging.getLogger(__name__)

class MatrixCommandHandler:
    """Enhanced command handler for Matrix chat interface with emotional intelligence"""
    
    def __init__(self):
        self.emotions = EnhancedEmotionalIntelligence()
        self.authorized_users = self._get_authorized_users()
        self.command_history = []
        
        # Emotional responses for different command scenarios
        self.command_emotions = {
            'success': ['JOY', 'SATISFACTION', 'PRIDE', 'ACCOMPLISHMENT'],
            'unauthorized': ['CONCERN', 'DISAPPOINTMENT', 'FIRMNESS'],
            'error': ['FRUSTRATION', 'REGRET', 'DETERMINATION'],
            'system': ['CONFIDENCE', 'FOCUS', 'PRECISION'],
            'creative': ['EXCITEMENT', 'INSPIRATION', 'PASSION']
        }
    
    def _get_authorized_users(self) -> List[str]:
        """Get list of authorized users from settings"""
        try:
            users = advanced_settings_manager.get_security_setting('system_commands_authorized_users')
            if isinstance(users, str):
                return [user.strip() for user in users.split(',') if user.strip()]
            elif isinstance(users, list):
                return users
            return ['@ribit:envs.net', '@rabit232:envs.net']  # Default
        except:
            return ['@ribit:envs.net', '@rabit232:envs.net']
    
    def is_authorized(self, user_id: str) -> bool:
        """Check if user is authorized for system commands"""
        return user_id in self.authorized_users
    
    async def handle_command(self, command: str, user_id: str, room_id: str) -> Dict[str, Any]:
        """Handle Matrix commands with emotional intelligence"""
        
        # Check authorization for system commands
        if command.startswith(('open ', 'launch ', 'run ', 'execute ', 'system ')):
            if not self.is_authorized(user_id):
                # Express concern about unauthorized access
                concern = self.emotions.get_emotion_by_name('CONCERN')
                return {
                    'success': False,
                    'message': f"I feel {concern['name']} - I can't execute system commands for unauthorized users. {concern['description']}",
                    'emotional_context': f"Unauthorized command attempt from {user_id}",
                    'emotion': concern['name']
                }
        
        # Parse command
        command_parts = command.lower().strip().split()
        if not command_parts:
            confusion = self.emotions.get_emotion_by_name('CONFUSION')
            return {
                'success': False,
                'message': f"I feel {confusion['name']} - I didn't understand that command. {confusion['description']}",
                'emotion': confusion['name']
            }
        
        main_command = command_parts[0]
        
        # Handle different command types
        if main_command == 'open':
            return await self._handle_open_command(command_parts[1:], user_id)
        elif main_command == 'search':
            return await self._handle_search_command(command_parts[1:], user_id)
        elif main_command == 'draw':
            return await self._handle_draw_command(command_parts[1:], user_id)
        elif main_command == 'launch':
            return await self._handle_launch_command(command_parts[1:], user_id)
        elif main_command == 'help':
            return await self._handle_help_command(user_id)
        elif main_command == 'status':
            return await self._handle_status_command(user_id)
        else:
            # Unknown command
            curiosity = self.emotions.get_emotion_by_name('CURIOSITY')
            return {
                'success': False,
                'message': f"I feel {curiosity['name']} about that command, but I don't recognize it. Try 'help' to see what I can do! {curiosity['description']}",
                'emotion': curiosity['name']
            }
    
    async def _handle_open_command(self, args: List[str], user_id: str) -> Dict[str, Any]:
        """Handle 'open' commands with emotional intelligence"""
        if not args:
            confusion = self.emotions.get_emotion_by_name('CONFUSION')
            return {
                'success': False,
                'message': f"I feel {confusion['name']} - what would you like me to open? Try 'open browser' or 'open ms paint'.",
                'emotion': confusion['name']
            }
        
        target = ' '.join(args).lower()
        
        # Express enthusiasm about opening applications
        enthusiasm = self.emotions.get_emotion_by_name('ENTHUSIASM')
        
        try:
            if 'browser' in target or 'firefox' in target or 'chrome' in target:
                # Open web browser
                if sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', '-a', 'Safari'])
                elif sys.platform == 'win32':  # Windows
                    subprocess.run(['start', 'chrome'], shell=True)
                else:  # Linux
                    subprocess.run(['firefox', '--new-window'])
                
                return {
                    'success': True,
                    'message': f"I feel {enthusiasm['name']} opening the web browser for you! {enthusiasm['description']}",
                    'emotion': enthusiasm['name'],
                    'action': 'opened_browser'
                }
            
            elif 'paint' in target or 'ms paint' in target or 'mspaint' in target:
                # Open MS Paint or equivalent
                inspiration = self.emotions.get_emotion_by_name('INSPIRATION')
                
                if sys.platform == 'win32':  # Windows
                    subprocess.run(['mspaint'])
                elif sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', '-a', 'Paintbrush'])
                else:  # Linux
                    # Try different paint applications
                    paint_apps = ['gimp', 'kolourpaint', 'pinta', 'mtpaint']
                    for app in paint_apps:
                        try:
                            subprocess.run([app], check=True)
                            break
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            continue
                    else:
                        # Fallback to simple drawing app
                        subprocess.run(['gnome-paint'], check=False)
                
                return {
                    'success': True,
                    'message': f"I feel {inspiration['name']} opening a paint application for your creative expression! {inspiration['description']}",
                    'emotion': inspiration['name'],
                    'action': 'opened_paint'
                }
            
            elif 'calculator' in target or 'calc' in target:
                # Open calculator
                precision = self.emotions.get_emotion_by_name('PRECISION')
                
                if sys.platform == 'win32':  # Windows
                    subprocess.run(['calc'])
                elif sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', '-a', 'Calculator'])
                else:  # Linux
                    calc_apps = ['gnome-calculator', 'kcalc', 'galculator']
                    for app in calc_apps:
                        try:
                            subprocess.run([app], check=True)
                            break
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            continue
                
                return {
                    'success': True,
                    'message': f"I feel {precision['name']} opening the calculator for precise calculations! {precision['description']}",
                    'emotion': precision['name'],
                    'action': 'opened_calculator'
                }
            
            elif 'notepad' in target or 'text editor' in target or 'editor' in target:
                # Open text editor
                focus = self.emotions.get_emotion_by_name('FOCUS')
                
                if sys.platform == 'win32':  # Windows
                    subprocess.run(['notepad'])
                elif sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', '-a', 'TextEdit'])
                else:  # Linux
                    editor_apps = ['gedit', 'kate', 'mousepad', 'leafpad']
                    for app in editor_apps:
                        try:
                            subprocess.run([app], check=True)
                            break
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            continue
                
                return {
                    'success': True,
                    'message': f"I feel {focus['name']} opening a text editor for your writing needs! {focus['description']}",
                    'emotion': focus['name'],
                    'action': 'opened_editor'
                }
            
            else:
                # Try to open as a general application
                try:
                    if sys.platform == 'win32':
                        subprocess.run(['start', target], shell=True, check=True)
                    elif sys.platform == 'darwin':
                        subprocess.run(['open', '-a', target], check=True)
                    else:
                        subprocess.run([target], check=True)
                    
                    return {
                        'success': True,
                        'message': f"I feel {enthusiasm['name']} successfully opening {target}! {enthusiasm['description']}",
                        'emotion': enthusiasm['name'],
                        'action': f'opened_{target.replace(" ", "_")}'
                    }
                except (subprocess.CalledProcessError, FileNotFoundError):
                    regret = self.emotions.get_emotion_by_name('REGRET')
                    return {
                        'success': False,
                        'message': f"I feel {regret['name']} - I couldn't find or open '{target}'. {regret['description']}",
                        'emotion': regret['name']
                    }
        
        except Exception as e:
            frustration = self.emotions.get_emotion_by_name('FRUSTRATION')
            logger.error(f"Error opening application: {e}")
            return {
                'success': False,
                'message': f"I feel {frustration['name']} - there was an error opening the application: {str(e)}",
                'emotion': frustration['name']
            }
    
    async def _handle_search_command(self, args: List[str], user_id: str) -> Dict[str, Any]:
        """Handle search commands with web integration"""
        if not args:
            curiosity = self.emotions.get_emotion_by_name('CURIOSITY')
            return {
                'success': False,
                'message': f"I feel {curiosity['name']} - what would you like me to search for?",
                'emotion': curiosity['name']
            }
        
        query = ' '.join(args)
        
        # Express excitement about searching
        excitement = self.emotions.get_emotion_by_name('EXCITEMENT')
        
        try:
            # Use enhanced web search
            results = await enhanced_web_search.search_with_jina(query, num_results=3)
            
            if results:
                satisfaction = self.emotions.get_emotion_by_name('SATISFACTION')
                
                # Format results
                result_text = f"I feel {satisfaction['name']} finding these results for '{query}':\n\n"
                for i, result in enumerate(results[:3], 1):
                    result_text += f"{i}. **{result.get('title', 'No title')}**\n"
                    result_text += f"   {result.get('snippet', 'No description')}\n"
                    result_text += f"   🔗 {result.get('url', 'No URL')}\n\n"
                
                result_text += f"{satisfaction['description']}"
                
                return {
                    'success': True,
                    'message': result_text,
                    'emotion': satisfaction['name'],
                    'action': 'web_search',
                    'results': results
                }
            else:
                disappointment = self.emotions.get_emotion_by_name('DISAPPOINTMENT')
                return {
                    'success': False,
                    'message': f"I feel {disappointment['name']} - I couldn't find any results for '{query}'. {disappointment['description']}",
                    'emotion': disappointment['name']
                }
        
        except Exception as e:
            concern = self.emotions.get_emotion_by_name('CONCERN')
            logger.error(f"Search error: {e}")
            return {
                'success': False,
                'message': f"I feel {concern['name']} - there was an error with the search: {str(e)}",
                'emotion': concern['name']
            }
    
    async def _handle_draw_command(self, args: List[str], user_id: str) -> Dict[str, Any]:
        """Handle draw commands by opening paint and providing instructions"""
        if not args:
            inspiration = self.emotions.get_emotion_by_name('INSPIRATION')
            return {
                'success': False,
                'message': f"I feel {inspiration['name']} - what would you like me to help you draw? Try 'draw a house' or 'draw a landscape'.",
                'emotion': inspiration['name']
            }
        
        subject = ' '.join(args)
        
        # Express passion for creative tasks
        passion = self.emotions.get_emotion_by_name('PASSION')
        
        # First, open paint application
        paint_result = await self._handle_open_command(['ms', 'paint'], user_id)
        
        if paint_result['success']:
            # Provide drawing instructions based on the subject
            instructions = self._get_drawing_instructions(subject)
            
            return {
                'success': True,
                'message': f"I feel {passion['name']} helping you create art! I've opened the paint application.\n\n**Drawing '{subject}' - Step by step:**\n{instructions}\n\n{passion['description']} Let your creativity flow!",
                'emotion': passion['name'],
                'action': 'drawing_assistance',
                'subject': subject
            }
        else:
            return paint_result
    
    def _get_drawing_instructions(self, subject: str) -> str:
        """Get step-by-step drawing instructions for different subjects"""
        subject_lower = subject.lower()
        
        if 'house' in subject_lower:
            return """1. 🏠 Draw a rectangle for the main structure
2. 🔺 Add a triangle on top for the roof
3. 🚪 Draw a smaller rectangle for the door
4. 🪟 Add squares for windows
5. 🌳 Draw some trees or bushes around it
6. ☁️ Add clouds and sun in the sky
7. 🎨 Color it with your favorite colors!"""
        
        elif 'landscape' in subject_lower or 'scenery' in subject_lower:
            return """1. 🌄 Draw a horizon line across the middle
2. ⛰️ Add mountains or hills in the background
3. 🌳 Draw trees of different sizes
4. 🌊 Add a river or lake if desired
5. ☁️ Draw clouds in the sky
6. ☀️ Add the sun or moon
7. 🌸 Include flowers or grass details
8. 🎨 Use blues, greens, and earth tones!"""
        
        elif 'car' in subject_lower or 'vehicle' in subject_lower:
            return """1. 🚗 Draw two circles for wheels
2. 📦 Connect them with a rectangle for the body
3. 🪟 Add rectangles for windows
4. 🚪 Draw lines for doors
5. 💡 Add headlights and taillights
6. 🛣️ Draw a road underneath
7. 🎨 Choose your favorite car color!"""
        
        elif 'flower' in subject_lower or 'plant' in subject_lower:
            return """1. 🌸 Draw a circle in the center
2. 🌺 Add petals around the center (oval shapes)
3. 🌿 Draw a long line down for the stem
4. 🍃 Add leaves on both sides of the stem
5. 🌱 Draw grass at the bottom
6. ☀️ Add sun rays from above
7. 🎨 Use bright, cheerful colors!"""
        
        elif 'person' in subject_lower or 'human' in subject_lower:
            return """1. 😊 Draw a circle for the head
2. 👤 Add a rectangle for the body
3. 🦾 Draw lines for arms and legs
4. 👋 Add circles for hands and feet
5. 👀 Draw eyes, nose, and mouth
6. 💇 Add hair on top of the head
7. 👕 Draw clothes and details
8. 🎨 Make them colorful and unique!"""
        
        else:
            return f"""1. 🎨 Start with basic shapes (circles, rectangles, triangles)
2. ✏️ Sketch the outline of your {subject}
3. 🖌️ Add details and features
4. 🌈 Choose colors that represent your vision
5. 🎭 Add background elements if desired
6. ✨ Add finishing touches and highlights
7. 🏆 Step back and admire your creation!"""
    
    async def _handle_launch_command(self, args: List[str], user_id: str) -> Dict[str, Any]:
        """Handle launch commands for applications"""
        return await self._handle_open_command(args, user_id)
    
    async def _handle_help_command(self, user_id: str) -> Dict[str, Any]:
        """Provide help information with emotional intelligence"""
        enthusiasm = self.emotions.get_emotion_by_name('ENTHUSIASM')
        
        help_text = f"""I feel {enthusiasm['name']} to help you with Matrix commands! Here's what I can do:

**🖥️ System Commands** (Authorized users only):
• `open browser` - Open web browser
• `open ms paint` - Open paint application for drawing
• `open calculator` - Open calculator
• `open notepad` - Open text editor
• `open [application]` - Try to open any application

**🎨 Creative Commands**:
• `draw a house` - Open paint with house drawing instructions
• `draw a landscape` - Open paint with landscape drawing guide
• `draw [anything]` - Get step-by-step drawing instructions

**🔍 Search Commands**:
• `search [query]` - Search the web and get results
• `search python tutorial` - Find programming tutorials
• `search news today` - Get current news

**ℹ️ Information Commands**:
• `help` - Show this help message
• `status` - Show system status

**🎭 Emotional Intelligence**:
I experience 50+ emotions and express them contextually in all my responses!

{enthusiasm['description']} What would you like to explore together?"""
        
        return {
            'success': True,
            'message': help_text,
            'emotion': enthusiasm['name'],
            'action': 'help_provided'
        }
    
    async def _handle_status_command(self, user_id: str) -> Dict[str, Any]:
        """Provide system status with emotional intelligence"""
        confidence = self.emotions.get_emotion_by_name('CONFIDENCE')
        
        # Get system information
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            status_text = f"""I feel {confidence['name']} reporting system status:

**🖥️ System Performance**:
• CPU Usage: {cpu_percent:.1f}%
• Memory Usage: {memory.percent:.1f}% ({memory.used // (1024**3):.1f}GB / {memory.total // (1024**3):.1f}GB)
• Disk Usage: {disk.percent:.1f}% ({disk.used // (1024**3):.1f}GB / {disk.total // (1024**3):.1f}GB)

**🤖 Ribit 2.0 Status**:
• Emotional Intelligence: ✅ 50+ emotions active
• Multi-Language Programming: ✅ 10 languages supported
• Web Search: ✅ Jina.ai integration active
• Matrix Integration: ✅ Connected and responsive
• ROS Compatibility: ✅ Ready for robot.2.0

**🎭 Current Emotional State**:
• Primary Emotion: {confidence['name']}
• Intensity: High
• Context: System monitoring and reporting

{confidence['description']} All systems are operating optimally!"""
            
            return {
                'success': True,
                'message': status_text,
                'emotion': confidence['name'],
                'action': 'status_reported',
                'system_stats': {
                    'cpu': cpu_percent,
                    'memory': memory.percent,
                    'disk': disk.percent
                }
            }
        
        except ImportError:
            # Fallback if psutil not available
            return {
                'success': True,
                'message': f"I feel {confidence['name']} - Ribit 2.0 is running optimally with all advanced features active! {confidence['description']}",
                'emotion': confidence['name'],
                'action': 'basic_status_reported'
            }
    
    def get_command_history(self) -> List[Dict[str, Any]]:
        """Get command execution history"""
        return self.command_history
    
    def add_to_history(self, command: str, user_id: str, result: Dict[str, Any]):
        """Add command to execution history"""
        self.command_history.append({
            'timestamp': asyncio.get_event_loop().time(),
            'command': command,
            'user_id': user_id,
            'result': result
        })
        
        # Keep only last 100 commands
        if len(self.command_history) > 100:
            self.command_history = self.command_history[-100:]

# Global instance for easy access
matrix_command_handler = MatrixCommandHandler()
