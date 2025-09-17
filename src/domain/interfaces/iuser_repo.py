from abc import ABC, abstractmethod
from typing import Optional
from src.domain.users import User, UserId

class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user(self, user_id: UserId) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_full_name(self, first_name: str | None = None,
        last_name: str | None = None,
        patronymic: str | None = None) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_phone(self, phone_number: str) -> Optional[User]:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: UserId) -> bool:
        pass
