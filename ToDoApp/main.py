from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .models import Base
from .database import engine
from .routers import activities, categories, auth, types, users

app = FastAPI()

Base.metadata.create_all(bind = engine)

app.mount('/static', StaticFiles(directory = 'ToDoApp/static'), name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/activities/activity-page", status_code=status.HTTP_302_FOUND)

@app.get('/life')
def health_check():
    return {'status': 'alive'}

app.include_router(activities.router)
app.include_router(categories.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(types.router)
