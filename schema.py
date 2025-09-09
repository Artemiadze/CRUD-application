from pydantic import BaseModel, ConfigDict
from datetime import date

class UsersBase(BaseModel):
    model_config = ConfigDict(from_attributes=True) # to read data from ORM models
    full_name: str
    phone_number: str
    birth_date: date
    passport: str

class UsersCreate(UsersBase):
    # ToDO
    pass

class UsersUpdate(UsersBase):
    # ToDO
    pass

class UsersOut(UsersBase):
    id: int