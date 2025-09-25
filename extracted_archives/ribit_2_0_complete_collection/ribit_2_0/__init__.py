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
from .matrix_bot import RibitMatrixBot
from .jina_integration import JinaSearchEngine
from .conversation_manager import AdvancedConversationManager, ConversationMessage, ConversationSummary

__version__ = "2.0.0"
__author__ = "Manus AI & rabit232"
__email__ = "contact@manus.im"
__description__ = "Enhanced AI agent with production-ready LLM emulator and emotional intelligence"

# Core classes for easy import
__all__ = [
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
    "AdvancedConversationManager",
    "ConversationMessage",
    "ConversationSummary",
    
    # Internet and communication
    "JinaSearchEngine",
    "RibitMatrixBot",
    
    # CLI functions
    "main_async",
    "main_cli",
]

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


