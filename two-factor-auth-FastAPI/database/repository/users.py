from core.hashing import Hasher
from database.models.users import User, UserProfile
from schemas.users import UserCreate
from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db: Session):
    user = User(
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        secret = user.secret
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user

def get_user_id_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user.id

def if_profile_exists(id: int, db: Session):
    exists = db.query(UserProfile).filter(UserProfile.user_id == id).first()
    if exists != None:
        return True
    return False

def get_name_by_id(id: int, db: Session):
    user = db.query(UserProfile).filter(UserProfile.id == id).first()
    if user != None:
        return user.username
    return None

def get_age_by_id(id: int, db: Session):
    user = db.query(UserProfile).filter(UserProfile.id == id).first()
    if user != None:
        return user.age
    return None

def get_interests_by_id(id: int, db: Session):
    user = db.query(UserProfile).filter(UserProfile.id == id).first()
    if user != None:
        return user.interests
    return None

def get_description_by_id(id: int, db: Session):
    user = db.query(UserProfile).filter(UserProfile.id == id).first()
    if user != None:
        return user.description
    return None