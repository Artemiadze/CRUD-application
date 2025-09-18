from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.infrastructure.database import get_db
from src.schemas.passport_schema import PassportCreate, PassportUpdate, PassportOut
from src.services.passport_service import PassportService
from src.utils.exceptions import NotFoundError, DuplicateError, DomainValidationError
from src.core.logger import get_logger


router = APIRouter(prefix="/passports", tags=["passports"])

def get_service(db: Session = Depends(get_db)) -> PassportService:
    return PassportService(db)

@router.post("/", response_model=PassportOut)
def create_passport(passport_in: PassportCreate, service: PassportService = Depends(get_service)):
    logger = get_logger(user_id=passport_in.user_id)
    logger.info(f"[create_passport] payload={passport_in.model_dump()}")

    try:
        passport = service.create_passport(passport_in)
    except NotFoundError:
        logger.warning(f"[create_passport] user not found id={passport_in.user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    except DuplicateError as e:
        logger.warning(f"[create_passport] duplicate: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except DomainValidationError as e:
        logger.error(f"[create_passport] validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    logger.info(f"[create_passport] created id={passport.id}")
    return passport

@router.get("/{passport_id}", response_model=PassportOut)
def get_passport(passport_id: UUID, service: PassportService = Depends(get_service)):
    logger = get_logger(passport_id)
    logger.info(f"[get_passport] id={passport_id}")

    try:
        return service.get_passport(passport_id)
    except NotFoundError:
        logger.warning(f"[get_passport] not found id={passport_id}")
        raise HTTPException(status_code=404, detail="Passport not found")
    
@router.put("/{passport_id}", response_model=PassportOut)
def update_passport(passport_id: UUID, passport_in: PassportUpdate, service: PassportService = Depends(get_service)):
    logger = get_logger(passport_id)
    logger.info(f"[update_passport] payload={passport_in.model_dump()}")

    try:
        return service.update_passport(passport_id, passport_in)
    except NotFoundError:
        logger.warning(f"[update_passport] not found id={passport_id}")
        raise HTTPException(status_code=404, detail="Passport not found")
    except DuplicateError as e:
        logger.warning(f"[update_passport] duplicate: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except DomainValidationError as e:
        logger.error(f"[update_passport] validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{passport_id}")
def delete_passport(passport_id: UUID, service: PassportService = Depends(get_service)):
    logger = get_logger(passport_id)
    logger.info(f"[delete_passport] attempt to delete id={passport_id}")

    try:
        service.delete_passport(passport_id)
    except NotFoundError:
        logger.warning(f"[delete_passport] not found id={passport_id}")
        raise HTTPException(status_code=404, detail="Passport not found")

    logger.info(f"[delete_passport] deleted id={passport_id}")
    return {"detail": "Passport deleted successfully"}