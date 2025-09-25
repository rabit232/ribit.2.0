# Integration Guidelines for Ribit 2.0

Ribit 2.0 is designed to be a flexible and extensible agent that can be integrated with a variety of systems, including robotic platforms. This guide provides instructions on how to integrate your own systems with Ribit 2.0.

## Integrating with the Controller

The `controller.py` module is the interface between the Ribit 2.0 agent and the system it is controlling. By default, it uses `pyautogui` and `pynput` to control the mouse and keyboard of a desktop environment. To integrate Ribit 2.0 with a different system, such as a robot, you will need to create a custom controller.

### Creating a Custom Controller

A custom controller must implement the same methods as the `VisionSystemController` class in `controller.py`. These methods are:

- `move_mouse(x, y)`: Move the system's manipulator to the specified coordinates.
- `click()`: Perform a click action.
- `type_text(text)`: Type the given text.
- `press_key(key)`: Press a special key (e.g., 'enter').
- `run_command(command)`: Execute a command on the system.

Here is an example of a custom controller for a hypothetical robot:

```python
class RobotController:
    def __init__(self, robot_ip):
        # Initialize connection to the robot
        self.robot = Robot(robot_ip)

    def move_mouse(self, x, y):
        # Convert screen coordinates to robot coordinates
        robot_x, robot_y = self.convert_coords(x, y)
        self.robot.move_to(robot_x, robot_y)

    def click(self):
        self.robot.gripper.close()
        self.robot.gripper.open()

    def type_text(self, text):
        # This might not be applicable to all robots
        print(f"Robot received text: {text}")

    def press_key(self, key):
        # This might not be applicable to all robots
        print(f"Robot received key press: {key}")

    def run_command(self, command):
        # Execute a command on the robot's OS
        self.robot.run_command(command)
```

### Using the Custom Controller

To use your custom controller, you will need to modify the `agent.py` file to instantiate your controller instead of the default `VisionSystemController`.

## Integrating with the LLM

The `llm_wrapper.py` module is the interface between the Ribit 2.0 agent and the Large Language Model (LLM). By default, it is designed to work with a local LLM executable. To use a different LLM, such as a cloud-based API, you will need to create a custom LLM wrapper.

### Creating a Custom LLM Wrapper

A custom LLM wrapper must implement the same `get_decision(prompt)` method as the `Ribit20LLM` class in `llm_wrapper.py`. This method takes a prompt string as input and returns a string containing the LLM's decision.

Here is an example of a custom LLM wrapper for a hypothetical cloud-based LLM API:

```python
import requests

class CloudLLMWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.example.com/llm"

    def get_decision(self, prompt):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"prompt": prompt}
        response = requests.post(self.api_url, headers=headers, json=data)
        return response.json()["decision"]
```

### Using the Custom LLM Wrapper

To use your custom LLM wrapper, you will need to modify the `agent.py` file to instantiate your wrapper instead of the default `Ribit20LLM`.

