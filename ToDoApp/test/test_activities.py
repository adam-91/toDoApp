from fastapi import status
from ..routers.activities import get_db, get_current_user
from ..models import Activities
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_activity):
    response = client.get('/activities/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': 1,
        'name': 'Test tittle 1',
        'description': 'test description 1',
        'priority': 5,
        'active': True,
        'progress': 25,
        'category_id': 1,
        'type_id': 1,
        'user_id': 1
    }]

def test_read_one_authenticated(test_activity):
    response = client.get('/activities/activity/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'name': 'Test tittle 1',
        'description': 'test description 1',
        'priority': 5,
        'active': True,
        'progress': 25,
        'category_id': 1,
        'type_id': 1,
        'user_id': 1
    }

def test_read_authenticated_not_found(test_activity):
    response = client.get('/activities/activity/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Activity not found'}

def test_create_activity(test_activity):
    request_data = {
        'name': 'Test tittle 2',
        'description': 'test description 2',
        'priority': 2,
        'active': True,
        'progress': 22,
    }

    response = client.post('/activities/activity/', json = request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Activities).filter(Activities.id == 2).first()
    assert model.active == request_data.get('active')
    assert model.progress == request_data.get('progress')
    assert model.priority == request_data.get('priority')
    assert model.description == request_data.get('description')
    assert model.name == request_data.get('name')

def test_update_activity(test_activity):
    request_data = {
        'name': 'Updated Test tittle 2',
        'description': 'Updated test description 2',
        'priority': 3,
        'active': False,
        'progress': 24,
    }

    response = client.put('/activities/activity/1', json = request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Activities).filter(Activities.id == 1).first()
    assert model.active == request_data.get('active')
    assert model.progress == request_data.get('progress')
    assert model.priority == request_data.get('priority')
    assert model.description == request_data.get('description')
    assert model.name == request_data.get('name')

def test_update_actiyity_not_found(test_activity):
    request_data = {
        'name': 'Updated Test tittle 2',
        'description': 'Updated test description 2',
        'priority': 3,
        'active': False,
        'progress': 24,
    }

    response = client.put('/activities/activity/999', json = request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Activity not found'}

def test_delete_activity(test_activity):
    response = client.delete('/activities/activity/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Activities).filter(Activities.id == 1).first()

    assert model is None

def test_delete_activity_not_found(test_activity):
    response = client.delete('/activities/activity/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Activity not found'}


