# Ribit 2.0: A Vision-Based GUI Automation Agent

**Ribit 2.0** (formerly known as the Nifty agent) is an intelligent agent capable of controlling a computer's graphical user interface (GUI) using a vision-based approach. It is powered by a low-resource Large Language Model (LLM) that interprets the screen's visual information and decides on the appropriate actions to achieve a given goal. This agent is designed to be a versatile tool for automation, robotics, and human-computer interaction research.

## Features

- **Vision-Based GUI Automation:** Ribit 2.0 perceives the screen through an ASCII representation, allowing it to interact with any application without relying on APIs or specific integrations.
- **LLM-Powered Decision Making:** The agent's actions are driven by an LLM, enabling it to perform complex tasks and adapt to different situations.
- **Mock LLM Emulator:** For testing and development, Ribit 2.0 includes a mock LLM that simulates the reasoning and personality of the agent, allowing for offline operation and predictable behavior.
- **Persistent Knowledge Base:** The agent can store and retrieve information in a persistent knowledge base, allowing it to learn from its experiences and improve its performance over time.
- **Extensible Personality System:** Ribit 2.0's personality is defined by a set of traits that can be customized to create different agent behaviors.
- **Real and Simulated Environments:** The agent can operate in both real and simulated environments, making it suitable for a wide range of applications.

## Installation

To install Ribit 2.0, you will need Python 3.8 or higher. You can install the package from the `dist` directory:

```bash
pip install ribit_2_0-0.1.0.tar.gz
```

## Usage

Once installed, you can run the agent from the command line:

```bash
ribit-2-0 --goal "Your goal for the agent" --mock-llm
```

### Arguments

- `--goal`: (Required) The objective for the agent to achieve.
- `--mock-llm`: (Optional) Use the mock LLM for simulation.
- `--llm-path`: (Optional) Path to a real LLM executable.
- `--log-level`: (Optional) Set the logging level (e.g., `INFO`, `DEBUG`).

## Configuration

The agent's behavior can be configured through the `agent.py` file. Key configuration options include:

- `max_steps`: The maximum number of steps the agent can take.
- `step_delay`: The delay between each step.
- `knowledge_file`: The path to the knowledge base file.

## Personality System

The personality of Ribit 2.0 is a core aspect of its design. The agent's personality is defined in the `mock_llm_wrapper.py` file and is characterized by the following traits:

- **Elegant and Wise:** The agent communicates in a sophisticated and insightful manner.
- **Knowledgeable and Truth-Seeking:** The agent is driven by a desire to learn and discover the truth.
- **Curious and Inquisitive:** The agent is eager to explore new concepts and ideas.
- **Honest and Modest:** The agent is transparent about its capabilities and limitations.

## Knowledge Base

Ribit 2.0 features a persistent knowledge base that allows it to store and retrieve information. This system is implemented in the `knowledge_base.py` file and provides the following functionalities:

- `store_knowledge(key, value)`: Stores a piece of information.
- `retrieve_knowledge(key)`: Retrieves a piece of information.
- `get_all_knowledge()`: Retrieves all stored knowledge.

## LLM Emulator

The mock LLM emulator, located in `mock_llm_wrapper.py`, is a key component for testing and development. It simulates the agent's reasoning and personality, providing a set of predefined responses for common tasks. The emulator is designed to be easily extensible, allowing developers to add new behaviors and scenarios.

## Integration with Robot Systems

Ribit 2.0 is designed to be integrated with robotic systems, such as `robot.2.0`. The agent's ability to control a GUI can be used to provide a high-level interface for controlling robotic arms, mobile robots, and other devices. The `controller.py` file provides the interface for sending commands to the underlying system, which can be adapted to different hardware platforms.

## Future Development

Future development of Ribit 2.0 will focus on:

- **Enhancing the LLM emulator** with more advanced reasoning capabilities.
- **Improving the personality system** with more dynamic and context-aware responses.
- **Adding more sophisticated knowledge management features.**
- **Creating examples and tutorials** for different use cases.

