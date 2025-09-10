from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schema
from database import get_db

# creating router
router = APIRouter(prefix="/users", tags=["users"])

# endpoints for CRUD operations
@router.post("/", response_model=schema.UsersOut)
def create_user(user: schema.UsersCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.get("/id/{user_id}", response_model=schema.UsersOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Person not found")
    return user

@router.get("/by_name", response_model=schema.UsersOut)
def get_user_by_name(full_name: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_name(db, full_name)
    if not user:
        raise HTTPException(status_code=404, detail="Person not found")
    return user

@router.put("/{user_id}", response_model=schema.UsersOut)
def update_user(user_id: int, user_updated: schema.UsersUpdate, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, user_updated)
    if not user:
        raise HTTPException(status_code=404, detail="Person not found")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"detail": "User deleted"}