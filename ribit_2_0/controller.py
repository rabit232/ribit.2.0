import logging
import os

logger = logging.getLogger(__name__)

# Conditional import for pyautogui and pynput
# These will only be imported if a DISPLAY is available
# Otherwise, HAS_GUI_LIBS_CONTROLLER will be False
try:
    import pyautogui
    from pynput.mouse import Button, Controller as MouseController
    from pynput.keyboard import Key, Controller as KeyboardController
    # Check if DISPLAY is actually set, as pyautogui can be installed but not functional
    if 'DISPLAY' in os.environ:
        HAS_GUI_LIBS_CONTROLLER = True
        logger.info("DISPLAY environment variable is set. GUI libraries are active.")
    else:
        # Check for Xvfb/Virtual Display setup
        try:
            subprocess.run(['which', 'Xvfb'], check=True, capture_output=True)
            logger.warning("DISPLAY not set, but Xvfb is installed. Please ensure Xvfb is running and DISPLAY is exported for GUI control.")
            raise KeyError("DISPLAY environment variable not set.")
        except subprocess.CalledProcessError:
            logger.warning("DISPLAY not set and Xvfb not found. Running in full headless/mock mode.")
            raise KeyError("DISPLAY environment variable not set.")
except (ImportError, KeyError) as e:
    logger.warning(f"Controller: Could not import GUI libraries (pyautogui/pynput) or DISPLAY not set: {e}. Using mock controller functionality.")
    pyautogui = None
    MouseController = None
    KeyboardController = None
    HAS_GUI_LIBS_CONTROLLER = False

import subprocess

class VisionSystemController:
    """v3: Hardened, clamped, and smooth controls. Now with headless support."""
    def __init__(self):
        if not HAS_GUI_LIBS_CONTROLLER:
            logger.warning("VisionSystemController initialized in MOCK mode due to missing GUI libraries.")
            self.mouse = None # No real mouse controller
            self.keyboard = None # No real keyboard controller
            self.screen_width = 1920 # Default mock values
            self.screen_height = 1080
        else:
            self.mouse = MouseController()
            self.keyboard = KeyboardController()
            self.screen_width, self.screen_height = pyautogui.size()
            logger.info("VisionSystemController v3 initialized.")

    def move_mouse(self, x, y):
        if not HAS_GUI_LIBS_CONTROLLER:
            logger.info(f"SIMULATED ACTION: Smoothly moving mouse to ({x}, {y})")
            return f"Simulated mouse moved to ({x}, {y})."

        base_x = int(x * (self.screen_width / 128.0))
        base_y = int(y * (self.screen_height / (128.0 * self.screen_height / self.screen_width)))
        target_x = max(0, min(self.screen_width - 1, base_x))
        target_y = max(0, min(self.screen_height - 1, base_y))
        
        logger.info(f"ACTION: Smoothly moving mouse to clamped ({target_x}, {target_y})")
        pyautogui.moveTo(target_x, target_y, duration=0.25)
        return f"Mouse moved to ({target_x}, {target_y})."

    def click(self):
        if not HAS_GUI_LIBS_CONTROLLER:
            logger.info(f"SIMULATED ACTION: Clicking left button.")
            return "Simulated mouse clicked."

        logger.info(f"ACTION: Clicking left button.")
        self.mouse.click(Button.left, 1)
        return "Mouse clicked."

    def type_text(self, text):
        if not HAS_GUI_LIBS_CONTROLLER:
            logger.info(f"SIMULATED ACTION: Typing: \'{text}\'")
            return f"Simulated typed: \'{text}\'"

        logger.info(f"ACTION: Typing: \'{text}\'")
        self.keyboard.type(text)
        return f"Typed: \'{text}\'"

    def press_key(self, key_name):
        if not HAS_GUI_LIBS_CONTROLLER:
            logger.info(f"SIMULATED ACTION: Pressing key: {key_name}")
            return f"Simulated pressed key: {key_name}"

        logger.info(f"ACTION: Pressing key: {key_name}")
        key_to_press = getattr(Key, key_name, key_name)
        self.keyboard.press(key_to_press)
        self.keyboard.release(key_to_press)
        return f"Pressed key: {key_name}"

    def run_command(self, command, *args, **kwargs):
        # This can always run, even in headless mode, as it uses subprocess
        # The command might be passed as a single string or a tuple if ast.literal_eval parses it that way
        # Ensure it's treated as a single command string
        if isinstance(command, tuple):
            command_str = ".".join(command) # Reconstruct if it was split by ast.literal_eval
        else:
            command_str = command

        logger.info(f"ACTION: Executing command: \'{command_str}\' with args={args}, kwargs={kwargs}")
        try:
            # In a real headless environment, this would still run the command
            # For a full simulation, we might want to mock this too, but for now, let it try
            result = subprocess.run(command_str, shell=True, capture_output=True, text=True, check=False)
            return f"Command executed. Output: {(result.stdout or result.stderr)[:200]}"
        except Exception as e:
            return f"Failed to execute command: {e}"
            
    def uncertain(self):
        logger.info("ACTION: LLM is uncertain. Pausing.")
        return "LLM indicated uncertainty."


