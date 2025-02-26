from fastapi import FastAPI

from .models import Base
from .database import engine
from .routers import activities, categories, auth, users

app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.get('/life')
def health_check():
    return {'status': 'alive'}

app.include_router(activities.router)
app.include_router(categories.router)
app.include_router(auth.router)
app.include_router(users.router)
