from fastapi import FastAPI
from database import Base, engine
from routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI()

# including user router
app.include_router(users.router)
