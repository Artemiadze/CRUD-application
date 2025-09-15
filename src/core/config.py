import os
import logging
from pydantic_settings import BaseSettings

# Creating directory for the database if it doesn't exist
os.makedirs(os.path.dirname("src/database/users.db"), exist_ok=True)

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./src/database/users.db"


# Configuring logging
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        filename = "ServiceLogs.log",
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    logger = logging.getLogger("app")
    return logger


logger = setup_logging()
settings = Settings()