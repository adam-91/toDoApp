from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

class Activities(Base):
    __tablename__ = 'Activities'

    id = Column(Integer, primary_key = True, index = True)
    name =  Column(String)
    description =  Column(String)
    priority =  Column(Integer, default = 1)
    progress =  Column(Integer, default = 0)
    active = Column(Boolean, default = False)
    category_id = Column(Integer, ForeignKey('Categories.id'), default = 1)
    type_id = Column(Integer, ForeignKey('Types.id'), default = 1)
    user_id = Column(Integer, ForeignKey('Users.id'))

class Categories(Base):
    __tablename__ = 'Categories'

    id =  Column(Integer, primary_key = True, index = True)
    name =  Column(String)
    description =  Column(String)
    level = Column(Integer)
    picture = Column(String)
    active = Column(Boolean)

class Types (Base):
    __tablename__ = 'Types'

    id =  Column(Integer, primary_key = True, index = True)
    name =  Column(String)
    description =  Column(String)
    active = Column(Boolean)
    
class Users(Base):
    __tablename__ = 'Users'

    id =  Column(Integer, primary_key = True, index = True)
    login = Column(String, unique = True)
    name = Column(String)
    second_name = Column(String)
    surname = Column(String)
    email = Column(String,unique = True)
    phone = Column(String, unique = True)
    hashed_password = Column(String)
    creation_date = Column(DateTime)
    active = Column(Boolean)


    