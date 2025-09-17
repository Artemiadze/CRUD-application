import yaml
from pathlib import Path
from pydantic import BaseModel
from typing import Dict

class TableConfig(BaseModel):
    file: str
    primary_key: str

class DatabaseConfig(BaseModel):
    engine: str
    name: str
    tables: Dict[str, TableConfig]

    def get_table_path(self, table_name: str, base_dir: Path) -> Path:
        table = self.tables.get(table_name)
        if table is None:
            raise ValueError(f"Table {table_name} not found in config")
        return base_dir / table.file

class PathsConfig(BaseModel):
    database_dir: Path
    log_dir: Path

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


def load_config(path: str = "config.yaml") -> AppConfig:
    with open(path, "r", encoding="utf-8") as f:
        cfg_dict = yaml.safe_load(f)
    return AppConfig(**cfg_dict)

# Load configuration at module level
configs = load_config()

# Create necessary directories
configs.paths.database_dir.mkdir(parents=True, exist_ok=True)
