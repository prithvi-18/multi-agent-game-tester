import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    max_concurrent_tests: int = 3
    default_timeout_seconds: int = 300
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
