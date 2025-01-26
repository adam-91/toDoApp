from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Activities(Base):
    __tablename__ = 'Activities'

    id = Column(Integer, primary_key = True, index = True)
    name =  Column(String)
    description =  Column(String)
    priority =  Column(Integer, default = 1)
    progress =  Column(Integer, default = 0)
    active = Column(Boolean, default = False)