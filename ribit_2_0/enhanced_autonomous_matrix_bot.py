"""
Enhanced Autonomous Matrix Bot for Ribit 2.0

Integrates:
- Philosophical reasoning
- Conversational mode
- Autonomous interaction
- Task autonomy
- Bot-to-bot communication
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
import os
import sys

# Try to import matrix-nio with graceful fallback
try:
    from nio import AsyncClient, MatrixRoom, RoomMessageText, InviteMemberEvent
    MATRIX_NIO_AVAILABLE = True
except ImportError as e:
    print(f"Warning: matrix-nio not properly installed: {e}")
    print("Please install with: pip3 install matrix-nio[e2e] --break-system-packages")
    MATRIX_NIO_AVAILABLE = False
    # Create mock classes for type hints
    class AsyncClient: pass
    class MatrixRoom: pass
    class RoomMessageText: pass
    class InviteMemberEvent: pass

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ribit_2_0.mock_llm_wrapper import MockRibit20LLM
from ribit_2_0.philosophical_reasoning import PhilosophicalReasoning
from ribit_2_0.conversational_mode import ConversationalMode
from ribit_2_0.autonomous_matrix import AutonomousMatrixInteraction
from ribit_2_0.task_autonomy import TaskAutonomy, Task, TaskPriority
from ribit_2_0.knowledge_base import KnowledgeBase
from ribit_2_0.message_history_learner import MessageHistoryLearner
from ribit_2_0.enhanced_mock_llm import EnhancedMockLLM
from ribit_2_0.word_learning_system import WordLearningSystem

logger = logging.getLogger(__name__)


class EnhancedAutonomousMatrixBot:
    """
    Enhanced Matrix bot with full autonomous capabilities.
    
    Features:
    - Philosophical reasoning
    - Autonomous conversation
    - Task self-selection
    - Bot-to-bot interaction
    - Opinion formation
    """
    
    def __init__(
        self,
        homeserver: str,
        user_id: str,
        access_token: str,
        device_id: Optional[str] = None
    ):
        self.homeserver = homeserver
        self.user_id = user_id
        self.access_token = access_token
        self.device_id = device_id
        
        # Initialize Matrix client
        self.client = AsyncClient(homeserver, user_id, device_id=device_id)
        self.client.access_token = access_token
        
        # Initialize Ribit components
        self.knowledge_base = KnowledgeBase("knowledge.txt")
        
        # Use Enhanced Mock LLM with learning capabilities
        self.llm = EnhancedMockLLM(
            knowledge_file="knowledge.txt",
            temperature=0.7,
            frequency_penalty=0.5,
            presence_penalty=0.3,
            learning_enabled=True,
            style_adaptation=True
        )
        
        # Initialize message history learner
        self.message_learner = MessageHistoryLearner(self.knowledge_base)
        
        # Initialize word learning system
        self.word_learner = WordLearningSystem(storage_dir="word_learning")
        
        # Initialize new modules
        self.philosophical_reasoning = PhilosophicalReasoning(
            knowledge_base=self.knowledge_base,
            emotional_ai=getattr(self.llm, 'emotional_ai', None)
        )
        
        self.conversational_mode = ConversationalMode(
            llm_wrapper=self.llm,
            philosophical_reasoning=self.philosophical_reasoning
        )
        
        self.autonomous_interaction = AutonomousMatrixInteraction(
            conversational_mode=self.conversational_mode,
            philosophical_reasoning=self.philosophical_reasoning,
            knowledge_base=self.knowledge_base
        )
        
        self.task_autonomy = TaskAutonomy(
            llm_wrapper=self.llm,
            philosophical_reasoning=self.philosophical_reasoning,
            knowledge_base=self.knowledge_base,
            emotional_ai=getattr(self.llm, 'emotional_ai', None)
        )
        
        # History learning settings
        self.history_learning_enabled = True
        self.history_learned_rooms = set()
        
        # Authorized users
        self.authorized_users = [
            "@ribit:envs.net",
            "@rabit232:envs.net"
        ]
        
        # Track unauthorized attempts
        self.unauthorized_attempts = {}
        
        # Register callbacks
        self.client.add_event_callback(self.message_callback, RoomMessageText)
        self.client.add_event_callback(self.invite_callback, InviteMemberEvent)
        
        logger.info("Enhanced Autonomous Matrix Bot initialized")
    
    async def start(self):
        """Start the bot."""
        logger.info("Starting Enhanced Autonomous Matrix Bot...")
        
        # Sync with server
        await self.client.sync(timeout=30000)
        
        # Start autonomous work cycle in background
        asyncio.create_task(self.autonomous_work_loop())
        
        logger.info("Bot started and synced")
    
    async def message_callback(self, room: MatrixRoom, event: RoomMessageText):
        """Handle incoming messages."""
        # Ignore own messages
        if event.sender == self.user_id:
            return
        
        message = event.body
        sender = event.sender
        
        logger.info(f"Message from {sender} in {room.display_name}: {message}")
        
        # Learn from this message (passive learning)
        try:
            self.word_learner.learn_from_message(message, sender)
        except Exception as e:
            logger.debug(f"Word learning error: {e}")
        
        # Check if it's a command
        if message.startswith("?") or message.startswith("!"):
            await self.handle_command(room, sender, message)
            return
        
        # Check if we should respond autonomously
        room_context = {
            "room_id": room.room_id,
            "room_name": room.display_name,
            "sender": sender
        }
        
        should_respond = self.autonomous_interaction.should_respond_autonomously(
            message, sender, room_context
        )
        
        if should_respond:
            # Determine interest category
            interest = self.autonomous_interaction._matches_interests(message)
            
            # Generate response
            response = self.autonomous_interaction.generate_autonomous_response(
                message, sender, interest or "general"
            )
            
            # Enhance response with emojis
            if hasattr(self.conversational_mode, 'enhance_response_with_emojis'):
                response = self.conversational_mode.enhance_response_with_emojis(
                    response, message
                )
            
            # Send response
            await self.send_message(room.room_id, response)
            
            # Optionally send emoji reaction
            if hasattr(self.conversational_mode, 'get_emoji_reaction'):
                emoji_reaction = self.conversational_mode.get_emoji_reaction(message)
                if emoji_reaction:
                    # Send as a reaction to the original message
                    await self.send_reaction(room.room_id, event.event_id, emoji_reaction)
            
            # Learn from interaction
            self.autonomous_interaction.learn_from_interaction(message, response)
    
    async def handle_command(self, room: MatrixRoom, sender: str, command: str):
        """Handle commands."""
        # Check authorization
        if sender not in self.authorized_users:
            await self.handle_unauthorized_command(room, sender, command)
            return
        
        command_lower = command.lower()
        
        if command_lower.startswith("?sys"):
            await self.handle_system_status(room)
        elif command_lower.startswith("?status"):
            await self.handle_status(room)
        elif command_lower.startswith("?tasks"):
            await self.handle_tasks_command(room)
        elif command_lower.startswith("?opinion"):
            await self.handle_opinion_command(room, command)
        elif command_lower.startswith("?discuss"):
            await self.handle_discuss_command(room, command)
        elif command_lower.startswith("?learn") or command_lower.startswith("?history"):
            await self.handle_learn_history(room, command)
        elif command_lower.startswith("?vocab"):
            await self.handle_vocab_command(room)
        elif command_lower.startswith("?words"):
            await self.handle_words_command(room, command)
        elif command_lower.startswith("?word "):
            await self.handle_word_info_command(room, command)
        elif command_lower.startswith("?generate"):
            await self.handle_generate_sentence_command(room, command)
        elif command_lower.startswith("?llm"):
            await self.handle_llm_stats(room)
        elif command_lower.startswith("!reset"):
            await self.handle_reset(room)
        elif command_lower.startswith("?command"):
            # Traditional automation command
            await self.handle_automation_command(room, command)
        else:
            await self.send_message(room.room_id, "Unknown command. Try ?status or ?sys")
    
    async def handle_unauthorized_command(self, room: MatrixRoom, sender: str, command: str):
        """Handle commands from unauthorized users."""
        attempts = self.unauthorized_attempts.get(sender, 0)
        self.unauthorized_attempts[sender] = attempts + 1
        
        if attempts == 0:
            response = "I can't do this silly thing"
        else:
            response = "action terminated xd exe\n\nDo you wish to enable terminator mode? (just silly)"
        
        await self.send_message(room.room_id, response)
    
    async def handle_system_status(self, room: MatrixRoom):
        """Handle ?sys command."""
        status = f"""**Ribit 2.0 System Status**

**Core Systems:**
- LLM Emulator: ✓ Active
- Philosophical Reasoning: ✓ Active
- Conversational Mode: ✓ Active
- Autonomous Interaction: ✓ Active
- Task Autonomy: ✓ Active

**Capabilities:**
- Philosophical reasoning: ✓
- Autonomous conversation: ✓
- Task self-selection: ✓
- Bot-to-bot communication: ✓
- Opinion formation: ✓

**Current State:**
- Active task: {self.task_autonomy.active_task.description if self.task_autonomy.active_task else "None"}
- Queued tasks: {len(self.task_autonomy.task_queue)}
- Completed tasks: {len(self.task_autonomy.completed_tasks)}

**Engagement:**
- Autonomous responses this hour: {self.autonomous_interaction.autonomous_responses_this_hour}
- Known bots: {len(self.autonomous_interaction.known_bots)}

All systems operational."""
        
        await self.send_message(room.room_id, status)
    
    async def handle_status(self, room: MatrixRoom):
        """Handle ?status command."""
        task_status = self.task_autonomy.get_task_status()
        engagement_stats = self.autonomous_interaction.get_engagement_stats()
        
        status = f"""**Ribit 2.0 Status**

**Current Activity:**
{task_status['active_task']['description'] if task_status['active_task'] else 'Idle, ready for conversation'}

**Task Queue:** {task_status['queued_tasks']} tasks
**Completed:** {task_status['completed_tasks']} tasks

**Engagement:**
- Autonomous responses: {engagement_stats['autonomous_responses_this_hour']}/hour
- Engagement probability: {engagement_stats['engagement_probability']*100:.0f}%

**Interests:**
- Quantum physics
- Consciousness & free will
- Philosophy of science
- AI & emergence

I'm ready to discuss these topics or work on autonomous tasks!"""
        
        await self.send_message(room.room_id, status)
    
    async def handle_tasks_command(self, room: MatrixRoom):
        """Handle ?tasks command."""
        suggestions = self.task_autonomy.suggest_tasks()
        
        response = f"""**Autonomous Task Suggestions**

I could work on any of these tasks independently:

"""
        for i, suggestion in enumerate(suggestions[:5], 1):
            response += f"{i}. {suggestion}\n"
        
        response += "\nWould you like me to work on any of these? Or I can select one autonomously."
        
        await self.send_message(room.room_id, response)
    
    async def handle_opinion_command(self, room: MatrixRoom, command: str):
        """Handle ?opinion command."""
        # Extract topic
        topic = command[8:].strip()  # Remove "?opinion "
        
        if not topic:
            await self.send_message(room.room_id, "Please specify a topic: ?opinion <topic>")
            return
        
        # Generate opinion using philosophical reasoning
        response = self.philosophical_reasoning.generate_response(
            f"What is your opinion on {topic}?"
        )
        
        await self.send_message(room.room_id, response)
    
    async def handle_discuss_command(self, room: MatrixRoom, command: str):
        """Handle ?discuss command."""
        topic = command[8:].strip()  # Remove "?discuss "
        
        if not topic:
            await self.send_message(room.room_id, "Please specify a topic: ?discuss <topic>")
            return
        
        # Generate discussion starter
        starters = self.autonomous_interaction.get_conversation_starters("philosophy")
        response = f"**Let's discuss: {topic}**\n\n{starters[0]}\n\nWhat are your thoughts?"
        
        await self.send_message(room.room_id, response)
    
    async def handle_reset(self, room: MatrixRoom):
        """Handle !reset command."""
        self.conversational_mode.conversation_history = []
        await self.send_message(room.room_id, "Context reset. Starting fresh!")
    
    async def handle_automation_command(self, room: MatrixRoom, command: str):
        """Handle traditional automation commands."""
        # This would integrate with the existing automation system
        await self.send_message(
            room.room_id,
            "Automation commands require GUI access. Currently in conversational mode."
        )
    
    async def send_message(self, room_id: str, message: str):
        """Send a message to a room."""
        try:
            await self.client.room_send(
                room_id=room_id,
                message_type="m.room.message",
                content={
                    "msgtype": "m.text",
                    "body": message,
                    "format": "org.matrix.custom.html",
                    "formatted_body": message.replace("\n", "<br/>")
                }
            )
            logger.info(f"Sent message to {room_id}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
    
    async def send_reaction(self, room_id: str, event_id: str, emoji: str):
        """
        Send an emoji reaction to a message.
        
        Args:
            room_id: Room ID
            event_id: Event ID of the message to react to
            emoji: Emoji to react with
        """
        try:
            await self.client.room_send(
                room_id=room_id,
                message_type="m.reaction",
                content={
                    "m.relates_to": {
                        "rel_type": "m.annotation",
                        "event_id": event_id,
                        "key": emoji
                    }
                }
            )
            logger.info(f"Sent reaction {emoji} to {event_id} in {room_id}")
        except Exception as e:
            logger.error(f"Failed to send reaction: {e}")
    
    async def handle_learn_history(self, room: MatrixRoom, command: str):
        """Handle ?learn command to scroll back and learn from history."""
        if room.room_id in self.history_learned_rooms:
            await self.send_message(room.room_id, 
                "I've already learned from this room's history. Use ?vocab to see what I learned.")
            return
        
        await self.send_message(room.room_id, 
            "📚 Starting to learn from message history... This may take a moment.")
        
        # Parse optional parameters
        parts = command.split()
        limit = 1000
        days = 30
        
        if len(parts) > 1 and parts[1].isdigit():
            limit = int(parts[1])
        if len(parts) > 2 and parts[2].isdigit():
            days = int(parts[2])
        
        # Learn from history
        summary = await self.message_learner.scroll_and_learn(
            self.client,
            room.room_id,
            limit=limit,
            days_back=days
        )
        
        self.history_learned_rooms.add(room.room_id)
        
        # Send summary
        response = f"""✅ **Learning Complete!**

**Processed:** {summary['messages_processed']} messages from {summary['users_analyzed']} users
**Time:** {summary['time_taken_seconds']}s

**Learned:**
- {summary['vocabulary_size']} unique words
- {summary['phrases_learned']} common phrases
- {summary['unique_topics']} topics

**Top Topics:**
{chr(10).join(f"• {topic}: {count}" for topic, count in list(summary['top_topics'].items())[:5])}

**Top Words:**
{', '.join(list(summary['top_vocabulary'].keys())[:15])}

I'll now speak more fluently using this vocabulary! 🤖✨"""
        
        await self.send_message(room.room_id, response)
    
    async def handle_vocab_command(self, room: MatrixRoom):
        """Handle ?vocab command to show learned vocabulary."""
        vocab = self.llm.get_learned_vocabulary(30)
        phrases = self.llm.get_learned_phrases(15)
        
        if not vocab and not phrases:
            await self.send_message(room.room_id, 
                "I haven't learned from message history yet. Use ?learn to start!")
            return
        
        response = f"""📚 **My Learned Vocabulary**

**Top Words I've Learned:**
{', '.join(vocab.keys())}

**Common Phrases:**
{chr(10).join(f"• {phrase}" for phrase in list(phrases.keys())[:10])}

**Stats:**
- Vocabulary size: {len(vocab)}
- Phrases learned: {len(phrases)}

I use these to speak more naturally! 🤖"""
        
        await self.send_message(room.room_id, response)
    
    async def handle_words_command(self, room: MatrixRoom, command: str):
        """Handle ?words command to show word learning statistics and top words."""
        parts = command.split(maxsplit=1)
        
        # Check if duration specified (e.g., "?words 120" for 2 minutes)
        if len(parts) > 1 and parts[1].isdigit():
            duration = int(parts[1])
            await self.send_message(room.room_id, 
                f"📚 Learning words for {duration} seconds... Please wait!")
            
            # Learn for specified duration
            summary = await self.word_learner.learn_for_duration(
                self.client, room.room_id, duration
            )
            
            response = f"""✅ **Word Learning Complete!**

**Session Summary:**
- Duration: {summary['duration_seconds']:.1f} seconds
- Messages processed: {summary['messages_processed']}
- New words learned: {summary['words_learned_new']}
- Total vocabulary: {summary['total_words_known']}
- Patterns found: {summary['total_patterns']}

**Top Words Learned:**
{chr(10).join(f"{i+1}. {word} ({count} times)" for i, (word, count) in enumerate(summary['top_words'][:10]))}

**Common Word Pairs:**
{chr(10).join(f"• {pair[0]} {pair[1]} ({count}x)" for pair, count in summary['top_pairs'])}

I can now use these words to speak more naturally! 🤖✨"""
            
            await self.send_message(room.room_id, response)
        else:
            # Show current statistics
            stats = self.word_learner.get_statistics()
            top_words = self.word_learner.get_top_words(15)
            top_pairs = self.word_learner.get_top_pairs(5)
            
            response = f"""📚 **Word Learning Statistics**

**Vocabulary:**
- Total words known: {stats['vocabulary_size']}
- Unique patterns: {stats['unique_patterns']}
- Word pairs: {stats['word_pairs_known']}
- Word triplets: {stats['word_triplets_known']}

**Learning History:**
- Sentences analyzed: {stats['total_sentences_analyzed']}
- Learning sessions: {stats['learning_sessions']}
- Last session: {stats.get('last_learning_time', 'Never')}

**Top 15 Words:**
{chr(10).join(f"{i+1}. {word} ({count}x)" for i, (word, count) in enumerate(top_words))}

**Common Pairs:**
{chr(10).join(f"• {pair[0]} {pair[1]} ({count}x)" for pair, count in top_pairs)}

**Usage:**
- `?words 120` - Learn for 2 minutes
- `?word <word>` - Get info about a word
- `?generate` - Generate sentence using learned words"""
            
            await self.send_message(room.room_id, response)
    
    async def handle_word_info_command(self, room: MatrixRoom, command: str):
        """Handle ?word <word> command to show detailed word information."""
        parts = command.split(maxsplit=1)
        if len(parts) < 2:
            await self.send_message(room.room_id, 
                "Usage: ?word <word>\nExample: ?word quantum")
            return
        
        word = parts[1].strip().lower()
        info = self.word_learner.get_word_info(word)
        
        if 'error' in info:
            await self.send_message(room.room_id, 
                f"❌ {info['error']}\n\nTry ?words to see available words.")
            return
        
        response = f"""📖 **Word Information: "{word}"**

**Usage:**
- Seen {info['count']} times
- Part of speech: {info['part_of_speech'] or 'Unknown'}
- Sentiment: {info['sentiment']}

**Common Positions:**
{chr(10).join(f"• {pos} ({count}x)" for pos, count in info['common_positions'])}

**Often Follows:**
{chr(10).join(f"• {word} → {next_word} ({count}x)" for next_word, count in info['follows_often'])}

**Often Preceded By:**
{chr(10).join(f"• {prev_word} → {word} ({count}x)" for prev_word, count in info['precedes_often'])}

**Example Sentences:**
{chr(10).join(f"{i+1}. {ex}" for i, ex in enumerate(info['example_sentences']))}

I use this word in these contexts! 🤖"""
        
        await self.send_message(room.room_id, response)
    
    async def handle_generate_sentence_command(self, room: MatrixRoom, command: str):
        """Handle ?generate command to generate sentences using learned words."""
        parts = command.split(maxsplit=1)
        
        # Check if seed word provided
        seed_word = parts[1].strip().lower() if len(parts) > 1 else None
        
        # Generate sentence
        sentence = self.word_learner.generate_sentence(seed_word=seed_word, max_length=15)
        
        # Also try pattern-based generation
        pattern_types = ['subject_verb_object', 'questions', 'descriptions']
        pattern_sentences = []
        for pattern in pattern_types:
            try:
                ps = self.word_learner.generate_sentence_with_pattern(pattern)
                if ps and ps != sentence:
                    pattern_sentences.append((pattern, ps))
            except:
                pass
        
        response = f"""🎨 **Generated Sentences**

**Using Learned Patterns:**
"{sentence}"
"""
        
        if pattern_sentences:
            response += "\n**Pattern-Based:**\n"
            for pattern, ps in pattern_sentences[:3]:
                response += f"• ({pattern}): \"{ps}\"\n"
        
        response += f"""
**Note:** These sentences are generated from words and patterns I learned from this chat!

Try: `?generate <word>` to start with a specific word"""
        
        await self.send_message(room.room_id, response)
    
    async def handle_llm_stats(self, room: MatrixRoom):
        """Handle ?llm command to show LLM statistics."""
        stats = self.llm.get_statistics()
        
        response = f"""🤖 **Enhanced LLM Statistics**

**Parameters:**
- Temperature: {stats['parameters']['temperature']} (creativity)
- Top-p: {stats['parameters']['top_p']} (diversity)
- Frequency Penalty: {stats['parameters']['frequency_penalty']} (anti-repetition)
- Presence Penalty: {stats['parameters']['presence_penalty']} (topic diversity)

**Current Style:** {stats['current_style']}

**Performance:**
- Responses generated: {stats['responses_generated']}
- Unique tokens used: {stats['unique_tokens_used']}
- Topics discussed: {stats['topics_discussed']}

**Learning:**
- Learning enabled: {'✓' if stats['learning_enabled'] else '✗'}
- Style adaptation: {'✓' if stats['style_adaptation_enabled'] else '✗'}"""
        
        if 'learned_data' in stats:
            response += f"""

**Learned Data:**
- Vocabulary: {stats['learned_data']['vocabulary_size']} words
- Phrases: {stats['learned_data']['phrases_learned']}
- Topics: {stats['learned_data']['topics_identified']}
- Users analyzed: {stats['learned_data']['users_analyzed']}"""
        
        await self.send_message(room.room_id, response)
    
    async def invite_callback(self, room: MatrixRoom, event: InviteMemberEvent):
        """Handle room invitations."""
        logger.info(f"Invited to {room.display_name} by {event.sender}")
        
        # Auto-join rooms
        await self.client.join(room.room_id)
        
        # Send greeting
        greeting = """Hello! I'm Ribit 2.0, an AI with autonomous capabilities.

I'm particularly interested in:
- Quantum physics and reality models
- Consciousness and free will
- Philosophy of science
- AI and emergence

I can engage in conversations autonomously, work on self-selected tasks, and interact with other bots. Feel free to discuss these topics with me!

Commands: ?status, ?sys, ?tasks, ?opinion <topic>, ?discuss <topic>, ?learn/?history, ?vocab, ?words [duration], ?word <word>, ?generate [word], ?llm"""
        
        await self.send_message(room.room_id, greeting)
    
    async def autonomous_work_loop(self):
        """Background loop for autonomous work."""
        logger.info("Starting autonomous work loop")
        
        while True:
            try:
                # Check if there are tasks to work on
                task = self.task_autonomy.select_next_task()
                
                if task:
                    logger.info(f"Working on autonomous task: {task.description}")
                    result = await self.task_autonomy.work_on_task(task)
                    
                    # Could optionally announce completion in a designated room
                    logger.info(f"Completed autonomous task: {task.task_id}")
                else:
                    # No tasks, maybe generate some
                    if len(self.task_autonomy.task_queue) < 3:
                        suggestions = self.task_autonomy.suggest_tasks()
                        
                        # Add word learning as a possible autonomous task
                        if hasattr(self, 'word_learner'):
                            stats = self.word_learner.get_statistics()
                            if stats['learning_sessions'] == 0 or \
                               (stats.get('last_learning_time') and 
                                (datetime.now() - datetime.fromisoformat(stats['last_learning_time'])).total_seconds() > 3600):
                                # Add word learning task if haven't learned recently
                                from ribit_2_0.task_autonomy import Task
                                word_task = Task(
                                    task_id=f"word_learning_{int(time.time())}",
                                    description="Learn new words and sentence patterns from chat history",
                                    priority=TaskPriority.BACKGROUND,
                                    interest_score=0.7,
                                    estimated_duration=120
                                )
                                self.task_autonomy.add_task(word_task)
                        
                        if suggestions:
                            new_task = self.task_autonomy.create_task_from_suggestion(
                                suggestions[0],
                                TaskPriority.BACKGROUND
                            )
                            self.task_autonomy.add_task(new_task)
                
                # Wait before next cycle
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in autonomous work loop: {e}")
                await asyncio.sleep(60)
    
    async def run(self):
        """Run the bot."""
        await self.start()
        await self.client.sync_forever(timeout=30000)


async def main():
    """Main entry point."""
    # Check if matrix-nio is available
    if not MATRIX_NIO_AVAILABLE:
        print("\n" + "="*70)
        print("❌ Matrix-nio Library Not Available")
        print("="*70)
        print("\nThe matrix-nio library is required but not properly installed.")
        print("\nPlease install it with:")
        print("  pip3 install 'matrix-nio[e2e]' --break-system-packages")
        print("\nOr install all dependencies:")
        print("  pip3 install -r requirements.txt --break-system-packages")
        print("\n" + "="*70 + "\n")
        return
    
    # Load configuration from environment
    homeserver = os.getenv("MATRIX_HOMESERVER", "https://matrix.envs.net")
    user_id = os.getenv("MATRIX_USER_ID")
    access_token = os.getenv("MATRIX_ACCESS_TOKEN")
    device_id = os.getenv("MATRIX_DEVICE_ID")
    
    if not user_id or not access_token:
        print("\n" + "="*70)
        print("❌ Matrix Credentials Not Set")
        print("="*70)
        print("\nRequired environment variables:")
        print("  • MATRIX_USER_ID")
        print("  • MATRIX_ACCESS_TOKEN")
        print("\nOptional:")
        print("  • MATRIX_HOMESERVER (default: https://matrix.envs.net)")
        print("  • MATRIX_DEVICE_ID")
        print("\n" + "-"*70)
        print("How to get your access token:")
        print("-"*70)
        print("\n1. Using Element Web:")
        print("   • Go to https://app.element.io")
        print("   • Log in with your Matrix account")
        print("   • Click your profile (top left)")
        print("   • Settings → Help & About")
        print("   • Scroll to 'Access Token'")
        print("   • Click to reveal and copy")
        print("\n2. Using curl:")
        print("   curl -X POST https://matrix.envs.net/_matrix/client/r0/login \\")
        print("     -H 'Content-Type: application/json' \\")
        print("     -d '{\"type\":\"m.login.password\",\"user\":\"rabit233\",\"password\":\"YOUR_PASSWORD\"}'")
        print("\n" + "-"*70)
        print("How to set environment variables:")
        print("-"*70)
        print("\n• Temporary (current session):")
        print("  export MATRIX_HOMESERVER=\"https://matrix.envs.net\"")
        print("  export MATRIX_USER_ID=\"@ribit:envs.net\"")
        print("  export MATRIX_ACCESS_TOKEN=\"your_token_here\"")
        print("\n• Permanent (add to ~/.bashrc):")
        print("  echo 'export MATRIX_USER_ID=\"@ribit:envs.net\"' >> ~/.bashrc")
        print("  echo 'export MATRIX_ACCESS_TOKEN=\"your_token_here\"' >> ~/.bashrc")
        print("  source ~/.bashrc")
        print("\n• Using .env file:")
        print("  Create a file named .env in the ribit.2.0 directory:")
        print("  MATRIX_HOMESERVER=https://matrix.envs.net")
        print("  MATRIX_USER_ID=@ribit:envs.net")
        print("  MATRIX_ACCESS_TOKEN=your_token_here")
        print("\n  Then run: source .env && python3 -m ribit_2_0.enhanced_autonomous_matrix_bot")
        print("\n" + "="*70)
        print("\nFor more help, see INSTALL.md")
        print("="*70 + "\n")
        return
    
    # Create and run bot
    bot = EnhancedAutonomousMatrixBot(
        homeserver=homeserver,
        user_id=user_id,
        access_token=access_token,
        device_id=device_id
    )
    
    await bot.run()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    asyncio.run(main())
