from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
import uuid

from src.domain.passport import Passport
from src.domain.identifiers  import PassportId
from src.infrastructure.models.passport import PassportModel
from src.domain.interfaces.ipassport_repo import IPassportRepository
from src.core.logger import get_logger

class PassportRepository(IPassportRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, obj: PassportModel) -> Passport:
        return Passport(
            id=PassportId(uuid.UUID(obj.id)), # Convert string ID back to UUID for domain model
            birth_date=obj.birth_date,
            passport_number=obj.passport_number,
            passport_series=obj.passport_series,
            receipt_date=obj.receipt_date,
            user_id=PassportId(uuid.UUID(obj.user_id))  # Convert string ID back to UUID for domain model
        )
    
    def create_passport(self, passport: Passport) -> Passport:
        logger = get_logger()
        log_message = str(passport.passport_series) + ", " + str(passport.passport_number)
        logger.debug(f"[PassportRepository.create_passport] DB: inserting passport {log_message}")

        try:
            db_obj = {key: value for key, value in passport.__dict__.items() if key != 'id' and value is not None}
            db_passport = PassportModel(**db_obj)
            self.db.add(db_passport)
            self.db.commit()
            self.db.refresh(db_passport)
            return self._to_domain(db_passport)
        except Exception as e:
            logger.error(f"[PassportRepository.create_passport] DB error while creating passport {log_message.strip()}: {e}")
            self.db.rollback()
            raise
    
    def get_passport(self, passport_id: PassportId) -> Passport | None:
        str_id = str(passport_id)

        logger = get_logger()
        logger.debug(f"[PassportRepository.get_passport] DB: fetching passport with id={str_id}")

        db_passport = self.db.query(PassportModel).options(joinedload(PassportModel.user)).filter(PassportModel.id == str(str_id)).first()
        if db_passport:
            return self._to_domain(db_passport)
        return None
    
    def get_passport_by_series_and_number(self, series: str, number: str) -> Passport | None:
        logger = get_logger()
        logger.debug(f"[PassportRepository.get_passport_by_series_and_number] DB: fetching passport with series={series} and number={number}")

        db_passport = self.db.query(PassportModel).options(joinedload(PassportModel.user)).filter(
        and_(
            PassportModel.passport_series == series,
            PassportModel.passport_number == number
            )
        ).first()

        if db_passport:
            return self._to_domain(db_passport)
        return None
    
    def get_passport_by_number(self, number: str) -> Passport | None:
        logger = get_logger()
        logger.debug(f"[PassportRepository.get_passport_by_number] DB: fetching user with passport={number}")

        obj = self.db.query(PassportModel).filter(PassportModel.passport_number == number).first()
        if obj:
            return self._to_domain(obj)
        return None
    
    def get_passport_by_series(self, series: str) -> Passport | None:
        logger = get_logger()
        logger.debug(f"[PassportRepository.get_passport_by_series] DB: fetching user with passport={series}")

        obj = self.db.query(PassportModel).filter(PassportModel.passport_series == series).first()
        if obj:
            return self._to_domain(obj)
        return None
    
    def update_passport(self, passport: Passport) -> Passport:
        str_id = str(passport.id)
        logger = get_logger()
        logger.debug(f"[PassportRepository.update_passport] DB: updating passport with id={str_id}")

        db_passport = self.db.query(PassportModel).filter(PassportModel.id == str(passport.id)).first()
        if not db_passport:
            logger.warning(f"[PassportRepository.update_passport] DB: passport with id={str_id} not found")
            return None
        
        for field in ["birth_date", "passport_number", "passport_series", "receipt_date", "user_id"]:
            value = getattr(passport, field, None)
            if value is not None:
                setattr(db_passport, field, value)

        self.db.commit()
        self.db.refresh(db_passport)

        logger.info(f"[PassportRepository.update_passport] DB: passport with id={str_id} updated successfully")
        return self._to_domain(db_passport)
    
    def delete_passport(self, passport_id: PassportId) -> bool:
        str_id = str(passport_id)
        logger = get_logger()
        logger.debug(f"[PassportRepository.delete_passport] DB: deleting passport with id={str_id}")

        db_passport = self.db.query(PassportModel).filter(PassportModel.id == str(passport_id)).first()
        if not db_passport:
            logger.warning(f"[PassportRepository.delete_passport] DB: passport with id={str_id} not found for deletion")
            return False
        
        self.db.delete(db_passport)
        self.db.commit()
        logger.info(f"[PassportRepository.delete_passport] DB: passport with id={str_id} deleted successfully")
        return True
