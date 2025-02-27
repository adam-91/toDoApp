from fastapi import status
from ..routers.types import get_db, get_current_user
from ..models import Types
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_types(test_types):
    response = client.get("/types")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['name'] == 'Zadanie jednorazowe'
    assert response.json()[0]['description'] == 'Zadanie jednorazowe, zrób i zakończ'
    assert response.json()[0]['active'] == True
    assert len(response.json()) == 1

def test_return_type(test_types):
    response = client.get("/types/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['name'] == 'Zadanie jednorazowe'
    assert response.json()['description'] == 'Zadanie jednorazowe, zrób i zakończ'
    assert response.json()['active'] == True

def test_return_not_existed_type(test_types):
    response = client.get("/types/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_type(test_types):
    request_data = {
        'name': 'Zadanie cykliczne',
        'description': 'Zadanie wykonywane co jakiś czas',
        'active': True
    }

    response = client.post('/types', json = request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    type = db.query(Types).filter(Types.id == 2).first()

    assert type.name == request_data.get('name')
    assert type.description == request_data.get('description')
    assert type.active == request_data.get('active')

def test_update_type(test_types):
    request_data = {
        'name': 'Zadanie cykliczne',
        'description': 'Zadanie wykonywane co jakiś czas',
        'active': True
    }

    response = client.put('/types/1', json = request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    type = db.query(Types).filter(Types.id == 1).first()

    assert type.name == request_data.get('name')
    assert type.description == request_data.get('description')
    assert type.active == request_data.get('active')

def test_delete_type(test_types):
    response = client.delete('/types/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    type_model = db.query(Types).filter(Types.id == 1).first()

    assert type_model.active == False
