#!/usr/bin/env python3
"""
Megabite Interactive CLI
=========================

Interactive command-line interface for Megabite AI.
Allows asking questions, posting thought experiments, and learning from text.

Commands:
- ask <question>         - Ask Megabite a question
- thought <experiment>   - Post a thought experiment for analysis
- learn <text>          - Learn from text and add to knowledge base
- opinion <topic>       - Get Megabite's opinion on a topic
- status                - Check Megabite status
- help                  - Show available commands
- exit/quit             - Exit the CLI

Author: Manus AI for rabit232/megabite
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from megabite_core.megabite_llm import MegabiteLLM
from megabite_core.word_learning_system import WordLearningSystem
from megabite_core.enhanced_emotions import EnhancedEmotionalIntelligence
from megabite_core.philosophical_reasoning import PhilosophicalReasoning
from megabite_core.conversation_manager import AdvancedConversationManager, ConversationMessage
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class MegabiteCLI:
    """Interactive CLI for Megabite AI."""
    
    def __init__(self):
        """Initialize Megabite CLI."""
        print("\n" + "="*60)
        print("🧠 Megabite Interactive CLI")
        print("="*60)
        print("Initializing Megabite AI systems...")
        
        # Initialize core systems
        self.llm = MegabiteLLM()
        self.word_learner = WordLearningSystem()
        self.emotions = EnhancedEmotionalIntelligence()
        self.conversation = AdvancedConversationManager()
        
        # Try to initialize philosophical reasoning
        try:
            self.philosophy = PhilosophicalReasoning()
        except Exception as e:
            logger.warning(f"Philosophical reasoning not available: {e}")
            self.philosophy = None
        
        print("✅ Megabite AI initialized!")
        print("\nType 'help' for available commands, 'exit' to quit.\n")
    
    def show_help(self):
        """Show available commands."""
        help_text = """
╔════════════════════════════════════════════════════════════╗
║                  Megabite CLI Commands                     ║
╚════════════════════════════════════════════════════════════╝

📝 Basic Commands:
  ask <question>         Ask Megabite a question
  thought <experiment>   Post a thought experiment for analysis
  learn <text>          Learn from text and add to knowledge base
  opinion <topic>       Get Megabite's opinion on a topic
  
🔧 System Commands:
  status                Check Megabite system status
  stats                 Show learning statistics
  help                  Show this help message
  clear                 Clear the screen
  exit / quit           Exit the CLI

💡 Tips:
  - You can paste long text after 'thought' or 'learn'
  - Megabite learns from everything you teach it
  - Use 'opinion' to get philosophical perspectives
  - All interactions are saved to the knowledge base

Examples:
  ask What is consciousness?
  thought If a tree falls in a forest...
  learn The universe is deterministic at macro scale
  opinion free will vs determinism
"""
        print(help_text)
    
    def ask_question(self, question: str):
        """Ask Megabite a question."""
        if not question.strip():
            print("❌ Please provide a question.")
            return
        
        print(f"\n🤔 Processing: {question[:60]}...")
        
        # Get emotional context
        emotion = self.emotions.get_emotion_by_context(
            context=question,
            situation="curiosity"
        )
        
        # Generate response
        response = self.llm.generate_response(question, context=[])
        
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
            user_id="megabite",
            message_type="bot",
            content=response,
            timestamp=datetime.now()
        )
        self.conversation.add_message(user_msg)
        self.conversation.add_message(bot_msg)
        
        print(f"\n💭 Emotion: {emotion}")
        print(f"\n🧠 Megabite Response:\n{response}\n")
    
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
        
        # Generate Megabite's response
        response = self.llm.generate_response(
            f"Analyze this thought experiment: {experiment[:500]}",
            context=[]
        )
        
        # Get emotional response
        emotion = self.emotions.get_emotion_by_context(
            context=experiment,
            situation="confidence"
        )
        
        print(f"💭 Emotional Response: {emotion}")
        print(f"\n🧠 Megabite's Analysis:\n{response}\n")
        
        # Update knowledge base
        try:
            concept = experiment.split('.')[0][:50]
            self.llm.update_knowledge(concept, experiment[:200])
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
                    self.llm.update_knowledge(concept, sentence.strip()[:100])
            print("\n✅ Added to Megabite's knowledge base!")
        except Exception as e:
            logger.warning(f"Knowledge update failed: {e}")
    
    def get_opinion(self, topic: str):
        """Get Megabite's opinion on a topic."""
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
        
        # Generate opinion
        prompt = f"What is your opinion on: {topic}? Provide a thoughtful, philosophical perspective."
        response = self.llm.generate_response(prompt, context=[])
        
        # Get emotional stance
        emotion = self.emotions.get_emotion_by_context(
            context=topic,
            situation="confidence"
        )
        
        print(f"💭 Emotional Stance: {emotion}")
        print(f"\n🧠 Megabite's Opinion:\n{response}\n")
    
    def show_status(self):
        """Show system status."""
        status = self.llm.check_status()
        stats = self.word_learner.get_statistics()
        
        print("\n" + "="*60)
        print("📊 Megabite System Status")
        print("="*60)
        print(f"\n🧠 LLM Status:")
        print(f"   Name: {status['name']}")
        print(f"   Available: {status['available']}")
        print(f"   Status: {status['status_message']}")
        
        print(f"\n📚 Learning Statistics:")
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
        print("📊 Learning Statistics")
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
                user_input = input("megabite> ").strip()
                
                if not user_input:
                    continue
                
                # Parse command
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                # Process command
                if command in ['exit', 'quit']:
                    print("\n👋 Goodbye! Megabite shutting down...\n")
                    break
                
                elif command in ['help', '?help']:
                    self.show_help()
                
                elif command == 'clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                
                elif command == 'status':
                    self.show_status()
                
                elif command == 'stats':
                    self.show_stats()
                
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
        cli = MegabiteCLI()
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
