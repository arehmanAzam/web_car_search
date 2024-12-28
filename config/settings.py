from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Car Search API"
    
    class Config:
        env_file = ".env"

settings = Settings()