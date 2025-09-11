from sqlalchemy import  Column, Integer, String, Date
from src.infrastructure.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    phone_number = Column(String, index=True)
    birth_date = Column(Date)
    passport = Column(String, unique=True)
