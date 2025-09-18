import logging
from typing import Optional
from src.core.config import configs

class LoggerAdapter(logging.LoggerAdapter):
    """
    Custom logger adapter to add contextual information to log records.
    """

    def process(self, msg, kwargs):
        # Add all extra context information to the log message
        context = " ".join(f"{k}={v}" for k, v in self.extra.items())
        return f"[{context}] {msg}", kwargs
    

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


def get_logger(**kwargs) -> LoggerAdapter:
    """
    Factory function to get a logger with arbitrary context.
    If a context value is None, it defaults to 'anon'.
    Args:
        **kwargs: Arbitrary keyword arguments for logging context.
    Returns:
        LoggerAdapter: Logger with provided context.
    """
    main_logger = logging.getLogger("app")
    clean_kwargs = {k: (v if v is not None else "anon") for k, v in kwargs.items()}
    return LoggerAdapter(main_logger, clean_kwargs)