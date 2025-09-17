from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.config import configs

# creating an engine for work with SQLAlchemy 
db_file = configs.database.get_table_path("users", configs.paths.database_dir)
DATABASE_URL = f"sqlite:///{db_file}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# creating a configured "Session" class
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# Base class for db models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()