"""
Ribit 2.0: Enhanced AI Agent with Production-Ready LLM Emulator

An elegant, wise, and knowledgeable AI agent for GUI automation and robotic control
with advanced emotional intelligence, ROS integration, Matrix bot capabilities,
and Jina.ai-powered internet search.

Author: Manus AI & rabit232
Version: 2.0.0
"""

from .agent import Ribit20Agent, main_async, main_cli
from .controller import VisionSystemController
from .llm_wrapper import Ribit20LLM
from .mock_llm_wrapper import MockRibit20LLM
from .mock_controller import MockVisionSystemController
from .knowledge_base import KnowledgeBase
from .ros_controller import RibitROSController

try:
    from .matrix_bot import RibitMatrixBot
except Exception as e:
    print(f"Warning: Could not import RibitMatrixBot: {e}")
    RibitMatrixBot = None

try:
    from .jina_integration import JinaSearchEngine
except Exception as e:
    print(f"Warning: Could not import JinaSearchEngine: {e}")
    JinaSearchEngine = None

try:
    from .conversation_manager import AdvancedConversationManager, ConversationMessage, ConversationSummary
except Exception as e:
    print(f"Warning: Could not import conversation_manager: {e}")
    AdvancedConversationManager = None
    ConversationMessage = None
    ConversationSummary = None

__version__ = "2.0.0"
__author__ = "Manus AI & rabit232"
__email__ = "contact@manus.im"
__description__ = "Enhanced AI agent with production-ready LLM emulator and emotional intelligence"

# Core classes for easy import
_all_exports = [
    # Main agent and controllers
    "Ribit20Agent",
    "VisionSystemController",
    "MockVisionSystemController",
    "RibitROSController",

    # LLM interfaces
    "Ribit20LLM",
    "MockRibit20LLM",

    # Knowledge and conversation management
    "KnowledgeBase",

    # CLI functions
    "main_async",
    "main_cli",
]

# Add optional exports if they were successfully imported
if RibitMatrixBot is not None:
    _all_exports.append("RibitMatrixBot")
if JinaSearchEngine is not None:
    _all_exports.append("JinaSearchEngine")
if AdvancedConversationManager is not None:
    _all_exports.extend(["AdvancedConversationManager", "ConversationMessage", "ConversationSummary"])

__all__ = _all_exports

# Package metadata
__package_info__ = {
    "name": "ribit_2_0",
    "version": __version__,
    "description": __description__,
    "author": __author__,
    "email": __email__,
    "url": "https://github.com/rabit232/ribit.2.0",
    "keywords": ["ai", "agent", "automation", "robotics", "ros", "matrix", "llm", "emotional-intelligence"],
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
}


