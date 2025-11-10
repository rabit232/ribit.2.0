"""
Megabite - Matrix Learning Commands

Handles ?words, ?opinion, ?perspective, ?learn, ?personality commands in Matrix chat.

Author: Manus AI
"""

import logging
from typing import Optional, Dict, Any
import asyncio

from .word_learning_manager import WordLearningManager
from .perspective_system import PerspectiveSystem
from .opinion_engine import OpinionEngine
from .llm_manager import LLMManager

logger = logging.getLogger(__name__)


class MatrixLearningCommands:
    """Handles learning-related Matrix commands."""

    def __init__(
        self,
        llm_manager: LLMManager,
        word_learning: WordLearningManager,
        perspective_system: PerspectiveSystem,
        opinion_engine: OpinionEngine
    ):
        """Initialize command handler."""
        self.llm = llm_manager
        self.word_learning = word_learning
        self.perspective = perspective_system
        self.opinion = opinion_engine

    async def handle_words_command(self, user_id: str, room_id: str) -> str:
        """Handle ?words command - show vocabulary statistics."""
        try:
            stats = await self.word_learning.get_vocabulary_stats()
            iq = await self.word_learning.get_intelligence_quotient()

            total_words = stats.get('total_words', 0)
            total_uses = stats.get('total_occurrences', 0)
            avg_uses = stats.get('average_occurrences', 0)

            most_common = stats.get('most_common', [])
            recent = stats.get('recently_learned', [])

            response = f"""📚 **My Vocabulary Statistics**

**Overview:**
- Total words learned: **{total_words}**
- Total word usages: **{total_uses}**
- Average uses per word: **{avg_uses:.1f}**

**Intelligence:**
- Intelligence level: **{iq.get('intelligence_level', 'unknown')}**
- Total weight: **{iq.get('total_weight', 1.0):.2f}**
- Vocabulary weight: **{iq.get('vocabulary_weight', 0.0):.2f}**

**Most Common Words:**
"""

            for i, word_data in enumerate(most_common[:5], 1):
                word = word_data.get('word', '')
                count = word_data.get('count', 0)
                response += f"{i}. {word} ({count} times)\n"

            response += "\n**Recently Learned:**\n"
            for i, word_data in enumerate(recent[:5], 1):
                word = word_data.get('word', '')
                response += f"{i}. {word}\n"

            return response

        except Exception as e:
            logger.error(f"Error in ?words command: {e}")
            return f"Error getting vocabulary stats: {str(e)}"

    async def handle_opinion_command(
        self,
        question: str,
        user_id: str,
        room_id: str
    ) -> str:
        """Handle ?opinion command - form opinion on question."""
        if not question.strip():
            return "Please ask a question. Usage: ?opinion What do you think about AI?"

        try:
            result = await self.opinion.form_opinion(question, user_id, room_id)

            confidence = result.get('confidence', 0.5)
            confidence_str = "high" if confidence > 0.7 else "moderate" if confidence > 0.4 else "low"

            response = f"""💭 **My Opinion**

**Question:** {question}

**Opinion:**
{result.get('opinion', 'Unable to form opinion.')}

**Reasoning:**
{result.get('reasoning', 'No reasoning available.')}

**Confidence:** {confidence_str} ({confidence:.0%})
"""

            if result.get('is_cached'):
                response += "\n*(This opinion was formed previously)*"

            return response

        except Exception as e:
            logger.error(f"Error in ?opinion command: {e}")
            return f"Error forming opinion: {str(e)}"

    async def handle_perspective_command(
        self,
        text: str,
        user_id: str,
        room_id: str,
        message_id: Optional[str] = None
    ) -> str:
        """Handle ?perspective command - analyze large text."""
        if not text.strip():
            return "Please provide text to analyze. You can paste up to 10MB of text."

        text_size = len(text.encode('utf-8'))
        if text_size > 10 * 1024 * 1024:
            return f"Text too large: {text_size/1024/1024:.1f}MB (max 10MB)"

        try:
            # Send initial response
            initial = f"🔍 **Analyzing {text_size/1024:.1f}KB of text...**\n\nThis may take a moment..."

            # Start analysis
            result = await self.perspective.analyze_perspective(
                text, user_id, room_id, message_id
            )

            # Build response
            topics = result.get('main_topics', [])
            concepts = result.get('key_concepts', [])
            score = result.get('interesting_score', 0)
            integrated = result.get('integrated_to_personality', False)

            response = f"""✨ **Perspective Analysis Complete**

**Text Size:** {text_size/1024:.1f}KB ({result.get('word_count', 0)} words)
**Processing Time:** {result.get('processing_time_ms', 0)/1000:.1f}s

**Main Topics:**
{', '.join(topics[:5])}

**Key Concepts:**
{', '.join(concepts[:7])}

**My Opinion:**
{result.get('bot_opinion', 'No opinion formed.')}

**My Reasoning:**
{result.get('bot_reasoning', 'No reasoning available.')}

**Learning Results:**
- Words learned: {result.get('words_learned', 0)}
- Patterns extracted: {result.get('patterns_extracted', 0)}
- Interestingness score: {score:.0%}
"""

            if integrated:
                response += "\n🌟 **This content was so interesting, I've integrated it into my personality!**"
                updates = result.get('personality_updates', {})
                new_traits = updates.get('new_traits', [])
                if new_traits:
                    response += f"\nNew interests: {', '.join(new_traits)}"

            return response

        except Exception as e:
            logger.error(f"Error in ?perspective command: {e}")
            return f"Error analyzing perspective: {str(e)}"

    async def handle_learn_command(
        self,
        months: int,
        user_id: str,
        room_id: str,
        matrix_client: Any = None
    ) -> str:
        """Handle ?learn command - learn from chat history."""
        if months < 1 or months > 12:
            return "Please specify 1-12 months. Usage: ?learn 3"

        if not matrix_client:
            return "Matrix client not available for history learning."

        try:
            response = f"📖 **Learning from {months} months of chat history...**\n\n"

            # This would integrate with Ribit 2.0's message_history_learner
            # For now, return placeholder
            response += "This feature requires integration with Matrix room history.\n"
            response += f"Will scroll back {months} months and learn all words and patterns.\n"
            response += "\nComing soon!"

            return response

        except Exception as e:
            logger.error(f"Error in ?learn command: {e}")
            return f"Error learning from history: {str(e)}"

    async def handle_personality_command(self, user_id: str, room_id: str) -> str:
        """Handle ?personality command - show personality traits."""
        try:
            # Get personality summary from Supabase
            summary = await self.opinion.client.rpc('get_personality_summary').execute()

            if not summary.data:
                return "I don't have any personality traits yet. Analyze some interesting content with ?perspective!"

            data = summary.data
            total = data.get('total_traits', 0)
            active = data.get('active_traits', 0)
            strongest = data.get('strongest_traits', [])

            response = f"""🎭 **My Personality**

**Overview:**
- Total traits: {total}
- Active traits: {active}

**Strongest Traits:**
"""

            for i, trait in enumerate(strongest[:7], 1):
                name = trait.get('name', '').replace('_', ' ').title()
                strength = trait.get('strength', 0)
                category = trait.get('category', 'unknown')
                response += f"{i}. {name} [{category}] - strength: {strength:.0%}\n"

            return response

        except Exception as e:
            logger.error(f"Error in ?personality command: {e}")
            return f"Error getting personality: {str(e)}"

    async def handle_vocabulary_command(
        self,
        format: str,
        user_id: str,
        room_id: str
    ) -> str:
        """Handle ?vocabulary command - export vocabulary."""
        if format not in ['json', 'csv', 'text']:
            format = 'text'

        try:
            if format == 'text':
                # Return text summary
                words = await self.word_learning.get_most_common_words(limit=50)

                response = "📖 **My Vocabulary (Top 50 Words)**\n\n"
                for i, word_data in enumerate(words, 1):
                    word = word_data.get('word', '')
                    count = word_data.get('count', 0)
                    score = word_data.get('importance_score', 1.0)
                    response += f"{i:2d}. {word:15s} - {count:4d} uses (importance: {score:.1f})\n"

                return response
            else:
                # Export as file (would need file upload capability)
                vocab_data = await self.word_learning.export_vocabulary(format)
                return f"Vocabulary export ({format}):\n```{vocab_data[:500]}...\n```\n*(Full export would be saved to file)*"

        except Exception as e:
            logger.error(f"Error in ?vocabulary command: {e}")
            return f"Error exporting vocabulary: {str(e)}"

    async def handle_command(
        self,
        command: str,
        args: str,
        user_id: str,
        room_id: str,
        message_id: Optional[str] = None,
        matrix_client: Any = None
    ) -> str:
        """
        Main command dispatcher.

        Args:
            command: Command name (words, opinion, perspective, etc.)
            args: Command arguments
            user_id: Matrix user ID
            room_id: Matrix room ID
            message_id: Optional message ID
            matrix_client: Optional Matrix client for history

        Returns:
            Response string
        """
        command = command.lower().strip()

        if command == 'words':
            return await self.handle_words_command(user_id, room_id)

        elif command == 'opinion':
            return await self.handle_opinion_command(args, user_id, room_id)

        elif command == 'perspective':
            return await self.handle_perspective_command(
                args, user_id, room_id, message_id
            )

        elif command == 'learn':
            try:
                months = int(args.strip()) if args.strip() else 3
            except ValueError:
                months = 3
            return await self.handle_learn_command(
                months, user_id, room_id, matrix_client
            )

        elif command == 'personality':
            return await self.handle_personality_command(user_id, room_id)

        elif command == 'vocabulary':
            format_arg = args.strip().lower() if args.strip() else 'text'
            return await self.handle_vocabulary_command(format_arg, user_id, room_id)

        else:
            return f"Unknown learning command: {command}\n\nAvailable commands:\n?words, ?opinion, ?perspective, ?learn, ?personality, ?vocabulary"
