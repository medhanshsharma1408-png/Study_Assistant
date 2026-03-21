from pydantic_settings import BaseSettings
from pathlib import Path

ENV_PATH = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    groq_api_key: str
    model: str = "llama-3.1-8b-instant"
    temperature: float = 0.0
    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"

settings = Settings()