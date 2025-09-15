import os
import logging
from pydantic_settings import BaseSettings

# Creating directory for the database if it doesn't exist
os.makedirs(os.path.dirname("src/database/users.db"), exist_ok=True)

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./src/database/users.db"


class UserLoggerAdapter(logging.LoggerAdapter):
    """
    Custom logger adapter to add contextual information to log records.
    """

    def process(self, msg, kwargs):
        user_id = self.extra.get("user_id", "anon")
        return f"[user_id={user_id}] {msg}", kwargs
    

# Configuring logging
def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        filename = "ServiceLogs.log",
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    logger = logging.getLogger("app")
    return logger


main_logger = setup_logging()

settings = Settings()


def get_user_logger(user_id: int | None = None):
    """
    Factory function to get a logger with user_id context.
    If user_id is None, it defaults to 'non'.
    """
    return UserLoggerAdapter(main_logger, {"user_id": user_id})