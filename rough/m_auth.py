from sqlalchemy import Column,Integer,String
from database import get_db,Base

class User(Base):
    __tablename___ == "users"