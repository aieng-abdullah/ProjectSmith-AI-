"""
Application configuration module.

This module loads environment variables and exposes a strongly-typed
configuration object used across the application. Configuration values
are loaded from the system environment or a `.env` file using python-dotenv.

The module also configures global logging behavior.
"""


import os
import logging
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    GROQ_API_KEY: str
    MODEL_NAME: str
    TEMPERATURE: float
    STREAMING:bool
    POSTGRES_URL : str
    FAST_API:str



    @staticmethod
    def load() -> "Settings":
        groq_api_key = os.getenv("GROQ_API_KEY", "")
        
        postgres_url = os.getenv("POSTGRES_URL", "postgresql://test:test@localhost:5432/test")
        
        fast_api = os.getenv("FAST_API", "http://localhost:8000")

        return Settings(
            GROQ_API_KEY=groq_api_key,
            MODEL_NAME=os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"),
            TEMPERATURE=float(os.getenv("TEMPERATURE", 0.7)),
            STREAMING=os.getenv("STREAMING", "true").lower() == "true",
            POSTGRES_URL=postgres_url,
            FAST_API=fast_api,
        )


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logging.getLogger("httpx").setLevel(logging.WARNING)

# Create a single settings instance
settings = Settings.load()
