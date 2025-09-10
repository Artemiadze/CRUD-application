from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users

# create the database tables
Base.metadata.create_all(bind=engine)

# initialize FastAPI app
app = FastAPI()

# including user router
app.include_router(users.router)
