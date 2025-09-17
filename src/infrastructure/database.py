from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.config import configs

# creating an engine for work with SQLAlchemy 
DATABASE_URL = f"sqlite:///{configs.database.path}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# creating a configured "Session" class
SessionLocal = sessionmaker(autoflush=True, bind=engine)

# Base class for db models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()