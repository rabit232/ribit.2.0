import subprocess
import time
import logging

logger = logging.getLogger(__name__)

class Ribit20LLM:
    """A wrapper to communicate with the Ribit 2.0 LLM executable."""
    def __init__(self, llm_executable_path):
        self.llm_executable_path = llm_executable_path
        self.process = None
        self._start_process()

    def _start_process(self):
        try:
            self.process = subprocess.Popen(
                [self.llm_executable_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            time.sleep(10) # Give the model time to load
            logger.info("Ribit 2.0 LLM process started.")
        except FileNotFoundError:
            logger.error(f"Ribit 2.0 executable not found at {self.llm_executable_path}. Please ensure it\"s compiled and the path is correct.")
            raise
        except Exception as e:
            logger.error(f"Failed to start Ribit 2.0 LLM process: {e}")
            raise

    def get_decision(self, prompt):
        """Sends a prompt to the LLM and gets a single-line command back."""
        if not self.process or self.process.poll() is not None:
            logger.warning("Ribit 2.0 LLM process is not running. Attempting to restart...")
            self._start_process()

        logger.debug(f"--- Sending prompt to LLM ---\n{prompt[:300]}...")
        
        self.process.stdin.write(prompt + '\n') # Corrected line
        self.process.stdin.flush()
        
        response = self.process.stdout.readline().strip()
        
        logger.debug(f"--- LLM Response ---\n{response}\n")
        return response

    def close(self):
        if self.process:
            self.process.terminate()
            logger.info("Ribit 2.0 LLM process terminated.")
            self.process = None

    def __del__(self):
        self.close() # Ensure process is terminated on object deletion




