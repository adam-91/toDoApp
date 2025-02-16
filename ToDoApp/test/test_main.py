from fastapi.testclient import TestClient
from ..main import app
from fastapi import status

client = TestClient(app)

def test():
    assert 1 == 1

def test_return_health_check():
    response = client.get('/life')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'alive'}


