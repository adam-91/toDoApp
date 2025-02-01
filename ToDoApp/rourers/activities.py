
from models import Activities
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Path
from database import SessionLocal
from starlette import status
from pydantic import BaseModel, Field

router = APIRouter()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]

class ActivitiesRequest(BaseModel):
    name: str = Field(min_length=3)
    description: str = Field(min_length=3)
    priority: int = Field(gt=0,lt=11)
    progress: int = Field(gt=-1,lt=101)
    active: bool

@router.get('/', status_code = status.HTTP_200_OK)
async def read_all_activities(db: db_dependancy):
    return db.query(Activities).all()

@router.get('/activity/{activity_id}', status_code = status.HTTP_200_OK)
async def read_activity(db: db_dependancy, activity_id: int = Path(gt=0)):
    activities_model =  db.query(Activities).filter(Activities.id == activity_id).first()
    if activities_model is not None:
        return activities_model
    raise HTTPException(status_code=404, detail='Activity not found')


@router.post('/activity', status_code=status.HTTP_201_CREATED)
async def create_activity(db: db_dependancy, activities_request: ActivitiesRequest):
    activities_model = Activities(**activities_request.model_dump())

    db.add(activities_model)
    db.commit()

@router.put('/activity/{activity_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_activity(db: db_dependancy, 
                          activities_request: ActivitiesRequest,
                          activity_id: int = Path(gt=0)):
    
    activities_model =  db.query(Activities).filter(Activities.id == activity_id).first()
    if activities_model is None:
        raise HTTPException(status_code=404, detail='Activity not found')
    
    activities_model = Activities(**activities_request.model_dump())
      
    activities_model.name = activities_request.name
    activities_model.description = activities_request.description
    activities_model.priority = activities_request.priority
    activities_model.progress = activities_request.progress
    activities_model.active = activities_request.active 

    #db.query(Activities).filter(Activities.id == activity_id).update(activities_model) 
    #Activities.update().where(Activities.id == activity_id).values(name = activities_request.name,
    #description = activities_request.description,
    #priority = activities_request.priority,
    #progress = activities_request.progress,
    #active = activities_request.active )
    db.add(activities_model)
    db.commit()

@router.delete('/activity/{actvity_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_actvity(db: db_dependancy, activity_id: int = Path(gt=0)):
    actvity_model = db.query(Activities).filter(Activities.id == activity_id).first()

    if actvity_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Actitivy not found')
    
    db.query(Activities).filter(Activities.id == activity_id).delete() 
    db.commit()
