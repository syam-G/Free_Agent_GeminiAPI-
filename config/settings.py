import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    MODEL_NAME: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    TEMPERATURE: float = float(os.getenv("AGENT_TEMPERATURE", "0.2"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    @classmethod
    def validate(cls):
        """Validates critical enterprise configurations before launching."""
        if not cls.API_KEY or cls.API_KEY == "your_gemini_api_key_here":
            print("[CRITICAL] GEMINI_API_KEY is not set in environment or .env file.")
            print("[CRITICAL] Please configure your key in .env before running.")
            sys.exit(1)

settings = Settings()