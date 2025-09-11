import os
from pydantic_settings import BaseSettings


os.makedirs(os.path.dirname("src/database/users.db"), exist_ok=True)

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./src/database/users.db"

settings = Settings()