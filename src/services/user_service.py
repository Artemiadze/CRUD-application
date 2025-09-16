from src.domain.users import User
from src.core.exceptions import DuplicateError, NotFoundError
from src.domain.interfaces.iuser_repo import IUserRepository

class UserService:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def create_user(self, user: User):
        if self.repo.get_user_by_full_name(
            user.first_name, user.last_name, user.patronymic
        ):
            raise DuplicateError(
                "full_name",
                f"{user.last_name} {user.first_name} {user.patronymic}"
            )
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
    
    def get_user_by_full_name(self, first_name: str | None = None,
        last_name: str | None = None,
        patronymic: str | None = None):
        user = self.repo.get_user_by_full_name(first_name, last_name, patronymic)
        if not user:
            log_message = str(first_name) + ", " + str(last_name) + ", " + str(patronymic)
            raise NotFoundError("User", log_message.strip())
        return user
    
    def update_user(self, user: User) -> User:
        existing_user = self.repo.get_user(user.id)
        if not existing_user:
            raise NotFoundError("User", user.id)

        if (
            (user.first_name and user.first_name != existing_user.first_name)
            or (user.last_name and user.last_name != existing_user.last_name)
            or (user.patronymic and user.patronymic != existing_user.patronymic)
        ):
            if self.repo.get_user_by_full_name(
                user.first_name or existing_user.first_name,
                user.last_name or existing_user.last_name,
                user.patronymic or existing_user.patronymic,
            ):
                raise DuplicateError(
                    "full_name",
                    f"{user.last_name or existing_user.last_name} "
                    f"{user.first_name or existing_user.first_name} "
                    f"{user.patronymic or existing_user.patronymic or ''}"
                )
        if user.phone_number and user.phone_number != existing_user.phone_number:
            if self.repo.get_user_by_phone(user.phone_number):
                raise DuplicateError("phone_number", user.phone_number)

        if user.passport_number and user.passport_number != existing_user.passport_number:
            if self.repo.get_user_by_passport(user.passport_number):
                raise DuplicateError("passport_number", user.passport_number)
            
        if user.passport_series and user.passport_series != existing_user.passport_series:
            if self.repo.get_user_by_passport(user.passport_series):
                raise DuplicateError("passport_series", user.passport_series)

        return self.repo.update(user)

    
    def delete_user(self, user_id: int):
        user = self.repo.get_user(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return self.repo.delete_user(user_id)
