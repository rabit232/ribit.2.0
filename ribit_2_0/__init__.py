try:
    from .agent import Ribit20Agent, main_async, main_cli
except Exception as e:
    print(f"Warning: Could not import agent module: {e}")
    Ribit20Agent = None
    main_async = None
    main_cli = None

try:
    from .controller import VisionSystemController
except Exception as e:
    print(f"Warning: Could not import VisionSystemController: {e}")
    VisionSystemController = None

try:
    from .llm_wrapper import Ribit20LLM
except Exception as e:
    print(f"Warning: Could not import Ribit20LLM: {e}")
    Ribit20LLM = None

try:
    from .mock_llm_wrapper import MockRibit20LLM
except Exception as e:
    print(f"Warning: Could not import MockRibit20LLM: {e}")
    MockRibit20LLM = None

try:
    from .mock_controller import MockVisionSystemController
except Exception as e:
    print(f"Warning: Could not import MockVisionSystemController: {e}")
    MockVisionSystemController = None

try:
    from .knowledge_base import KnowledgeBase
except Exception as e:
    print(f"Warning: Could not import KnowledgeBase: {e}")
    KnowledgeBase = None

try:
    from .ros_controller import RibitROSController
except Exception as e:
    print(f"Warning: Could not import RibitROSController: {e}")
    RibitROSController = None

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

try:
    from .megabite_llm import MegabiteLLM
except Exception as e:
    print(f"Warning: Could not import MegabiteLLM: {e}")
    MegabiteLLM = None

__version__ = "2.0.0"
__author__ = "Manus AI & rabit232"
__email__ = "contact@manus.im"
__description__ = "Enhanced AI agent with production-ready LLM emulator and emotional intelligence"

_all_exports = []

if Ribit20Agent is not None:
    _all_exports.append("Ribit20Agent")
if VisionSystemController is not None:
    _all_exports.append("VisionSystemController")
if MockVisionSystemController is not None:
    _all_exports.append("MockVisionSystemController")
if RibitROSController is not None:
    _all_exports.append("RibitROSController")
if Ribit20LLM is not None:
    _all_exports.append("Ribit20LLM")
if MockRibit20LLM is not None:
    _all_exports.append("MockRibit20LLM")
if KnowledgeBase is not None:
    _all_exports.append("KnowledgeBase")
if main_async is not None:
    _all_exports.append("main_async")
if main_cli is not None:
    _all_exports.append("main_cli")
if RibitMatrixBot is not None:
    _all_exports.append("RibitMatrixBot")
if JinaSearchEngine is not None:
    _all_exports.append("JinaSearchEngine")
if AdvancedConversationManager is not None:
    _all_exports.extend(["AdvancedConversationManager", "ConversationMessage", "ConversationSummary"])
if MegabiteLLM is not None:
    _all_exports.append("MegabiteLLM")

__all__ = _all_exports

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
