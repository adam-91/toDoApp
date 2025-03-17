from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from starlette import status
from pydantic import BaseModel, Field
from jose import jwt, JWTError

from ..models import Users
from ..database import SessionLocal

router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)

SECRET_KEY = '3b6cg7fcv43657vn8c7h6chj47loidfpsqmfdvbgf521zbbvto092hb6' 
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl = 'auth/token')


class CreateUserRequest(BaseModel):
    login: str = Field(min_length=3)
    email: str
    name: str
    second_name: str
    surname: str
    password: str
    phone: str = Field(min_length=9)

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="TodoApp/templates")

###########
## Pages ##
###########

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

###########
### API ###
###########

def authenticate_user(login: str, password: str, db):
    user = db.query(Users).filter(Users.login == login).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(login: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': login, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get('sub')
        user_id: int = payload.get('id')

        if login is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return {'login': login, 'user_id': user_id}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

@router.post('/',status_code = status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    try:

        existUser = db.query(Users).filter((Users.login == create_user_request.login) | (Users.email==create_user_request.email)).first()

        if existUser:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with this email or login exost in the system')
        
        create_user_model = Users(
            login = create_user_request.login,
            email = create_user_request.email,
            name =  create_user_request.name,
            second_name = create_user_request.second_name,
            surname = create_user_request.surname,
            hashed_password = bcrypt_context.hash(create_user_request.password),
            phone = create_user_request.phone,
            creation_date = datetime.now(timezone.utc),
            active = True
        )
    
        db.add(create_user_model)
        db.commit()

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong request data')

@router.post('/token', response_model=Token)
async def login_for_acess_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                                db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user ')
        
    token = create_access_token(user.login, user.id, timedelta(minutes=5))
    return {'access_token': token, 'token_type': 'bearer'}
