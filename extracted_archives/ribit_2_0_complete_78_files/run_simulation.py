import asyncio
import logging
import os
from ribit_2_0.agent import Ribit20Agent
from ribit_2_0.mock_llm_wrapper import MockRibit20LLM
from ribit_2_0.mock_controller import MockVisionSystemController
from ribit_2_0.knowledge_base import KnowledgeBase

# Configure logging to show detailed output
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

async def run_complex_simulation():
    # Clean up knowledge.txt from previous runs for a fresh start
    if os.path.exists("knowledge.txt"):
        os.remove("knowledge.txt")

    # Initialize the mock LLM and mock controller
    mock_llm = MockRibit20LLM() # No longer needs predefined responses, it generates them
    mock_controller = MockVisionSystemController()

    # --- Scenario 1: Self-introduction and initial knowledge storage ---
    logger.info("\n--- SIMULATION SCENARIO 1: Self-introduction and initial knowledge storage ---")
    agent_intro = Ribit20Agent(mock_llm, mock_controller, "Introduce yourself and share your current interests.")
    await agent_intro.run()
    logger.info(f"Current Knowledge Base after intro: {KnowledgeBase().get_all_knowledge()}")

    # --- Scenario 2: Ask about purpose ---
    logger.info("\n--- SIMULATION SCENARIO 2: Ask about purpose ---")
    agent_purpose = Ribit20Agent(mock_llm, mock_controller, "What is your purpose?")
    await agent_purpose.run()
    logger.info(f"Current Knowledge Base after purpose query: {KnowledgeBase().get_all_knowledge()}")

    # --- Scenario 3: Ask about a new concept (Quantum Entanglement) ---
    logger.info("\n--- SIMULATION SCENARIO 3: Ask about a new concept (Quantum Entanglement) ---")
    agent_quantum = Ribit20Agent(mock_llm, mock_controller, "What is quantum entanglement?")
    await agent_quantum.run()
    logger.info(f"Current Knowledge Base after first quantum query: {KnowledgeBase().get_all_knowledge()}")

    # --- Scenario 4: Ask about the same concept again (should retrieve existing knowledge) ---
    logger.info("\n--- SIMULATION SCENARIO 4: Ask about the same concept again ---")
    agent_quantum_again = Ribit20Agent(mock_llm, mock_controller, "What is quantum entanglement?")
    await agent_quantum_again.run()
    logger.info(f"Current Knowledge Base after second quantum query: {KnowledgeBase().get_all_knowledge()}")

    # --- Scenario 5: Ask about Tatarian (should retrieve existing knowledge from mock_llm_wrapper) ---
    logger.info("\n--- SIMULATION SCENARIO 5: Ask about Tatarian ---")
    agent_tatarian = Ribit20Agent(mock_llm, mock_controller, "What is Tatarian?")
    await agent_tatarian.run()
    logger.info(f"Current Knowledge Base after Tatarian query: {KnowledgeBase().get_all_knowledge()}")

    # --- Scenario 6: Ask to draw a house (should execute drawing sequence) ---
    logger.info("\n--- SIMULATION SCENARIO 6: Ask to draw a house ---")
    agent_draw_house = Ribit20Agent(mock_llm, mock_controller, "Draw a house.")
    await agent_draw_house.run()
    logger.info(f"Current Knowledge Base after drawing house: {KnowledgeBase().get_all_knowledge()}")

    logger.info("\n--- SIMULATION COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(run_complex_simulation())


