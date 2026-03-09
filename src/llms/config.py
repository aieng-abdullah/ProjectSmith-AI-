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

    @staticmethod
    def load() -> "Settings":
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY is missing in environment variables.")

        return Settings(
            GROQ_API_KEY=groq_api_key,
            MODEL_NAME=os.getenv("MODEL_NAME", "openai/gpt-oss-120b"),
            TEMPERATURE=float(os.getenv("TEMPERATURE", 0.7)),
            STREAMING=os.getenv("STREAMING", "true").lower() == "true",
        )


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logging.getLogger("httpx").setLevel(logging.WARNING)

# Create a single settings instance
settings = Settings.load()
