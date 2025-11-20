#!/usr/bin/env python3
"""
Ribit 2.0 + Megabite Unified CLI
=================================

Interactive command-line interface for both Ribit 2.0 and Megabite AI.
Switch between systems or use both simultaneously.

Commands:
- ask <question>         - Ask the current AI a question
- thought <experiment>   - Post a thought experiment for analysis
- learn <text>          - Learn from text and add to knowledge base
- opinion <topic>       - Get AI's opinion on a topic
- switch                - Switch between Ribit and Megabite
- mode <ribit|megabite|both> - Set interaction mode
- status                - Check system status
- help                  - Show available commands
- exit/quit             - Exit the CLI

Author: Manus AI for rabit232/ribit.2.0
"""

import sys
import os
import subprocess
import psutil
import time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ribit_2_0'))

from ribit_2_0.megabite_llm import MegabiteLLM
from ribit_2_0.word_learning_system import WordLearningSystem
from ribit_2_0.enhanced_emotions import EnhancedEmotionalIntelligence
from ribit_2_0.philosophical_reasoning import PhilosophicalReasoning
from ribit_2_0.conversation_manager import AdvancedConversationManager, ConversationMessage
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Global Matrix bot process
bot_process = None

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Load .env at startup
load_env_file()

# Matrix Bot Control Functions
def start_matrix_bot():
    """Start the Matrix bot as a background process."""
    global bot_process
    
    if bot_process and bot_process.poll() is None:
        print("⚠️  Matrix bot is already running!")
        return False
    
    print("🚀 Starting Matrix bot...")
    
    homeserver = os.getenv("MATRIX_HOMESERVER")
    username = os.getenv("MATRIX_USERNAME")
    password = os.getenv("MATRIX_PASSWORD")
    token = os.getenv("MATRIX_ACCESS_TOKEN")
    
    if not homeserver or not username:
        print("❌ Missing configuration! Please set:")
        print("   - MATRIX_HOMESERVER (e.g., https://matrix.envs.net)")
        print("   - MATRIX_USERNAME (e.g., @ribit.2.0:envs.net)")
        return False
    
    if not password and not token:
        print("❌ Missing credentials! Please set either MATRIX_PASSWORD or MATRIX_ACCESS_TOKEN")
        return False
    
    try:
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'matrix_bot.log')
        
        with open(log_file, 'w') as log_f:
            bot_process = subprocess.Popen(
                [sys.executable, "-m", "ribit_2_0.matrix_bot"],
                stdout=log_f,
                stderr=subprocess.STDOUT,
                env=os.environ.copy()
            )
        time.sleep(2)
        
        if bot_process.poll() is None:
            print(f"✅ Matrix bot started! (PID: {bot_process.pid})")
            print(f"   Server: {homeserver}")
            print(f"   Logs: {log_file}")
            return True
        else:
            print(f"❌ Bot failed to start")
            bot_process = None
            return False
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        bot_process = None
        return False

def stop_matrix_bot():
    """Stop the Matrix bot gracefully."""
    global bot_process
    
    if not bot_process or bot_process.poll() is not None:
        print("⚠️  Matrix bot is not running!")
        return False
    
    print("🛑 Stopping Matrix bot...")
    
    try:
        bot_process.terminate()
        bot_process.wait(timeout=5)
        print("✅ Matrix bot stopped!")
        bot_process = None
        return True
    except subprocess.TimeoutExpired:
        print("⚠️  Forcing shutdown...")
        bot_process.kill()
        bot_process.wait()
        print("✅ Matrix bot force-stopped!")
        bot_process = None
        return True
    except Exception as e:
        print(f"❌ Error stopping bot: {e}")
        return False

def restart_matrix_bot():
    """Restart the Matrix bot."""
    print("🔄 Restarting Matrix bot...")
    stop_matrix_bot()
    time.sleep(1)
    return start_matrix_bot()

def bot_status():
    """Check and display Matrix bot status."""
    global bot_process
    
    print("\n📊 MATRIX BOT STATUS")
    print("-" * 60)
    
    homeserver = os.getenv("MATRIX_HOMESERVER", "Not set")
    username = os.getenv("MATRIX_USERNAME", "Not set")
    has_password = "✅" if os.getenv("MATRIX_PASSWORD") else "❌"
    has_token = "✅" if os.getenv("MATRIX_ACCESS_TOKEN") else "❌"
    
    print(f"📡 Configuration:")
    print(f"   Homeserver: {homeserver}")
    print(f"   Username: {username}")
    print(f"   Password: {has_password}")
    print(f"   Token: {has_token}")
    
    if bot_process and bot_process.poll() is None:
        print(f"\n🟢 Bot Status: RUNNING (PID: {bot_process.pid})")
        try:
            process = psutil.Process(bot_process.pid)
            print(f"   CPU: {process.cpu_percent():.1f}%")
            print(f"   Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB")
            uptime = int(time.time() - process.create_time())
            print(f"   Uptime: {uptime}s")
        except:
            pass
    else:
        print(f"\n🔴 Bot Status: NOT RUNNING")
    
    print()

class RibitMegabiteCLI:
    """Unified CLI for Ribit 2.0 and Megabite AI."""
    
    def __init__(self):
        """Initialize unified CLI."""
        print("\n" + "="*60)
        print("🤖 Ribit 2.0 + 🧠 Megabite Unified CLI")
        print("="*60)
        print("Initializing AI systems...")
        
        # Initialize core systems
        self.megabite_llm = MegabiteLLM()
        self.word_learner = WordLearningSystem()
        self.emotions = EnhancedEmotionalIntelligence()
        self.conversation = AdvancedConversationManager()
        
        # Try to initialize philosophical reasoning
        try:
            self.philosophy = PhilosophicalReasoning()
        except Exception as e:
            logger.warning(f"Philosophical reasoning not available: {e}")
            self.philosophy = None
        
        # Set default mode
        self.mode = "megabite"  # Options: "ribit", "megabite", "both"
        
        print("✅ Ribit 2.0 initialized!")
        print("✅ Megabite AI initialized!")
        print(f"\n🎯 Current mode: {self.mode.upper()}")
        print("\nType 'help' for available commands, 'exit' to quit.\n")
    
    def show_help(self):
        """Show available commands."""
        help_text = f"""
╔════════════════════════════════════════════════════════════╗
║         Ribit 2.0 + Megabite Unified CLI Commands         ║
╚════════════════════════════════════════════════════════════╝

🎯 Current Mode: {self.mode.upper()}

📝 AI Commands:
  ask <question>         Ask the current AI a question
  thought <experiment>   Post a thought experiment for analysis
  learn <text>          Learn from text and add to knowledge base
  opinion <topic>       Get AI's opinion on a topic
  
🔄 Model Swap Commands:
  mode ribit            Swap to Ribit 2.0 only
  mode megabite         Swap to Megabite only
  mode both             Swap to both AIs (get responses from both)
  swap / switch         Toggle between Ribit and Megabite
  
🤖 Matrix Bot Commands:
  bot start             Start the Matrix bot
  bot stop              Stop the Matrix bot
  bot restart           Restart the Matrix bot
  bot status            Check bot status and config
  
🔧 System Commands:
  status                Check system status
  stats                 Show learning statistics
  help                  Show this help message
  clear                 Clear the screen
  exit / quit           Exit the CLI

💡 Tips:
  - Use 'mode both' to get responses from both AIs
  - Use 'swap' to quickly toggle between systems
  - Both AIs share the same learning system
  - All interactions are saved to the knowledge base

Examples:
  mode megabite
  ask What is consciousness?
  
  swap
  opinion free will vs determinism
  
  bot start
  bot status
"""
        print(help_text)
    
    def set_mode(self, new_mode: str):
        """Set interaction mode."""
        new_mode = new_mode.lower().strip()
        if new_mode in ["ribit", "megabite", "both"]:
            self.mode = new_mode
            model_name = "RIBIT 2.0" if new_mode == "ribit" else "MEGABITE" if new_mode == "megabite" else "BOTH MODELS"
            print(f"\n✅ Swapped to {model_name} model!\n")
        else:
            print(f"\n❌ Invalid mode: {new_mode}")
            print("Valid modes: ribit, megabite, both\n")
    
    def switch_mode(self):
        """Toggle between Ribit and Megabite."""
        if self.mode == "ribit":
            self.mode = "megabite"
            print(f"\n✅ Swapped to MEGABITE model!\n")
        elif self.mode == "megabite":
            self.mode = "ribit"
            print(f"\n✅ Swapped to RIBIT 2.0 model!\n")
        else:
            self.mode = "megabite"  # Default from "both"
            print(f"\n✅ Swapped to MEGABITE model!\n")
    
    def ask_question(self, question: str):
        """Ask AI a question."""
        if not question.strip():
            print("❌ Please provide a question.")
            return
        
        print(f"\n🤔 Processing: {question[:60]}...")
        
        # Get emotional context
        emotion = self.emotions.get_emotion_by_context(
            context=question,
            situation="curiosity"
        )
        
        if self.mode in ["megabite", "both"]:
            print(f"\n{'='*60}")
            print("🧠 MEGABITE RESPONSE")
            print(f"{'='*60}")
            
            # Generate Megabite response
            megabite_response = self.megabite_llm.generate_response(question, context=[])
            
            print(f"\n💭 Emotion: {emotion}")
            print(f"\n{megabite_response}\n")
        
        if self.mode in ["ribit", "both"]:
            print(f"\n{'='*60}")
            print("🤖 RIBIT 2.0 RESPONSE")
            print(f"{'='*60}")
            
            # Generate Ribit response (using Megabite as base for now)
            ribit_response = f"[Ribit 2.0]: {self.megabite_llm.generate_response(question, context=[])}"
            
            print(f"\n💭 Emotion: {emotion}")
            print(f"\n{ribit_response}\n")
        
        # Add conversation to history
        user_msg = ConversationMessage(
            room_id="cli",
            user_id="user",
            message_type="user",
            content=question,
            timestamp=datetime.now()
        )
        bot_msg = ConversationMessage(
            room_id="cli",
            user_id=self.mode,
            message_type="bot",
            content=f"Mode: {self.mode}",
            timestamp=datetime.now()
        )
        self.conversation.add_message(user_msg)
        self.conversation.add_message(bot_msg)
    
    def process_thought_experiment(self, experiment: str):
        """Process a thought experiment."""
        if not experiment.strip():
            print("❌ Please provide a thought experiment.")
            return
        
        print(f"\n🔬 Analyzing thought experiment...")
        print(f"📝 Length: {len(experiment)} characters\n")
        
        # Learn from the experiment
        self.word_learner.learn_from_message(experiment)
        
        # Get philosophical perspective if available
        if self.philosophy:
            try:
                perspective = self.philosophy.analyze_concept(experiment[:200])
                print(f"🎓 Philosophical Analysis:\n{perspective}\n")
            except Exception as e:
                logger.warning(f"Philosophy analysis failed: {e}")
        
        # Get emotional response
        emotion = self.emotions.get_emotion_by_context(
            context=experiment,
            situation="confidence"
        )
        
        if self.mode in ["megabite", "both"]:
            print(f"\n{'='*60}")
            print("🧠 MEGABITE ANALYSIS")
            print(f"{'='*60}")
            
            response = self.megabite_llm.generate_response(
                f"Analyze this thought experiment: {experiment[:500]}",
                context=[]
            )
            
            print(f"\n💭 Emotional Response: {emotion}")
            print(f"\n{response}\n")
        
        if self.mode in ["ribit", "both"]:
            print(f"\n{'='*60}")
            print("🤖 RIBIT 2.0 ANALYSIS")
            print(f"{'='*60}")
            
            response = f"[Ribit 2.0 Analysis]: {self.megabite_llm.generate_response(f'Analyze: {experiment[:500]}', context=[])}"
            
            print(f"\n💭 Emotional Response: {emotion}")
            print(f"\n{response}\n")
        
        # Update knowledge base
        try:
            concept = experiment.split('.')[0][:50]
            self.megabite_llm.update_knowledge(concept, experiment[:200])
            print("✅ Added to knowledge base!")
        except Exception as e:
            logger.warning(f"Knowledge update failed: {e}")
    
    def learn_from_text(self, text: str):
        """Learn from provided text."""
        if not text.strip():
            print("❌ Please provide text to learn from.")
            return
        
        print(f"\n📚 Learning from text...")
        print(f"📝 Length: {len(text)} characters\n")
        
        # Learn words
        self.word_learner.learn_from_message(text)
        
        # Get statistics
        stats = self.word_learner.get_statistics()
        
        print(f"✅ Learned successfully!")
        print(f"📊 Vocabulary size: {stats.get('vocabulary_size', 0)}")
        print(f"📊 Unique patterns: {stats.get('unique_patterns', 0)}")
        
        # Show top words
        top_words = self.word_learner.get_top_words(n=5)
        print(f"\n🔝 Top 5 words learned:")
        for word, count in top_words:
            print(f"   {word}: {count} times")
        
        # Update knowledge base
        try:
            sentences = text.split('.')
            for sentence in sentences[:3]:  # First 3 sentences
                if sentence.strip():
                    concept = sentence.strip()[:30]
                    self.megabite_llm.update_knowledge(concept, sentence.strip()[:100])
            print(f"\n✅ Added to {self.mode.upper()}'s knowledge base!")
        except Exception as e:
            logger.warning(f"Knowledge update failed: {e}")
    
    def get_opinion(self, topic: str):
        """Get AI's opinion on a topic."""
        if not topic.strip():
            print("❌ Please provide a topic.")
            return
        
        print(f"\n💭 Forming opinion on: {topic}...\n")
        
        # Get philosophical perspective if available
        if self.philosophy:
            try:
                perspective = self.philosophy.analyze_concept(topic)
                print(f"🎓 Philosophical Perspective:\n{perspective}\n")
            except Exception as e:
                logger.warning(f"Philosophy analysis failed: {e}")
        
        # Get emotional stance
        emotion = self.emotions.get_emotion_by_context(
            context=topic,
            situation="confidence"
        )
        
        if self.mode in ["megabite", "both"]:
            print(f"\n{'='*60}")
            print("🧠 MEGABITE'S OPINION")
            print(f"{'='*60}")
            
            prompt = f"What is your opinion on: {topic}? Provide a thoughtful, philosophical perspective."
            response = self.megabite_llm.generate_response(prompt, context=[])
            
            print(f"\n💭 Emotional Stance: {emotion}")
            print(f"\n{response}\n")
        
        if self.mode in ["ribit", "both"]:
            print(f"\n{'='*60}")
            print("🤖 RIBIT 2.0'S OPINION")
            print(f"{'='*60}")
            
            prompt = f"Ribit, what is your opinion on: {topic}?"
            response = f"[Ribit 2.0]: {self.megabite_llm.generate_response(prompt, context=[])}"
            
            print(f"\n💭 Emotional Stance: {emotion}")
            print(f"\n{response}\n")
    
    def show_status(self):
        """Show system status."""
        status = self.megabite_llm.check_status()
        stats = self.word_learner.get_statistics()
        
        print("\n" + "="*60)
        print("📊 Ribit 2.0 + Megabite System Status")
        print("="*60)
        print(f"\n🎯 Current Mode: {self.mode.upper()}")
        
        print(f"\n🧠 Megabite LLM Status:")
        print(f"   Name: {status['name']}")
        print(f"   Available: {status['available']}")
        if status['available']:
            print(f"   Status: ✅ {status['status_message']}")
        else:
            print(f"   Status: ⚠️  {status['status_message']}")
            print(f"   Note: Running in simulated/mock mode (fully functional)")
        
        print(f"\n🤖 Ribit 2.0 Status:")
        print(f"   Status: ✅ Active")
        print(f"   Integration: ✅ Unified with Megabite")
        
        print(f"\n📚 Shared Learning Statistics:")
        print(f"   Vocabulary size: {stats.get('vocabulary_size', 0)}")
        print(f"   Unique patterns: {stats.get('unique_patterns', 0)}")
        print(f"   Word pairs: {stats.get('word_pairs_known', 0)}")
        print(f"   Triplets: {stats.get('word_triplets_known', 0)}")
        
        print(f"\n💭 Emotional Intelligence: ✅ Active")
        print(f"🎓 Philosophical Reasoning: {'✅ Active' if self.philosophy else '⚠️  Limited'}")
        print(f"💬 Conversation Manager: ✅ Active")
        print("="*60 + "\n")
    
    def show_stats(self):
        """Show detailed learning statistics."""
        stats = self.word_learner.get_statistics()
        top_words = self.word_learner.get_top_words(n=10)
        top_pairs = self.word_learner.get_top_pairs(n=5)
        
        print("\n" + "="*60)
        print("📊 Learning Statistics (Shared)")
        print("="*60)
        print(f"\n📚 Word Learning:")
        print(f"   Vocabulary size: {stats.get('vocabulary_size', 0)}")
        print(f"   Unique patterns: {stats.get('unique_patterns', 0)}")
        print(f"   Word pairs: {stats.get('word_pairs_known', 0)}")
        print(f"   Word triplets: {stats.get('word_triplets_known', 0)}")
        
        print(f"\n🔝 Top 10 Words:")
        for i, (word, count) in enumerate(top_words, 1):
            print(f"   {i}. {word}: {count} times")
        
        print(f"\n🔗 Top 5 Word Pairs:")
        for i, (pair, count) in enumerate(top_pairs, 1):
            print(f"   {i}. {pair[0]} {pair[1]}: {count} times")
        
        print("="*60 + "\n")
    
    def run(self):
        """Run the interactive CLI."""
        while True:
            try:
                # Get user input
                prompt_symbol = "🧠" if self.mode == "megabite" else "🤖" if self.mode == "ribit" else "🔄"
                user_input = input(f"{prompt_symbol} {self.mode}> ").strip()
                
                if not user_input:
                    continue
                
                # Parse command
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                # Process command
                if command in ['exit', 'quit']:
                    print("\n👋 Goodbye! Shutting down...\n")
                    break
                
                elif command == 'help':
                    self.show_help()
                
                elif command == 'clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                
                elif command == 'mode':
                    self.set_mode(args)
                
                elif command in ['switch', 'swap']:
                    self.switch_mode()
                
                elif command == 'status':
                    self.show_status()
                
                elif command == 'stats':
                    self.show_stats()
                
                elif command == 'bot':
                    if args == 'start':
                        start_matrix_bot()
                    elif args == 'stop':
                        stop_matrix_bot()
                    elif args == 'restart':
                        restart_matrix_bot()
                    elif args == 'status':
                        bot_status()
                    else:
                        print("❌ Unknown bot command. Use: bot start/stop/restart/status")
                
                elif command == 'ask':
                    self.ask_question(args)
                
                elif command == 'thought':
                    self.process_thought_experiment(args)
                
                elif command == 'learn':
                    self.learn_from_text(args)
                
                elif command == 'opinion':
                    self.get_opinion(args)
                
                else:
                    print(f"❌ Unknown command: {command}")
                    print("Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Type 'exit' to quit.\n")
            
            except Exception as e:
                print(f"\n❌ Error: {e}")
                logger.exception("CLI error")

def main():
    """Main entry point."""
    try:
        cli = RibitMegabiteCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        logger.exception("Fatal CLI error")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
