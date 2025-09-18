from datetime import date

from src.domain.passport import Passport, PassportID
from src.utils.exceptions import DuplicateError, NotFoundError
from src.domain.interfaces.ipassport_repo import IPassportRepository

class PassportService:
    def __init__(self, repo: IPassportRepository):
        self.repo = repo

    def create_passport(self, passport: Passport):
        # Business logic
        if passport.birth_date > date.today():
            raise ValueError("Birth date cannot be in the future.")
        
        if passport.receipt_date and passport.receipt_date < passport.birth_date:
            raise ValueError("Receipt date cannot be before birth date.")
        
        if self.repo.get_passport_by_number(passport.passport_number):
            raise DuplicateError("passport_number", passport.passport_number)
        
        if self.repo.get_passport_by_series_and_number(passport.passport_series, passport.passport_number):
            raise DuplicateError("passport", f"{passport.passport_series} {passport.passport_number}")

        return self.repo.create_passport(passport)

    def get_passport(self, passport_id: PassportID):
        passport = self.repo.get_passport(passport_id)
        if not passport:
            raise NotFoundError("Passport", passport_id)
        return passport
        
    def get_passport_by_series_and_number(self,series: str, number: str):
        passport = self.repo.get_passport_by_series_and_number(series, number)
        if not passport:
            log_message = str(series) + ' ' + str(number)
            raise NotFoundError("Passport", log_message.strip())
        return passport
    
    def update_passport(self, passport: Passport):
        existing_passport = self.repo.get_passport(passport.id)
        if not existing_passport:
            raise NotFoundError("Passport", passport.id)
        
        if passport.birth_date and passport.birth_date > date.today():
            raise ValueError("Birth date cannot be in the future.")
        
        # Check if the receipt date is valid
        if passport.receipt_date:
            if passport.birth_date and passport.receipt_date < passport.birth_date:
                raise ValueError("Receipt date cannot be before birth date.")
            elif (
                passport.birth_date is None
                and existing_passport.birth_date is not None
                and passport.receipt_date < existing_passport.birth_date
            ):
                raise ValueError("Receipt date cannot be before birth date.")
        
        if passport.passport_number and passport.passport_number != existing_passport.passport_number:
            if self.repo.get_passport_by_number(passport.passport_number):
                raise DuplicateError("passport_number", passport.passport_number)
            
        if passport.passport_series and passport.passport_series != existing_passport.passport_series:
            if self.repo.get_passport_by_series(passport.passport_series):
                raise DuplicateError("passport_series", passport.passport_series)
        
        return self.repo.update_passport(passport)
    
    def delete_passport(self, passport_id: PassportID):
        user = self.repo.get_passport(passport_id)
        if not user:
            raise NotFoundError("Passport", passport_id)
        return self.repo.delete_passport(passport_id)