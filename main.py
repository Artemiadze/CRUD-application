from database import engine, Base
from database import SessionLocal
import models

from fastapi import FastAPI

# creating table
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

