from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
 
db_folder = "./app/database"
os.makedirs(db_folder, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_folder}/users.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
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