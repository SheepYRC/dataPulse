import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "DataPulse"
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    SQLITE_DB_PATH: Path = DATA_DIR / "datapulse.db"
    DUCKDB_PATH: Path = DATA_DIR / "analytics.duckdb"
    SNAPSHOT_DIR: Path = DATA_DIR / "snapshots"
    
    # Ensure directories exist
    def setup_directories(self):
        for directory in [self.DATA_DIR, self.SNAPSHOT_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.setup_directories()
