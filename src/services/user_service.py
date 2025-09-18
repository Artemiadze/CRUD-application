from src.domain.users import User
from src.domain.passport import Passport
from src.domain.identifiers import UserId
from src.schemas.user_schema import UsersUpdate
from src.schemas.passport_schema import PassportUpdate
from src.utils.exceptions import DuplicateError, NotFoundError
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
    
    def update_user(self, user_id: UserId, user_data: UsersUpdate, passport_data: PassportUpdate | None = None) -> User:

        # Get existing user
        existing_user = self.user_repo.get_user(user_id)
        if not existing_user:
            raise NotFoundError("User", user_id)

        # Check for duplicates
        first_name = user_data.first_name or existing_user.first_name
        last_name = user_data.last_name or existing_user.last_name
        patronymic = user_data.patronymic or existing_user.patronymic
        if (first_name != existing_user.first_name 
            or last_name != existing_user.last_name 
            or patronymic != existing_user.patronymic):
            if self.user_repo.get_user_by_full_name(first_name, last_name, patronymic):
                raise DuplicateError(
                    "full_name",
                    f"{last_name} {first_name} {patronymic or ''}".strip()
                )

        phone_number = user_data.phone_number or existing_user.phone_number
        if phone_number != existing_user.phone_number:
            if self.user_repo.get_user_by_phone(phone_number):
                raise DuplicateError("phone_number", phone_number)

        # Update user
        updated_user = self.user_repo.update_user(
            User(
                id=user_id,
                first_name=user_data.first_name or existing_user.first_name,
                last_name=user_data.last_name or existing_user.last_name,
                patronymic=user_data.patronymic or existing_user.patronymic,
                phone_number=phone_number
            )
        )

        # Update or create passport if exist
        if passport_data:
            existing_passport = self.passport_repo.get_passport_by_series_and_number(
                passport_data.passport_series,
                passport_data.passport_number
            )

            passport_domain = Passport(
                id=existing_passport.id if existing_passport else None,
                birth_date=passport_data.birth_date,
                passport_series=passport_data.passport_series,
                passport_number=passport_data.passport_number,
                receipt_date=passport_data.receipt_date,
                user_id=updated_user.id,
            )

            if existing_passport:
                self.passport_repo.update_passport(passport_domain)
            else:
                self.passport_repo.create_passport(passport_domain)

        return updated_user

    
    def delete_user(self, user_id: UserId) -> bool:
        existing_user = self.repo.get_user(user_id)
        if not existing_user:
            raise NotFoundError("User", user_id)

        # Deletion users and hit data in passport (using cascade)
        return self.repo.delete_user(user_id)