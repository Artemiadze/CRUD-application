from abc import ABC, abstractmethod
from typing import Optional
from src.domain.passport import Passport, PassportID

class IPassportRepository(ABC):
    @abstractmethod
    def create_passport(self, user: Passport) -> Passport:
        pass

    @abstractmethod
    def get_passport(self, user_id: PassportID) -> Optional[Passport]:
        pass

    @abstractmethod
    def get_passport_by_number(self, passport_number: str) -> Optional[Passport]:
        pass

    @abstractmethod
    def get_passport_by_series(self, passport_series: str) -> Optional[Passport]:
        pass

    @abstractmethod
    def get_passport_by_series_and_number(self, series: str, number: str) -> Optional[Passport]:
        pass

    @abstractmethod
    def update_passport(self, user: Passport) -> Passport:
        pass

    @abstractmethod
    def delete_passport(self, user_id: PassportID) -> bool:
        pass