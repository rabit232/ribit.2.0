import logging

logger = logging.getLogger(__name__)

class MockVisionSystemController:
    def __init__(self):
        logger.info("Mock VisionSystemController initialized.")

    def move_mouse(self, x, y):
        logger.info(f"SIMULATED ACTION: Smoothly moving mouse to ({x}, {y})")
        return f"Simulated mouse moved to ({x}, {y})."

    def click(self):
        logger.info(f"SIMULATED ACTION: Clicking left button.")
        return "Simulated mouse clicked."

    def type_text(self, text: str):
        logger.info(f"SIMULATED ACTION: Typing: \'{text}\'")
        return f"Simulated typed: \'{text}\'"

    def press_key(self, key_name: str):
        logger.info(f"SIMULATED ACTION: Pressing key: {key_name}")
        return f"Simulated pressed key: {key_name}"

    def run_command(self, command: str, *args, **kwargs):
        logger.info(f"SIMULATED ACTION: Executing command: \'{command}\' with args={args}, kwargs={kwargs}")
        return f"Simulated command executed: {command}"
            
    def uncertain(self):
        logger.info("SIMULATED ACTION: LLM is uncertain. Pausing.")
        return "Simulated LLM indicated uncertainty."


