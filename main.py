from database import engine, Base
from database import SessionLocal

import models, schema

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

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

@app.post("/users/", response_model=schema.UsersOut)
def create_user(user: schema.UsersCreate, db: Session = Depends(get_db)):
    db_user = models.Users(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=schema.UsersOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    # ToDO: handle user not found
    return user

@app.get("/users/{user_id}", response_model=schema.UsersOut)
def get_user_by_name(full_name: str, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.full_name == full_name).first()
    # ToDO: handle user not found
    return user

@app.put("/users/{user_id}", response_model=schema.UsersOut)
def update_user(user_id: int, user_updated: schema.UsersUpdate, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    # ToDO: handle user not found
    for key, value in user_updated.model_dump().items():
        # update attributes in user object
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    # ToDO: handle user not found
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}

