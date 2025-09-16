from sqlalchemy import  Column, Integer, String, Date
from src.infrastructure.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    patronymic = Column(String, index=True)
    phone_number = Column(String, index=True)
    birth_date = Column(Date)
    passport_number = Column(String(6), nullable=False, unique=True)
    passport_series = Column(String(4), nullable=False)
