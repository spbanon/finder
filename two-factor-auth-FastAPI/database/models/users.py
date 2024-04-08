from database.base_class import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    profiles = relationship("UserProfile", back_populates="user")
    
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    interests = Column(String, nullable=True)
    description = Column(String, nullable=True)
    photo_path = Column(String, nullable=True)  # Путь к фотографии в файловой системе

    user_id = Column(Integer, ForeignKey("user.id"))  # Ссылка на пользователя

    user = relationship("User", back_populates="profiles")