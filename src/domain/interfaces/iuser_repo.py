from abc import ABC, abstractmethod
from typing import Optional
from src.domain.users import User

class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_name(self, full_name: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_phone(self, phone_number: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_passport(self, passport: str) -> Optional[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass
