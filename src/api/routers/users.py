from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.schemas import UsersCreate, UsersOut, UsersUpdate
from src.infrastructure.database import get_db
from src.infrastructure.repository.user_repo import UserRepository
from src.services.user_service import UserService
from src.domain.users import DomainValidationError

# creating router
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UsersOut)
def create_user(user_in: UsersCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)

    try:
        user = service.create_user(user_in)  # pydantic → domain в сервисе
    except DomainValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return user


@router.get("/id/{user_id}", response_model=UsersOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)

    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/by_name", response_model=UsersOut)
def get_user_by_name(full_name: str, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)

    user = service.get_user_by_name(full_name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UsersOut)
def update_user(user_id: int, user_updated: UsersUpdate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)

    user = service.update_user(user_id, user_updated)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)

    ok = service.delete_user(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}