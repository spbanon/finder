from core.config import settings
from database.base import Base
from database.session import engine
from database.utils import check_db_connected
from database.utils import check_db_disconnected
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database.models.users import User,UserProfile
from typing import List
from webapps.base import api_router as web_app_router
import uuid
from database.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from webapps.login.route_login import last_mail
from clip_api import ClipPipeline
from database.repository.users import get_user_id_by_email, if_profile_exists,get_name_by_id,get_age_by_id,get_interests_by_id,get_description_by_id
import os
def wrapper(func):
    def wrap(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except Exception as e:
            return e
    return wrap


def include_router(app):
    app.include_router(web_app_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    create_tables()
    return app


app = start_application()


@app.on_event("startup")
async def app_startup():
    await check_db_connected()


@app.on_event("shutdown")
async def app_shutdown():
    await check_db_disconnected()
from PIL import Image   
@wrapper
@app.post("/save-profile/")
async def save_profile(
    email: str = Form(...),
    username: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    interests: str = Form(None),
    description: str = Form(None),
    photo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    id = get_user_id_by_email(email=email,db=db)
    if photo:
        if os.path.exists(f'./storage/{id}.jpeg'):
            os.remove(f'./storage/{id}.jpeg')
        name = uuid.uuid4()
        with open(f'./storage/{name}.jpeg', "wb") as buffer:
            buffer.write(photo.file.read())
            with Image.open(f'./storage/{name}.jpeg') as img:
                resized_img = img.resize((200, 200))
                with open(f'./storage/{id}.jpeg', 'wb') as f:
                    resized_img.save(f)
        os.remove(f'./storage/{name}.jpeg')
    
    print(f'id == {id}, mail == {email}')
    #description = get_description_by_id(id,db)
    profile = UserProfile(
        username=username,
        age=age,
        gender=gender,
        interests=interests,
        description=description,
        photo_path=f'./storage/{name}',
        user_id = id
    )
    exists = if_profile_exists(id=id,db=db)
    if not exists:
        db.add(profile)
        db.commit()
        db.refresh(profile)
    else:
        profile_new = db.query(UserProfile).filter(UserProfile.user_id == id).first()
        setattr(profile_new, 'username', username)
        setattr(profile_new, 'age', age)
        setattr(profile_new, 'gender', gender)
        setattr(profile_new, 'interests', interests)
        setattr(profile_new, 'description', description)
        setattr(profile_new, 'photo_path', f'./storage/{name}')
        db.merge(profile_new)

        db.commit()
        


    return {"message": "Профиль успешно сохранен!"}

app.mount("/storage", StaticFiles(directory="/Users/kirillcadaev/Desktop/123/two-factor-auth-FastAPI/storage/"), name="storage")
from fastapi import Query
@app.post("/photos")
async def get_photos(email: str = Form(...), db: Session = Depends(get_db)):
    print(email)
    id = get_user_id_by_email(email=email,db=db)
    print(id)
    photo_data = {}
    description = get_description_by_id(id,db=db)
    print(description)
    if description == None or len(description) < 4:
        files = os.listdir('/Users/kirillcadaev/Desktop/123/two-factor-auth-FastAPI/storage/')
        for file in files:
            id = int (file[:-5])
            name = get_name_by_id(id,db=db)
            age = get_age_by_id(id,db=db)
            about = get_interests_by_id(id,db)
            photo_data[file] = {'url': file, 'text': f'Меня зовут {name}, мне {age}.\n {about}'}
            
    else:
        clip = ClipPipeline()
        res = clip('/Users/kirillcadaev/Desktop/123/two-factor-auth-FastAPI/storage/',description)
        if res != None:
            print(res)
            for elements in res.keys():
                id = int (elements[:-5])
                name = get_name_by_id(id,db=db)
                age = get_age_by_id(id,db=db)
                about = get_interests_by_id(id,db)
                photo_data[elements] = {'url': elements, 'text': f'Меня зовут {name}, мне {age}.\n {about}'}
        else:
            print('unlucky')
    
    
    return photo_data

