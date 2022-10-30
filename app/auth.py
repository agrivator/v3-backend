# authentication routes
import sys
sys.path.append("/")

from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from dotenv import load_dotenv,find_dotenv
from server.database import engine, SessionLocal
from server import models
import os

load_dotenv(find_dotenv())

secret_key = os.getenv('SECRET_KEY')
algorithm = os.environ.get('ALGORITHM')



route = APIRouter()
models.Base.metadata.create_all(bind=engine)
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

# user model
class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    name: str
    password: str
    mobile: str

# functions
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# hash password
def get_hash_password(password):
    return bcrypt_context.hash(password)

# verify hashed password
def verify_hash_password(plain_password,hashed_password):
    return bcrypt_context.verify(plain_password,hashed_password)

# authenticate user
async def authenticate_user(username:str, password:str , db):
    user = db.query(models.User).filter(models.User.username==username).first()
    if not user:
        return False
    if not verify_hash_password(password,user.hashed_password):
        return False
    return True

# create access token
def create_access_token(username:str, user_id:int):
    encode = {"sub":username,"id":user_id}

    return jwt.encode(encode,secret_key,algorithm=algorithm)


# create user
@route.post("/create/user")
async def create_user(create_user: CreateUser, db: Session= Depends(get_db)):
    create_user_model = models.User()
    create_user_model.name=create_user.name
    create_user_model.username=create_user.username
    create_user_model.email=create_user.email
    create_user_model.hashed_password = get_hash_password(create_user.password)
    create_user_model.mobile=create_user.mobile
    create_user_model.role_id=1
    create_user_model.reg_at=datetime.now()
    create_user_model.last_login=datetime.now()
    create_user_model.is_active=True
    db.add(create_user_model)
    db.commit()
    return {"Status":"successful"}

# get token
@route.post("/token")
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(),
                                 db:Session=Depends(get_db)):
    user = authenticate_user(form_data.username,form_data.password,db)

    if not user:
        raise HTTPException(status_code=404,detail='User not found')

    user_det = db.query(models.User).filter(form_data.username==models.User.username).first()
    token =  create_access_token(username=user_det.username,user_id=user_det.id)
    return token