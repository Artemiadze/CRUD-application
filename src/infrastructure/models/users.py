from sqlalchemy import  Column, String, Date
from uuid import uuid4

from src.infrastructure.database import Base

class UserModel(Base):
    __tablename__ = "users"

    # Generated ID as a string to store UUID
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    patronymic = Column(String, index=True)
    phone_number = Column(String, index=True)
    birth_date = Column(Date)
    passport_number = Column(String(6), nullable=False, unique=True)
    passport_series = Column(String(4), nullable=False)
