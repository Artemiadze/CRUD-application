from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
 
SQLALCHEMY_DATABASE_URL = "sqlite:///./people.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Base class for db models
Base = declarative_base()