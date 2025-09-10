from database import engine, Base
from database import SessionLocal

import models, schema

from fastapi import FastAPI, Depends, HTTPException
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

@app.get("/users/id/{user_id}", response_model=schema.UsersOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Person not found")
    return user

@app.get("/users/by_name", response_model=schema.UsersOut)
def get_user_by_name(full_name: str, db: Session = Depends(get_db)):
    print("full_name received:", full_name)
    user = db.query(models.Users).filter(models.Users.full_name == full_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="Person not found")
    return user

@app.put("/users/{user_id}", response_model=schema.UsersOut)
def update_user(user_id: int, user_updated: schema.UsersUpdate, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Person not found")
    
    # Get only the fields that were provided in the request
    update_data = user_updated.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Person not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}

