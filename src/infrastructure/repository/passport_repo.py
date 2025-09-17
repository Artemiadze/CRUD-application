from sqlalchemy.orm import Session
import uuid

from src.domain.passport import Passport, PassportID
from src.infrastructure.models.passport import PassportModel
from src.domain.interfaces.ipassport_repo import IPassportRepository
from src.core.logger import get_user_logger

class PassportRepository(IPassportRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, obj: PassportModel) -> Passport:
        return Passport(
            id=PassportID(uuid.UUID(obj.id)), # Convert string ID back to UUID for domain model
            birth_date=obj.birth_date,
            passport_number=obj.passport_number,
            passport_series=obj.passport_series,
            receipt_date=obj.receipt_date,
            user_id=PassportID(uuid.UUID(obj.user_id))  # Convert string ID back to UUID for domain model
        )
    
    def create_passport(self, passport: Passport) -> Passport:
        logger = get_user_logger()
        log_message = str(passport.passport_series) + ", " + str(passport.passport_number)
        logger.debug(f"[PassportRepository.create_passport] DB: inserting passport {log_message}")

        try:
            db_passport = PassportModel(
                id=str(passport.id),  # Store UUID as string in DB
                birth_date=passport.birth_date,
                passport_number=passport.passport_number,
                passport_series=passport.passport_series,
                receipt_date=passport.receipt_date,
                user_id=str(passport.user_id)  # Store UUID as string in DB
            )
            self.db.add(db_passport)
            self.db.commit()
            self.db.refresh(db_passport)
            return self._to_domain(db_passport)
        except Exception as e:
            logger.error(f"[PassportRepository.create_passport] DB error while creating passport {log_message.strip()}: {e}")
            self.db.rollback()
            raise
    
    def get_passport(self, passport_id: PassportID) -> Passport | None:
        str_id = str(passport_id)

        logger = get_user_logger()
        logger.debug(f"[PassportRepository.get_passport] DB: fetching passport with id={str_id}")

        db_passport = self.db.query(PassportModel).filter(PassportModel.id == str(str_id)).first()
        if db_passport:
            return self._to_domain(str_id)
        return None
    
    def get_passport_by_number(self, passport_number: str) -> Passport | None:
        logger = get_user_logger()
        logger.debug(f"[PassportRepository.get_passport_by_number] DB: fetching passport with number={passport_number}")

        db_passport = self.db.query(PassportModel).filter(PassportModel.passport_number == passport_number).first()
        if db_passport:
            return self._to_domain(db_passport)
        return None
    
    def get_passport_by_series(self, passport_series: str) -> Passport | None:
        logger = get_user_logger()
        logger.debug(f"[PassportRepository.get_passport_by_series] DB: fetching passport with series={passport_series}")

        db_passport = self.db.query(PassportModel).filter(PassportModel.passport_series == passport_series).first()
        if db_passport:
            return self._to_domain(db_passport)
        return None
    
    def get_passport_by_series_and_number(self, series: str, number: str) -> Passport | None:
        logger = get_user_logger()
        logger.debug(f"[PassportRepository.get_passport_by_series_and_number] DB: fetching passport with series={series} and number={number}")

        db_passport = self.db.query(PassportModel).filter(
            PassportModel.passport_series == series,
            PassportModel.passport_number == number
        ).first()
        
        if db_passport:
            return self._to_domain(db_passport)
        return None
    
    def update_passport(self, passport: Passport) -> Passport:
        str_id = str(passport.id)
        logger = get_user_logger()
        logger.debug(f"[PassportRepository.update_passport] DB: updating passport with id={str_id}")

        db_passport = self.db.query(PassportModel).filter(PassportModel.id == str(passport.id)).first()
        if not db_passport:
            logger.warning(f"[PassportRepository.update_passport] DB: passport with id={str_id} not found")
            return None
        
        db_passport.birth_date = passport.birth_date
        db_passport.passport_number = passport.passport_number
        db_passport.passport_series = passport.passport_series
        db_passport.receipt_date = passport.receipt_date
        db_passport.user_id = str(passport.user_id)  # Store UUID as string in DB
        self.db.commit()
        self.db.refresh(db_passport)

        logger.info(f"[PassportRepository.update_passport] DB: passport with id={str_id} updated successfully")
        return self._to_domain(db_passport)
    
    def delete_passport(self, passport_id: PassportID) -> bool:
        str_id = str(passport_id)
        logger = get_user_logger()
        logger.debug(f"[PassportRepository.delete_passport] DB: deleting passport with id={str_id}")

        db_passport = self.db.query(PassportModel).filter(PassportModel.id == str(passport_id)).first()
        if not db_passport:
            logger.warning(f"[PassportRepository.delete_passport] DB: passport with id={str_id} not found for deletion")
            return False
        
        self.db.delete(db_passport)
        self.db.commit()
        logger.info(f"[PassportRepository.delete_passport] DB: passport with id={str_id} deleted successfully")
        return True
