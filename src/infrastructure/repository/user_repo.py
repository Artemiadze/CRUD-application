from sqlalchemy.orm import Session, joinedload
import uuid

from src.domain.users import User
from src.domain.identifiers  import UserId
from src.infrastructure.models.users import UserModel
from src.domain.interfaces.iuser_repo import IUserRepository
from src.core.logger import get_logger

class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, obj: UserModel) -> User:
        return User(
            id=UserId(uuid.UUID(obj.id)), # Convert string ID back to UUID for domain model
            first_name=obj.first_name,
            last_name=obj.last_name,
            patronymic=obj.patronymic,
            phone_number=obj.phone_number
        )

    def create_user(self, user: User) -> User:
        logger = get_logger()
        log_message = str(user.first_name) + ", " + str(user.last_name) + ", " + str(user.patronymic)
        logger.debug(f"[UserRepository.create_user] DB: inserting user {log_message}")

        try:
            # Convert User domain model to UserModel ORM instance
            user_dict = {key: value for key, value in user.__dict__.items() if key != 'id' or value is not None}
            obj = UserModel(**user_dict)

            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            logger.info(f"[UserRepository.create_user] DB: user created with id={obj.id}")
            return self._to_domain(obj)
        except Exception as e:
            logger.error(f"[UserRepository.create_user] DB error while creating user {log_message.strip()}: {e}")
            self.db.rollback()
            raise

    def get_user(self, user_id: UserId) -> User | None:
        str_id = str(user_id)

        logger = get_logger()
        logger.debug(f"[UserRepository.get_user] DB: fetching user with id={str_id}")

        obj = self.db.query(UserModel).options(joinedload(UserModel.passports)).filter(UserModel.id == str_id).first()

        if obj:
            return self._to_domain(obj)
        return None

    def get_user_by_full_name(self, first_name: str | None = None,
        last_name: str | None = None,
        patronymic: str | None = None)  -> list[User]:

        logger = get_logger()
        log_message = str(first_name) + ", " + str(last_name) + ", " + str(patronymic)
        logger.debug(f"[UserRepository.get_user_by_name] DB: fetching user with name={log_message.strip()}")

        query = self.db.query(UserModel)

        if first_name:
            query = query.options(joinedload(UserModel.passports)).filter(UserModel.first_name == first_name)
        if last_name:
            query = query.options(joinedload(UserModel.passports)).filter(UserModel.last_name == last_name)
        if patronymic:
            query = query.options(joinedload(UserModel.passports)).filter(UserModel.patronymic == patronymic)

        objs = query.all()
        return [self._to_domain(obj) for obj in objs]
    
    def get_user_by_phone(self, phone_number: str) -> User | None:
        logger = get_logger()
        logger.debug(f"[UserRepository.get_user_by_phone] DB: fetching user with phone_number={phone_number}")

        obj = self.db.query(UserModel).options(joinedload(UserModel.passports)).filter(UserModel.phone_number == phone_number).first()
        if obj:
            return self._to_domain(obj)
        return None

    def update_user(self, user: User) -> User:
        str_id = str(user.id)

        logger = get_logger()
        logger.debug(f"[UserRepository.update] DB: updating user id={str_id}")
        
        obj = self.db.query(UserModel).options(joinedload(UserModel.passports))\
                    .filter(UserModel.id == str_id).first()
        if not obj:
            logger.warning(f"[UserRepository.update] DB: user with id={str_id} not found for update")
            return None

        # Update user fields if provided
        for field in ["first_name", "last_name", "patronymic", "phone_number"]:
            # From domain model, only update if value is not None
            value = getattr(user, field, None)
            if value is not None:
                setattr(obj, field, value)

        self.db.commit()
        self.db.refresh(obj)
        logger.info(f"[UserRepository.update] DB: user id={str(obj.id)}, updated")
        return self._to_domain(obj)

    def delete_user(self, user_id: UserId) -> bool | None:
        str_id = str(user_id)
        logger = get_logger()
        logger.debug(f"[UserRepository.delete_user] DB: deleting user id={str_id}")

        obj = self.db.query(UserModel).filter(UserModel.id == str_id).first()
        if not obj:
            logger.warning(f"[UserRepository.delete_user] DB: user with id={str_id} not found for delete")
            return None
        
        self.db.delete(obj)
        self.db.commit()
        logger.info(f"[UserRepository.delete_user] DB: user with id={str_id} deleted")
        return True