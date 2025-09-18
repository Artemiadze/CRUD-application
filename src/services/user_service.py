from src.domain.users import User, UserId
from src.domain.passport import Passport, PassportID
from src.core.exceptions import DuplicateError, NotFoundError
from src.domain.interfaces.ipassport_repo import IPassportRepository
from src.domain.interfaces.iuser_repo import IUserRepository

class UserService:
    def __init__(self, user_repo: IUserRepository, passport_repo: IPassportRepository):
        self.user_repo = user_repo
        self.passport_repo = passport_repo

    def create_user(self, user: User, passport: Passport | None = None) -> User:
        # Check for duplicates
        if self.user_repo.get_user_by_full_name(
            user.first_name, user.last_name, user.patronymic
        ):
            raise DuplicateError(
                "full_name",
                f"{user.last_name} {user.first_name} {user.patronymic or ''}".strip()
            )

        if self.user_repo.get_user_by_phone(user.phone_number):
            raise DuplicateError("phone_number", user.phone_number)

        # Create user object
        created_user = self.user_repo.create_user(user)

        # Create him passport if exist
        if passport:
            passport.user_id = created_user.id
            self.passport_repo.create_passport(passport)

        return created_user
    
    def get_user(self, user_id: UserId) -> User:
        user = self.user_repo.get_user(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return user
    
    def get_user_by_full_name(self, first_name: str | None = None,
        last_name: str | None = None,
        patronymic: str | None = None):
        user = self.user_repo.get_user_by_full_name(first_name, last_name, patronymic)
        if not user:
            log_message = str(first_name) + ", " + str(last_name) + ", " + str(patronymic)
            raise NotFoundError("User", log_message.strip())
        return user
    
    def update_user(self, user: User, passport: Passport | None = None) -> User:
        existing_user = self.user_repo.get_user(user.id)
        if not existing_user:
            raise NotFoundError("User", user.id)

        if (
            (user.first_name and user.first_name != existing_user.first_name)
            or (user.last_name and user.last_name != existing_user.last_name)
            or (user.patronymic and user.patronymic != existing_user.patronymic)
        ):
            if self.user_repo.get_user_by_full_name(
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
            if self.user_repo.get_user_by_phone(user.phone_number):
                raise DuplicateError("phone_number", user.phone_number)

        # Update user
        updated_user = self.user_repo.update_user(user)

        # Check passport' data  if exist
        if passport:
            existing_passport = self.passport_repo.get_passport_by_series_and_number(
                passport.passport_series, passport.passport_number
            )
            if existing_passport:
                # Updating
                passport.id = existing_passport.id
                passport.user_id = updated_user.id
                self.passport_repo.update_passport(passport)
            else:
                # Create new passport object if it didn't exist before
                passport.user_id = updated_user.id
                self.passport_repo.create_passport(passport)

        return updated_user

    
    def delete_user(self, user_id: UserId) -> bool:
        existing_user = self.repo.get_user(user_id)
        if not existing_user:
            raise NotFoundError("User", user_id)

        # Deletion users and hit data in passport (using cascade)
        return self.repo.delete_user(user_id)