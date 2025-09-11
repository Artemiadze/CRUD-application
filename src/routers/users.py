from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import src.crud, src.schema
from src.database import get_db

# creating router
router = APIRouter(prefix="/users", tags=["users"])

# CRUD operation endpoints for interacting with HTTP requests
@router.post("/", response_model=src.schema.UsersOut)
def create_user(user: src.schema.UsersCreate, db: Session = Depends(get_db)):
    return src.crud.create_user(db, user)

@router.get("/id/{user_id}", response_model=src.schema.UsersOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = src.crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Person not found")
    return user

@router.get("/by_name", response_model=src.schema.UsersOut)
def get_user_by_name(full_name: str, db: Session = Depends(get_db)):
    user = src.crud.get_user_by_name(db, full_name)
    if not user:
        raise HTTPException(status_code=404, detail="Person not found")
    return user

@router.put("/{user_id}", response_model=src.schema.UsersOut)
def update_user(user_id: int, user_updated: src.schema.UsersUpdate, db: Session = Depends(get_db)):
    user = src.crud.update_user(db, user_id, user_updated)
    if not user:
        raise HTTPException(status_code=404, detail="Person not found")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    ok = src.crud.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"detail": "User deleted"}