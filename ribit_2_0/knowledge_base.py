import os
import logging

logger = logging.getLogger(__name__)

class KnowledgeBase:
    def __init__(self, storage_file="knowledge.txt"):
        self.storage_file = storage_file
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, "w") as f:
                f.write("") # Create an empty file if it doesn't exist
            logger.info(f"KnowledgeBase file created: {self.storage_file}")

    def store_knowledge(self, key: str, value: str):
        try:
            with open(self.storage_file, "a") as f:
                f.write(f"[{key}]: {value}\n")
            logger.info(f"Stored knowledge: [{key}] = {value}")
            return f"Knowledge stored under key: {key}"
        except Exception as e:
            logger.error(f"Error storing knowledge: {e}")
            return f"Error storing knowledge: {e}"

    def retrieve_knowledge(self, key: str):
        try:
            with open(self.storage_file, "r") as f:
                for line in f:
                    if line.startswith(f"[{key}]"):
                        value = line.split(": ", 1)[1].strip()
                        logger.info(f"Retrieved knowledge: [{key}] = {value}")
                        return value
            logger.info(f"Knowledge not found for key: {key}")
            return f"Knowledge not found for key: {key}"
        except Exception as e:
            logger.error(f"Error retrieving knowledge: {e}")
            return f"Error retrieving knowledge: {e}"

    def get_all_knowledge(self):
        try:
            with open(self.storage_file, "r") as f:
                content = f.read()
            logger.info("Retrieved all knowledge.")
            return content
        except Exception as e:
            logger.error(f"Error getting all knowledge: {e}")
            return f"Error getting all knowledge: {e}"


