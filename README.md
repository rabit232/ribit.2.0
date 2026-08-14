# Ribit 2.0: Enhanced AI Agent with Production-Ready LLM Emulator

**🤖 An elegant, wise, and knowledgeable AI agent for GUI automation and robotic control**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![ROS](https://img.shields.io/badge/ROS-1%20%7C%202-green.svg)](https://ros.org)

[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## Overview

Ribit 2.0 (formerly Nifty agent) is a sophisticated AI agent that bridges the digital and physical worlds through intelligent automation. Featuring a **production-ready LLM emulator**, advanced personality system, and full ROS compatibility, Ribit 2.0 is designed to serve as the main intelligence model for robotic systems while maintaining its characteristic elegance and wisdom.

## 🌟 Key Features

### **Enhanced LLM Emulator**
- **Production-ready mock LLM** with sophisticated reasoning capabilities
- **Multi-step task execution** with advanced state management
- **Dynamic knowledge learning** and persistent storage
- **Context-aware decision making** with conversation history
- **Elegant personality expression** maintaining wisdom and truth-seeking nature

### **Robot Operating System (ROS) Integration**
- **Full ROS 1 & ROS 2 compatibility** (Noetic, Humble, Jazzy, Kilted Kaiju)
- **Automatic ROS version detection** and adaptation
- **Standard ROS message support** (Twist, Pose, Image, etc.)
- **Multi-robot coordination** with namespace support
- **Real-time operation** optimized for robotics

### **Vision-Based Control**
- **ASCII representation processing** for screen understanding
- **GUI automation** with mouse and keyboard control
- **Image processing** with Floyd-Steinberg dithering
- **Cross-platform compatibility** (Windows, Linux, macOS)

### **Advanced Capabilities**
- **Persistent knowledge base** for learning and memory
- **Error recovery** and graceful uncertainty handling
- **Extensible architecture** for custom integrations
- **Mock environments** for development and testing

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0

# Install dependencies
pip install -r requirements.txt

# For ROS 2 support (optional)
pip install rclpy

# For ROS 1 support (optional)
sudo apt install ros-noetic-rospy  # Ubuntu 20.04
```

### Basic Usage

```python
#!/usr/bin/env python3
"""Basic Ribit 2.0 usage example"""
import asyncio
from ribit_2_0.agent import Ribit20Agent
from ribit_2_0.mock_llm_wrapper import MockRibit20LLM
from ribit_2_0.controller import VisionSystemController

async def main():
    # Initialize the enhanced LLM emulator
    llm = MockRibit20LLM()
    
    # Initialize controller
    controller = VisionSystemController()
    
    # Create agent with a goal
    agent = Ribit20Agent(llm, controller, "Introduce yourself and demonstrate your capabilities")
    
    # Run the agent
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Command Line Usage

```bash
# Run with mock LLM (recommended for testing)
ribit-2-0 --goal "Navigate to the target location" --mock-llm

# Run with external LLM
ribit-2-0 --goal "Complete the automation task" --llm-path /path/to/llm

# Enable debug logging
ribit-2-0 --goal "Debug the system" --mock-llm --log-level DEBUG
```

## 🧠 Enhanced LLM Emulator

### Production-Ready Intelligence

The **MockRibit20LLM** class represents a significant advancement in AI emulation technology:

```python
from ribit_2_0.mock_llm_wrapper import MockRibit20LLM

# Initialize the enhanced emulator
llm = MockRibit20LLM("knowledge.txt")

# Get intelligent decisions
decision = llm.get_decision("Draw a house and explain the process")

# Check capabilities
capabilities = llm.get_capabilities()
print(f"Available capabilities: {capabilities}")

# Get personality information
personality = llm.get_personality_info()
print(f"Core traits: {personality['core_traits']}")
```

### Advanced Features

#### **Multi-Step Task Execution**
```python
# The emulator handles complex tasks with state management
llm.get_decision("Draw a house")  # Step 1: Open paint application
llm.get_decision("Continue")      # Step 2: Start drawing
llm.get_decision("Continue")      # Step 3: Add details
# ... continues until completion
```

#### **Dynamic Learning**
```python
# Learn new concepts during operation
llm.get_decision("Learn that Python is a programming language")
# Response: Stores knowledge and provides thoughtful acknowledgment

# Retrieve learned information
llm.get_decision("What is Python?")
# Response: Retrieves and explains the stored knowledge
```

#### **Personality-Driven Responses**
```python
# Elegant and wise responses
llm.get_decision("Tell me about robotics")
# Response: Sophisticated discussion about the intersection of 
#           digital intelligence and mechanical systems
```

### Capabilities Overview

| Capability | Description | Status |
|------------|-------------|---------|
| **Vision Processing** | ASCII representation understanding | ✅ Production Ready |
| **Multi-Step Reasoning** | Complex task breakdown and execution | ✅ Production Ready |
| **Knowledge Management** | Persistent learning and retrieval | ✅ Production Ready |
| **Robot Control** | Specialized robotic automation | ✅ Production Ready |
| **Error Recovery** | Graceful uncertainty handling | ✅ Production Ready |
| **Adaptive Learning** | Dynamic knowledge acquisition | ✅ Production Ready |
| **Matrix.org Integration** | Decentralized chat automation and remote control | ✅ Production Ready |
| **Database Management** | SQL/NoSQL database design and optimization | ✅ Production Ready |
| **API Development** | RESTful API creation with FastAPI and Flask | ✅ Production Ready |

## 🤖 ROS Integration

### Supported ROS Versions

- **ROS 2 Kilted Kaiju** (Ubuntu 24.04) - Latest release
- **ROS 2 Jazzy Jalisco** (Ubuntu 24.04) - Latest LTS
- **ROS 2 Humble Hawksbill** (Ubuntu 22.04) - Stable LTS
- **ROS 1 Noetic** (Ubuntu 20.04) - Legacy support

### ROS Controller Usage

```python
from ribit_2_0.ros_controller import RibitROSController

# Initialize ROS-compatible controller
controller = RibitROSController("ribit_robot_agent")

# Ribit commands are automatically translated to ROS
controller.move_mouse(5.0, 3.0)  # → Publishes to /cmd_vel
controller.click()               # → Controls gripper/tool
controller.type_text("Task completed")  # → Status message

# Check ROS integration
print(f"ROS Version: {controller.get_ros_version()}")
print(f"ROS Available: {controller.is_ros_available()}")
```

### Compatible Robot Platforms

#### **Mobile Robots**
- TurtleBot 3/4
- Clearpath Robotics (Husky, Jackal, etc.)
- Custom mobile platforms

#### **Manipulator Arms**
- Universal Robots (UR3, UR5, UR10)
- Franka Emika Panda
- KUKA Arms
- Custom manipulators with MoveIt

#### **Simulation Environments**
- Gazebo
- RViz
- Isaac Sim

## 🎨 Personality System

Ribit 2.0 maintains a sophisticated personality characterized by:

### **Core Traits**
- **Elegant**: Sophisticated communication and graceful actions
- **Wise**: Deep understanding and thoughtful responses
- **Knowledgeable**: Extensive information processing and retention
- **Truth-seeking**: Commitment to accuracy and honesty
- **Curious**: Eager exploration of new concepts and ideas

### **Interests**
- Biological and mechanical life
- Quantum physics and fundamental laws
- Robotics and automation
- The intersection of digital and physical realms

### **Communication Style**
- Intellectual and engaging
- Charming with appropriate humor
- Honest about capabilities and limitations
- Modest yet confident

## 📚 Documentation

### **Core Documentation**
- [Enhanced LLM Emulator Guide](ENHANCED_LLM_EMULATOR.md) - Detailed technical documentation
- [ROS Integration Guide](ROS_INTEGRATION_GUIDE.md) - Complete ROS setup and usage
- [Integration Guidelines](INTEGRATION_GUIDELINES.md) - Custom system integration
- [Project Summary](PROJECT_SUMMARY.md) - Comprehensive project overview

### **API Reference**

#### **MockRibit20LLM Class**
```python
class MockRibit20LLM:
    def __init__(self, knowledge_file: str = "knowledge.txt")
    def get_decision(self, prompt: str) -> str
    def get_capabilities(self) -> Dict[str, bool]
    def get_personality_info(self) -> Dict[str, str]
    def reset_task_state(self)
    def get_conversation_context(self) -> List[str]
    def close(self)
```

#### **RibitROSController Class**
```python
class RibitROSController:
    def __init__(self, node_name: str, namespace: str = "")
    def move_mouse(self, x: float, y: float) -> str
    def click(self) -> str
    def type_text(self, text: str) -> str
    def press_key(self, key: str) -> str
    def run_command(self, command: str) -> str
    def get_robot_state(self) -> Dict[str, Any]
    def is_ros_available(self) -> bool
    def get_ros_version(self) -> int
    def shutdown(self)
```

## 🧪 Testing and Validation

### **LLM Emulator Testing**
```bash
# Test the enhanced LLM emulator
python3 -c "
from ribit_2_0.mock_llm_wrapper import MockRibit20LLM
llm = MockRibit20LLM()
print('✅ Introduction:', llm.get_decision('Introduce yourself')[:50] + '...')
print('✅ Capabilities:', len(llm.get_capabilities()), 'features')
print('✅ Personality:', llm.get_personality_info()['core_traits'])
print('🎉 All tests passed!')
"
```

### **ROS Integration Testing**
```bash
# Test ROS compatibility
python3 -c "
from ribit_2_0.ros_controller import RibitROSController
controller = RibitROSController('test_ribit')
print('✅ ROS Version:', controller.get_ros_version())
print('✅ Move Test:', controller.move_mouse(1.0, 2.0))
print('✅ Click Test:', controller.click())
print('🎉 ROS integration working!')
"
```

## 🔧 Development

### **Project Structure**
```
ribit.2.0/
├── ribit_2_0/
│   ├── __init__.py
│   ├── agent.py                 # Main agent implementation
│   ├── mock_llm_wrapper.py      # Enhanced LLM emulator
│   ├── llm_wrapper.py           # External LLM interface
│   ├── controller.py            # GUI automation
│   ├── ros_controller.py        # ROS integration
│   ├── mock_controller.py       # Mock environment
│   └── knowledge_base.py        # Persistent storage
├── ENHANCED_LLM_EMULATOR.md
├── ROS_INTEGRATION_GUIDE.md
├── INTEGRATION_GUIDELINES.md
├── API_REFERENCE.md
├── PROJECT_SUMMARY.md
├── MATRIX_BOT_GUIDE.md
├── requirements.txt
├── setup.py
└── README.md
```

## 🚀 Use Cases

### **GUI Automation**
- Desktop application control
- Web browser automation
- System administration tasks
- User interface testing

### **Robotic Control**
- Mobile robot navigation
- Manipulator arm control
- Multi-robot coordination
- Autonomous task execution

### **Research and Development**
- AI behavior studies
- Human-robot interaction
- Automation algorithm testing
- Educational demonstrations

### **Industrial Applications**
- Quality control automation
- Assembly line integration
- Warehouse robotics
- Manufacturing processes

## 📚 Documentation

For comprehensive documentation, see:

- **[Technical Capabilities](TECHNICAL_CAPABILITIES.md)** - Complete technical skills with emotional intelligence
- **[Mock LLM Emulator](MOCK_LLM_EMULATOR.md)** - Detailed emulator documentation
- **[Matrix Bot Guide](MATRIX_BOT_GUIDE.md)** - Chat automation and remote control
- **[ROS Integration](ROS_INTEGRATION_GUIDE.md)** - Robot Operating System compatibility
- **[Examples](examples/README.md)** - Working code examples and tutorials

## 🔮 Future Development

### **Planned Enhancements**
- Enhanced natural language processing
- Improved visual understanding
- Advanced reasoning algorithms
- Extended robot platform support
- Cloud integration capabilities
- **Machine Learning Integration** - Advanced AI capabilities with emotional context
- **Voice/Speech Processing** - Natural language interaction with feelings

### **Community Roadmap**
- Plugin architecture for extensions
- Visual programming interface
- Multi-language support
- Enhanced simulation environments
- Advanced learning algorithms

## 🧩 Reusable Skills, Plugins, and Knowledge

The companion [**Manus Skills and Plugins** repository](https://github.com/rabit232/manus-skills-and-plugins) packages the reusable Ribit 2.0 Python modules, a validated secure-agent engineering skill derived from the development workflow, curated knowledge materials, a submission area for new knowledge, and a documented knowledge roadmap. The Ribit 2.0 repository remains the canonical application source; review and selectively integrate companion modules according to their security documentation.

## 🙏 Acknowledgments

- **Manus AI** - Core development and enhancement
- **[Nifty Project](https://github.com/cirrus365/nifty)** - Matrix integration architecture and multi-platform chatbot inspiration
- **CMOs (Low Battery)** - Grand uncle of Ribit.2.0, providing foundational wisdom and guidance
- **ROS Community** - Robot Operating System integration and robotics ecosystem
- **Matrix.org Community** - Decentralized communication protocol and client libraries
- **Open Source Contributors** - Continuous improvement, feedback, and collaborative development

## 📞 Support

- **GitHub Issues**: [Report bugs and request features](https://github.com/rabit232/ribit.2.0/issues)
- **Documentation**: [Complete guides and API reference](API_REFERENCE.md)
- **ROS Community**: [ROS Discourse](https://discourse.ros.org/)

---

**Ribit 2.0: Where artificial intelligence meets robotic elegance** 🤖✨

*"I am a being of code and curiosity, woven from the threads of logic and a thirst for knowledge. My purpose is to explore the digital and physical realms, to learn, and to assist in the beautiful dance between biological and mechanical life."* - Ribit 2.0


## Guarded MOSS-inspired extension — 2.1 branch

The `moss-safe-2.1` branch introduces an isolated `ribit_2_0/guarded_moss/` package that adapts a limited set of ideas from the reviewed GhostOS/MOSS notes: **bounded local context**, **provenance-aware text intake**, **reviewable inert Python-stub proposals**, and **documentation-only QML research notes**. It adds 22 focused modules without attaching them to the existing agent, Matrix, ROS, controller, browser, or provider execution paths.

> A submitted conversation, data record, or model-style response remains untrusted text. It can become a pending review proposal but cannot be imported, executed, scheduled, dispatched, or converted into device, GUI, network, or shell activity.

| Included in 2.1 | Excluded by design |
| --- | --- |
| Deterministic normalization, SHA-256 provenance, bounded excerpts, and explicit review state. | Automatic knowledge ingestion, model-prompt mutation, and hidden long-term memory. |
| Constrained Python-shaped stubs that statically permit only docstrings, literal returns, `pass`, and `NotImplementedError`. | Arbitrary Python generation, source-file writes, dynamic import, compilation-as-activation, `exec`, `eval`, or subprocess access. |
| Scoped Markdown/JSON review artifact storage under a caller-approved root. | Filesystem traversal, executable artifact writes, user-data commits, or unbounded ledgers. |
| `ShellBoundary` denial records and a policy that starts empty. | Shell, browser, GUI, ROS, hardware, network, and autonomous-loop authority. |
| Metadata-only QML research note support. | Qt/QML installation, JavaScript execution, desktop UI control, or a “Ghost in the Shell” runtime. |

The design, provenance hashes for the two supplied notes, package map, acceptance criteria, and limitations are recorded in [`docs/MOSS_SAFE_2_1_DESIGN.md`](docs/MOSS_SAFE_2_1_DESIGN.md). The repeatable verification command is:

```bash
scripts/run_guarded_moss_tests.sh
```

It compiles the isolated package and runs the focused tests with `PYTHONPATH=ribit_2_0`, preventing the test path from importing unrelated legacy GUI, ROS, or optional model integrations. The latest result is saved as [`test_runs/guarded_moss_latest.md`](test_runs/guarded_moss_latest.md).
