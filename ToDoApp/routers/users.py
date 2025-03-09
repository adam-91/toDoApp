from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from passlib.context import CryptContext
import re

from ..database import SessionLocal
from ..models import Users
from .auth import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class PasswordVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

def valid_email_format(email: str):
    regex = r'\b[a-z0-9._?%+-]+@[a-z0-9.-]+.[a-z]{2,7}\b'

    if re.fullmatch(regex, email.lower()):
        return True
    else:
        return False

###########
### API ###
###########

@router.get('/', status_code = status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, 
                          db: db_dependency, 
                          password_verification: PasswordVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    if user_model is None:
        raise HTTPException(status_code=404, detail='Error on password change')
    
    if not bcrypt_context.verify(password_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    
    user_model.hashed_password = bcrypt_context.hash(password_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put('/name/{name}', status_code=status.HTTP_204_NO_CONTENT)
async def change_user_name(user: user_dependency, 
                          db: db_dependency, 
                          name: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.name = name
    db.add(user_model)
    db.commit()
    
@router.put('/second_name/{second_name}',status_code=status.HTTP_204_NO_CONTENT)
async def change_user_second_name(user: user_dependency, 
                          db: db_dependency, 
                          second_name: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.second_name = second_name
    db.add(user_model)
    db.commit()

@router.put('/surname/{surname}',status_code=status.HTTP_204_NO_CONTENT)
async def change_user_surname(user: user_dependency, 
                          db: db_dependency, 
                          surname: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.surname = surname
    db.add(user_model)
    db.commit()

@router.put('/email/{email}',status_code=status.HTTP_204_NO_CONTENT)
async def change_user_email(user: user_dependency, 
                          db: db_dependency, 
                          email: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    if not valid_email_format(email):
        raise HTTPException(status_code=400, detail='Email veryfication faild')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=400, detail='Email veryfication faild')

    user_model.email = email
    db.add(user_model)
    db.commit()

@router.put('/phone/{phone}',status_code=status.HTTP_204_NO_CONTENT)
async def change_user_phone(user: user_dependency, 
                          db: db_dependency, 
                          phone: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    #if not valid_email_format(phone):
    #    raise HTTPException(status_code=401, detail='Phone veryfication faild')
       
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.phone = phone
    db.add(user_model)
    db.commit()

