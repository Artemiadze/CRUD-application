from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.schemas.user_schema import UsersCreate, UsersOut, UsersUpdate
from src.infrastructure.database import get_db
from src.infrastructure.repository.user_repo import UserRepository
from src.services.user_service import UserService
from src.domain.users import DomainValidationError
from src.core.config import get_user_logger

# creating router
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UsersOut)
def create_user(user_in: UsersCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)
    
    logger = get_user_logger(user_id=None)
    logger.info(f"POST /users - payload: {user_in.model_dump()}")

    try:
        user = service.create_user(user_in)
        logger = get_user_logger(user_id=user.id)
        logger.info(f"User created: {user.id}")
    except DomainValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    return user


@router.get("/id/{user_id}", response_model=UsersOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)

    user = service.get_user(user_id)
    logger = get_user_logger(user_id=user_id)
    logger.info(f"GET /users/id/{user_id} - fetched user: {user_id}")

    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"User retrieved: {user.id}")
    return user


@router.get("/by_name", response_model=UsersOut)
def get_user_by_name(full_name: str, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)

    user = service.get_user_by_name(full_name)
    logger = get_user_logger(user_id=user.id if user else None)
    logger.info(f"GET /users/by_name - fetched user by name: {full_name}")

    if not user:
        logger.warning(f"User not found with name: {full_name}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"User retrieved: {user.id}")
    return user


@router.put("/{user_id}", response_model=UsersOut)
def update_user(user_id: int, user_updated: UsersUpdate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)

    user = service.update_user(user_id, user_updated)
    logger = get_user_logger(user_id=user_id)
    logger.info(f"PUT /users/{user_id} - update payload: {user_updated.model_dump()}")

    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"User updated: {user.id}")
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)

    ok = service.delete_user(user_id)
    logger = get_user_logger(user_id=user_id)
    logger.info(f"DELETE /users/{user_id} - attempt to delete user")

    if not ok:
        logger.warning(f"User not found with ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(f"User deleted: {user_id}")
    return {"detail": "User deleted successfully"}