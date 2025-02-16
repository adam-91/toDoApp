from datetime import timedelta, timezone
from jose import jwt
from fastapi import HTTPException
import pytest

from ..routers.auth import authenticate_user, create_access_token, get_current_user, get_db, SECRET_KEY, ALGORITHM
from .utils import *

app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.login, 'test_password', db)
    assert authenticated_user is not None
    assert authenticated_user.login == test_user.login

    non_existent_user = authenticate_user('wrong_user_name', 'test_password', db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.login, 'wrong_password', db)
    assert wrong_password_user is False

def test_create_access_token():
    login = 'test_user'
    user_id = 1
    expires_delta = timedelta(days=1)
    token = create_access_token(login, user_id, expires_delta)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],
                               options={'verify_signature': False})
    
    assert decoded_token['sub'] == login
    assert decoded_token['id'] == user_id

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub': 'test 2', 'id': 1}
    expires_delta = timedelta(days=1)
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    assert token is not None

    user = await get_current_user(token)
    assert user == {'login': 'test 2', 'user_id': 1}

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate user'