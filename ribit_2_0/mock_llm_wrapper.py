import logging
import asyncio

logger = logging.getLogger(__name__)

class MockRibit20LLM:
    """A mock wrapper for the Ribit 2.0 LLM, returning predefined responses."""
    def __init__(self, responses: list):
        self.responses = responses
        self.call_count = 0
        logger.info("Mock Ribit 2.0 LLM initialized with predefined responses.")

    def get_decision(self, prompt: str) -> str:
        logger.debug(f"--- Mock LLM received prompt ---\n{prompt[:300]}...")
        if self.call_count < len(self.responses):
            decision = self.responses[self.call_count]
            self.call_count += 1
            logger.info(f"--- Mock LLM Response ({self.call_count}/{len(self.responses)}) ---\n{decision}\n")
            return decision
        else:
            logger.warning("Mock LLM has no more predefined responses. Returning \'uncertain()\'.")
            return "uncertain()"

    def close(self):
        logger.info("Mock Ribit 2.0 LLM closed.")

    async def _async_init(self):
        # Simulate async initialization if needed by the agent\'s run method
        pass


