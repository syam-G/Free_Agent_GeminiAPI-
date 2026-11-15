from google import genai
from google.genai import types
from config.settings import settings
from utils.logger import logger
from core.prompts import ENTERPRISE_SYSTEM_INSTRUCTION
from tools import ALL_TOOLS

class EnterpriseAgent:
    """Manages the lifecycle of an autonomous AI Agent."""

    def __init__(self):
        # Validate settings at initialization
        settings.validate()
        
        logger.info("Initializing Gemini Client (Model: %s, Temperature: %s)", 
                    settings.MODEL_NAME, settings.TEMPERATURE)
        self.client = genai.Client(api_key=settings.API_KEY)
        
        self.chat = self.client.chats.create(
            model=settings.MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=ENTERPRISE_SYSTEM_INSTRUCTION,
                temperature=settings.TEMPERATURE,
                tools=ALL_TOOLS,
            )
        )
        logger.info("Agent initialized with %d registered tools.", len(ALL_TOOLS))

    def ask(self, message: str) -> str:
        """Sends a message to the agent and returns the final synthesized response."""
        logger.info("User prompt received: '%s'", message)
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            logger.error("Error during agent execution: %s", e)
            raise e