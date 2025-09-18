from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.domain.users import User, UserId
from src.schemas.user_schema import UsersCreate, UsersOut, UsersUpdate
from src.infrastructure.database import get_db
from src.infrastructure.repository.user_repo import UserRepository
from src.services.user_service import UserService
from src.utils.exceptions import DomainValidationError, DuplicateError, NotFoundError
from src.core.logger import get_logger

# creating router
router = APIRouter(prefix="/users", tags=["users"])


def get_service(db: Session = Depends(get_db)) -> UserService:
    """
    Dependency to get UserService with a database session.
    """
    return UserService(db)

@router.post("/", response_model=UsersOut)
def create_user(user_in: UsersCreate, service: UserService = Depends(get_service)):
    logger = get_logger(user_id=None)
    logger.info(f"[create_user] POST /users - payload: {user_in.model_dump()}")

    try:
        user = service.create_user(user_in)
    except DomainValidationError as e:
        logger.error(f"[create_user] Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    logger.info(f"[create_user] User created id={user.id}")
    return user

@router.get("/id/{user_id}", response_model=UsersOut)
def get_user(user_id: UUID, service: UserService = Depends(get_service)):
    logger = get_logger(user_id=user_id)
    logger.info(f"[get_user] GET /users/id/{user_id} - fetched user: {user_id}")

    try:
        # parsed_id = UserId(UUID(user_id))
        # user = service.get_user(parsed_id)
        return service.get_user(UserId(user_id))
    except NotFoundError:
        logger.warning(f"[get_user] not found id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/find", response_model=List[UsersOut])
def get_user_by_full_name(first_name: str | None = Query(None),
    last_name: str | None = Query(None),
    patronymic: str | None = Query(None),
    service: UserService = Depends(get_service)):


    logger = get_logger(user_id=None)
    log_message = str(first_name) + ", " + str(last_name) + ", " + str(patronymic)
    logger.info(f"[get_user_by_full_name] GET /users/by_name - fetched user by name: {log_message.strip()}")

    try:
        user = service.get_user_by_full_name(first_name, last_name, patronymic)
        logger.info(f"[get_user_by_full_name] User retrieved: {log_message.strip()}")
        return user
    except NotFoundError:
        logger.warning(f"[get_user_by_full_name] User not found with name: {log_message.strip()}")
        raise HTTPException(status_code=404, detail="User not found")

"""
@router.put("/{user_id}", response_model=UsersOut)
def update_user(user_id: str, user_updated: UsersUpdate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)

    logger = get_logger(user_id=user_id)
    logger.info(f"[update_user] PUT /users/{user_id} - update payload: {user_updated.model_dump()}")

    try:
        parsed_id = UserId(UUID(user_id))
        existing_user = service.get_user(parsed_id)

        # Create a new User instance with updated fields
        updated_user = User(
            id=parsed_id,
            first_name=user_updated.first_name or existing_user.first_name,
            last_name=user_updated.last_name or existing_user.last_name,
            patronymic=user_updated.patronymic or existing_user.patronymic,
            phone_number=user_updated.phone_number or existing_user.phone_number,
        )

        user = service.update_user(updated_user)

    except NotFoundError:
        logger.warning(f"[update_user] User not found with ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    except DuplicateError as e:
        logger.warning(f"[update_user] Duplicate error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    logger.info(f"[update_user] User updated: {user.id}")
    return user
"""

@router.put("/{user_id}", response_model=UsersOut)
def update_user(
    user_id: UUID, user_in: UsersUpdate, service: UserService = Depends(get_service)
):
    logger = get_logger(user_id=user_id)
    logger.info(f"[update_user] PUT /users/{user_id} - update payload: {user_in.model_dump()}")

    try:
        # parsed_id = UserId(UUID(user_id))
        # return service.get_user(parsed_id)
        return service.update_user(UserId(user_id), user_in)
    except NotFoundError:
        logger.warning(f"[update_user] not found id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    except DuplicateError as e:
        logger.warning(f"[update_user] Duplicate error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}")
def delete_user(user_id: UUID, service: UserService = Depends(get_service)):
    logger = get_logger(user_id=user_id)
    logger.info(f"[delete_user] DELETE /users/{user_id} - attempt to delete user")

    try:
        #parsed_id = UserId(UUID(user_id))
        #service.delete_user(parsed_id)
        service.delete_user(UserId(user_id))
    except NotFoundError:
        logger.warning(f"[delete_user] not found id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(f"[delete_user] deleted id={user_id}")
    return {"detail": "User deleted successfully"}