from pydantic import BaseModel
from pathlib import Path
from src.schemas.db_config import DatabaseConfig

class PathsConfig(BaseModel):
    database_dir: Path

class LoggingConfig(BaseModel):
    file_name: str
    file_level: str
    console_level: str
    format: str

class AppConfig(BaseModel):
    env: str
    project_name: str
    paths: PathsConfig
    database: DatabaseConfig
    logging: LoggingConfig

