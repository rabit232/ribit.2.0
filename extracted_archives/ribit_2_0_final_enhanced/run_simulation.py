import asyncio
from ribit_2_0.agent import Ribit20Agent
from ribit_2_0.mock_llm_wrapper import MockRibit20LLM
from ribit_2_0.mock_controller import MockVisionSystemController

async def main():
    """Runs a simulation of the Ribit 2.0 agent with a mock LLM and controller."""
    print("--- Starting Ribit 2.0 Simulation ---")

    # 1. Initialize the Mock LLM and Controller
    llm = MockRibit20LLM()
    controller = MockVisionSystemController()

    # 2. Define the goal for the agent
    goal = "Introduce yourself and then learn that the sky is blue."

    # 3. Create and run the agent
    agent = Ribit20Agent(llm, controller, goal)
    await agent.run()

    print("--- Ribit 2.0 Simulation Finished ---")

if __name__ == "__main__":
    asyncio.run(main()
