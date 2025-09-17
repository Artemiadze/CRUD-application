import logging
from typing import Optional
from src.core.config import configs

class UserLoggerAdapter(logging.LoggerAdapter):
    """
    Custom logger adapter to add contextual information to log records.
    """

    def process(self, msg, kwargs):
        user_id = self.extra.get("user_id", "anon")
        return f"[user_id={user_id}] {msg}", kwargs
    

def setup_logging() -> logging.Logger:
    """
    Configure logging for the application with file and console output.
    
    Returns:
        logging.Logger: Configured logger with name 'app'.
    """
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    
    # Avoid adding handlers multiple times
    if not logger.handlers:
        formatter = logging.Formatter(configs.logging.format)
        
        # File handler (DEBUG and above) (mode='w' to overwrite on each run)
        file_handler = logging.FileHandler(configs.logging.file_name, mode='w')
        file_handler.setLevel(configs.logging.file_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler (INFO and above)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(configs.logging.console_level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    
    # Configure third-party loggers
    # logging.getLogger("uvicorn").setLevel(logging.INFO)
    # logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    # logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
    
    return logger


def get_user_logger(user_id: Optional[int] = None) -> UserLoggerAdapter:
    """
    Factory function to get a logger with user_id context.
    If user_id is None, it defaults to 'anon'.
    
    Args:
        user_id (Optional[int]): The ID of the user for logging context.
    
    Returns:
        UserLoggerAdapter: Logger with user_id context.
    """
    main_logger = logging.getLogger("app")
    return UserLoggerAdapter(main_logger, {"user_id": user_id if user_id is not None else "anon"})