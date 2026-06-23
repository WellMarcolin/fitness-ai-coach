from pydantic_settings import BaseSettings
from typing import Literal
import os


class Settings(BaseSettings):
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: str = "http://localhost:3000"

    # Intervals.icu
    intervals_athlete_id: str = ""
    intervals_api_key: str = ""

    # LLM Provider
    llm_provider: Literal["deepseek", "glm", "groq", "ollama"] = "deepseek"

    # DeepSeek
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"

    # GLM (Zhipu)
    glm_api_key: str = ""
    glm_model: str = "glm-4-flash"

    # Groq
    groq_api_key: str = ""
    groq_model: str = "llama3-70b-8192"

    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"

    # Telegram
    telegram_bot_token: str = ""
    telegram_webhook_url: str = ""

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/fitness_coach.db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

# Allow env override
_db_url = os.environ.get("DATABASE_URL")
if _db_url:
    settings.database_url = _db_url
