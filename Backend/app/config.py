from pydantic_settings import BaseSettings
from pathlib import Path

ENV_PATH = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    groq_api_key: str
    database_url: str
    model: str = "llama-3.1-8b-instant"
    temperature: float = 0.0
    allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()