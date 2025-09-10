from sqlalchemy.orm import Session
import app.models, app.schema

# CRUD operations for working with Users table
def create_user(db: Session, user: app.schema.UsersCreate):
    db_user = app.models.Users(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(app.models.Users).filter(app.models.Users.id == user_id).first()

def get_user_by_name(db: Session, full_name: str):
    return db.query(app.models.Users).filter(app.models.Users.full_name == full_name).first()

def update_user(db: Session, user_id: int, user_updated: app.schema.UsersUpdate):
    user = get_user(db, user_id)
    if not user:
        return None
    update_data = user_updated.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return True