# Ribit 2.0

A vision-based GUI automation agent powered by a low-resource LLM, now known as Ribit 2.0.

This package provides the tools to run a sophisticated AI agent capable of seeing the screen, understanding user goals, and controlling the mouse and keyboard to accomplish tasks in a graphical user interface.

## Features

- **Vision-Based Control**: Uses screen captures and ASCII-art conversion to allow a local LLM to perceive the GUI.
- **Mouse & Keyboard Automation**: Full control over the mouse and keyboard via `pynput` and `pyautogui`.
- **LLM Integration**: Includes a wrapper for communicating with a local LLM executable.
- **Safe & Robust**: Implements failsafes, coordinate clamping, and safe command parsing.
- **Knowledge Base**: Persistent storage and retrieval of information for learning and memory.
- **Personality**: Configurable personality traits for more engaging interactions.

## Installation

To install this package, you will first need to build it from the source directory:

```bash
python3 -m pip install wheel
python3 setup.py sdist bdist_wheel
```

Then, you can install the generated wheel file:

```bash
pip install dist/ribit_2_0-0.1.0-py3-none-any.whl
```

## Usage

After installation, you can use the agent from the command line:

```bash
ribit-2-0 --goal "Your goal here" --nifty-path /path/to/your/llm/executable
```

Or, to run with the mock LLM for demonstration (e.g., to see the personality):

```bash
ribit-2-0 --mock-llm --goal "Introduce yourself and share your current interests."
```

Replace `--nifty-path` with the actual path to your low-resource LLM executable. The agent will create a `knowledge.txt` file in the directory where it is run to store its persistent knowledge.


