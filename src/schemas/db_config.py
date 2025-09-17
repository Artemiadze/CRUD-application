from pydantic import BaseModel
from pathlib import Path
from typing import Dict

class TableConfig(BaseModel):
    primary_key: str = "id"

class DatabaseConfig(BaseModel):
    engine: str
    name: str
    tables: Dict[str, TableConfig]

    @property
    def path(self) -> Path:
        return Path("./src/database") / self.name

    def get_table_path(self, table_name: str, base_dir: Path) -> Path:
        table = self.tables.get(table_name)
        if table is None:
            raise ValueError(f"Table {table_name} not found in config")
        
        # Construct the full path to the database file
        return base_dir / self.name