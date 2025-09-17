from sqlalchemy import  Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4

from src.infrastructure.database import Base

class PassportModel(Base):
    __tablename__ = "passport"

    # Generated ID as a string to store UUID
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    birth_date = Column(Date)
    passport_number = Column(String(6), nullable=False, unique=True)
    passport_series = Column(String(4), nullable=False)
    receipt_date = Column(Date)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    user = relationship("UserModel", back_populates="passports")