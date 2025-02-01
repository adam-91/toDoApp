import models as models
from fastapi import FastAPI
from database import engine
from rourers import activities, auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(activities.router)
app.include_router(auth.router)
