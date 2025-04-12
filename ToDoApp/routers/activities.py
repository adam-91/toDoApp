from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Path, Request
from fastapi.templating import Jinja2Templates
from starlette import status
from pydantic import BaseModel, Field

from ..models import Activities, Categories, Types
from ..database import SessionLocal
from .auth import get_current_user
from .utils import redirect_to_login

router = APIRouter(
    prefix = '/activities',
    tags = ['activities']
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
class ActivitiesRequest(BaseModel):
    name: str = Field(min_length=3)
    description: str = Field(min_length=3)
    priority: int = Field(gt=0,lt=11)
    progress: int = Field(gt=-1,lt=101)
    active: bool


###########
## Pages ##
###########

@router.get('/activity-page')
async def render_activities_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()
        
        activities = db.query(Activities).filter(Activities.user_id == user.get("id")).all()
        return templates.TemplateResponse("activities.html", {"request": request, "user": user, "activities": activities})

    except:
        return redirect_to_login()
    
@router.get('/add-page')
async def render_activities_add_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        
        if user is None:
            return redirect_to_login()
        
        types = db.query(Types).filter(Types.active == True).all()
        categories = db.query(Categories).filter(Categories.active == True).all()
        return templates.TemplateResponse("add-activities.html", {"request": request, "user": user, "types": types, "categories": categories})

    except:
        return redirect_to_login()

###########
### API ###
###########

@router.get('/', status_code = status.HTTP_200_OK)
async def read_all_activities(user: user_dependency,
                              db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Faild')
    
    return db.query(Activities).filter(Activities.user_id == user.get('id')).all()

@router.get('/activity/{activity_id}', status_code = status.HTTP_200_OK)
async def read_activity(user: user_dependency,
                        db: db_dependency, 
                        activity_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Faild')
    
    activities_model =  db.query(Activities).filter(Activities.id == activity_id)\
    .filter(Activities.user_id == user.get('id')).first()
    
    if activities_model is not None:
        return activities_model
    raise HTTPException(status_code=404, detail='Activity not found')

@router.post('/activity', status_code=status.HTTP_201_CREATED)
async def create_activity(user: user_dependency,
                          db: db_dependency, 
                          activities_request: ActivitiesRequest):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Faild')
    activities_model = Activities(**activities_request.model_dump(), user_id = user.get('id'))

    db.add(activities_model)
    db.commit()

@router.put('/activity/{activity_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_activity(user: user_dependency,
                          db: db_dependency, 
                          activities_request: ActivitiesRequest,
                          activity_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Faild')
    
    activities_model =  db.query(Activities).filter(Activities.id == activity_id)\
        .filter(Activities.user_id == user.get('id')).first()
    
    if activities_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Activity not found')
       
    activities_model.name = activities_request.name
    activities_model.description = activities_request.description
    activities_model.priority = activities_request.priority
    activities_model.progress = activities_request.progress
    activities_model.active = activities_request.active 

    db.add(activities_model)
    db.commit()

@router.delete('/activity/{activity_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_actvity(user: user_dependency,
                         db: db_dependency, 
                         activity_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Faild')
    
    actvity_model = db.query(Activities).filter(Activities.id == activity_id)\
        .filter(Activities.user_id == user.get('id')).first()

    if actvity_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Activity not found')
    
    db.query(Activities).filter(Activities.id == activity_id).delete() 
    db.commit()
