from src.domain.users import User, DomainValidationError
from src.infrastructure.repository.user_repo import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, user: User):
        if self.repo.get_user_by_name(user.full_name):
            raise DomainValidationError("The name is already taken")
        if self.repo.get_user_by_phone(user.phone_number):
            raise DomainValidationError("The phone number is already taken")
        if self.repo.get_user_by_passport(user.passport):
            raise DomainValidationError("The passport is already taken")
        
        return self.repo.create_user(user)
    
    def get_user(self, user_id: int):
        return self.repo.get_user(user_id)
    
    def get_user_by_name(self, full_name: str):
        return self.repo.get_user_by_name(full_name)
    
    def update_user(self, user: User):        
        updated_user = self.repo.get_user(user.id)
        if not updated_user:
            return None
        
        if user.full_name and user.full_name != updated_user.full_name:
            if self.repo.get_user_by_name(user.full_name):
                raise DomainValidationError("The name is already taken")
        
        if user.phone_number and user.phone_number != updated_user.phone_number:
            if self.repo.get_user_by_phone(user.phone_number):
                raise DomainValidationError("The phone number is already taken")
        
        if user.passport and user.passport != updated_user.passport:
            if self.repo.get_user_by_passport(user.passport):
                raise DomainValidationError("The passport is already taken")
        
        return self.repo.update(user)
    
    def delete_user(self, user_id: int):
        user = self.repo.get_user(user_id)
        if not user:
            return None
        return self.repo.delete(user_id)
