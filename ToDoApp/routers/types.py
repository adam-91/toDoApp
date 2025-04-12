from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from starlette import status
from pydantic import BaseModel, Field

from ..models import Types, Activities
from ..database import SessionLocal
from .auth import get_current_user
from .utils import redirect_to_login

router = APIRouter(
    prefix='/types',
    tags=['types']
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

templates = Jinja2Templates(directory="ToDoApp/templates")

class TypeRequest(BaseModel):
    name: str = Field(min_length=3)
    description: str = Field(min_length=3)
    active: bool

###########
## Pages ##
###########

@router.get('/add-page')
async def render_types_add_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()
        
        types = db.query(Types).filter(Types.active == True).all()
        return templates.TemplateResponse("add-types.html", {"request": request, "user": user, "types": types})

    except:
        return redirect_to_login()

###########
### API ###
###########

@router.get('/', status_code = status.HTTP_200_OK)
async def get_types(db: db_dependency):
    return db.query(Types).all()

@router.get('/{type_id}', status_code = status.HTTP_200_OK)
async def get_types(db: db_dependency, type_id: int):
    type =  db.query(Types).filter(Types.id == type_id).first()

    if type is None:
        raise HTTPException(status_code=404, detail='Type not found.')
    return type

@router.post('/', status_code = status.HTTP_204_NO_CONTENT)
async def create_type(db: db_dependency,
                      user: user_dependency,
                      type_request: TypeRequest):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    type_model = Types(**type_request.model_dump())

    db.add(type_model)
    db.commit()


@router.put('/{type_id}', status_code = status.HTTP_204_NO_CONTENT)
async def update_type(db: db_dependency,
                      user: user_dependency,
                      type_id: int,
                      type_request: TypeRequest):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    type_model = db.query(Types).filter(Types.id == type_id).first()

    if type_model is None:
         raise HTTPException(status_code=404, detail='Type not found')
    
                      
    type_model.name = type_request.name
    type_model.description = type_request.description
    type_model.active = type_request.active

    db.add(type_model)
    db.commit()

@router.delete('/{type_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_type(db: db_dependency,
                      user: user_dependency,
                      type_id: int):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    type_model = db.query(Types).filter(Types.id == type_id).first()

    if type_model is None:
         raise HTTPException(status_code=404, detail='Type not found')
    
    is_used = db.query(Activities).filter(Activities.type_id == type_id).filter(Activities.active == True).first()
    if is_used is not None:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail='Type is used by some activities')
    
    type_model.active = False
    
    db.add(type_model)
    db.commit()

