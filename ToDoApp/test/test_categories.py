from fastapi import status
from ..routers.categories import get_db, get_current_user
from ..models import Categories
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_categories(test_category):
    response = client.get("/categories")

    assert response.status_code == status.HTTP_200_OK
    
    assert response.json()[0]['name'] == 'Czynności'
    assert response.json()[0]['description'] == 'Ogólna kategoria'
    assert response.json()[0]['level'] == 1
    assert response.json()[0]['picture'] == 'no picture'
    assert response.json()[0]['active'] == True
    assert len(response.json()) == 1
        

def test_return_category(test_category):
    response = client.get("/categories/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['name'] == 'Czynności'
    assert response.json()['description'] == 'Ogólna kategoria'
    assert response.json()['level'] == 1
    assert response.json()['picture'] == 'no picture'
    assert response.json()['active'] == True

def test_update_category(test_category):
    category_request = {
                'name': 'Czynności 2',
                'description': 'Ogólna kategoria 2',
                'level': 2,
                'picture': 'picture exist',
                'active': True
    }

    response = client.put("/categories/1", json = category_request)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    category_model = db.query(Categories).filter(Categories.id == 1).first()

    assert category_model.name == category_request.get('name')
    assert category_model.description == category_request.get('description')
    assert category_model.level == category_request.get('level')
    assert category_model.picture == category_request.get('picture')

def test_delete_category(test_category):
    response = client.delete("/categories/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    category_model = db.query(Categories).filter(Categories.id == 1).first()
    
    assert category_model  is None

