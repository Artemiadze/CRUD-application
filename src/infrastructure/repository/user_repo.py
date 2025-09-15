from sqlalchemy.orm import Session
from src.domain.users import User
from src.infrastructure.models.users import UserModel
from src.domain.interfaces.iuser_repo import IUserRepository
from src.core.logger import main_logger

class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, obj: UserModel) -> User:
        return User(
            id=obj.id,
            full_name=obj.full_name,
            phone_number=obj.phone_number,
            birth_date=obj.birth_date,
            passport=obj.passport
        )

    def create_user(self, user: User):
        main_logger.debug(f"[UserRepository.create_user] DB: inserting user {user.full_name}")
        try:
            obj = UserModel(**user.__dict__)
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            main_logger.info(f"[UserRepository.create_user] DB: user created with id={obj.id}")
            return self._to_domain(obj)
        except Exception as e:
            main_logger.error(f"[UserRepository.create_user] DB error while creating user {user.full_name}: {e}")
            self.db.rollback()
            raise

    def get_user(self, user_id: int):
        main_logger.debug(f"[UserRepository.get_user] DB: fetching user with id={user_id}")
        obj = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if obj:
            return self._to_domain(obj)
        return None

    def get_user_by_name(self, full_name: str):
        main_logger.debug(f"[UserRepository.get_user_by_name] DB: fetching user with name={full_name}")
        obj = self.db.query(UserModel).filter(UserModel.full_name == full_name).first()
        if obj:
            return self._to_domain(obj)
        return None
    
    def get_user_by_phone(self, phone_number: str):
        main_logger.debug(f"[UserRepository.get_user_by_phone] DB: fetching user with phone_number={phone_number}")
        obj = self.db.query(UserModel).filter(UserModel.phone_number == phone_number).first()
        if obj:
            return self._to_domain(obj)
        return None

    def get_user_by_passport(self, passport: str):
        main_logger.debug(f"[UserRepository.get_user_by_passport] DB: fetching user with passport={passport}")
        obj = self.db.query(UserModel).filter(UserModel.passport == passport).first()
        if obj:
            return self._to_domain(obj)
        return None

    def update(self, user: User) -> User:
        main_logger.debug(f"[UserRepository.update] DB: updating user id={user.id}")
        obj = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not obj:
            main_logger.warning(f"[UserRepository.update] DB: user with id={user.id} not found for update")
            return None
        
        # Update only provided fields
        if user.full_name is not None:
            obj.full_name = user.full_name
        if user.phone_number is not None:
            obj.phone_number = user.phone_number
        if user.birth_date is not None:
            obj.birth_date = user.birth_date
        if user.passport is not None:
            obj.passport = user.passport

        self.db.commit()
        self.db.refresh(obj)
        main_logger.info(f"[UserRepository.update] DB: user id={obj.id}, updated")
        return self._to_domain(obj)

    def delete_user(self, user_id: int):
        main_logger.debug(f"[UserRepository.delete_user] DB: deleting user id={user_id}")
        obj = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not obj:
            main_logger.warning(f"[UserRepository.delete_user] DB: user with id={user_id} not found for delete")
            return None
        self.db.delete(obj)
        self.db.commit()
        main_logger.info(f"[UserRepository.delete_user] DB: user with id={user_id} deleted")
        return True