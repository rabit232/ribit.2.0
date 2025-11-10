"""
Megabite - Ribit 2.0 Compatibility Layer

Ensures seamless integration between Megabite and Ribit 2.0 modules.
Handles naming conflicts and provides backward compatibility.

Author: Manus AI
"""

import sys
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class RibitCompatibilityLayer:
    """Manages compatibility between Megabite and Ribit 2.0."""

    def __init__(self):
        """Initialize compatibility layer."""
        self.ribit_modules = {}
        self.megabite_modules = {}
        self.conflicts_resolved = {}

    def load_ribit_modules(self) -> dict:
        """Load Ribit 2.0 modules with graceful fallback."""
        modules = {}

        # Try to import Ribit 2.0 modules
        module_names = [
            'conversation_manager',
            'enhanced_emotions',
            'matrix_bot',
            'word_learning_system',
            'message_history_learner',
            'linguistics_engine',
            'conversational_mode',
            'knowledge_base'
        ]

        for module_name in module_names:
            try:
                # Import from ribit_2_0 package
                full_name = f'ribit_2_0.{module_name}'
                if full_name in sys.modules:
                    modules[module_name] = sys.modules[full_name]
                else:
                    module = __import__(full_name, fromlist=[module_name])
                    modules[module_name] = module
                logger.info(f"Loaded Ribit 2.0 module: {module_name}")
            except ImportError as e:
                logger.warning(f"Could not load Ribit 2.0 module {module_name}: {e}")
                modules[module_name] = None

        self.ribit_modules = modules
        return modules

    def get_word_learning_system(self) -> Optional[Any]:
        """Get Ribit 2.0 word learning system if available."""
        if 'word_learning_system' not in self.ribit_modules:
            self.load_ribit_modules()

        module = self.ribit_modules.get('word_learning_system')
        if module:
            try:
                return module.WordLearningSystem
            except AttributeError:
                return None
        return None

    def get_message_history_learner(self) -> Optional[Any]:
        """Get Ribit 2.0 message history learner if available."""
        if 'message_history_learner' not in self.ribit_modules:
            self.load_ribit_modules()

        module = self.ribit_modules.get('message_history_learner')
        if module:
            try:
                return module.MessageHistoryLearner
            except AttributeError:
                return None
        return None

    def get_conversation_manager(self) -> Optional[Any]:
        """Get Ribit 2.0 conversation manager if available."""
        if 'conversation_manager' not in self.ribit_modules:
            self.load_ribit_modules()

        module = self.ribit_modules.get('conversation_manager')
        if module:
            try:
                return module.AdvancedConversationManager
            except AttributeError:
                return None
        return None

    def get_enhanced_emotions(self) -> Optional[Any]:
        """Get Ribit 2.0 enhanced emotions if available."""
        if 'enhanced_emotions' not in self.ribit_modules:
            self.load_ribit_modules()

        module = self.ribit_modules.get('enhanced_emotions')
        if module:
            try:
                return module.EnhancedEmotionalIntelligence
            except AttributeError:
                return None
        return None

    def bridge_word_learning(
        self,
        ribit_word_learner: Any,
        megabite_word_manager: Any
    ):
        """Bridge between Ribit 2.0 word learning and Megabite word learning."""
        # This allows both systems to work together
        # Ribit 2.0 learns words locally, Megabite persists to Supabase

        class BridgedWordLearning:
            def __init__(self, ribit_learner, megabite_manager):
                self.ribit = ribit_learner
                self.megabite = megabite_manager

            async def learn_from_message(self, message: str, **kwargs):
                # Use both systems
                results = {}

                # Ribit 2.0 local learning
                if self.ribit:
                    try:
                        self.ribit.learn_from_message(message)
                        results['ribit_local'] = True
                    except Exception as e:
                        logger.warning(f"Ribit local learning failed: {e}")
                        results['ribit_local'] = False

                # Megabite Supabase learning
                if self.megabite:
                    try:
                        stats = await self.megabite.learn_from_message(message, **kwargs)
                        results['megabite_stats'] = stats
                    except Exception as e:
                        logger.warning(f"Megabite learning failed: {e}")
                        results['megabite_stats'] = None

                return results

        return BridgedWordLearning(ribit_word_learner, megabite_word_manager)

    def create_unified_interface(self):
        """Create unified interface for all features."""
        return {
            'word_learning': self.get_word_learning_system(),
            'history_learner': self.get_message_history_learner(),
            'conversation_manager': self.get_conversation_manager(),
            'emotions': self.get_enhanced_emotions(),
            'available_modules': list(self.ribit_modules.keys())
        }


# Global compatibility instance
_compat_layer = None


def get_compat_layer() -> RibitCompatibilityLayer:
    """Get global compatibility layer instance."""
    global _compat_layer
    if _compat_layer is None:
        _compat_layer = RibitCompatibilityLayer()
    return _compat_layer


def ensure_compatibility():
    """Ensure Megabite and Ribit 2.0 work together."""
    layer = get_compat_layer()
    layer.load_ribit_modules()

    available = [name for name, mod in layer.ribit_modules.items() if mod is not None]
    unavailable = [name for name, mod in layer.ribit_modules.items() if mod is None]

    logger.info(f"Ribit 2.0 compatibility: {len(available)} modules available")
    if unavailable:
        logger.info(f"Unavailable modules (optional): {', '.join(unavailable)}")

    return layer
