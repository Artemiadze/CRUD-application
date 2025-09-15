from sqlalchemy.orm import Session
from src.domain.users import User
from src.infrastructure.models.users import UserModel
from src.domain.interfaces.iuser_repo import IUserRepository
from src.core.config import logger

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
        logger.debug(f"DB: inserting user {user.full_name}")
        try:
            obj = UserModel(**user.__dict__)
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            logger.info(f"DB: user created with id={obj.id}")
            return self._to_domain(obj)
        except Exception as e:
            logger.error(f"DB error while creating user {user.full_name}: {e}")
            self.db.rollback()
            raise

    def get_user(self, user_id: int):
        logger.debug(f"DB: fetching user with id={user_id}")
        obj = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if obj:
            return self._to_domain(obj)
        return None

    def get_user_by_name(self, full_name: str):
        logger.debug(f"DB: fetching user with name={full_name}")
        obj = self.db.query(UserModel).filter(UserModel.full_name == full_name).first()
        if obj:
            return self._to_domain(obj)
        return None
    
    def get_user_by_phone(self, phone_number: str):
        logger.debug(f"DB: fetching user with phone_number={phone_number}")
        obj = self.db.query(UserModel).filter(UserModel.phone_number == phone_number).first()
        if obj:
            return self._to_domain(obj)
        return None

    def get_user_by_passport(self, passport: str):
        logger.debug(f"DB: fetching user with passport={passport}")
        obj = self.db.query(UserModel).filter(UserModel.passport == passport).first()
        if obj:
            return self._to_domain(obj)
        return None

    def update(self, user: User) -> User:
        logger.debug(f"DB: updating user id={user.id}")
        obj = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not obj:
            logger.warning(f"DB: user with id={user.id} not found for update")
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
        logger.info(f"DB: user id={obj.id}, updated")
        return self._to_domain(obj)

    def delete_user(self, user_id: int):
        logger.debug(f"DB: deleting user id={user_id}")
        obj = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not obj:
            logger.warning(f"DB: user with id={user_id} not found for delete")
            return None
        self.db.delete(obj)
        self.db.commit()
        logger.info(f"DB: user with id={user_id} deleted")
        return True