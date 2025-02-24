from fastapi import status
from ..routers.users import get_db, get_current_user
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['login'] == 'test 2'
    assert response.json()['email'] == 'test@a.pl'
    assert response.json()['name'] == 'Ariel'
    assert response.json()['surname'] == 'Gruszkowski'
    assert response.json()['phone'] == '+48 000 000 000'
    assert response.json()['second_name'] == 'test'

def test_change_password_success(test_user):
    response = client.put("/user/password", json={"password": "test_password",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/password", json={"password": "wrong_password",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}


def test_change_phone_number_success(test_user):
    response = client.put("/user/phone/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_name(test_user):
    response = client.put("/user/name/new_test_name")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/user")
    assert response.json()['name'] == 'new_test_name'

def test_change_name(test_user):
    response = client.put("/user/second_name/new_test_second_name")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/user")
    assert response.json()['second_name'] == 'new_test_second_name'

def test_change_name(test_user):
    response = client.put("/user/surname/new_test_surname")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/user")
    assert response.json()['ssurname'] == 'new_test_surname'

