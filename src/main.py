from fastapi import FastAPI
from src.infrastructure.database import Base, engine
from src.core.logger import setup_logging
from src.api.routers import users

# create the database tables
Base.metadata.create_all(bind=engine)

setup_logging()

# initialize FastAPI app
app = FastAPI()

# including user router
app.include_router(users.router)
