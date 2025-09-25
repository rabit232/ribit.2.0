# Ribit 2.0 Examples

This directory contains comprehensive examples demonstrating the capabilities of the MockRibit20LLM emulator and its integration with various systems.

## Available Examples

### 1. Basic Usage (`basic_usage.py`)

Demonstrates fundamental MockRibit20LLM functionality:

- **Initialization and setup**
- **Basic decision making**
- **Capabilities assessment**
- **Personality interaction**
- **Knowledge learning and retrieval**
- **Conversation context management**
- **Error handling**

**Run the example:**
```bash
cd examples
python3 basic_usage.py
```

**Expected output:**
- Introduction and personality demonstration
- Capabilities listing (6 core features)
- Basic command execution examples
- Knowledge learning and retrieval test
- Conversation context summary

### 2. Multi-Step Tasks (`multi_step_tasks.py`)

Showcases advanced multi-step task execution capabilities:

- **Drawing task with multiple steps**
- **Robot control task coordination**
- **Progressive learning sequences**
- **Creative task execution**
- **Complex problem solving**

**Run the example:**
```bash
cd examples
python3 multi_step_tasks.py
```

**Expected output:**
- Step-by-step task execution
- State management demonstration
- Context preservation across steps
- Creative and analytical task handling

### 3. ROS Integration (`ros_integration.py`)

Demonstrates integration with Robot Operating System:

- **Mobile robot control**
- **Manipulator arm control**
- **Sensor data integration**
- **Multi-robot coordination**
- **Emergency handling**
- **Learning from ROS interactions**

**Run the example:**
```bash
cd examples
python3 ros_integration.py
```

**Expected output:**
- ROS controller initialization
- Robot command execution
- State monitoring and feedback
- Multi-robot coordination
- Emergency response procedures

## Example Features Demonstrated

### Core AI Capabilities

| Feature | Basic Usage | Multi-Step | ROS Integration |
|---------|-------------|------------|-----------------|
| **Decision Making** | ✅ | ✅ | ✅ |
| **Knowledge Learning** | ✅ | ✅ | ✅ |
| **Personality Expression** | ✅ | ✅ | ✅ |
| **Context Awareness** | ✅ | ✅ | ✅ |
| **Error Handling** | ✅ | ✅ | ✅ |
| **State Management** | ❌ | ✅ | ✅ |
| **Multi-Step Reasoning** | ❌ | ✅ | ✅ |
| **Robot Control** | ❌ | ✅ | ✅ |

### Integration Capabilities

| Integration | Demonstrated | Example File |
|-------------|--------------|--------------|
| **Standalone Operation** | ✅ | `basic_usage.py` |
| **Complex Task Execution** | ✅ | `multi_step_tasks.py` |
| **ROS 1 Compatibility** | ✅ | `ros_integration.py` |
| **ROS 2 Compatibility** | ✅ | `ros_integration.py` |
| **Multi-Robot Systems** | ✅ | `ros_integration.py` |
| **Emergency Handling** | ✅ | `ros_integration.py` |

## Running the Examples

### Prerequisites

Ensure you have Ribit 2.0 installed:

```bash
# From the main ribit.2.0 directory
pip install -e .
```

### Basic Execution

All examples can be run directly:

```bash
# Navigate to examples directory
cd ribit.2.0/examples

# Run any example
python3 basic_usage.py
python3 multi_step_tasks.py
python3 ros_integration.py
```

### With ROS Support

For ROS integration examples, optionally install ROS:

```bash
# ROS 2 (recommended)
pip install rclpy

# ROS 1 (legacy)
sudo apt install ros-noetic-rospy
```

**Note:** Examples work in mock mode without ROS installation.

## Example Output Samples

### Basic Usage Output
```
=== MockRibit20LLM - Basic Usage Example ===

🤖 Initializing MockRibit20LLM...
✅ Emulator initialized successfully!

🎭 Introduction: run_command('notepad.exe')
type_text('Greetings! I am Ribit 2.0, an elegant AI agent born from the c...

🔧 Available Capabilities:
   ✅ Vision Processing
   ✅ Multi Step Reasoning
   ✅ Knowledge Management
   ✅ Robot Control
   ✅ Error Recovery
   ✅ Adaptive Learning
```

### Multi-Step Tasks Output
```
🎨 Multi-Step Drawing Task
Step 1: run_command('mspaint.exe')
Step 2: type_text('Creating a beautiful dwelling with careful attention...')
Step 3: move_mouse(400, 300)
Step 4: click()
Step 5: goal_achieved('House drawing completed with artistic flair!')
✅ Drawing task completed!
```

### ROS Integration Output
```
📡 Initializing ROS Controller...
✅ ROS Controller initialized! (Version: 0)
ℹ️  Running in mock ROS mode (no ROS installation detected)

🚗 Mobile Robot Control Demonstration
🧠 AI Decision: move_mouse(250, 150)
🤖 ROS Execution: Mock: Moved to (5.00, 3.00)
📍 Robot Position: (5.0, 3.0)
```

## Customizing Examples

### Adding New Examples

Create new example files following this template:

```python
#!/usr/bin/env python3
"""
Your Example Title

Description of what this example demonstrates.

Author: Your Name
Date: Current Date
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ribit_2_0.mock_llm_wrapper import MockRibit20LLM

def main():
    """Your example main function."""
    llm = MockRibit20LLM("your_knowledge.txt")
    
    # Your example code here
    
    llm.close()

if __name__ == "__main__":
    main()
```

### Modifying Existing Examples

Examples are designed to be educational and modifiable:

- **Change prompts** to test different scenarios
- **Add new test cases** to explore specific features
- **Modify timing** between steps for different pacing
- **Extend functionality** with additional capabilities

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure Ribit 2.0 is installed
pip install -e .

# Check installation
python3 -c "import ribit_2_0; print('Import successful')"
```

**Permission Errors:**
```bash
# Make examples executable
chmod +x examples/*.py
```

**ROS Not Found:**
```
# Examples work without ROS (mock mode)
# Install ROS for full functionality:
pip install rclpy  # ROS 2
```

### Debug Mode

Enable debug logging in any example:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your example code here
```

## Contributing Examples

We welcome contributions of new examples! Please:

1. Follow the existing code style
2. Include comprehensive comments
3. Add error handling
4. Test thoroughly
5. Update this README

### Example Ideas

- **Computer vision integration**
- **Natural language processing**
- **Custom robot platform integration**
- **Industrial automation scenarios**
- **Educational demonstrations**
- **Performance benchmarking**

## Support

For questions about examples:

- **GitHub Issues**: [Report problems or request new examples](https://github.com/rabit232/ribit.2.0/issues)
- **Documentation**: [Main documentation](../README.md)
- **API Reference**: [MockRibit20LLM documentation](../MOCK_LLM_EMULATOR.md)

---

**Happy experimenting with Ribit 2.0!** 🤖✨
