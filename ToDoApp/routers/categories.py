from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Path, Request
from fastapi.templating import Jinja2Templates
from starlette import status
from pydantic import BaseModel, Field

from ..models import Categories, Activities
from ..database import SessionLocal
from .auth import get_current_user
from .utils import redirect_to_login

router = APIRouter(
    prefix='/categories',
    tags=['categories']
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
class CategoriesRequest(BaseModel):
    name: str = Field(min_length=3)
    description: str = Field(min_length=3)
    level: int = Field(gt=0,lt=4)
    picture: str
    active: bool

###########
## Pages ##
###########

@router.get('/add-page')
async def render_categories_add_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()
        
        categories = db.query(Categories).filter(Categories.active == True).all()
        return templates.TemplateResponse("add-categories.html", {"request": request, "user": user, "categories": categories})

    except:
        return redirect_to_login()

###########
### API ###
###########

@router.get('/', status_code = status.HTTP_200_OK)
async def get_categories(db: db_dependency):
    return db.query(Categories).all()

@router.get('/{category_id}', status_code = status.HTTP_200_OK)
async def get_category(db: db_dependency,
                                    category_id: int = Path(gt=0)):
    category_model = db.query(Categories).filter(Categories.id == category_id).first()

    if category_model is not None:
        return category_model
    raise HTTPException(status_code=404, detail='Category not found')

@router.post('/', status_code = status.HTTP_204_NO_CONTENT)
async def create_category(db: db_dependency, 
                            user: user_dependency,
                            category: CategoriesRequest):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Faild')
    
    category_model = Categories(**category.model_dump())

    db.add(category_model)
    db.commit()

@router.put('/{category_id}', status_code = status.HTTP_204_NO_CONTENT)
async def change_acategories(user: user_dependency,
                             db: db_dependency,
                             category_request: CategoriesRequest,
                             category_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Faild')
    
    category_model = db.query(Categories).filter(Categories.id == category_id).first()

    if category_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    
    category_model.name = category_request.name
    category_model.description = category_request.description
    category_model.level = category_request.level
    category_model.picture = category_request.picture
    
    db.add(category_model)
    db.commit()
    return

@router.delete('/{category_id}', status_code = status.HTTP_204_NO_CONTENT)
async def change_acategories(db: db_dependency, 
                             user: user_dependency,
                             category_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Faild')
    
    category_model = db.query(Categories).filter(Categories.id == category_id).first()

    if category_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    
    is_used = db.query(Activities).filter(Activities.category_id == category_id).filter(Activities.active == True).first()

    if is_used is not None:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail='Category is used by some activities')
    
    category_model.active = False
    
    db.add(category_model)
    db.commit()
    return
