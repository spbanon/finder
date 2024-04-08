from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    secret: str
    
class UserCreateProfile(BaseModel):
    username: str
    age: int
    gender: str
    interests: str
    description: str
    photo_path: str
    user_mail: str

class ShowUser(BaseModel):
    email: str

    class Config: 
        orm_mode = True