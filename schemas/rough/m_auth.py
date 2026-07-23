from sqlalchemy import Column,Integer,String
from database import get_db,Base

class User(Base):
    __tablename___ = "users"
    
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,index=True)
    email = Column(String,unique=True,index=True)
    password = Column(String,True)
        