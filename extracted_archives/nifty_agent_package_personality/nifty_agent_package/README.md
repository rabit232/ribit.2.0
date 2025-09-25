# Nifty Agent

A vision-based GUI automation agent powered by a low-resource LLM.

This package provides the tools to run a sophisticated AI agent capable of seeing the screen, understanding user goals, and controlling the mouse and keyboard to accomplish tasks in a graphical user interface.

## Features

- **Vision-Based Control**: Uses screen captures and ASCII-art conversion to allow a local LLM to perceive the GUI.
- **Mouse & Keyboard Automation**: Full control over the mouse and keyboard via `pynput` and `pyautogui`.
- **LLM Integration**: Includes a wrapper for communicating with a local LLM executable (like the one we developed).
- **Safe & Robust**: Implements failsafes, coordinate clamping, and safe command parsing.

## Installation

To install this package, you will first need to build it from the source directory:

```bash
python3 -m pip install wheel
python3 setup.py sdist bdist_wheel
```

Then, you can install the generated wheel file:

```bash
pip install dist/nifty_agent-0.1.0-py3-none-any.whl
```

## Usage

After installation, you can use the agent from the command line:

```bash
nifty-agent --goal "Your goal here" --nifty-path /path/to/your/llm/executable
```


