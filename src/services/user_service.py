from src.domain.users import User
from src.core.exceptions import DuplicateError, NotFoundError
from src.domain.interfaces.iuser_repo import IUserRepository

class UserService:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def create_user(self, user: User):
        if self.repo.get_user_by_name(user.full_name):
            raise DuplicateError("full_name", user.full_name)
        if self.repo.get_user_by_phone(user.phone_number):
            raise DuplicateError("phone_number", user.phone_number)
        if self.repo.get_user_by_passport(user.passport):
            raise DuplicateError("passport", user.passport)
        
        return self.repo.create_user(user)
    
    def get_user(self, user_id: int):
        user = self.repo.get_user(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return user
    
    def get_user_by_name(self, full_name: str):
        user = self.repo.get_user_by_name(full_name)
        if not user:
            raise NotFoundError("User", full_name)
        return user
    
    def update_user(self, user: User) -> User:
        existing_user = self.repo.get_user(user.id)
        if not existing_user:
            raise NotFoundError("User", user.id)

        if user.full_name and user.full_name != existing_user.full_name:
            if self.repo.get_user_by_name(user.full_name):
                raise DuplicateError("full_name", user.full_name)

        if user.phone_number and user.phone_number != existing_user.phone_number:
            if self.repo.get_user_by_phone(user.phone_number):
                raise DuplicateError("phone_number", user.phone_number)

        if user.passport and user.passport != existing_user.passport:
            if self.repo.get_user_by_passport(user.passport):
                raise DuplicateError("passport", user.passport)

        return self.repo.update(user)

    
    def delete_user(self, user_id: int):
        user = self.repo.get_user(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return self.repo.delete_user(user_id)
