from sqlalchemy.orm import Session
from src.domain.users import User
from src.infrastructure.models.users import UserModel
from src.domain.interfaces.iuser_repo import IUserRepository

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

    def create_user(self, user):
        obj = UserModel(**user.__dict__)

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_domain(obj)

    def get_user(self, user_id: int):
        obj = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if obj:
            return self._to_domain(obj)
        return None

    def get_user_by_name(self, full_name: str):
        obj = self.db.query(UserModel).filter(UserModel.full_name == full_name).first()
        if obj:
            return self._to_domain(obj)
        return None
    
    def get_user_by_phone(self, phone_number: str):
        obj = self.db.query(UserModel).filter(UserModel.phone_number == phone_number).first()
        if obj:
            return self._to_domain(obj)
        return None

    def get_user_by_passport(self, passport: str):
        obj = self.db.query(UserModel).filter(UserModel.passport == passport).first()
        if obj:
            return self._to_domain(obj)
        return None

    def update(self, user: User) -> User:
        obj = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not obj:
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
        return self._to_domain(obj)

    def delete_user(self, user_id: int):
        obj = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not obj:
            return None
        self.db.delete(obj)
        self.db.commit()
        return True