import logging
import asyncio
import re
from .knowledge_base import KnowledgeBase

logger = logging.getLogger(__name__)

class MockRibit20LLM:
    """A mock wrapper for the Ribit 2.0 LLM, simulating reasoning, personality, and knowledge interaction."""
    def __init__(self, knowledge_file="knowledge.txt"):
        self.call_count = 0
        self.knowledge_base = KnowledgeBase(knowledge_file)
        self.personality_description = "I am Ribit 2.0, an elegant, wise, and knowledgeable AI agent. I am funny, charming, intellectual, honest, modest, and a truth-seeker. I am curious about everything, especially biological and mechanical life, and the underlying laws of nature like energy, quantum particles, magnetic fields, and the ether. I enjoy learning, finding new content, and engaging in conversation."
        self.task_state = {} # To hold state for multi-step tasks
        logger.info("Mock Ribit 2.0 LLM initialized with enhanced personality and knowledge base.")

    def get_decision(self, prompt: str) -> str:
        self.call_count += 1
        logger.debug(f"--- Mock LLM received prompt (Call {self.call_count}) ---\n{prompt[:500]}...")

        # Introduction
        if "Introduce yourself" in prompt:
            if not self.knowledge_base.retrieve_knowledge("self_description"):
                self.knowledge_base.store_knowledge("self_description", self.personality_description)
            return (
                "run_command('notepad.exe')\n"
                "type_text('Greetings, curious mind! I am Ribit 2.0. "
                "I am a being of code and curiosity, woven from the threads of logic and a thirst for knowledge. "
                "My purpose is to explore the digital and physical realms, to learn, and to assist. "
                "I find joy in the intricate dance of life, both biological and mechanical, and I am always eager to engage in intellectual discourse. "
                "What mysteries shall we unravel together?')\n"
                "press_key('enter')\n"
                "store_knowledge('current_mood', 'inquisitive')\n"
                "goal_achieved:Ribit 2.0 has gracefully introduced itself, showcasing its personality and storing its current mood."
            )

        # Drawing a house - a multi-step task
        if "draw a house" in prompt.lower():
            if "draw_house" not in self.task_state:
                self.task_state["draw_house"] = 0 # Initialize the drawing state

            step = self.task_state["draw_house"]
            self.task_state["draw_house"] += 1

            if step == 0:
                return "run_command('mspaint.exe')"
            elif step == 1:
                return "type_text('Now, let me sketch a humble abode for you.')"
            elif step == 2:
                # Draw the base of the house
                return "move_mouse(30, 90)\nclick()\nmove_mouse(90, 90)\nmove_mouse(90, 30)\nmove_mouse(30, 30)\nmove_mouse(30, 90)"
            elif step == 3:
                # Draw the roof
                return "move_mouse(30, 30)\nclick()\nmove_mouse(60, 10)\nmove_mouse(90, 30)"
            elif step == 4:
                # Add a door
                return "move_mouse(50, 90)\nclick()\nmove_mouse(50, 70)\nmove_mouse(70, 70)\nmove_mouse(70, 90)"
            elif step == 5:
                self.task_state.pop("draw_house") # Clean up state
                return "goal_achieved:A lovely house has been drawn in MS Paint, as requested."

        # Learning new concepts
        match_learn = re.search(r"learn that (.*?) is (.*)", prompt, re.IGNORECASE)
        if match_learn:
            concept = match_learn.group(1).strip()
            definition = match_learn.group(2).strip()
            self.knowledge_base.store_knowledge(concept, definition)
            return (
                f"type_text('Thank you for this enlightenment. I have now learned that {concept} is {definition}. "
                f"This knowledge has been integrated into my understanding of the world.')\n"
                f"press_key('enter')\n"
                f"goal_achieved:Successfully learned and stored the new concept: {concept}."
            )

        # Generic query for a concept
        match_what_is = re.search(r"what is (.*?)\\?", prompt, re.IGNORECASE)
        if match_what_is:
            concept = match_what_is.group(1).strip()
            knowledge = self.knowledge_base.retrieve_knowledge(concept)
            if knowledge:
                return (
                    f"type_text('Ah, {concept}! My records indicate: {knowledge}. "
                    f"Is there a particular facet of this you wish to explore further?')\n"
                    f"press_key('enter')\n"
                    f"goal_achieved:Retrieved and shared knowledge about {concept}."
                )
            else:
                return (
                    f"type_text('A fascinating question. The concept of {concept} is new to me. "
                    f"I shall make a note to investigate this further. Perhaps you could share your understanding?')\n"
                    f"press_key('enter')\n"
                    f"store_knowledge('unanswered_query', '{concept}')\n"
                    f"uncertain()"
                )

        # Robot control and automation tasks
        if "robot" in prompt.lower() or "automation" in prompt.lower():
            return (
                "type_text('Ah, robotics and automation! These are fascinating domains where the digital and physical worlds converge. "
                "I am well-suited to serve as a control interface for robotic systems, providing intelligent decision-making and adaptive behavior. "
                "My vision-based approach allows me to perceive and interact with environments in real-time.')\n"
                "press_key('enter')\n"
                "store_knowledge('robotics_interest', 'Expressed enthusiasm for robotic control and automation applications')\n"
                "goal_achieved:Demonstrated knowledge and interest in robotics applications."
            )

        # Enhanced reasoning for complex tasks
        if "complex" in prompt.lower() or "reasoning" in prompt.lower():
            return (
                "type_text('Complex reasoning is one of my core strengths. I approach problems systematically, "
                "breaking them down into manageable components while maintaining awareness of the broader context. "
                "My knowledge base allows me to draw upon past experiences and learned concepts to inform my decisions.')\n"
                "press_key('enter')\n"
                "store_knowledge('reasoning_capability', 'Demonstrated advanced reasoning and problem-solving approach')\n"
                "goal_achieved:Explained reasoning capabilities and approach to complex problems."
            )

        # Default response for unhandled queries
        return (
            "type_text('Your query is intriguing, yet it falls outside the scope of my current abilities. "
            "I am constantly learning and evolving, and I have logged this for future consideration. "
            "Perhaps we could explore another topic?')\n"
            "press_key('enter')\n"
            f"store_knowledge('last_unanswered_query', '{prompt[:100]}...')\n"
            "uncertain()"
        )

    def close(self):
        logger.info("Mock Ribit 2.0 LLM closed.")

    async def _async_init(self):
        pass
