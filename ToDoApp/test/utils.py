from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from datetime import datetime

import pytest

from ..database import Base
from ..main import app
from ..models import Activities, Categories, Users
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass = StaticPool,

)

date = datetime(2025, 2, 1, 6, 0, 0)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base.metadata.create_all(bind = engine)

def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db 
    finally:
        db.close()

def override_get_current_user():
    return {
            'login': 'test1', 
            'id': 1, 
            'name': 'Gabriel', 
            'second_name': 'Kacper',
            'surname': 'Malinowski', 
            'email': 'test1234@com.pl',
            'phone': '+48 000 000 000',
            'creation_date': date,
            'active': True,
            }

client = TestClient(app)

@pytest.fixture
def test_activity():
    activity = Activities(
        name = 'Test tittle 1',
        description = 'test description 1',
        priority = 5,
        active = True,
        progress = 25,
        category_id = 1,
        type_id = 1,
        user_id = 1
    )

    db = TestingSessionLocal()
    db.add(activity)
    db.commit()
    yield activity
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM Activities;'))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        login='test 2',
        email='test@a.pl',
        name='Ariel',
        second_name='test',
        surname='Gruszkowski',
        hashed_password = bcrypt_context.hash('test_password'),
        phone= '+48 000 000 000',
        creation_date= date,
        active = True
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()

    yield user
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users;'))
        connection.commit()

@pytest.fixture
def test_user2():
    user = Users(
        login = 'test1', 
        name = 'Gabriel', 
        second_name = 'Kacper',
        surname = 'Malinowski', 
        email = 'test1234@com.pl',
        phone = '+48 000 000 000',
        creation_date = date,
        active = True,
        hashed_password = bcrypt_context.hash('test_password'),
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()

    yield user
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users;'))
        connection.commit()

@pytest.fixture
def test_category():
    category = Categories(
        name = 'Czynności',
        description = 'Ogólna kategoria',
        level = 1,
        picture = 'no picture',
        active = True,
    )

    db = TestingSessionLocal()
    db.add(category)
    db.commit()

    yield category
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM Categories;'))
        connection.commit()