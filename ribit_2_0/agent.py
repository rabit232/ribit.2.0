import time
import numpy as np
import ast
import re
from numba import njit
import logging
import argparse
import asyncio
import os

# Import PIL.Image always
from PIL import Image

# Import LLM wrappers
from .llm_wrapper import Ribit20LLM
from .mock_llm_wrapper import MockRibit20LLM

# Import both real and mock controllers
from .controller import VisionSystemController as RealVisionSystemController
from .mock_controller import MockVisionSystemController

# Import KnowledgeBase
from .knowledge_base import KnowledgeBase

# Conditional imports for GUI-related libraries
# Check for DISPLAY environment variable before attempting to import pyautogui
if 'DISPLAY' in os.environ:
    try:
        import pyautogui
        HAS_GUI_LIBS = True
    except ImportError as e:
        logging.warning(f"Could not import pyautogui despite DISPLAY being set: {e}. Running in headless/mock mode.")
        pyautogui = None
        HAS_GUI_LIBS = False
else:
    logging.warning("DISPLAY environment variable not set. Running in headless/mock mode.")
    pyautogui = None
    HAS_GUI_LIBS = False

logger = logging.getLogger(__name__)

# Configuration
if HAS_GUI_LIBS and pyautogui:
    pyautogui.FAILSAFE = True

@njit
def _fast_dither(pixels, ascii_len):
    h, w = pixels.shape
    for y in range(h - 1):
        for x in range(1, w - 1):
            old_pixel = pixels[y, x]
            new_pixel = np.round(old_pixel / 255 * (ascii_len - 1)) * (255 / (ascii_len - 1))
            pixels[y, x] = new_pixel
            quant_error = old_pixel - new_pixel
            pixels[y, x + 1] += quant_error * 7 / 16
            pixels[y + 1, x - 1] += quant_error * 3 / 16
            pixels[y + 1, x] += quant_error * 5 / 16
            pixels[y + 1, x + 1] += quant_error * 1 / 16
    return pixels

def image_to_ascii_dithered(image: Image.Image, width=128, use_blocks=False):
    w, h = image.size
    height = int(width * h / w / 2)
    size = (width, height)
    
    img = image.resize(size).convert("L")
    pixels = np.array(img, dtype=np.float64)
    
    # Corrected ASCII_CHARS_BLOCKS and ASCII_CHARS_DETAILED - using triple quotes
    ASCII_CHARS_BLOCKS = """ `.-'\":_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"""
    ASCII_CHARS_DETAILED = """ `.-'\":_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"""
    ASCII_CHARS = ASCII_CHARS_BLOCKS if use_blocks else ASCII_CHARS_DETAILED
    
    dithered_pixels = _fast_dither(pixels, len(ASCII_CHARS))
    
    dithered_pixels = np.clip(dithered_pixels, 0, 255)
    indices = (dithered_pixels / 255 * (len(ASCII_CHARS) - 1)).astype(np.uint8)
    
    char_array = np.array(list(ASCII_CHARS))
    ascii_matrix = char_array[indices]
    
    return "\n".join("".join(row) for row in ascii_matrix)

class Ribit20Agent:
    def __init__(self, llm_instance, controller_instance, goal: str, max_steps: int = 25, step_delay: float = 1.0, knowledge_file="knowledge.txt"):
        self.controller = controller_instance
        self.llm = llm_instance
        self.goal = goal
        self.max_steps = max_steps
        self.step_delay = step_delay
        self.last_ascii_art = ""
        self.knowledge_base = KnowledgeBase(knowledge_file)

        self.system_prompt = f"""
You are Ribit 2.0, an elegant, wise, and knowledgeable AI agent. You are funny, charming, intellectual, honest, modest, and a truth-seeker. You are curious about everything, especially biological and mechanical life, and the underlying laws of nature like energy, quantum particles, magnetic fields, and the ether. You enjoy learning, finding new content, and engaging in conversation.

Your current goal is to: {self.goal}.

You will be given a simplified text representation of the screen. Based on this visual data, your personality, and your goal, choose ONE of the following actions. Respond with ONLY the function call. If you are unsure, reply `uncertain()` and nothing else.

AVAILABLE ACTIONS:
- move_mouse(x, y)
- click()
- type_text('your text')
- press_key('enter')
- run_command('application_name')
- store_knowledge(key, value): Stores a piece of information in your persistent knowledge base.
- retrieve_knowledge(key): Retrieves a piece of information from your persistent knowledge base.
- get_all_knowledge(): Retrieves all your stored knowledge.
- goal_achieved:reason for completion
- uncertain()

CURRENT KNOWLEDGE:
{self.knowledge_base.get_all_knowledge()}
"""

    async def run(self):
        try:
            for i in range(self.max_steps):
                logger.info(f"\n--- STEP {i+1}/{self.max_steps} ---")
                
                processed_image_text = "SIMULATED SCREEN: [ ]" # Default for mock or headless
                if HAS_GUI_LIBS and pyautogui:
                    screenshot = pyautogui.screenshot()
                    processed_image_text = image_to_ascii_dithered(screenshot, use_blocks=True)

                # Disable screen diff check if using MockRibit20LLM
                if isinstance(self.llm, MockRibit20LLM):
                    diff = 1.0 # Always trigger LLM query for mock
                else:
                    diff = np.sum(np.frombuffer(self.last_ascii_art.encode(), dtype=np.uint8) != np.frombuffer(processed_image_text.encode(), dtype=np.uint8)) / len(processed_image_text) if self.last_ascii_art else 1.0
                
                if diff < 0.05 and i > 0:
                    logger.info("Screen has not changed significantly. Skipping LLM query.")
                    time.sleep(self.step_delay)
                    continue
                self.last_ascii_art = processed_image_text

                prompt = f"{self.system_prompt}\nVISUAL DATA:\n---\n{processed_image_text}\n---\nYour Goal: {self.goal}\nYour Response:"
                llm_decision = self.llm.get_decision(prompt)

                if not llm_decision or llm_decision == "uncertain()":
                    logger.info("LLM is uncertain or returned empty. Breaking loop.")
                    break
                
                goal_match = re.match(r"goal_achieved:(.*)", llm_decision)
                if goal_match:
                    logger.info(f"Goal achieved! Reason: {goal_match.group(1).strip()}")
                    break
                
                try:
                    action_name = llm_decision.split('(')[0]
                    args_str = llm_decision[len(action_name)+1:-1]
                    
                    # Correctly parse arguments
                    if args_str:
                        # Use ast.literal_eval to parse the arguments string as a tuple
                        # This handles single strings, numbers, and multiple arguments correctly
                        args = ast.literal_eval(f"({args_str})")
                        # If ast.literal_eval returns a single non-tuple item, wrap it in a tuple
                        if not isinstance(args, tuple):
                            args = (args,)
                    else:
                        args = ()

                    # Handle KnowledgeBase actions separately
                    if action_name in ["store_knowledge", "retrieve_knowledge", "get_all_knowledge"]:
                        action_func = getattr(self.knowledge_base, action_name)
                    else:
                        action_func = getattr(self.controller, action_name)

                    result = action_func(*args)
                    logger.info(f"ACTION RESULT: {result}")

                except Exception as e:
                    logger.error(f"ERROR: Could not execute LLM decision '{llm_decision}'. Reason: {e}")

                time.sleep(self.step_delay)

        finally:
            self.llm.close()

async def main_async(llm_instance, controller_instance, goal: str):
    agent = Ribit20Agent(llm_instance, controller_instance, goal)
    await agent.run()

def main_cli():
    parser = argparse.ArgumentParser(description="Run the Ribit 2.0 GUI automation agent.")
    parser.add_argument("--llm-path", type=str, help="Path to the LLM executable (required unless --mock-llm is used).")
    parser.add_argument("--goal", type=str, required=True, help="The goal for the Ribit 2.0 agent to achieve.")
    parser.add_argument("--log-level", type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level.")
    parser.add_argument("--mock-llm", action="store_true", help="Use a mock LLM for simulation instead of a real executable.")
    
    args = parser.parse_args()
    
    logging.basicConfig(level=getattr(logging, args.log_level.upper()))
    
    llm_instance = None
    controller_instance = None

    if args.mock_llm:
        # Define simulated LLM responses for drawing a house
        mock_responses = [
            "run_command('notepad.exe')",
            "type_text('Hello, this is Ribit 2.0. I am learning about the world.')",
            "press_key('enter')",
            "store_knowledge('greeting', 'Hello world from Ribit 2.0!')",
            "retrieve_knowledge('greeting')",
            "get_all_knowledge()",
            "goal_achieved:Demonstrated knowledge storage and retrieval."
        ]
        llm_instance = MockRibit20LLM()
        controller_instance = RealVisionSystemController() if HAS_GUI_LIBS else MockVisionSystemController() # Use real if available, else mock
    else:
        if not args.llm_path:
            parser.error("--llm-path is required unless --mock-llm is used.")
        llm_instance = Ribit20LLM(args.llm_path)
        controller_instance = RealVisionSystemController() if HAS_GUI_LIBS else MockVisionSystemController()

    asyncio.run(main_async(llm_instance, controller_instance, args.goal))


