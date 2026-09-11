from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./material_rebirth.db"
    GROQ_API_KEY: str = ""
    LLAMA_MODEL: str = "llama-3.3-70b-versatile"
    LLAMA_VISION_MODEL: str = "llama-3.2-11b-vision-preview"
    LLAMA_BASE_URL: str = "https://api.groq.com/openai/v1"
    YOLO_MODEL_PATH: str = ""
    MAPS_API_KEY: str = ""
    DEMO_MODE: bool = False
    UPLOAD_DIR: str = "uploads"
    SECRET_KEY: str = "change-me"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()
