from src.domain.users import User, DomainValidationError
from src.infrastructure.repository.user_repo import UserRepository
from src.schemas.user_schema import UsersUpdate
from src.domain.interfaces.iuser_repo import IUserRepository

class UserService:
    def __init__(self, repo: IUserRepository):
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
    
    def update_user(self, user_id: int, user_updated: UsersUpdate):
        # Получаем существующего пользователя
        existing_user = self.repo.get_user(user_id)
        if not existing_user:
            return None

        # Проверяем уникальность полей, если они обновляются
        if user_updated.full_name and user_updated.full_name != existing_user.full_name:
            if self.repo.get_user_by_name(user_updated.full_name):
                raise DomainValidationError("The name is already taken")

        if user_updated.phone_number and user_updated.phone_number != existing_user.phone_number:
            if self.repo.get_user_by_phone(user_updated.phone_number):
                raise DomainValidationError("The phone number is already taken")

        if user_updated.passport and user_updated.passport != existing_user.passport:
            if self.repo.get_user_by_passport(user_updated.passport):
                raise DomainValidationError("The passport is already taken")

        # Обновляем только те поля, которые пришли в UsersUpdate
        updated_user = User(
            id=user_id,
            full_name=user_updated.full_name or existing_user.full_name,
            phone_number=user_updated.phone_number or existing_user.phone_number,
            birth_date=user_updated.birth_date or existing_user.birth_date,
            passport=user_updated.passport or existing_user.passport
        )

        return self.repo.update(updated_user)
    
    def delete_user(self, user_id: int):
        user = self.repo.get_user(user_id)
        if not user:
            return None
        return self.repo.delete_user(user_id)
