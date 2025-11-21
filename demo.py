#!/usr/bin/env python3
"""
Ribit 2.0 Demo - Interactive Console Application
Demonstrates the core functionality of Ribit 2.0 AI agent
"""

import sys
import os
import subprocess
import signal
import time
import psutil

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file if it exists
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

# Load .env file at startup
load_env_file()

from ribit_2_0.mock_llm_wrapper import MockRibit20LLM

# Global variable to track Matrix bot process
bot_process = None

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
        print("   And either:")
        print("   - MATRIX_PASSWORD")
        print("   - MATRIX_ACCESS_TOKEN")
        return False
    
    if not password and not token:
        print("❌ Missing credentials! Please set either MATRIX_PASSWORD or MATRIX_ACCESS_TOKEN")
        return False
    
    try:
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'matrix_bot.log')
        
        # Start bot with output redirected to log file
        with open(log_file, 'w') as log_f:
            bot_process = subprocess.Popen(
                [sys.executable, "-m", "ribit_2_0.matrix_bot"],
                stdout=log_f,
                stderr=subprocess.STDOUT,
                env=os.environ.copy()
            )
        time.sleep(2)
        
        if bot_process.poll() is None:
            print(f"✅ Matrix bot started successfully! (PID: {bot_process.pid})")
            print(f"   Server: {homeserver}")
            print(f"   User: {username}")
            print(f"   📝 Logs: {log_file}")
            return True
        else:
            print(f"❌ Bot failed to start - check Matrix credentials and homeserver")
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
        pid = bot_process.pid
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        
        bot_process.terminate()
        
        try:
            bot_process.wait(timeout=5)
            print("✅ Matrix bot stopped gracefully!")
        except subprocess.TimeoutExpired:
            print("⚠️  Bot didn't stop gracefully, forcing...")
            bot_process.kill()
            bot_process.wait()
            print("✅ Matrix bot force-stopped!")
        
        for child in children:
            try:
                child.terminate()
            except:
                pass
        
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
    
    print("📊 MATRIX BOT STATUS")
    print("-" * 70)
    
    homeserver = os.getenv("MATRIX_HOMESERVER", "Not set")
    username = os.getenv("MATRIX_USERNAME", "Not set")
    has_password = "✅" if os.getenv("MATRIX_PASSWORD") else "❌"
    has_token = "✅" if os.getenv("MATRIX_ACCESS_TOKEN") else "❌"
    
    print(f"\n📡 Configuration:")
    print(f"   Homeserver: {homeserver}")
    print(f"   Username: {username}")
    print(f"   Password: {has_password}")
    print(f"   Access Token: {has_token}")
    
    if bot_process and bot_process.poll() is None:
        print(f"\n🟢 Bot Status: RUNNING (PID: {bot_process.pid})")
        try:
            process = psutil.Process(bot_process.pid)
            print(f"   CPU: {process.cpu_percent():.1f}%")
            print(f"   Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB")
            print(f"   Uptime: {int(time.time() - process.create_time())} seconds")
        except:
            pass
    else:
        print(f"\n🔴 Bot Status: NOT RUNNING")
    
    print()

def learn_words_from_rooms():
    """Scan Matrix rooms and learn new words."""
    print("📚 LEARNING WORDS FROM MATRIX ROOMS")
    print("-" * 70)
    
    # Check configuration
    homeserver = os.getenv("MATRIX_HOMESERVER")
    username = os.getenv("MATRIX_USERNAME")
    password = os.getenv("MATRIX_PASSWORD")
    token = os.getenv("MATRIX_ACCESS_TOKEN")
    
    if not homeserver or not username or (not password and not token):
        print("\n❌ Matrix credentials not configured!")
        print("💡 Set up your Matrix credentials first (see option 13)")
        print()
        return
    
    try:
        import asyncio
        from nio import AsyncClient, RoomMessagesResponse
        from ribit_2_0.matrix_history_tracker import MatrixHistoryTracker
        
        print("\n🔍 Connecting to Matrix...")
        
        # Ask for message limit
        limit_input = input("👉 How many recent messages per room? (default 100, max 500): ").strip()
        if limit_input:
            try:
                msg_limit = int(limit_input)
                msg_limit = min(msg_limit, 500)
            except ValueError:
                print("⚠️  Invalid number, using default (100)")
                msg_limit = 100
        else:
            msg_limit = 100
        
        async def fetch_and_learn():
            """Async function to fetch messages and learn words."""
            # Initialize client
            client = AsyncClient(homeserver, username)
            
            # Login
            if token:
                client.access_token = token
                client.user_id = username
            else:
                login_response = await client.login(password)
                if not login_response or hasattr(login_response, 'message'):
                    print(f"❌ Login failed: {getattr(login_response, 'message', 'Unknown error')}")
                    await client.close()
                    return
            
            # Sync to get rooms
            print("🔄 Syncing rooms...")
            await client.sync(timeout=30000)
            
            joined_rooms = list(client.rooms.keys())
            print(f"✅ Found {len(joined_rooms)} joined rooms")
            
            if not joined_rooms:
                print("⚠️  No rooms found! Invite the bot to some rooms first.")
                await client.close()
                return
            
            # Initialize history tracker
            db_path = os.getenv("MATRIX_HISTORY_DB", "matrix_message_history.db")
            tracker = MatrixHistoryTracker(db_path=db_path)
            
            total_messages = 0
            total_words_before = tracker.get_statistics().get('words_learned', 0)
            
            print(f"\n📖 Learning from {len(joined_rooms)} rooms ({msg_limit} messages each)...\n")
            
            # Fetch messages from each room
            for i, room_id in enumerate(joined_rooms, 1):
                room = client.rooms[room_id]
                room_name = room.display_name or room.room_id[:20]
                
                print(f"  [{i}/{len(joined_rooms)}] {room_name}...", end=" ")
                
                try:
                    # Fetch recent messages
                    response = await client.room_messages(
                        room_id=room_id,
                        start="",
                        limit=msg_limit
                    )
                    
                    if isinstance(response, RoomMessagesResponse):
                        message_count = 0
                        for event in response.chunk:
                            if hasattr(event, 'body') and hasattr(event, 'sender'):
                                # Add message to tracker (which learns words)
                                tracker.add_message(
                                    room_id=room_id,
                                    sender=event.sender,
                                    message_text=event.body,
                                    sender_name=None
                                )
                                message_count += 1
                        
                        total_messages += message_count
                        print(f"✅ {message_count} messages")
                    else:
                        print("⚠️  Failed to fetch")
                        
                except Exception as e:
                    print(f"❌ Error: {str(e)[:30]}")
            
            await client.close()
            
            # Show results
            total_words_after = tracker.get_statistics().get('words_learned', 0)
            new_words = total_words_after - total_words_before
            
            print(f"\n✅ Learning complete!")
            print(f"   📊 Processed: {total_messages} messages")
            print(f"   📚 Total words in library: {total_words_after}")
            print(f"   🆕 New words learned: {new_words}")
            print()
        
        # Run the async function
        asyncio.run(fetch_and_learn())
        
    except ImportError as e:
        print(f"\n❌ Required modules not available: {e}")
        print("💡 Make sure matrix-nio is installed")
        print()
    except Exception as e:
        print(f"\n❌ Error learning words: {e}")
        import traceback
        traceback.print_exc()
        print()

def print_header():
    """Print the Ribit 2.0 welcome header."""
    print("\n" + "=" * 70)
    print("🤖 Ribit 2.0: Enhanced AI Agent Demo")
    print("=" * 70)
    print("An elegant, wise AI agent for GUI automation and robotic control")
    print("=" * 70 + "\n")

def print_menu():
    """Print the interactive menu."""
    print("\n" + "-" * 70)
    print("Available Commands:")
    print("-" * 70)
    print("  1. Introduction - Meet Ribit 2.0")
    print("  2. Capabilities - View available features")
    print("  3. Personality - Learn about Ribit's character")
    print("  4. Ask Question - Have a conversation with Ribit")
    print("  5. Learn Knowledge - Teach Ribit something new")
    print("  6. Recall Knowledge - Ask Ribit to recall information")
    print("  7. Task Execution - Demonstrate automation capabilities")
    print("  8. Conversation History - View recent context")
    print("-" * 70)
    print("  Matrix Word Library:")
    print("  9. View Learned Words - Show words from Matrix history")
    print("-" * 70)
    print("  Matrix Bot Controls:")
    print("  10. Start Matrix Bot - Launch the bot")
    print("  11. Stop Matrix Bot - Stop the bot")
    print("  12. Restart Matrix Bot - Restart the bot")
    print("  13. Bot Status - Check bot status and config")
    print("  14. Learn Words from Rooms - Scan Matrix rooms and learn new words")
    print("-" * 70)
    print("  Matrix Bot Commands (test simulation):")
    print("  15. Teach Bot (?learn) - Teach the bot new knowledge")
    print("  16. Switch Model (?model) - Change image analysis model")
    print("  17. Switch Personality (?personality) - Change bot personality")
    print("  18. Bot Help (?help) - Show bot command reference")
    print("  19. Bot Status (?status) - Check bot settings")
    print("-" * 70)
    print("  0. Exit")
    print("-" * 70)

def main():
    """Main demo application."""
    print_header()
    
    print("🔧 Initializing Ribit 2.0 LLM Emulator...")
    try:
        llm = MockRibit20LLM()
        print("✅ Ribit 2.0 initialized successfully!\n")
    except Exception as e:
        print(f"❌ Error initializing Ribit 2.0: {e}")
        return
    
    running = True
    
    while running:
        print_menu()
        choice = input("\n👉 Enter your choice (0-19): ").strip()
        
        print("\n" + "=" * 70)
        
        if choice == "1":
            # Introduction
            print("🎭 INTRODUCTION")
            print("-" * 70)
            response = llm.get_decision("Introduce yourself and tell me about your purpose")
            print(f"\n{response}\n")
            
        elif choice == "2":
            # Capabilities
            print("🔧 CAPABILITIES")
            print("-" * 70)
            capabilities = llm.get_capabilities()
            print("\nRibit 2.0 Features:")
            for capability, status in capabilities.items():
                status_icon = "✅" if status else "❌"
                print(f"  {status_icon} {capability.replace('_', ' ').title()}")
            print()
            
        elif choice == "3":
            # Personality
            print("🎨 PERSONALITY")
            print("-" * 70)
            personality = llm.get_personality_info()
            print("\nPersonality Profile:")
            for key, value in personality.items():
                print(f"  • {key.replace('_', ' ').title()}: {value}")
            print()
            
        elif choice == "4":
            # Ask Question
            print("💬 ASK A QUESTION")
            print("-" * 70)
            question = input("\n👉 Your question: ").strip()
            if question:
                response = llm.get_decision(question)
                print(f"\n🤖 Ribit: {response}\n")
            else:
                print("⚠️  No question entered.\n")
                
        elif choice == "5":
            # Learn Knowledge
            print("📚 TEACH RIBIT")
            print("-" * 70)
            knowledge = input("\n👉 What would you like to teach? (e.g., 'Learn that Python is a programming language'): ").strip()
            if knowledge:
                response = llm.get_decision(knowledge)
                print(f"\n🤖 Ribit: {response}\n")
            else:
                print("⚠️  No knowledge entered.\n")
                
        elif choice == "6":
            # Recall Knowledge
            print("🧠 RECALL KNOWLEDGE")
            print("-" * 70)
            query = input("\n👉 What should Ribit recall? (e.g., 'What is Python?'): ").strip()
            if query:
                response = llm.get_decision(query)
                print(f"\n🤖 Ribit: {response}\n")
            else:
                print("⚠️  No query entered.\n")
                
        elif choice == "7":
            # Task Execution
            print("🎯 TASK EXECUTION DEMO")
            print("-" * 70)
            print("\nDemonstrating automation capabilities...")
            tasks = [
                "Move to coordinates (100, 200)",
                "Click on the target",
                "Type 'Hello, World!'",
                "Explain what you just did"
            ]
            for i, task in enumerate(tasks, 1):
                print(f"\n{i}. Task: {task}")
                response = llm.get_decision(task)
                print(f"   Response: {response}")
            print()
            
        elif choice == "8":
            # Conversation History
            print("📜 CONVERSATION HISTORY")
            print("-" * 70)
            context = llm.get_conversation_context()
            print(f"\nTotal conversation entries: {len(context)}")
            if context:
                print("\nRecent context (last 5 entries):")
                for i, entry in enumerate(context[-5:], 1):
                    print(f"  {i}. {entry[:60]}...")
            else:
                print("\n⚠️  No conversation history yet.")
            print()
            
        elif choice == "9":
            # View Learned Words
            print("📚 MATRIX WORD LIBRARY")
            print("-" * 70)
            try:
                from ribit_2_0.matrix_history_tracker import MatrixHistoryTracker
                import os
                
                # Ask for limit
                limit_input = input("\n👉 How many words to show? (default 120, max 500): ").strip()
                if limit_input:
                    try:
                        limit = int(limit_input)
                        limit = min(limit, 500)  # Cap at 500
                    except ValueError:
                        print("⚠️  Invalid number, using default (120)")
                        limit = 120
                else:
                    limit = 120
                
                # Initialize tracker
                db_path = os.getenv("MATRIX_HISTORY_DB", "matrix_message_history.db")
                if not os.path.exists(db_path):
                    print(f"\n⚠️  No Matrix history database found at {db_path}")
                    print("💡 Start the Matrix bot first to begin learning words!")
                else:
                    tracker = MatrixHistoryTracker(db_path=db_path)
                    
                    # Get words
                    words = tracker.get_word_library(limit=limit)
                    
                    if not words:
                        print("\n📚 No words have been learned yet from Matrix conversations.")
                        print("💡 The bot learns words automatically as people chat!")
                    else:
                        stats = tracker.get_statistics()
                        total_words = stats.get('words_learned', len(words))
                        
                        print(f"\n📚 Top {len(words)} of {total_words} learned words (from 3-month history):\n")
                        
                        # Display in columns
                        for i, word_data in enumerate(words, 1):
                            word = word_data.get('word', '')
                            frequency = word_data.get('frequency', 0)
                            print(f"  {i:3d}. {word:20s} ({frequency} times)")
                        
                        print(f"\n✅ Showing {len(words)} words from {total_words} total learned words")
                        
            except ImportError:
                print("\n❌ Matrix history tracker not available")
            except Exception as e:
                print(f"\n❌ Error accessing word library: {e}")
            
            print()
            
        elif choice == "10":
            # Start Matrix Bot
            start_matrix_bot()
            
        elif choice == "11":
            # Stop Matrix Bot
            stop_matrix_bot()
            
        elif choice == "12":
            # Restart Matrix Bot
            restart_matrix_bot()
            
        elif choice == "13":
            # Bot Status
            bot_status()
            
        elif choice == "14":
            # Learn Words from Rooms
            learn_words_from_rooms()
        
        elif choice == "15":
            # Teach Bot (?learn command)
            print("📚 TEACH RIBIT (?learn)")
            print("-" * 70)
            text = input("\n👉 What would you like to teach? (e.g., 'Python is a programming language'): ").strip()
            if text:
                print(f"\n✅ **Knowledge Learned!**")
                print(f"\n📝 **Text:** {text[:100]}{'...' if len(text) > 100 else ''}")
                print(f"\n📊 **Learning Progress:**")
                print(f"• Vocabulary size: Learning...")
                print(f"• Patterns learned: Tracking...")
                print(f"• Words tracked: Updating...")
                print(f"\n🧠 I've added this to my knowledge base and will use it in future conversations!")
            else:
                print("⚠️  No text entered.\n")
            print()
        
        elif choice == "16":
            # Switch Model (?model command)
            print("🎨 IMAGE ANALYSIS MODELS (?model)")
            print("-" * 70)
            print("\n✅ offline (currently selected)")
            print("   Private, no external APIs needed")
            print("\n○ webai-gemini")
            print("   Google Gemini Vision API")
            print("\n○ webai-gpt4")
            print("   OpenAI GPT-4 Vision")
            print("\n○ webai-claude")
            print("   Claude 3 Vision")
            model = input("\n👉 Enter model name (or press Enter to skip): ").strip().lower()
            if model:
                print(f"\n✅ Image analysis model updated!")
                print(f"\n**New model:** {model}")
                print(f"Upload an image to test the new model!")
            print()
        
        elif choice == "17":
            # Switch Personality (?personality command)
            print("🎭 BOT PERSONALITY (?personality)")
            print("-" * 70)
            print("\n✅ ribit (currently selected)")
            print("   Technical AI assistant mode")
            print("\n○ megabite")
            print("   Friendly companion mode")
            personality = input("\n👉 Enter personality name (ribit/megabite or press Enter to skip): ").strip().lower()
            if personality in ['ribit', 'megabite']:
                print(f"\n✅ Personality updated!")
                print(f"\n**New personality:** {personality}")
                print(f"Try chatting with me to see the difference!")
            elif personality:
                print(f"\n❌ Unknown personality: {personality}")
            print()
        
        elif choice == "18":
            # Bot Help (?help command)
            print("📚 RIBIT COMMANDS REFERENCE (?help)")
            print("-" * 70)
            help_msg = """
**Chat:**
• ribit.2.0 <message> - Chat with me
• !reset - Clear conversation context

**General Commands:**
• ?help - Show this help
• ?status - Show your current settings
• ?search <query> - Search 3-month message history
• ?history - View message history statistics
• ?words [number] - View learned words (default: 120, max: 500)
• ?learn <text> - Teach me new knowledge and add to my vocabulary

**Image Analysis:**
• Upload any image - I'll analyze it automatically!
• ?model list - Show available image analysis models
• ?model <name> - Switch to different model

**Personality:**
• ?personality list - Show available personalities
• ?personality ribit - Technical AI assistant mode
• ?personality megabite - Friendly companion mode

**Authorized Commands** (admin users only):
• ?sys - System status
• ?command <action> - Execute actions

**Examples:**
• ?model webai-gemini - Use Gemini for image analysis
• ?personality megabite - Switch to friendly mode
• ?learn Python is a powerful programming language
• ?search did alice mention python last week?
"""
            print(help_msg)
        
        elif choice == "19":
            # Bot Status (?status command)
            print("🤖 RIBIT BOT STATUS (?status)")
            print("-" * 70)
            status_msg = """
**Core Status:** Operational ✅
**LLM Emulator:** Active
**Controller:** Ready

**Your Settings:**
• Image Model: **offline**
  Private, no external APIs needed
• Personality: **ribit**
  Technical AI assistant mode

**Capabilities:**
• Image Analysis: ✅
• Message Search: ✅
• Knowledge Learning: ✅
• Personality Switching: ✅
• Word Learning: ✅

**Personality:** analytical, helpful, wise, direct
"""
            print(status_msg)
            print()
        
        elif choice == "0":
            # Exit
            print("👋 GOODBYE")
            print("-" * 70)
            print("\nThank you for exploring Ribit 2.0!")
            if bot_process and bot_process.poll() is None:
                print("🛑 Stopping Matrix bot before exit...")
                stop_matrix_bot()
            print("🤖 Shutting down gracefully...\n")
            llm.close()
            running = False
            
        else:
            print("⚠️  Invalid choice. Please enter 0-19.\n")
    
    print("=" * 70)
    print("✅ Demo completed successfully!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user. Exiting gracefully...")
        if bot_process and bot_process.poll() is None:
            print("🛑 Stopping Matrix bot...")
            stop_matrix_bot()
        print()
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        if bot_process and bot_process.poll() is None:
            print("🛑 Stopping Matrix bot...")
            stop_matrix_bot()
        import traceback
        traceback.print_exc()
