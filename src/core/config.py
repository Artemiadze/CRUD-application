import yaml
from src.schemas.config import AppConfig


def load_config(path: str = "config.yaml") -> AppConfig:
    with open(path, "r", encoding="utf-8") as f:
        cfg_dict = yaml.safe_load(f)
    return AppConfig(**cfg_dict)

# Load configuration at module level
configs = load_config()

# Create necessary directories
configs.paths.database_dir.mkdir(parents=True, exist_ok=True)
